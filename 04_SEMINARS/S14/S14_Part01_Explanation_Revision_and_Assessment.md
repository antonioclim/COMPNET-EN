#### Seminar 14

## Revision and team project assessment

This seminar supports two linked activities:

* revision of the course as an integrated system rather than as isolated topics
* preparation for the team project assessment, including the viva style discussion

The central principle is that claims must be backed by reproducible evidence.
In networks, evidence is typically a configuration, a trace and a deterministic test.

---

### Assessment pipeline overview

[FIG] assets/images/fig-assessment-workflow.png

The workflow is designed to separate two dimensions:

* automated verification of requirements that can be checked deterministically
* human assessment of reasoning, design trade-offs and understanding

---

### What is assessed

Project assessment typically evaluates:

* correctness: does the system behave as specified under normal conditions
* robustness: does it behave predictably under loss, delay or malformed input
* reproducibility: can an independent assessor reproduce results from scripts
* security posture: are common misconfigurations avoided and are threats discussed
* communication: is the documentation precise and is the viva coherent

The precise criteria depend on the selected project and the chosen E1, E2 and E3 scope.

---

### Evidence expectations

The fastest way to assess a networking project is to treat it as an experiment.
Every requirement should be supported by an artefact and a command.

Use the evidence table guidance in:

* `02_PROJECTS/00_common/README_STANDARD_RC2026.md`

As a rule, evidence should be:

* exact: use paths, commands and test identifiers
* local: prefer artefacts in the repository rather than external screenshots
* bounded: specify expected outputs and tolerances

---

### The viva format

A viva is not a quiz.
It is a short technical discussion intended to confirm that the work is understood.

Typical viva prompts:

* Explain your architecture end to end and justify each major component.
* Show how you validated protocol behaviour using a trace.
* If the network becomes lossy, what changes and which layer is responsible?
* Identify one security risk in your design and one concrete mitigation.

Good viva answers are structured.
State the assumption, state the mechanism and state the consequence.

---

### Revision strategy linked to projects

Revision becomes easier if you map course topics to what you built.
For example:

* addressing and subnetting appear in Docker networks and in routing constraints
* TCP and UDP behaviour appears in client server traces and in timeouts
* DNS and HTTP appear in service discovery and reverse proxying
* security appears in authentication choices and in hardened defaults

If you can explain your own system, you can typically answer examination questions that describe similar scenarios.
