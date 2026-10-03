# NIST-Aligned Assessment Lifecycle

This educational outline is informed by risk-management, incident-handling, and data-integrity concepts commonly associated with NIST publications. It is not a claim of NIST compliance, certification, or endorsement.

## 1. Prepare and authorize

Define the business question, written authorization, systems, permitted methods, prohibited actions, data classes, contacts, retention, and stop conditions. Establish change-control and escalation routes before any collection.

## 2. Scope and minimize

Translate the question into the smallest practical set of read-only observations. Identify privacy impacts, expected endpoint load, exclusion rules, and what evidence would be insufficient to support a conclusion.

## 3. Collect safely

Use approved, non-destructive collection methods. Record timing, tool version, scope, handler role, and integrity information when appropriate. Stop and escalate on out-of-scope or sensitive data.

## 4. Analyze with context

Review sanitized or approved artifacts against the stated objective. Preserve provenance and distinguish observations from hypotheses. Describe confidence, alternatives, and limitations; do not infer compromise or attribution beyond available evidence.

## 5. Stabilize through controlled change

Propose prioritized, reversible remediation actions with owner, risk, dependencies, rollback, and verification criteria. Obtain required approval before changes and avoid unplanned endpoint modification.

## 6. Verify and communicate

Confirm approved changes against documented success criteria. Report what was observed, what changed, remaining risks, and unresolved questions in clear, non-absolute language.

## 7. Retain and close

Apply the agreed retention and disposal process. Preserve only authorized records, document custody and disposition, and capture process improvements without retaining unnecessary client details.

## References for further study

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST SP 800-61 Rev. 2, Computer Security Incident Handling Guide](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response](https://csrc.nist.gov/pubs/sp/800/86/final)
