# Threat Model and Privacy Boundaries

## Purpose

This document defines the safety and privacy constraints for a fictionalized first-visit endpoint assessment lab. It is a design aid, not a substitute for client authorization, legal review, or an approved rules-of-engagement document.

## Assets to protect

| Asset | Primary risk | Boundary |
|---|---|---|
| Client and employee privacy | Exposure of personal or operational data | Use synthetic/redacted fixtures; do not commit production data. |
| Credentials and access tokens | Unauthorized access or replay | Do not collect, display, store, or test credentials. |
| Endpoint availability and integrity | Disruption or unintended change | Use non-destructive, read-only patterns unless a separately approved change exists. |
| Evidence integrity | Misleading or unverifiable conclusions | Record origin, handler, timestamps, scope, and integrity checks in the evidence template. |
| Professional trust | Overclaiming assessment results | State assumptions, limits, and uncertainty; do not assert compromise or attribution without support. |

## Trust boundaries and threats

| Boundary | Example threat | Required control |
|---|---|---|
| Endpoint to collector | Excessive or sensitive collection | Collect only approved, necessary fields; exclude credentials and personal data. |
| Collector to analyst | Artifact tampering or ambiguous provenance | Use approved transfer paths, access restriction, and documented hashes when applicable. |
| Analyst to repository | Accidental publication of client artifacts | Use synthetic fixtures, `.gitignore`, review, and secret scanning before merge. |
| Repository to portfolio viewer | Misinterpretation as operational guidance | Keep authorization notices, non-goals, and limitations adjacent to examples. |

## Explicit non-goals

The lab excludes exploitation, malware, persistence, credential extraction, evasion, invasive surveillance, endpoint-protection bypass, and any collection outside written authorization. It does not provide incident attribution or a guarantee that compromise will be detected.

## Privacy decision rules

1. Confirm written authorization, purpose, systems, data classes, handlers, and retention period before collection.
2. Prefer aggregate, pseudonymized, or synthetic representations over host- or person-specific artifacts.
3. Stop collection and escalate when unapproved sensitive data appears.
4. Store assessment artifacts only in an approved location with access control; the repository is not an evidence vault.
5. Dispose of approved working copies at the end of the retention period and record the disposition.

## Residual risk

Even read-only collection can expose sensitive information or affect endpoint performance. Scope limits, sampling, review, and client-approved change control reduce but do not eliminate this risk.
