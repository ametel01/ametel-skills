---
title: Concurrency Patterns
description: Lock ordering, queue processing, advisory locks, and deadlock avoidance
tags: postgres, concurrency, locks, deadlocks, skip-locked, advisory-locks
---

# Concurrency Patterns

Use this reference when diagnosing lock waits, deadlocks, duplicate work, queue workers, or application-level coordination.

## Short Transactions

Keep transactions focused on database work. Do not hold locks while calling external APIs, rendering files, waiting for user input, or doing long CPU work. Set `idle_in_transaction_session_timeout` to cap leaked transactions.

## Deterministic Lock Ordering

When a transaction touches multiple rows, lock them in one stable order everywhere in the application. Inconsistent order is the usual cause of avoidable deadlocks.

```sql
SELECT id
FROM account
WHERE id = ANY($1)
ORDER BY id
FOR UPDATE;
```

Apps must retry serialization failures and deadlocks with jittered backoff. Retrying the same transaction body is the correctness mechanism, not an exceptional fallback.

## Queue Workers

Use `FOR UPDATE SKIP LOCKED` so workers claim different jobs without blocking each other:

```sql
WITH next_job AS (
  SELECT id
  FROM job
  WHERE status = 'queued'
  ORDER BY priority DESC, id
  FOR UPDATE SKIP LOCKED
  LIMIT 1
)
UPDATE job
SET status = 'running', started_at = now()
WHERE id = (SELECT id FROM next_job)
RETURNING *;
```

Back the queue scan with an index matching the predicate and order, usually `(status, priority DESC, id)`.

## Advisory Locks

Use transaction-scoped advisory locks for application-level mutual exclusion when no single row naturally owns the lock.

```sql
SELECT pg_try_advisory_xact_lock(hashtext('billing:' || $1::text));
```

Prefer `pg_try_advisory_xact_lock` to avoid unbounded waits. Do not use session-level advisory locks through transaction pooling; the next statement may run on a different backend or release state unexpectedly.

## Lock Diagnostics

Start from blocked sessions, then identify blockers:

```sql
SELECT blocked.pid AS blocked_pid,
       blocker.pid AS blocker_pid,
       blocked.query AS blocked_query,
       blocker.query AS blocker_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocker
  ON blocker.pid = ANY(pg_blocking_pids(blocked.pid));
```
