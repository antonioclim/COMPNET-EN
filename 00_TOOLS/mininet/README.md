# Mininet / Open vSwitch utilities

## `ovs_reset.sh`

A **lab-only** deep reset helper for Mininet + Open vSwitch.

### When to use it

Use this script when:

- Mininet topologies hang at **“Waiting for switches to connect”**;
- OVS bridges are left behind after an unclean shutdown;
- `sudo mn -c` is **not** enough.

### What it does

1. Stops common Mininet and controller processes (best effort).
2. Deletes all Open vSwitch bridges recorded in the OVS database.
3. Runs `mn -c` when Mininet is installed.
4. Restarts the Open vSwitch service (best effort).
5. Verifies that no bridges remain.

### Usage

```bash
# Non-destructive check
bash 00_TOOLS/mininet/ovs_reset.sh --verify

# Full reset (requires sudo)
sudo bash 00_TOOLS/mininet/ovs_reset.sh
```

### Safety note

This script removes **all** OVS bridges on the host. Do not run it on machines
where Open vSwitch is used outside the lab.
