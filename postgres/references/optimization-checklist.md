---
title: Database Optimization Checklist
description: Optimize checklist
tags: postgres, optimization, indexes, partitioning, maintenance
---

# Optimization Checklist

When optimizing performance, check the following:

- Start from evidence: `pg_stat_statements`, logs, wait events, and `EXPLAIN (ANALYZE, BUFFERS)` for representative slow queries
- Look for unused indexes (0 scans; exclude unique/primary indexes and verify stats age first)
- Look for duplicate indexes
- Check for missing indexes on selective WHERE, JOIN, ORDER BY, and RLS policy columns
- Check for large sequential scans, bad row estimates, high heap fetches, external sorts, and temp blocks in query plans
- Check for N+1 query patterns, deep OFFSET pagination, unbounded SELECTs, and row-at-a-time writes
- Replace check-then-insert races with `INSERT ... ON CONFLICT` where a unique constraint defines the conflict
- Review RLS policies for per-row expensive functions and unindexed tenant/user predicates
- Review lock waits, deadlocks, idle-in-transaction sessions, and worker queues that need `SKIP LOCKED`
- Archive audit/log tables >10GB
- Review tables >500GB for partitioning (>100GB for time-series/logs)
- Verify all extensions are supported
- Check for circular foreign key dependencies
- Consider alternatives to UUID primary keys for large tables
- Configure connection pooling for OLTP workloads
- **Always confirm with a human before removing any indexes, dropping partitions, archiving tables, or performing other destructive actions**
