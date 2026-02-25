# 02_administration_security/assets/puml — A-Project Architecture Diagrams

Thirty PlantUML source files providing three diagrams per A-project: an architecture overview, a demo-scenario sequence and a message-flow diagram.

## Naming Convention

Each file follows the pattern `fig-A{NN}-{type}.puml`:

| Suffix | Diagram type | Purpose |
|---|---|---|
| `-architecture` | Component/deployment diagram | Mininet topology, OVS bridges and container layout |
| `-demo-scenario` | Sequence diagram | Demonstration script: attacker/defender/observer interactions |
| `-message-flow` | Sequence diagram | Protocol-level exchange during E2 automated run |

## File Count

30 files total (10 projects × 3 diagrams). Every project from A01 to A10 has a complete set.

## Usage

Render via the parent script:

```bash
bash ../render.sh
```

Output PNGs appear in `../images/`.

## Cross-References

Each diagram set corresponds to a project brief in [`../../`](../../) (e.g. `fig-A01-architecture.puml` illustrates `A01_sdn_firewall_filtering_policies_via_openflow_rules.md`).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/02_administration_security/assets/puml
```
