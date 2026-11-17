# Python self-study: canonical COMPNET-EN paths

Use this map with the [Python guide](PYTHON_NETWORKING_GUIDE.md) and its ten HTML
modules. Run terminal commands from the **repository root inside the Linux VM or
selected WSL environment**. A slide's Simulate/Show output control displays a
prepared teaching illustration; it does not execute Python or generate a capture.

| Module | Real source or entry point | What to inspect or run |
|---|---|---|
| 1–2: setup and reading | [05_ping_latency.py](examples/05_ping_latency.py) | Dataclass, argparse, subprocess result and bounded failure handling |
| 3: bytes and text | [02_bytes_vs_str.py](examples/02_bytes_vs_str.py) | Encoding, decoding and temporary-file ownership |
| 4: sockets | [01_socket_tcp.py](examples/01_socket_tcp.py), [S02](../../04_SEMINARS/S02/) | Separate server/client processes and the actual protocol handout |
| 5: organisation | [03_struct_parsing.py](examples/03_struct_parsing.py) | Importable functions, IPHeader dataclass and main guard |
| 6: CLI | [05_ping_latency.py](examples/05_ping_latency.py), [lab runner](../../00_TOOLS/lab_runner/) | The actual --help and documented arguments |
| 7: packet analysis | [S07](../../04_SEMINARS/S07/), [PCAP tools](../../00_TOOLS/pcap/) | Capture privileges, interfaces and parsed fields |
| 8: concurrency | [S03 multi-client server](../../04_SEMINARS/S03/S03_Part01_Example_TCP_Multi_client_Server.py) | Client lifetime, framing and concurrency |
| 9: HTTP | [S08](../../04_SEMINARS/S08/), [C10 scenarios](../../03_LECTURES/C10/) | HTTP framing, request/response bytes and proxy behaviour |
| 10: debugging | [04_error_handling.py](examples/04_error_handling.py), [tests](examples/tests/) | Resource ownership, errors and component regression evidence |

## First runnable checks

```bash
cd "$HOME/COMPNET-EN"
python3 "00_APPENDIX/a)PYTHON_self_study_guide/examples/05_ping_latency.py" --host 127.0.0.1 --count 3
python3 "00_APPENDIX/a)PYTHON_self_study_guide/examples/02_bytes_vs_str.py"
python3 "00_APPENDIX/a)PYTHON_self_study_guide/examples/03_struct_parsing.py"
```

The ping helper needs Linux `ping` (iputils-ping). A missing command, unsuccessful
reply or unparsed RTT produces a non-zero exit. Report those observations rather
than substituting the slide's example timings.

For the socket example, use two Linux terminals in the repository root:

```bash
# Terminal A: stop with Ctrl+C after the experiment.
python3 "00_APPENDIX/a)PYTHON_self_study_guide/examples/01_socket_tcp.py" server 9090
```

```bash
# Terminal B
python3 "00_APPENDIX/a)PYTHON_self_study_guide/examples/01_socket_tcp.py" client 127.0.0.1 9090 "Test"
```

For subnetting, the C05 calculator accepts a positional address/prefix:

```bash
python3 03_LECTURES/C05/assets/scenario-cidr-basic/cidr-calc.py 192.168.23.233/24
```

Do not assume every course script implements argparse or a common `--mode` option.
The S04 text framing, binary framing and pickle-based UDP exercise are defined by
[S04's source and handouts](../../04_SEMINARS/S04/). Generic JSON, checksum and package
sketches in this Python guide are separate learning examples.

## Provenance

Earlier versions of these optional materials referred to the external netROwsl kit.
The v1.5.0 revision maps learning activities to COMPNET-EN while retaining the Python
concepts. Repository v1.4.0 preserves the prior text. The VM remains
[MININET-SDN 1.0.0](https://doi.org/10.5281/zenodo.24289763); see
[environment routes](../docs/environment_routes.md) for installation and Portainer.
