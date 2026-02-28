# 01_network_applications/assets/puml — Project Architecture Diagrams

Fifty-four PlantUML source files providing three diagrams per S-project: an architecture overview, an E2 message-flow sequence and a state-transition diagram.

## Naming Convention

Each file follows the pattern `fig-S{NN}-{type}.puml`:

| Suffix | Diagram type | Purpose |
|---|---|---|
| `-architecture` | Component/deployment diagram | Container topology and network connections |
| `-e2-message-flow` | Sequence diagram | E2 test scenario: tester ↔ service protocol exchange |
| `-e3-states` | State diagram | Application-level state machine (connections, sessions, errors) |

## File Count

60 files total (20 projects × 3 diagrams). Every project from S01 to S20 has a complete set.

## Usage

Render via the parent script:

```bash
bash ../render.sh
```

Output PNGs appear in `../images/`.

## Cross-References

Each diagram set corresponds to a project brief in [`../../`](../../) (for example `fig-S16-architecture.puml` illustrates `S16_collaborative_text_editing_locking_notifications_and_versioned_saves.md`).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/01_network_applications/assets/puml
```
