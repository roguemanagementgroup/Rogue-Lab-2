# Rogue-Lab-2

Rogue-Lab-2 is a fictionalized, sanitized portfolio lab for planning and documenting a first-visit endpoint security assessment and stabilization engagement. It demonstrates careful assessment practice: establish authorization, minimize collection, preserve evidence integrity, communicate uncertainty, and prioritize safe remediation.

> **Authorization required.** Use these materials only on systems for which you have explicit, written authorization. This repository contains no client data and must not be used to collect credentials, evade controls, establish persistence, exploit systems, or conduct surveillance.

## Scope

The lab will model a limited, non-destructive endpoint review at a client office. Future examples will use synthetic or redacted fixtures only. Any collection pattern introduced later must be read-only by default, narrowly scoped, reviewable, and appropriate to the approved rules of engagement.

This is not an incident-response service, an endpoint-detection product, or a compromise-attribution tool. Findings will be described as observations with stated limits; they will not claim to prove compromise, identify an actor, or establish causation without supporting evidence.

## Planned phases

1. **Foundation (current):** governance, authorization boundaries, privacy controls, evidence handling, lifecycle, and CI safeguards.
2. **Assessment design:** approved objectives, scoping worksheets, synthetic fixtures, and non-destructive collection specifications.
3. **Stabilization planning:** prioritized remediation guidance, change-control artifacts, and rollback-aware verification plans.
4. **Portfolio presentation:** sanitized example reports, decision records, and documentation review.

## Evidence minimization

Collect only what the approved question requires, retain it only for the agreed period, and use the least sensitive representation that remains useful. Do not commit raw endpoint logs, forensic images, network captures, account data, host identifiers, serial numbers, IP addresses, secrets, or personal information. See [privacy boundaries](docs/threat-model-and-privacy-boundaries.md) and the [evidence template](docs/evidence-handling-and-chain-of-custody-template.md).

## Assessment approach

The [assessment lifecycle](docs/nist-aligned-assessment-lifecycle.md) is informed by relevant NIST concepts, including risk-based planning, evidence integrity, and recovery-oriented validation. It is an educational outline and **does not claim NIST certification, validation, or formal compliance**.

## Repository conventions

- Keep fixtures synthetic or demonstrably redacted.
- Record assumptions, collection limits, and uncertainty with every assessment artifact.
- Treat authorization changes, scope expansion, and retention exceptions as explicit approvals.
- Report suspected sensitive content rather than committing it; see [SECURITY.md](SECURITY.md).

## License

Source code in this repository is licensed under the [Apache License 2.0](LICENSE). Original documentation and templates are available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), so portfolio materials can be shared with attribution while preserving the Apache terms for code. Third-party material, if added, remains subject to its own license.

## Portfolio context

This private repository is intended to show recruiters and reviewers how an endpoint-security practitioner turns a scoped first visit into safe, defensible, and human-readable work products. A suitable repository description is: **“Sanitized endpoint security assessment and stabilization portfolio lab.”** Suggested topics: `cybersecurity`, `endpoint-security`, `security-assessment`, `incident-readiness`, `privacy-by-design`, and `portfolio`.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [SECURITY.md](SECURITY.md) before proposing changes.
