The following materials make up **the first part of the seminar**:

## **STAGE 1 — Triangle Topology with 3 Routers + Static Routing (Mininet)**

As in earlier seminars, the deliverables consist of:

1. **`index_routing-triangle_explanation.md`**
2. **`index_routing-triangle_topology.py`** – complete, annotated Mininet code
3. **`index_routing-triangle_tasks.md`** – student exercises + deliverable

Once this part is complete, the SDN section follows.

---

# 1. `index_routing-triangle_explanation.md`

```markdown
### Introduction: Routing across Three Routers (Triangle Topology)

This section uses Mininet to build a topology comprising three Linux routers (Mininet nodes with IP forwarding enabled) and two hosts. The goal is to configure static routes so that h1 and h3 can communicate through different paths within the triangle.

Topology used:

```

```
h1
 |
r1 ----- r2
 \       /
  \     /
    r3
    |
    h3
```

```

This structure supports the analysis of:
- static routing over multiple paths
- routing tables distributed across several routers
- how configuration changes affect the `traceroute` output
- path switching by modifying a single hop

---

### Addressing Scheme

For simplicity, /30 subnets are used — one per point-to-point link:

| Link            | Subnet        | r1 IP      | r2 IP      | r3 IP      | h1/h3 |
|-----------------|---------------|------------|------------|------------|-------|
| h1 ↔ r1         | 10.0.1.0/30   | 10.0.1.1   | —          | —          | 10.0.1.2 |
| r1 ↔ r2         | 10.0.12.0/30  | 10.0.12.1  | 10.0.12.2  | —          | —     |
| r2 ↔ r3         | 10.0.23.0/30  | —          | 10.0.23.1  | 10.0.23.2  | —     |
| r1 ↔ r3         | 10.0.13.0/30  | 10.0.13.1  | —          | 10.0.13.2  | —     |
| r3 ↔ h3         | 10.0.3.0/30   | —          | —          | 10.0.3.1   | 10.0.3.2 |
