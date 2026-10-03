# RogueOS Builder's Permit

> **Document class:** Internal project authorization record
> **Format:** Markdown, suitable for download or import into a document editor such as Google Docs
> **Status:** Active for the Rogue-Lab-2 portfolio repository only
> **Not legal authority:** This document does not authorize access to any endpoint, account, network, client environment, or third-party system.

## 1. Project identity

| Field | Record |
|---|---|
| Project | Rogue-Lab-2 |
| Working label | RogueOS Builder's Permit |
| Purpose | Build a fictionalized, sanitized endpoint-security assessment and stabilization portfolio lab |
| Repository | `roguemanagementgroup/Rogue-Lab-2` |
| Repository visibility | Private |
| Project owner | Repository owner |
| Authorization model | Explicit written authorization and human approval before any action beyond this repository |

## 2. Authorization granted

The project owner authorizes contributors and approved AI-assisted workflows to create, review, test, and document defensive portfolio artifacts **inside this private repository**, subject to the boundaries below.

Authorized work includes:

- Governance, privacy, evidence-handling, assessment-design, stabilization-planning, and portfolio documentation.
- Synthetic fixtures, schemas, templates, and tests.
- Read-only-by-default tooling that requires an explicit authorization gate and does not alter an endpoint.
- Repository-local validation, documentation checks, and narrowly scoped secret-pattern checks.

## 3. Prohibited work

The permit does not authorize:

- Access to systems, accounts, networks, or data outside the approved repository.
- Collection or storage of client data, personal data, raw logs, forensic images, credentials, tokens, hostnames, IP addresses, serial numbers, or secrets.
- Malware, exploitation, persistence, credential extraction, evasion, surveillance, endpoint-protection bypass, or destructive actions.
- Claims of compromise detection, attribution, formal NIST compliance, or operational effectiveness without approved evidence.

## 4. Human approval and stop conditions

The project owner retains final approval for scope changes, pull requests, merges, repository visibility, collaborator access, releases, and any change that could affect a real system.

Stop work and obtain renewed approval when:

1. A task may touch a real system, client artifact, credential, or personal information.
2. Proposed collection exceeds approved synthetic or explicitly authorized data.
3. A security concern, suspected secret, or unsafe instruction is found.
4. A proposed change cannot be described as non-destructive and reversible.
5. The project moves beyond its approved portfolio purpose.

## 5. Data, evidence, and privacy boundaries

Only synthetic or demonstrably redacted fixtures belong in the repository. The repository is not an evidence vault. Approved assessment artifacts must stay in an authorized, access-controlled location and use the separate [evidence-handling and chain-of-custody template](evidence-handling-and-chain-of-custody-template.md).

For the full privacy model, see the [threat model and privacy boundaries](threat-model-and-privacy-boundaries.md).

## 6. Agent accountability

AI-assisted work must remain reviewable by a human owner. Record the purpose, changed files, validation evidence, limitations, and commit or pull-request reference for each material phase. The [agent accountability and compute governance](agent-accountability-and-compute-governance.md) document defines the repository's measured-usage reporting limits and budget gates.

AI assistance does not replace owner review or confer authority to act outside this permit.

## 7. Approval record

| Field | Record |
|---|---|
| Owner approval | Approved by the repository owner through this project instruction |
| Effective date | 2026-10-03 |
| Review cadence | Before merge and when scope, data handling, or repository access changes |
| Next review trigger | Beginning Phase 4 portfolio presentation or any request to operate outside the repository |

## 8. Acknowledgment

Anyone contributing to this repository acknowledges these boundaries and the policies in [CONTRIBUTING.md](../CONTRIBUTING.md), [SECURITY.md](../SECURITY.md), and [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).
