# RC2026 Team Guide for Gitea, Git, Freeze Tags and Moodle Submissions

**Audience:** all RC2026 project teams  
**Scope:** practical day-to-day work on the team repository and the official submission workflow for **E1**, **E2** and **E3**  
**Style:** operational, concrete and written to prevent avoidable mistakes

---

## 1. What this guide is for

This guide explains the **current working workflow** for RC2026 team repositories on Gitea.

It is designed to reduce confusion about:

- team names, repository names and project codes
- working on `main` versus working on a temporary branch
- whether you need a pull request
- how to create and verify `e1-freeze`, `e2-freeze` and `e3-freeze`
- what exactly must be submitted in Moodle
- what happens if your team submits more than once
- what the most common Git and Gitea messages actually mean

This guide **does not replace** your project brief and the common course materials. You must still read:

- your assigned project brief in `02_PROJECTS/01_network_applications/`
- the shared materials in `02_PROJECTS/00_common/`

---

## 2. The short version

If you read nothing else, remember these rules.

1. Your team already has a repository. Do **not** create a new one.
2. The final assessed version for each stage must be on **`main`**.
3. A working branch is optional. A pull request is **not** required.
4. The assessed commit must have a **lightweight Git tag**:
   - `e1-freeze`
   - `e2-freeze`
   - `e3-freeze`
5. Moodle submission contains **exactly four lines**:
   - `Team slug:`
   - `Commit hash:`
   - `Submitted by Gitea username:`
   - `Optional note:`
6. The commit hash in Moodle must match the commit pointed to by the stage tag.
7. If your team submits more than once, the workflow is designed so that the **first valid** submission determines lateness and the **latest valid** submission is the version intended for grading.
8. If something looks wrong, send the **exact command** you ran and the **exact full output**.

---

## 3. Names you must not confuse

These names are different and you must use the correct one in the correct place.

| Term | Example | What it means | Where you use it |
|---|---|---|---|
| **Team slug** | `team-08` | the team identifier | Moodle submission, team references, internal communication |
| **Repository name** | `team-08-s05` | the actual Gitea repository | clone URL, Gitea web page, `git clone` |
| **Project code** | `S05` | the assigned project | briefs, `project.yml`, `E1_contract.yml`, `E3_evidence_map.yml` |
| **Gitea username** | `almasanuiany10` | the username before `@stud.ase.ro` | login, Git pushes, Moodle `Submitted by Gitea username` |
| **Commit hash** | `cbb84fbcae18ff4ba64e4132284f0fadd6f7f5eb` | the exact commit to be graded | Moodle `Commit hash`, verification in Gitea |
| **Freeze tag** | `e1-freeze` | the stage marker that points to the commit to be graded | Git tags and Gitea `Tags` |

### Example

If your team is **team-08** and your project is **S05**:

- team slug = `team-08`
- repository = `team-08-s05`
- project code = `S05`

These are **not interchangeable**.

---

## 4. Current workflow on the RC2026 Gitea instance

### 4.1 What is normal

On the current RC2026 Gitea setup:

- your repository already exists
- you do not need to create a repository
- you do not need to submit a pull request
- you may work directly on `main` or on a temporary branch first
- the final assessed version must end up on `main`
- the official stage submission is a **Git tag + Moodle text submission**
- the absence of a visible **Pull Request** workflow is **not** an error for this course
- the absence of a visible **Actions** tab in your team repository is **not** an error for this course
- you do not need to configure anything under **Settings → Tags**

### 4.2 What this means in practice

A safe mental model is this:

1. do your work
2. make sure the final version is on `main`
3. create the correct stage tag on that final commit
4. verify the tag in Gitea
5. paste the four required lines in Moodle

That is the official flow.

---

## 5. Deadlines, penalties and stage gates

### 5.1 Current deadlines

The published deadlines are:

| Stage | Current deadline |
|---|---|
| **E1** | 22 March 2026, 23:59 EET |
| **E2** | 18 April 2026, 23:59 EEST |
| **E3** | 23 May 2026, 23:59 EEST |

> **Important**  
> Moodle is the authoritative source for the due date. If Moodle is changed later, Moodle wins.

### 5.2 Late penalties

| Stage | Penalty | Maximum penalty |
|---|---:|---:|
| **E1** | 1 point per started day late | 20 points |
| **E2** | 1 point per started day late | 20 points |
| **E3** | 10 points per started day late | 40 points |

There is a **24-hour administrative grace period** before any late penalty starts.

### 5.3 Stage gates

| Rule | Meaning |
|---|---|
| **E2 gate** | E2 carries no value unless E1 has been passed with a net score of at least 15% |
| **E3 gate** | E3 carries no value unless E2 has also been passed with a net score of at least 15% |

So if you fail a stage badly enough, later stages can become void.

---

## 6. Minimum repository structure

Your repository must keep the expected top-level structure.

```text
.
├─ README.md
├─ docs/
│  ├─ E1_specification.md
│  ├─ E1_phase0_observations.md
│  ├─ E2_pcap_analysis.md
│  └─ E3_final_documentation.md
├─ src/
├─ scripts/
├─ tests/
├─ docker/
│  └─ docker-compose.yml
├─ tools/
│  ├─ validate_pcap.py
│  └─ pcap_rules/
│     └─ <CODE>.json
├─ artifacts/
│  └─ pcap/
│     └─ traffic_e2.pcap
├─ Makefile
└─ MANIFEST.txt
```

### 6.1 What is flexible

You may organise **subfolders inside `src/`** as you like.

For example, these are usually fine:

- `src/phase0/`
- `src/phase1/`
- `src/backend/`
- `src/client/`

### 6.2 What is not flexible

The **top-level required files and folders** must still exist.

For example:

- `docs/E1_specification.md` must still exist
- `docs/E1_phase0_observations.md` must still exist
- `docker/docker-compose.yml` must exist at that path for the expected structure
- `tools/validate_pcap.py` and `tools/pcap_rules/SNN.json` must exist for E2

So a structure such as `src/phase1/` is fine **inside `src/`**. It does **not** replace the required top-level files.

---

## 7. Before you start any stage

Run these checks first.

### 7.1 Confirm you are in the correct repository

```bash
git remote -v
```

### Expected success

You should see a URL like:

```text
https://sop.ase.ro:30000/ase-networking/team-08-s05.git
```

### Problem signs

- the repository name contains the wrong team slug
- the repository name contains the wrong project code
- the remote points to GitHub or another unrelated repository

### 7.2 Confirm your current branch

```bash
git branch --show-current
```

### Expected success

You should see something like:

```text
main
```

or a working branch such as:

```text
e1-work
```

### 7.3 Pull the current remote `main`

```bash
git checkout main
git pull --ff-only origin main
```

### Expected success

One of these is normal:

```text
Already up to date.
```

or

```text
Updating <old>..<new>
Fast-forward
```

### Problem signs

- `fatal: not a git repository`
- authentication failed
- merge conflicts on `git pull`

If `git pull --ff-only` fails because you already created local commits on `main`, stop and inspect carefully before continuing.

---

## 8. Recommended Git workflows

There are two sensible ways to work.

## 8.1 Option A — the simplest workflow: work directly on `main`

Use this if your team is small and you coordinate well.

```bash
git checkout main
git pull --ff-only origin main
# edit files
# run local checks
git add .
git commit -m "E1: update specification and phase 0 observations"
git push origin main
```

### Good output after the push

```text
To https://sop.ase.ro:30000/ase-networking/team-08-s05.git
   <old>..<new>  main -> main
```

## 8.2 Option B — the safer workflow: work on a temporary branch then merge into `main`

Use this if several team members are editing at the same time.

```bash
git checkout main
git pull --ff-only origin main
git checkout -b e1-work
# edit files
# run local checks
git add .
git commit -m "E1: complete specification and phase 0 observations"
git push origin e1-work
```

When you are ready to prepare the final stage version:

```bash
git checkout main
git pull --ff-only origin main
git merge e1-work
git push origin main
```

### Important

- a pull request is **not** required
- the final assessed version must still be on `main`
- if the merge is a **fast-forward**, Gitea may not show a separate “merge commit” afterwards and that is completely normal

### Good outputs for `git merge e1-work`

Any of these can be normal:

```text
Already up to date.
```

```text
Fast-forward
```

```text
Merge made by the 'ort' strategy.
```

### Real problem output

```text
CONFLICT (content): Merge conflict in <file>
Automatic merge failed
```

If you get a conflict, resolve it locally, run your checks again and only then push `main`.

---

## 9. E1 — complete step-by-step guide

## 9.1 What E1 is

E1 is the stage for:

- **Specification**
- **Phase 0 Wireshark observations**

## 9.2 Minimum files that must exist for E1

At a minimum, make sure these files exist and are filled in sensibly:

```text
project.yml
E1_contract.yml
docs/E1_specification.md
docs/E1_phase0_observations.md
```

### Notes

- `project.yml` must contain your correct project code, team ID and repository URL
- `E1_contract.yml` must not stay as a placeholder
- `docs/E1_specification.md` must describe your actual protocol and behaviour
- `docs/E1_phase0_observations.md` must contain your actual observations, filters, findings and design decisions

## 9.3 What `E1_contract.yml` must contain at minimum

Your schema requires:

- `project_code`
- at least **one** channel
- at least **one** operation
- an `e2_scenario` with at least **one** step

So a file that still says `REPLACE_ME` is not a finished E1 contract.

## 9.4 Local E1 self-check

From the repository root, run:

```bash
python3 scripts/check_e1.py --repo-root .
```

If Python complains that modules are missing, install the required ones first:

```bash
python3 -m pip install pyyaml jsonschema
```

### Expected success output

```json
{
  "stage": "E1",
  "missing": [],
  "status": "OK"
}
```

### Problem output example

```json
{
  "stage": "E1",
  "missing": [
    "docs/E1_phase0_observations.md"
  ],
  "status": "FAIL"
}
```

### What success means

It means the required files exist and the YAML files validate against the current schemas.

### What it does **not** mean

It does **not** mean you have already earned a good mark. It only means the basic structure is valid.

## 9.5 E1 submission workflow

### Step 1 — update `main`

```bash
git checkout main
git pull --ff-only origin main
```

### Step 2 — if you worked on a branch, merge it into `main`

```bash
git merge e1-work
```

Replace `e1-work` with your real branch name.

### Step 3 — push `main`

```bash
git push origin main
```

### Expected success

Either of these is fine:

```text
main -> main
```

or

```text
Everything up-to-date
```

`Everything up-to-date` simply means remote `main` already has the same commit.

### Step 4 — create the freeze tag

```bash
git tag e1-freeze
git push origin e1-freeze
```

### Expected success

For a brand new tag, a typical success looks like:

```text
[new tag]         e1-freeze -> e1-freeze
```

### Also normal

```text
Everything up-to-date
```

This means the remote already has **the same tag on the same commit**.

### Real problem

```text
fatal: tag 'e1-freeze' already exists
```

This means the tag already exists locally. Inspect it before doing anything else.

### Step 5 — verify the tag hash locally

```bash
git rev-parse e1-freeze
```

### Expected success

You should get a full 40-character commit hash, for example:

```text
cbb84fbcae18ff4ba64e4132284f0fadd6f7f5eb
```

### Step 6 — verify in Gitea

In the Gitea web interface:

1. open your repository
2. click **Tags**
3. confirm that `e1-freeze` exists
4. confirm that the tag points to the same commit hash you saw locally
5. confirm that the final files are visible on `main`

### Step 7 — submit in Moodle

Paste **exactly** this format into the correct Moodle assignment:

```text
Team slug: team-08
Commit hash: cbb84fbcae18ff4ba64e4132284f0fadd6f7f5eb
Submitted by Gitea username: almasanuiany10
Optional note:
```

Replace the example values with your own.

### Important rules for E1 Moodle submission

- one team member is enough
- the team remains jointly responsible
- do not paste the repository URL
- do not paste the project code
- do not paste extra explanations unless the optional note is genuinely needed

## 9.6 How to know E1 is actually finished

E1 is in good operational shape when **all** of the following are true:

- the final version is on `main`
- `docs/E1_specification.md` is present and meaningful
- `docs/E1_phase0_observations.md` is present and meaningful
- `project.yml` is correct
- `E1_contract.yml` is correct
- the tag `e1-freeze` exists
- `git rev-parse e1-freeze` matches the commit hash submitted in Moodle
- the correct Moodle assignment contains the four required lines

---

## 10. E2 — complete step-by-step guide

## 10.1 What E2 is

E2 is the stage for the **deterministic automated scenario** and the **PCAP validation pipeline**.

The key output is:

```text
artifacts/pcap/traffic_e2.pcap
```

## 10.2 Minimum expectations for E2

Your repository must contain at least:

```text
docs/E2_pcap_analysis.md
docker/docker-compose.yml
tools/validate_pcap.py
tools/pcap_rules/SNN.json
artifacts/pcap/traffic_e2.pcap
Makefile
```

### Also important

`project.yml` contains the **single authoritative E2 entry point** in:

```yaml
commands:
  e2: ...
```

If you prefer `make e2`, then `commands.e2` should call that.

## 10.3 Very important template warning

The template contains placeholder scripts.

For example, the template `scripts/run_e2.sh` only writes a placeholder file and is **not** a real solution.

So before E2, your team must replace placeholder logic with real project logic.

## 10.4 Recommended E2 local checks

### Check 1 — run your actual E2 command

If your authoritative command is `make e2`:

```bash
make e2
```

If your authoritative command is still `bash scripts/run_e2.sh`:

```bash
bash scripts/run_e2.sh
```

### Success means

- the scenario runs end-to-end
- `pytest -m e2` is executed inside your pipeline
- `artifacts/pcap/traffic_e2.pcap` is produced
- the produced capture is non-empty

### Check 2 — validate the PCAP

Replace `S05` with your real project code.

```bash
python tools/validate_pcap.py --project S05 --pcap artifacts/pcap/traffic_e2.pcap
```

### Expected success

The exact text depends on the validator implementation, but you should see a pass or no failing rules.

### Problem sign

Any reported failing filter means your PCAP does not satisfy the expected traffic rules yet.

### Check 3 — run the public E2 sanity script

```bash
python3 scripts/check_e2.py --repo-root . --execute
```

### Expected success output

It should look broadly like this:

```json
{
  "stage": "E2",
  "command": "...",
  "executed": true,
  "pcap_exists": true,
  "pcap_size": 12345,
  "status": "OK"
}
```

### Problem output example

```json
{
  "stage": "E2",
  "command": "...",
  "executed": true,
  "pcap_exists": false,
  "pcap_size": 0,
  "status": "FAIL"
}
```

## 10.5 E2 submission workflow

The Git steps are the same pattern as E1.

```bash
git checkout main
git pull --ff-only origin main
# merge your working branch if needed
git merge e2-work
git push origin main
git tag e2-freeze
git push origin e2-freeze
git rev-parse e2-freeze
```

Then verify `e2-freeze` in Gitea and submit the four required lines in **RC2026 – E2 submission** in Moodle.

---

## 11. E3 — complete step-by-step guide

## 11.1 What E3 is

E3 is the final implementation stage and includes:

- the final integrated system
- final documentation
- an evidence table
- a **mandatory Flex component** in a non-Python language
- a complete `MANIFEST.txt`

## 11.2 Minimum expectations for E3

At a minimum, you need:

```text
E3_evidence_map.yml
docs/E3_final_documentation.md
docs/FLEX.md
MANIFEST.txt
flex/
```

## 11.3 Flex component rule

The Flex component must:

- be implemented in a language other than Python
- communicate with the main system using the protocol defined in E1
- not rely on shortcuts such as hardcoded values or direct access to internal server files

If there is no Flex component, the maximum achievable E3 mark is limited.

## 11.4 Evidence table rule

`docs/E3_final_documentation.md` must include a section headed:

```text
Evidence (ID → artefact/test/command)
```

Each requirement ID from the brief must be mapped to an **exact proof** such as:

- a test path
- a command
- a config file path
- a log file path
- a PCAP reference

If an ID is missing or the evidence is not reproducible, that criterion is treated as not met.

## 11.5 E3 local self-check

```bash
python3 scripts/check_e3.py --repo-root .
```

### Expected success output

```json
{
  "stage": "E3",
  "missing": [],
  "status": "OK"
}
```

### Problem output example

```json
{
  "stage": "E3",
  "missing": [
    "docs/FLEX.md",
    "MANIFEST.txt"
  ],
  "status": "FAIL"
}
```

## 11.6 E3 submission workflow

```bash
git checkout main
git pull --ff-only origin main
# merge your working branch if needed
git merge e3-work
git push origin main
git tag e3-freeze
git push origin e3-freeze
git rev-parse e3-freeze
```

Then verify the tag in Gitea and submit the four required lines in **RC2026 – E3 submission** in Moodle.

---

## 12. Multiple members, multiple commits, multiple pushes and multiple Moodle submissions

This is where many teams become confused.

## 12.1 Multiple commits by different members are normal

It is completely normal that:

- one member writes code
- another member edits documentation
- a third member prepares screenshots or tests
- several members push to the same repository

This is **not** a problem by itself.

### What actually matters for grading

For each stage, the decisive version is the commit pointed to by the stage tag:

- `e1-freeze`
- `e2-freeze`
- `e3-freeze`

So intermediate commits, branch names and the number of pushes do not by themselves define the final submission.

## 12.2 Multiple branches are normal

If your team has both:

- `main`
- `e1-work`

that is fine.

The only rule is this:

> the final assessed version must be on `main` and the freeze tag must point to that intended final commit.

## 12.3 Multiple pushes are normal

You may push many times while working.

That is normal.

What matters at submission time is:

- the final state on `main`
- the correct freeze tag
- the correct Moodle submission

## 12.4 Multiple Moodle submissions from the same team

This is the most important rule to understand.

### Practical interpretation

If your team submits more than once:

- the **first valid** submission is used to determine lateness
- the **latest valid** submission is the version intended for grading

### What counts as a valid submission

A submission is valid if at least these conditions are met:

- the `Team slug` exists and matches a real approved team
- the `Submitted by Gitea username` belongs to that team
- the `Commit hash` looks like a valid Git hash
- the submission is in the correct assignment for the stage

### Example A — two valid submissions before the deadline

- 21:00 — Alice submits a valid E1 submission for `team-08`
- 22:15 — Bob submits a new valid E1 submission for the same team with a newer hash

Result:

- lateness is calculated from **21:00**
- the version intended for grading is Bob’s **latest valid** submission

### Example B — first attempt invalid, second attempt valid

- 21:00 — Alice submits but forgets the team slug, so the submission is invalid
- 23:10 — Bob submits all four lines correctly

Result:

- the invalid attempt does **not** count as the first valid submission
- lateness is calculated from **23:10**, because that is the first valid one
- grading uses the latest valid one, which is also Bob’s in this example

### Example C — same member submits three times

- 20:00 — first valid submission
- 21:30 — second valid submission
- 22:05 — third valid submission

Result:

- lateness is calculated from **20:00**
- the version intended for grading is the **22:05** version

## 12.5 Good team discipline

To reduce confusion:

1. agree who prepares the final tag
2. agree who submits in Moodle
3. post the final tag hash in your team chat
4. do not silently move the freeze tag without telling the team
5. avoid unnecessary repeated submissions

---

## 13. The most common problems and the exact fix

## 13.1 “I cannot log in to Gitea”

### Check

- are you using the username before `@stud.ase.ro`?
- are you using your ID number as the initial password?

### If it still fails

Send:

- your institutional email address
- your expected Gitea username
- the exact login error message

Do **not** send your password.

---

## 13.2 “I cannot find my repository”

### Check

Your repository name should be of the form:

```text
team-XX-sYY
```

### Example

If you are in `team-08` with `S05`, the repository is:

```text
team-08-s05
```

### Common mistake

Trying to open:

```text
team-08
```

instead of:

```text
team-08-s05
```

---

## 13.3 “I do not see any Pull Request option”

That is **not** an error for this course.

You do **not** need a pull request to submit E1, E2 or E3.

If you worked on a branch, merge it locally into `main` and push `main`.

---

## 13.4 “I do not see any Actions tab”

That is also **not** an error for this course.

Students do not need Gitea Actions in the team repositories in order to submit stages.

---

## 13.5 “I worked on a branch. How do I submit?”

Use this sequence:

```bash
git checkout main
git pull --ff-only origin main
git merge <your-branch>
git push origin main
git tag e1-freeze
git push origin e1-freeze
git rev-parse e1-freeze
```

Replace `e1-freeze` with `e2-freeze` or `e3-freeze` when needed.

---

## 13.6 “`git merge <branch>` says `Already up to date.`”

That is usually **good news**.

It means the commits from that branch are already present in `main`.

### What to do next

Still verify:

```bash
git push origin main
git rev-parse HEAD
```

and then verify the correct stage tag.

---

## 13.7 “`git merge <branch>` says `Fast-forward` and Gitea does not show a separate merge commit”

That is normal.

A fast-forward merge does not create a separate merge commit. It simply moves `main` to the newer commit.

This is **not** a problem.

---

## 13.8 “`git push origin main` says `Everything up-to-date`”

This is normal if remote `main` already has the same commit.

### Verify

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

If both hashes match, your remote `main` is already correct.

---

## 13.9 “`git push origin main` says I am not allowed to push to protected branch main”

This should **not** be the normal student experience in the current workflow.

### What to do

Do **not** improvise.

Send all of the following:

- team slug
- repository name
- exact command
- exact full terminal output
- screenshot if helpful

---

## 13.10 “I created a commit with message `e1-freeze`. Is that enough?”

No.

A commit message called `e1-freeze` is **not** the same thing as the Git tag `e1-freeze`.

You still need:

```bash
git tag e1-freeze
git push origin e1-freeze
```

---

## 13.11 “`git tag e1-freeze` says the tag already exists”

Inspect the tag first.

```bash
git rev-parse e1-freeze
git show --no-patch --decorate e1-freeze
```

### If the tag already points to the correct final commit

Do nothing further. That is fine.

### If the tag points to the wrong commit and you are still correcting **before** final submission

A safe retag sequence is:

```bash
git tag -d e1-freeze
git push origin :refs/tags/e1-freeze
git tag e1-freeze
git push origin e1-freeze
git rev-parse e1-freeze
```

### Important warning

Do not keep moving tags casually after the deadline or after your team has already made a valid Moodle submission. Moodle time and Gitea history remain visible.

If you are already in that situation, stop and ask before changing anything else.

---

## 13.12 “`git push origin e1-freeze` says `Everything up-to-date`”

This often means there is **no problem at all**.

It usually means the remote already has `e1-freeze` on the same commit.

### Verify

```bash
git rev-parse e1-freeze
git fetch --tags origin
git show --no-patch --decorate e1-freeze
```

Then check the tag in Gitea.

If the tag and the intended hash match, you are done.

---

## 13.13 “Gitea still shows the old commit date or I do not see a new merge commit”

Do not rely on guesswork from one UI view.

Instead verify with:

```bash
git rev-parse HEAD
git rev-parse e1-freeze
```

and then verify that the tag badge is attached to the intended commit in Gitea.

Fast-forward merges especially can confuse students because they do not create a separate merge commit.

---

## 13.14 “We organised code as `src/phase0/` and `src/phase1/`. Is that allowed?”

Usually yes.

Subfolders **inside `src/`** are fine as long as the required top-level structure remains valid.

So this is fine:

```text
src/phase0/
src/phase1/
```

but you still need the expected top-level files such as:

```text
docs/E1_specification.md
docs/E1_phase0_observations.md
docker/docker-compose.yml
```

---

## 13.15 “Another team member already submitted in Moodle. Should I submit again?”

Only if your team genuinely needs to correct the submission.

Remember:

- first valid submission determines lateness
- latest valid submission is the version intended for grading

So repeated submissions are possible but should be used carefully and deliberately.

---

## 13.16 “Can one member push the commit and another member submit in Moodle?”

Yes.

That is allowed.

The commit author, the person who pushed and the person who submits in Moodle do **not** all need to be the same person.

What matters is that:

- the commit hash is correct
- the stage tag points to that commit
- the `Submitted by Gitea username` belongs to a real member of the same team

To keep things clean, the Moodle field should name the Gitea username of the person who is actually making the Moodle submission.

---

## 13.17 “We submitted the repository URL or project code in Moodle as well”

That extra information is not needed.

Only the four required lines should be submitted.

If you have already posted extra information once, do not panic. Make one clean valid submission in the correct format.

---

## 13.18 “We worked in the wrong repository”

Stop immediately.

Do not try to hide the mistake by copying files around blindly.

Report:

- the wrong repository name
- the correct repository name
- the exact commits involved
- whether anything has already been tagged or submitted in Moodle

---

## 14. Command quick reference with expected outputs

## 14.1 `git checkout main`

```bash
git checkout main
```

### Normal success

```text
Switched to branch 'main'
```

### Also normal

```text
Already on 'main'
```

### Problem

```text
error: pathspec 'main' did not match any file(s) known to git
```

This means your repository is damaged or you are not in the correct clone.

---

## 14.2 `git pull --ff-only origin main`

```bash
git pull --ff-only origin main
```

### Normal success

```text
Already up to date.
```

or

```text
Updating <old>..<new>
Fast-forward
```

### Problem

```text
fatal: Not possible to fast-forward, aborting.
```

This means local `main` has diverged. Stop and inspect before continuing.

---

## 14.3 `git merge <branch>`

```bash
git merge e1-work
```

### Normal success

```text
Fast-forward
```

or

```text
Already up to date.
```

or

```text
Merge made by the 'ort' strategy.
```

### Problem

```text
CONFLICT (content): Merge conflict in <file>
```

Resolve the conflict, then continue.

---

## 14.4 `git push origin main`

```bash
git push origin main
```

### Normal success

```text
main -> main
```

### Also normal

```text
Everything up-to-date
```

### Problem

```text
remote: error: Not allowed to push to protected branch main
```

Send the exact message and stop.

---

## 14.5 `git tag e1-freeze`

```bash
git tag e1-freeze
```

### Normal success

No output is normal.

### Problem

```text
fatal: tag 'e1-freeze' already exists
```

Inspect the existing tag before doing anything else.

---

## 14.6 `git push origin e1-freeze`

```bash
git push origin e1-freeze
```

### Normal success for a new tag

```text
[new tag]         e1-freeze -> e1-freeze
```

### Also normal

```text
Everything up-to-date
```

### Problem

```text
remote rejected
```

Send the exact full output.

---

## 14.7 `git rev-parse e1-freeze`

```bash
git rev-parse e1-freeze
```

### Normal success

A full 40-character hash.

### Problem

```text
fatal: ambiguous argument 'e1-freeze'
```

This means the tag does not exist locally under that name.

---

## 14.8 `python3 scripts/check_e1.py --repo-root .`

### Normal success

```json
{"stage": "E1", "missing": [], "status": "OK"}
```

### Problem

Missing files or YAML validation errors.

---

## 14.9 `python3 scripts/check_e2.py --repo-root . --execute`

### Normal success

- `pcap_exists: true`
- `pcap_size > 0`
- `status: OK`

### Problem

- no PCAP
- zero-byte PCAP
- command failure

---

## 14.10 `python3 scripts/check_e3.py --repo-root .`

### Normal success

```json
{"stage": "E3", "missing": [], "status": "OK"}
```

### Problem

Missing `E3_evidence_map.yml`, `docs/E3_final_documentation.md`, `docs/FLEX.md` or `MANIFEST.txt`.

---

## 15. Stage-by-stage final checklists

## 15.1 E1 final checklist

- [ ] I am in the correct repository `team-XX-sYY`
- [ ] `main` contains the final E1 version
- [ ] `project.yml` is correct
- [ ] `E1_contract.yml` is correct
- [ ] `docs/E1_specification.md` exists and is meaningful
- [ ] `docs/E1_phase0_observations.md` exists and is meaningful
- [ ] `python3 scripts/check_e1.py --repo-root .` gives `status: OK`
- [ ] `e1-freeze` exists locally
- [ ] `git rev-parse e1-freeze` gives the hash I intend to submit
- [ ] Gitea shows `e1-freeze` on the intended commit
- [ ] Moodle contains exactly the four required lines

## 15.2 E2 final checklist

- [ ] `main` contains the final E2 version
- [ ] `commands.e2` in `project.yml` points to the real end-to-end E2 command
- [ ] `docker/docker-compose.yml` exists
- [ ] `tools/validate_pcap.py` exists
- [ ] `tools/pcap_rules/SNN.json` exists for my project
- [ ] `artifacts/pcap/traffic_e2.pcap` is produced
- [ ] `make e2` or the authoritative E2 command works
- [ ] `python tools/validate_pcap.py --project SNN --pcap artifacts/pcap/traffic_e2.pcap` passes
- [ ] `python3 scripts/check_e2.py --repo-root . --execute` gives `status: OK`
- [ ] `e2-freeze` exists and is correct
- [ ] Moodle contains exactly the four required lines

## 15.3 E3 final checklist

- [ ] `main` contains the final E3 version
- [ ] `E3_evidence_map.yml` exists and is filled in
- [ ] `docs/E3_final_documentation.md` exists and includes the evidence table section
- [ ] `flex/` exists and contains the non-Python component
- [ ] `docs/FLEX.md` exists and is meaningful
- [ ] `MANIFEST.txt` is complete
- [ ] there is a minimal automated check for the Flex component
- [ ] `python3 scripts/check_e3.py --repo-root .` gives `status: OK`
- [ ] `e3-freeze` exists and is correct
- [ ] Moodle contains exactly the four required lines

---

## 16. If you need help, send a useful error report

When you report a problem, do **not** send only “it does not work”.

Send this instead:

```text
Team slug:
Repository:
Stage:
Branch currently checked out:
Command I ran:
Full terminal output:
Screenshot from Gitea (if relevant):
What I expected to happen:
```

### Example of a good report

```text
Team slug: team-08
Repository: team-08-s05
Stage: E1
Branch currently checked out: main
Command I ran: git push origin main
Full terminal output: remote: error: Not allowed to push to protected branch main
Screenshot from Gitea: attached
What I expected to happen: push the final E1 version to main
```

That kind of message is actionable.

---

## 17. Final advice

For each stage, keep the workflow boring and deterministic.

A good submission is one where:

- the repository is correct
- `main` is correct
- the tag is correct
- the hash is correct
- Moodle contains the four correct lines

If you are unsure, verify these five things in exactly that order.

Do not wait until the final minutes and do not assume that a branch, a commit message or a screenshot by itself counts as a submission.

The decisive artefacts are always:

- the correct team repository
- the correct final commit on `main`
- the correct stage tag
- the correct Moodle text submission

---

## 18. Source basis for this guide

This guide was prepared from the current RC2026 student announcement, the current student repository template and the current submission-processing rules used for RC2026.

Operationally, it reflects the present Gitea workflow in which:

- each team already has a repository
- stage submission is based on **push to repository + freeze tag + Moodle text submission**
- the repository structure and stage deliverables are checked against the current template and schemas
- repeated Moodle submissions are handled using the first valid submission for lateness and the latest valid submission for the grading target

