#### Seminar 14

## Tasks

The objective is to prepare a project submission that can be assessed quickly and fairly.

---

### Task 1: produce a clean reproducible run

1. Clone your team repository into a fresh directory.
2. Follow your own README instructions exactly.
3. Confirm that a full run produces the expected artefacts.

Minimum expectation:

* the repository can be set up without manual patching
* the run produces deterministic outputs or explains why bounded variability exists

---

### Task 2: run automated checks

Run your checks locally and record exact commands in your documentation.

If your repository uses pytest:

```bash
python -m pytest -q
```

If your repository uses Docker Compose for E2:

```bash
docker compose up --build --abort-on-container-exit
```

---

### Task 3: validate network evidence

If your project requires a PCAP artefact, ensure it can be validated deterministically.

Example pattern:

```bash
python tools/validate_pcap.py --project <CODE> --pcap artifacts/pcap/traffic_e2.pcap
```

Your documentation should include:

* the capture path
* the validation command
* the expected validation result

---

### Task 4: write an evidence table

Create a table mapping requirement identifiers to evidence.

Your table should include:

* the requirement ID
* a one sentence summary
* the exact path and command that demonstrates compliance
* the expected result

Avoid informal evidence such as screenshots unless a UI behaviour is the requirement.

---

### Task 5: prepare a short demonstration

Prepare a demonstration that fits within the allocated time.

Recommendation:

* start from a clean state
* run one end to end flow that exercises the core requirement
* show one trace or log excerpt that proves the flow
* show one negative case and explain expected failure behaviour

---

### Task 6: rehearse viva prompts

For each team member, prepare a brief answer for the following prompts:

* What is the design goal and what constraint shaped your solution most?
* Where does reliability come from in your system and where can it fail?
* Which configuration choice would you change if you had another week and why?
* What security risk is most relevant and what mitigation did you implement?

Your aim is not memorisation.
Your aim is to demonstrate structured reasoning.
