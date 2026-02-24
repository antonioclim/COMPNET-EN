#### Seminar 14

## Template: assessment rubric, evidence checklist and viva prompts

This file is a template.
It can be used in two ways:

* by assessors during marking
* by student teams as a structured self-audit before submission

---

### Rubric

Suggested scale:

* 0 = not demonstrated
* 1 = partially demonstrated
* 2 = demonstrated
* 3 = demonstrated clearly with evidence and justification

| Criterion | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Correctness | No working end to end flow | Flow works only in a narrow case | Flow works under stated assumptions | Flow works and failure modes are handled predictably |
| Reproducibility | Results cannot be reproduced | Reproduction requires manual intervention | One command or script reproduces results | Results are reproducible and documented with exact evidence |
| Protocol reasoning | Cannot explain observed behaviour | Explanations are vague or inconsistent | Explains key behaviours at the correct layer | Explains behaviours and trade-offs with trace based evidence |
| Testing and validation | No tests or validation | Tests exist but are incomplete | Tests cover core requirements | Tests cover core requirements and negative cases with clear outputs |
| Security posture | No security discussion | Mentions threats without mitigation | Implements at least one mitigation | Threat model is explicit and mitigations are justified |
| Documentation quality | Incomplete or ambiguous | Usable but missing evidence | Clear with correct commands | Clear, concise and evidence based with deterministic commands |

---

### Evidence checklist

Minimum evidence items for a networking project:

* `README.md` contains setup, run and cleanup instructions
* `docs/` contains the specification and final documentation
* a reproducible run produces artefacts under `artifacts/`
* if PCAP is required, the capture is present and validates deterministically
* tests can be executed in a clean environment

For each requirement identifier, record:

* the exact path containing the evidence
* the exact command that produces or validates it
* the expected output

---

### Viva prompts

These prompts are designed to test understanding rather than memory.

* Explain your architecture using the protocol stack as an organising principle.
* Identify one design trade-off and justify it using constraints and evidence.
* Show one trace segment and explain what it proves.
* If the network becomes lossy, what changes in your system and why?
* Identify one plausible attack on your system and one mitigation.
