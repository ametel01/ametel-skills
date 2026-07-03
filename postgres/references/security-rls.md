---
title: Security and Row-Level Security
description: Row-Level Security policy design, policy performance, and privilege scoping
tags: postgres, security, row-level-security, rls, privileges, supabase
---

# Security and RLS

Use this reference for multi-tenant data, PostgREST/Supabase-style APIs, or any schema that relies on database policies for authorization.

## RLS Baseline

- Enable RLS on tenant-owned tables and write policies for SELECT, INSERT, UPDATE, and DELETE paths that need access.
- Treat application-side filters as defense in depth, not as the only tenant boundary.
- Test both allowed and denied cases with the same role the application uses.
- Keep admin/service roles separate from ordinary application roles; do not give broad table grants to `PUBLIC`.

## Policy Performance

RLS predicates run as part of every protected query, so design them like query predicates:

- Index policy columns such as `tenant_id`, `organization_id`, `owner_id`, and `user_id`.
- Match policy predicates to common query filters so the planner can use the same composite indexes.
- Keep policy expressions simple; move expensive authorization checks into carefully reviewed helper functions.
- For request-context helper functions that are stable for the statement, consider a scalar subquery so PostgreSQL can evaluate once when safe. Verify with `EXPLAIN (ANALYZE, BUFFERS)`.

```sql
CREATE POLICY invoice_tenant_read ON invoice
FOR SELECT
USING (tenant_id = (SELECT current_setting('app.tenant_id', true)::uuid));

CREATE INDEX invoice_tenant_created_idx
  ON invoice (tenant_id, created_at DESC);
```

For Supabase projects, apply the same idea to `auth.uid()`/JWT helper checks where appropriate, and verify against the actual plan because policy shape, function volatility, and query predicates all affect whether the planner can optimize it.

## Privilege Scope

- Grant the minimum table, schema, function, and sequence privileges each role needs.
- Revoke default `PUBLIC` privileges on sensitive schemas and functions.
- Put privileged helper functions in a private schema, set a fixed `search_path`, and document why they need elevated privileges.
- Avoid `SECURITY DEFINER` unless the function is small, deterministic, and reviewed for SQL injection and search-path risks.

```sql
REVOKE ALL ON SCHEMA private FROM PUBLIC;
GRANT USAGE ON SCHEMA app TO app_user;
GRANT SELECT, INSERT, UPDATE ON app.invoice TO app_user;
```
