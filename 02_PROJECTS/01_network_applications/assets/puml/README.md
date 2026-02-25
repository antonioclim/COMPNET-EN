# 01_network_applications/assets/puml — Project Architecture Diagrams

Forty-five PlantUML source files providing three diagrams per S-project: an architecture overview, an E2 message-flow sequence and a state-transition diagram.

## Naming Convention

Each file follows the pattern `fig-S{NN}-{type}.puml`:

| Suffix | Diagram type | Purpose |
|---|---|---|
| `-architecture` | Component/deployment diagram | Container topology and network connections |
| `-e2-message-flow` | Sequence diagram | E2 test scenario: tester ↔ service protocol exchange |
| `-e3-states` | State diagram | Application-level state machine (connections, sessions, errors) |

## File Count

45 files total (15 projects × 3 diagrams). Every project from S01 to S15 has a complete set.

## Usage

Render via the parent script:

```bash
bash ../render.sh
```

Output PNGs appear in `../images/`.

## Cross-References

Each diagram set corresponds to a project brief in [`../../`](../../) (e.g. `fig-S01-architecture.puml` illustrates `S01_multi_client_tcp_chat_text_protocol_and_presence.md`).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/01_network_applications/assets/puml
```
