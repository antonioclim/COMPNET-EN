# N08: Kotlin/JVM Rosetta component acceptance

On 17 November 2026 the published Kotlin TCP echo fragment was compiled and
executed on Linux with Kotlin/JVM 2.4.21 and OpenJDK 21.0.13. All seven criteria
in the frozen protocol passed. This closes the previously pending Kotlin
component gate **N08 within the scope below**.

The teaching fragment did not require a source correction. This update publishes
the optional [probe program](check_kotlin_rosetta.py), its protocol and retained
evidence, and records the new result under F3-R13. It adds a QA program; existing
course runtime files, workflow definitions and licence terms remain unchanged.

## Tested identity and publication identity

| Item | Recorded identity |
| --- | --- |
| Tested commit | `7c79582c5750e9b94b1d7d34d269f080e91a32d3` |
| Tested tree | `355b2399aec344c63be855cf800c901c92ec4677` |
| Rosetta source SHA-256 | `7e83baf7bdced69fce7db7d1ec74fee4742fbbcbc1b07eb6d0f4ee906acb1b5f` |
| Executed harness SHA-256 | `fc90a248212151d4bcdfd7380f2488909f88481c612a4e5b893478a4acd0574e` |
| Protocol freeze | `2026-11-17T19:15:20Z` |
| Execution | `2026-11-17T19:17:00.476491+00:00` to `2026-11-17T19:17:13.655541+00:00` |

The tested checkout was clean. The commit which publishes these records is a
later successor: its exact SHA belongs to the integration receipt. Publication
does not imply a rerun on that successor. Rosetta and the published probe bytes
are linked to the execution by their hashes. The older F5 component results
retain their own source identity and are not added to the current counts.

## Observed results

| Criterion | Observation | Result |
| --- | --- | --- |
| K01 | Exact source identity and unique Kotlin-fence extraction | PASS |
| K02 | Original-port and derived-port wrappers both compiled, exit code 0 | PASS |
| K03 | Empty first client received EOF; the original server remained alive | PASS |
| K04 | All 6,144 binary bytes echoed exactly, followed by EOF | PASS |
| K05 | A further client after EOF received its distinct 22-byte payload | PASS |
| K06 | The same three scenarios passed on derived TCP port 50081 | PASS |
| K07 | Owned server processes stopped; no active owned-group members remained | PASS |

These counts describe **one probe, two compilations and six client scenarios**.
They are not added to pytest totals. On each port, the first three payload bytes
were echoed before the remaining bytes were sent. The full payload exceeds the
1,024-byte server buffer and contains every byte value, including NUL and values
above 127. Application writes were staged; no TCP segment-boundary control is
claimed.

For port **8080**, the extracted body was preserved byte for byte. Only an import
and a main-function wrapper were supplied outside that body, as required for
the published core fragment. For port **50081**, the sole body change was
`ServerSocket(8080)` to `ServerSocket(50081)`; this derivation has its own hash.
Rosetta contains no Kotlin binary-header parser. The high-port socket test does
not replace or relabel the historical Java unsigned-parsing probe.

The servers intentionally have an unbounded accept loop. After the observations,
the harness terminated its own processes with SIGTERM and verified cleanup.
Their cleanup exit code 143 is recorded separately from compiler exit code 0
and from the successful client observations.

## Evidence

- [Bounded attestation](evidence/kotlin/2026-11-17/N08_ATTESTATION.json).
- [Unmodified execution report](evidence/kotlin/2026-11-17/N08_KOTLIN_RESULTS.json).
- [Frozen protocol](evidence/kotlin/2026-11-17/PROTOCOL_N08.md) and
  [freeze record](evidence/kotlin/2026-11-17/PROTOCOL_FREEZE.json).
- [Diagnostic streams and command records](evidence/kotlin/2026-11-17/LOGS.json).
- [Generated-artifact manifest](evidence/kotlin/2026-11-17/ARTIFACTS.json).
- [Official compiler asset](evidence/kotlin/2026-11-17/OFFICIAL_COMPILER_ASSET.json),
  [download verification](evidence/kotlin/2026-11-17/COMPILER_DOWNLOAD.json) and
  [tool versions](evidence/kotlin/2026-11-17/TOOLCHAIN_READY.json).
- [Preparation review](evidence/kotlin/2026-11-17/PRE_EXECUTION_REVIEW.json) and
  [retained-evidence review](evidence/kotlin/2026-11-17/POST_EXECUTION_REVIEW.json).

The raw report preserves the original local paths. `LOGS.json` retains each
diagnostic stream and command record as exact UTF-8 text with its original byte
count and hash. `ARTIFACTS.json` maps the original files to these retained forms.
The compiler distribution and generated JARs are not committed. Their digests
identify this execution; rebuilding follows the recorded commands and is not
claimed to reproduce JAR packaging timestamps byte for byte.

## Reproduce the bounded probe

The [official command-line documentation](https://kotlinlang.org/docs/command-line.html)
describes standalone compilation. Use the pinned
[Kotlin 2.4.21 distribution](https://github.com/JetBrains/kotlin/releases/tag/v2.4.21)
and compare the downloaded ZIP with this recorded SHA-256 before extraction:

```text
7cc140e76daf416a0424a5557f99afd7ca89ebd463ea1101261e3e01c33e75cd
```

From the repository containing this note, prepare a separate clean worktree of
the actual tested commit. The command refuses to overwrite an existing worktree:

```sh
git worktree add --detach ../COMPNET-EN-N08-input 7c79582c5750e9b94b1d7d34d269f080e91a32d3
```

Then run the published harness, substituting the actual compiler location:

```sh
python3 -B 00_TOOLS/qa/check_kotlin_rosetta.py \
  --protocol-dir 00_TOOLS/qa/evidence/kotlin/2026-11-17 \
  --source-root ../COMPNET-EN-N08-input \
  --output-dir ../COMPNET-EN-N08-results \
  --kotlinc /path/to/kotlinc/bin/kotlinc \
  --java /usr/bin/java
```

This protocol requires Linux procfs. The output directory must be new or empty
and outside the input checkout. Ports 8080 and 50081 must be free. The harness
does not contact or stop an existing service: an occupied port or unverified
listener ownership is reported as blocked. It records the actual compiler/JVM
versions, handles interruption and retains partial results. It runs only when
explicitly invoked; it is not added to the automatic source gate or acceptance
collector.

## Remaining acceptance

This result is an actual Kotlin/JVM component execution. VM import/boot,
host-to-guest routes, native Windows, Docker/Mininet/OVS, real capture and transfer,
browser controls, workbook interaction and LMS import remain separate gates.
Concurrent service, arbitrary resets, production exception handling, performance,
IPv6 clients and Kotlin/Native are outside this protocol. F6 is not declared
complete, and no licence, merge, tag, release or Zenodo decision is inferred.
The [candidate acceptance record](REMEDIATION_v1.5.0.md) remains authoritative
for these outstanding scopes.
