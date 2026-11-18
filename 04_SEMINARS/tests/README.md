# Seminar regression checks

Run these from the repository root:

```bash
python3 -m venv .venv-seminar-tests
. .venv-seminar-tests/bin/activate
python -m pip install pytest
python -m pytest -q 04_SEMINARS/tests/test_protocol_regressions.py
node 04_SEMINARS/tests/test_html_models.cjs
```

The Python suite exercises the actual supplied handlers over local IPv4 sockets,
plus framing, serialisation, JSON-RPC and port/configuration boundary cases. It does
not send traffic to third-party systems. Tests use ephemeral local ports.

The Node checks execute the actual helper functions and routing/SDN state models
extracted from the HTML sources. Animation and DOM elements are replaced by explicit
stubs. They verify arithmetic, filtering, packet fields, gateways, return paths and
flow reuse; they are not native browser or accessibility acceptance.

These checks do not start Docker, Mininet, Open vSwitch or VirtualBox. The corresponding
laboratory walkthroughs, captures, platform-specific commands and rendered browser
interactions still require the documented native environments. Student TODOs remain
exercises, not promised completed implementations.
