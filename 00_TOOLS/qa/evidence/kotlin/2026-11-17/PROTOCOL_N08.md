# N08: Kotlin/JVM Rosetta echo-fragment protocol

## Status and purpose

This protocol is fixed before the first compilation or execution of the Kotlin
fragment. Reading tool versions is environment inspection, not snippet execution.
`PROTOCOL_FREEZE.json` records the SHA-256 of this document and `probe_kotlin.py`.
The harness refuses a mismatch. Any correction before the first compilation must
be recorded in a replacement freeze; a change after execution requires a new
protocol version and an explicit distinction between attempts.

The question is whether the published Kotlin TCP echo fragment compiles with the
identified Kotlin/JVM toolchain and fulfils its bounded byte-stream/EOF contract.
This protocol does not reopen the repository audit.

## Fixed input and toolchain

- Repository: `antonioclim/COMPNET-EN`.
- Candidate commit: `7c79582c5750e9b94b1d7d34d269f080e91a32d3`.
- Candidate tree: `355b2399aec344c63be855cf800c901c92ec4677`.
- Source: `00_APPENDIX/a)PYTHON_self_study_guide/comparisons/ROSETTA_STONE.md`.
- Source SHA-256: `7e83baf7bdced69fce7db7d1ec74fee4742fbbcbc1b07eb6d0f4ee906acb1b5f`.
- Compiler: Kotlin/JVM 2.4.21. The coordinator has already checked the official
  distribution archive: 89,733,618 bytes, SHA-256
  `7cc140e76daf416a0424a5557f99afd7ca89ebd463ea1101261e3e01c33e75cd`.
  This acquisition receipt belongs to the coordinator's evidence; the harness
  records its actual executable, compiler JAR and version separately.
- Java observed by the coordinator before this freeze: OpenJDK 21.0.13.
  The execution record retains the actual `java -version` output. `JAVACMD` and
  `JAVA_HOME` select the supplied Java executable for the Kotlin compiler.
- Host: Linux, with procfs available for process-owned listener verification.

Kotlin/JVM is the tested target. No claim about the distinct Kotlin/Native
compiler or runtime is permitted.

## Invocation and publication layout

The protocol directory is explicit and independent of the harness location.
The intended repository paths are `00_TOOLS/qa/check_kotlin_rosetta.py` and
`00_TOOLS/qa/evidence/kotlin/2026-11-17/` for the protocol and freeze. The script
can be renamed without changing its content hash. Its source-root argument still
requires the exact pinned candidate, which can be a separate clean worktree.

From the repository containing the published harness, with actual environment
paths substituted for the illustrative absolute paths:

```sh
python3 -B 00_TOOLS/qa/check_kotlin_rosetta.py \
  --protocol-dir 00_TOOLS/qa/evidence/kotlin/2026-11-17 \
  --source-root /path/to/clean/pinned-checkout \
  --output-dir /path/to/new-empty-output \
  --kotlinc /path/to/kotlinc/bin/kotlinc \
  --java /path/to/java
```

For the initial coordinator execution from the current workspace:

```sh
python3 -B N08_KOTLIN/probe_kotlin.py \
  --protocol-dir N08_KOTLIN \
  --source-root F3_R15_INTEGRATION/repository \
  --output-dir N08_KOTLIN/execution \
  --kotlinc N08_KOTLIN/toolchain/kotlinc/bin/kotlinc \
  --java /usr/bin/java
```

If stdout is redirected, its destination must be outside the initially empty
output directory. The harness copies the exact protocol, freeze and its own
source into the resulting evidence directory. Publication does not add this
probe to CI or the native-acceptance collector automatically.

## Extraction and generated wrappers

There is exactly one executable Kotlin fence in Rosetta Stone. The harness reads
its bytes directly, preserves the entire fence body, and adds only
`import java.net.ServerSocket` and `fun main() { ... }` outside that body.
It verifies the original source hash, clean Git identity, unique fence and exact
body placement. The extracted body, wrapper, generated JAR and diagnostics receive
separate SHA-256 records.

Two variants are fixed:

1. **`exact_8080`:** the original body, including `ServerSocket(8080)`, unchanged.
2. **`derived_50081`:** one replacement only,
   `ServerSocket(8080)` → `ServerSocket(50081)`. The original-body hash and the
   derived-body hash remain distinct. This is a derived socket-port test, not an
   execution of an unchanged published body.

The three `kotlin` fences in `MISCONCEPTIONS_BY_BACKGROUND.md` contain comments
and illustrative ellipses. They are not compiled or counted as runnable examples.
Rosetta Stone has no Kotlin binary-header parser; none is added by this protocol.
The historical Java unsigned values are not attributed to Kotlin.

## Fixed matrix

| ID | Criterion | Passing observation |
| --- | --- | --- |
| K01 | Exact extraction and identity | Pinned clean Git commit/tree, source hash and unique byte-preserved body |
| K02 | Kotlin/JVM compilation | Both wrappers compile successfully into the requested JARs |
| K03 | Empty first client | Exact variant receives zero bytes, returns EOF and keeps its accept loop alive |
| K04 | Fragmented binary echo | Exact variant echoes all 6,144 bytes identically, followed by EOF |
| K05 | Client after EOF | Exact variant accepts another client, echoes its distinct payload and remains alive |
| K06 | High socket port | Derived port-50081 variant passes compilation and the same three client scenarios |
| K07 | Owned-process cleanup | Direct children are reaped and no active members of their separately created groups remain |

For each variant, the first successful connection is the empty-client test, not
a discarded readiness connection. It performs `shutdown(SHUT_WR)` without data
and expects EOF. Readiness is established by inspecting the JVM's socket inode
through procfs before any connection is made.

The second client sends `bytes(range(256)) * 24`: exactly 6,144 bytes, covering
zero bytes and values above 127 and exceeding the 1,024-byte server buffer. It
first sends three bytes and receives their exact echo **before** sending the
remaining bytes in chunks of at most 997 bytes. It then half-closes its write
side, reads the rest of the echo and checks EOF. Application write sizes do not
claim control over TCP segment boundaries or individual server `read()` sizes.

The third client sends `b'N08-client-after-EOF\x00\xff'`, half-closes, receives the
exact echo and EOF, and checks that the server process is still alive.

## Ports, ownership and process limits

Only IPv4 loopback clients are used. The teaching fragment itself retains its
published `ServerSocket` binding behaviour. JVM startup includes
`-Djava.net.preferIPv4Stack=true`; the harness nevertheless understands socket
inode entries in both `/proc/net/tcp` and `/proc/net/tcp6`.

A preflight wildcard bind checks each fixed port without listening or connecting.
If a port is occupied, that variant is `BLOCKED`: there is no alternate port,
connection to the existing service or attempt to terminate it. Before every
client connection, the listener must belong to the JVM process launched by this
invocation. A competing listener observed after preflight also causes `BLOCKED`.
An inability to establish ownership from procfs prevents the connection.

All subprocesses start in a separate owned session. Cleanup sends signals only
to those recorded process groups, never to a process found by port or name.
The direct child is reaped through `Popen`; procfs confirms the absence of active
members of that owned group even if its leader exited earlier. Zombie/dead states
are recorded separately. The harness does not claim to reap nonchild descendants
that have been adopted by another parent.
Normal termination of the intentionally infinite teaching server is recorded as
harness cleanup, not as an application crash.

Fixed limits are 20 seconds for metadata/version commands, 60 seconds per
compilation, 12 seconds for startup, 3 seconds per socket operation (an absolute
3-second deadline for each complete `receive_exact` exchange), and
3 seconds for termination followed, if needed, by 2 seconds after a kill.
Interrupt signals set a persistent stop request. While cleanup is in progress,
the handler records the request without interrupting that cleanup. The partial
variant is saved and interruption propagates to the final report; no later
variant or compilation starts after that request.
No operation retries indefinitely. The output directory must be empty and outside
the source checkout; existing output evidence is not overwritten.

## Evidence and outcome interpretation

The JSON report retains commands, exact tool versions, exit codes, stdout/stderr
files, timings, hashes, extraction offsets, listener ownership, payload/echo
hashes, individual client results and cleanup details. Both variants are attempted
independently after valid source/toolchain preflight unless an interrupt requests
that the run stop. A block or failure produces
JSON, including retained partial observations. If the requested output location
cannot safely be written, JSON is emitted on stdout instead.

- `PASS` means the declared criterion was observed.
- `BLOCKED` identifies an environment, input or provenance condition that
  prevented the requested execution.
- `FAIL` records an unmet compilation, stream or deadline criterion and preserves
  diagnostics; it does not automatically establish a defect in the source.
- `ERROR` identifies a harness/input/cleanup failure requiring review.
- `NOT_RUN` preserves criteria that were never reached.

Known environment diagnostics and occupied/forbidden ports are separated from
observed contract mismatches. Nonzero compiler exits or I/O failures with
undetermined attribution require inspection before being called source defects.

Only a complete pass of both variants can yield
`PASS_KOTLIN_JVM_FRAGMENT_SCOPE_ONLY`. Other outcomes leave `N08_NOT_CLOSED`.
Current Kotlin results are not merged with historical C/Java/Node/Python test
counts and are not a new execution of those languages. The frozen source identity
allows their continuity to be discussed separately.

## Explicit limits

This protocol does not test arbitrary client resets, concurrent service,
production exception handling, throughput, UDP, remote hosts, IPv6 clients,
binary-header parsing in Kotlin, VM import/boot, Windows, Docker, Mininet/OVS,
browser interaction, native workbook use or LMS import. Those gates remain open.
OVA is neither requested nor accessed. Licence, merge, tags, releases and Zenodo
are not changed by this harness. A successful component probe does not complete
F6 or establish all native release gates.
