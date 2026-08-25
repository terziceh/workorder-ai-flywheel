# Architecture Decision Log

## ADR-001: Use independently generated synthetic data

**Date:** 2026-08-25  
**Status:** Accepted

**Context:** The public project is inspired by common facilities-data challenges, while professional operational data must remain private.

**Decision:** Generate all public facilities, assets, descriptions, taxonomies, identifiers, and quality issues independently in repository code.

**Tradeoff:** Synthetic data cannot perfectly reproduce production behavior, but it makes the project public, reproducible, and safe.

## ADR-002: Keep reusable logic outside notebooks

**Date:** 2026-08-25  
**Status:** Accepted

**Decision:** Use notebooks for exploration and communication only. Pipeline, modeling, and application logic belongs in the installable `src/workorder_ai` package.

**Tradeoff:** This requires slightly more setup but enables testing, reuse, and CI.
