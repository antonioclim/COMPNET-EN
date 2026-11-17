#!/usr/bin/env python3
"""Bounded N08 Kotlin/JVM fragment probe; no repository mutations or remote traffic."""
from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone

COMMIT = "7c79582c5750e9b94b1d7d34d269f080e91a32d3"
TREE = "355b2399aec344c63be855cf800c901c92ec4677"
SOURCE = "00_APPENDIX/a)PYTHON_self_study_guide/comparisons/ROSETTA_STONE.md"
SOURCE_SHA256 = "7e83baf7bdced69fce7db7d1ec74fee4742fbbcbc1b07eb6d0f4ee906acb1b5f"
EXPECTED_KOTLIN = "2.4.21"
TIMEOUTS = {"metadata": 20, "compile": 60, "startup": 12, "socket": 3,
            "cleanup_term": 3, "cleanup_kill": 2}
PREFIX = b"import java.net.ServerSocket\n\nfun main() {\n"
PAYLOAD = bytes(range(256)) * 24
FOLLOWUP = b"N08-client-after-EOF\x00\xff"
_INTERRUPTION = None
_CLEANUP_DEPTH = 0


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def describe(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": sha(data)}


class StopProbe(Exception):
    def __init__(self, status, domain, message, **details):
        super().__init__(message)
        self.record = {"status": status, "domain": domain, "message": message,
                       "defect_attribution": "NOT_ASSUMED", **details}


def blocked(domain, message, **details):
    raise StopProbe("BLOCKED", domain, message, **details)


def failed(domain, message, **details):
    raise StopProbe("FAIL", domain, message, **details)


def raise_if_interrupted(partial_variant=None):
    if _INTERRUPTION is not None:
        exc = StopProbe("ERROR", "HARNESS_INTERRUPTED", "Probe interrupted; no further compilation or scenario is started",
                        interruption=_INTERRUPTION)
        exc.partial_variant = partial_variant
        raise exc


def resolve_tool(value):
    found = shutil.which(value)
    if found is None:
        blocked("ENVIRONMENT", "Requested executable is unavailable", executable=value)
    path = Path(found).resolve()
    if not path.is_file() or not os.access(path, os.X_OK):
        blocked("ENVIRONMENT", "Requested executable is not an executable file", executable=str(path))
    return path


def owned_group_members(process_group):
    """Inspect only membership of the session/group created by this invocation."""
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return []
    members = []
    for directory in Path("/proc").iterdir():
        if not directory.name.isdigit():
            continue
        try:
            fields = (directory / "stat").read_text().rsplit(")", 1)[1].split()
        except FileNotFoundError:
            continue
        if int(fields[2]) != process_group:
            continue
        if int(fields[3]) != process_group:
            raise RuntimeError("Observed group does not belong to the separately created session")
        members.append({"pid": int(directory.name), "state": fields[0],
                        "parent_pid": int(fields[1]), "process_group": int(fields[2]),
                        "session": int(fields[3]), "active": fields[0] not in {"Z", "X"}})
    return members


def stop_owned(process):
    """Stop an owned group, reap its direct child and inspect remaining members."""
    global _CLEANUP_DEPTH
    _CLEANUP_DEPTH += 1
    item = {"pid": process.pid, "owned_session": True, "signals": [], "status": "PASS"}
    def wait_for_group(seconds):
        deadline = time.monotonic() + seconds
        while True:
            process.poll()  # Reap only our own direct child, if it has exited.
            observed = owned_group_members(process.pid)
            if not any(x["active"] for x in observed) or time.monotonic() >= deadline:
                return observed
            time.sleep(min(0.05, max(0.0, deadline - time.monotonic())))
    try:
        process.poll()
        observed = owned_group_members(process.pid)
        item["group_members_before"] = observed
        for signum, label, timeout in [(signal.SIGTERM, "SIGTERM", TIMEOUTS["cleanup_term"]),
                                       (signal.SIGKILL, "SIGKILL", TIMEOUTS["cleanup_kill"])]:
            if not any(x["active"] for x in observed):
                break
            try:
                os.killpg(process.pid, signum)
                item["signals"].append(label)
            except ProcessLookupError:
                pass
            observed = wait_for_group(timeout)
        process.poll()
        item["returncode"] = process.returncode
        item["direct_child_reaped"] = process.returncode is not None
        item["group_members_after"] = observed
        item["active_group_members_remaining"] = sum(x["active"] for x in observed)
        item["nonchild_descendants_reaped_by_harness"] = False
        if item["active_group_members_remaining"] or not item["direct_child_reaped"]:
            item.update(status="ERROR", domain="HARNESS_CLEANUP", error="Owned group or direct child did not finish within cleanup limits")
    except Exception as exc:
        item.update(status="ERROR", domain="HARNESS_CLEANUP", error=repr(exc))
    finally:
        _CLEANUP_DEPTH -= 1
    return item


def command(args, directory, name, timeout, env=None, cwd=None):
    """Persist every command and its complete small diagnostic streams."""
    raise_if_interrupted()
    started = time.monotonic()
    result = {"argv": [str(x) for x in args], "started_at_utc": utc(),
              "timeout_seconds": timeout, "status": "NOT_RUN"}
    process = None
    stdout = stderr = b""
    try:
        process = subprocess.Popen(result["argv"], cwd=cwd, env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            result.update(returncode=process.returncode,
                          status="PASS" if process.returncode == 0 else "NONZERO")
        except subprocess.TimeoutExpired:
            result["timeout_cleanup"] = stop_owned(process)
            stdout, stderr = process.communicate(timeout=TIMEOUTS["cleanup_kill"])
            result.update(returncode=process.returncode, status="TIMEOUT")
    except OSError as exc:
        result.update(status="BLOCKED", domain="ENVIRONMENT", error=repr(exc))
    finally:
        if process is not None:
            result["cleanup"] = stop_owned(process)
            if result["cleanup"]["status"] != "PASS":
                result["status"] = "ERROR"
        for label, data in [("stdout", stdout), ("stderr", stderr)]:
            path = directory / (name + "." + label + ".log")
            path.write_bytes(data)
            result[label] = describe(path)
        result["duration_seconds"] = round(time.monotonic() - started, 6)
        (directory / (name + ".command.json")).write_text(json.dumps(result, indent=2) + "\n")
    raise_if_interrupted()
    return result, stdout.decode("utf-8", errors="replace") + stderr.decode("utf-8", errors="replace")


def require_command(result, diagnostic, purpose):
    if result["status"] == "ERROR":
        raise StopProbe("ERROR", "HARNESS_COMMAND_CLEANUP", purpose + " cleanup could not be confirmed",
                        command_status=result["status"], diagnostic=diagnostic)
    if result["status"] != "PASS":
        blocked("ENVIRONMENT_OR_INPUT", purpose + " did not complete successfully",
                command_status=result["status"], diagnostic=diagnostic)


def verify_protocol(report, protocol_directory):
    directory = protocol_directory.resolve()
    protocol = directory / "PROTOCOL_N08.md"
    freeze_path = directory / "PROTOCOL_FREEZE.json"
    freeze = json.loads(freeze_path.read_text())
    if sha(protocol.read_bytes()) != freeze["protocol"]["sha256"]:
        blocked("PROVENANCE", "Protocol differs from the pre-compilation freeze")
    if sha(Path(__file__).read_bytes()) != freeze["harness"]["sha256"]:
        blocked("PROVENANCE", "Harness differs from the pre-compilation freeze")
    if freeze["first_compilation_performed_at_freeze"] is not False:
        blocked("PROVENANCE", "Freeze does not establish a protocol before compilation")
    report["protocol"] = {"document": describe(protocol), "freeze": describe(freeze_path),
                          "frozen_at_utc": freeze["frozen_at_utc"]}


def extract_source(source_root, output, report):
    git = resolve_tool("git")
    facts = {}
    for name, args in [("commit", ["rev-parse", "HEAD"]),
                       ("tree", ["rev-parse", "HEAD^{tree}"]),
                       ("status", ["status", "--porcelain", "--untracked-files=all"])]:
        item, diagnostic = command([git, "-C", source_root, *args], output, "git_" + name,
                                   TIMEOUTS["metadata"])
        require_command(item, diagnostic, "Git identity inspection")
        facts[name] = Path(item["stdout"]["path"]).read_text().strip()
    report["git"] = facts
    if facts != {"commit": COMMIT, "tree": TREE, "status": ""}:
        blocked("PROVENANCE", "An exact, clean checkout of the pinned candidate is required", observed=facts)
    path = source_root / SOURCE
    data = path.read_bytes()
    report["source"] = {**describe(path), "repository_relative_path": SOURCE}
    if sha(data) != SOURCE_SHA256:
        blocked("PROVENANCE", "Rosetta Stone does not match the pinned source hash")
    matches = list(re.finditer(rb"(?ms)^```kotlin[ \t]*\r?\n(.*?)^```[ \t]*\r?$", data))
    if len(matches) != 1:
        blocked("PROVENANCE", "Expected exactly one Kotlin fence", observed=len(matches))
    body = matches[0].group(1)
    if body.count(b"ServerSocket(8080)") != 1:
        blocked("PROVENANCE", "Expected exactly one original port constructor")
    path = output / "EXTRACTED_KOTLIN_BODY.kt"
    path.write_bytes(body)
    report["extracted_fragment"] = {**describe(path), "source_fence_count": 1,
        "source_first_line": data[:matches[0].start(1)].count(b"\n") + 1,
        "source_byte_start": matches[0].start(1), "source_byte_end": matches[0].end(1),
        "body_changed": False, "standalone_program": False}
    report["checks"]["K01"] = {"status": "PASS", "meaning": "Exact extraction and clean pinned checkout"}
    return body


def listener_ownership(process, port):
    """Read Linux procfs; never use a connection as an ownership probe."""
    try:
        inodes = set()
        for fd in (Path("/proc") / str(process.pid) / "fd").iterdir():
            try:
                target = os.readlink(fd)
            except FileNotFoundError:
                continue
            if target.startswith("socket:[") and target.endswith("]"):
                inodes.add(target[8:-1])
        listeners = []
        for table in ["tcp", "tcp6"]:
            path = Path("/proc/net") / table
            if not path.exists():
                continue
            for line in path.read_text().splitlines()[1:]:
                fields = line.split()
                if len(fields) > 9 and fields[3] == "0A" and int(fields[1].split(":")[1], 16) == port:
                    listeners.append({"table": table, "local_address_hex": fields[1],
                                      "inode": fields[9], "owned": fields[9] in inodes})
        return {"pid": process.pid, "port": port, "observed_at_utc": utc(),
                "listeners": listeners, "owned_listener": any(x["owned"] for x in listeners),
                "foreign_listener": any(not x["owned"] for x in listeners)}
    except (OSError, ValueError) as exc:
        blocked("ENVIRONMENT", "Cannot safely establish JVM listener ownership from procfs", error=repr(exc))


def runtime_exit_record(process, stderr_path):
    diagnostic = stderr_path.read_text(errors="replace")
    environment_markers = ["BindException", "Address already in use", "Permission denied",
                           "Operation not permitted", "UnsupportedClassVersionError", "OutOfMemoryError"]
    if any(text in diagnostic for text in environment_markers):
        blocked("ENVIRONMENT", "JVM exited before the requested probe could complete",
                returncode=process.returncode, diagnostic=diagnostic)
    failed("RUNTIME_REQUIRES_REVIEW", "JVM exited unexpectedly; source defect is not automatically inferred",
           returncode=process.returncode, diagnostic=diagnostic)


def connect_owned(process, port, stderr_path, observations):
    if process.poll() is not None:
        runtime_exit_record(process, stderr_path)
    ownership = listener_ownership(process, port)
    observations.append(ownership)
    if ownership["foreign_listener"]:
        blocked("ENVIRONMENT", "A non-owned listener is present; no connection attempted", ownership=ownership)
    if not ownership["owned_listener"]:
        blocked("ENVIRONMENT", "No listener owned by this JVM; no connection attempted", ownership=ownership)
    return socket.create_connection(("127.0.0.1", port), timeout=TIMEOUTS["socket"])


def receive_exact(connection, length):
    chunks = []
    remaining = length
    deadline = time.monotonic() + TIMEOUTS["socket"]
    while remaining:
        seconds_left = deadline - time.monotonic()
        if seconds_left <= 0:
            raise TimeoutError("Absolute receive deadline exceeded")
        connection.settimeout(seconds_left)
        chunk = connection.recv(min(4096, remaining))
        if not chunk:
            failed("RUNTIME_CONTRACT", "EOF arrived before the expected echo length", missing_bytes=remaining)
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def receive_eof(connection):
    connection.settimeout(TIMEOUTS["socket"])
    tail = connection.recv(1)
    if tail != b"":
        failed("RUNTIME_CONTRACT", "Expected EOF, but additional bytes were returned", extra_byte_hex=tail.hex())


def run_variant(name, port, body, original_body, output, kotlinc, java, compiler_env, retained_variants):
    raise_if_interrupted()
    directory = output / name
    directory.mkdir()
    wrapper = PREFIX + body + (b"" if body.endswith(b"\n") else b"\n") + b"}\n"
    source_path = directory / "RosettaKotlinAudit.kt"
    source_path.write_bytes(wrapper)
    assert wrapper[len(PREFIX):len(PREFIX) + len(body)] == body
    derived = port != 8080
    if derived:
        assert body == original_body.replace(b"ServerSocket(8080)", b"ServerSocket(50081)", 1)
    else:
        assert body == original_body
    result = {"name": name, "port": port, "endpoint": "127.0.0.1:" + str(port),
        "status": "NOT_RUN", "derived": derived,
        "source_transformation": "Only ServerSocket(8080) -> ServerSocket(50081)" if derived else "None",
        "body_sha256": sha(body), "body_bytes": len(body), "wrapper": describe(source_path),
        "wrapper_prefix_bytes": len(PREFIX), "body_preserved_byte_for_byte": True,
        "cases": {key: {"status": "NOT_RUN"} for key in ["empty_client", "fragmented_echo", "following_client"]},
        "ownership_observations": [], "cleanup": {"status": "NOT_RUN", "process_started": False}}
    # Retain the live record even if interruption occurs during final file writing.
    retained_variants.append(result)
    jar = directory / "rosetta-kotlin.jar"
    process = None
    active_case = None
    stdout_path, stderr_path = directory / "runtime.stdout.log", directory / "runtime.stderr.log"
    out_stream = err_stream = None
    try:
        compiled, diagnostics = command([kotlinc, source_path, "-include-runtime", "-d", jar],
                                        directory, "compile", TIMEOUTS["compile"], env=compiler_env)
        result["compilation"] = compiled
        if compiled["status"] == "ERROR":
            raise StopProbe("ERROR", "HARNESS_COMMAND_CLEANUP", "Compiler-process cleanup could not be confirmed",
                            diagnostic=diagnostics, cleanup=compiled.get("cleanup"))
        if compiled["status"] != "PASS":
            markers = ["UnsupportedClassVersionError", "Could not find or load main class", "OutOfMemoryError",
                       "Permission denied", "No space left on device"]
            if compiled["status"] in {"BLOCKED", "TIMEOUT"} or any(x in diagnostics for x in markers):
                blocked("ENVIRONMENT", "Compilation could not complete", diagnostic=diagnostics,
                        command_status=compiled["status"])
            failed("COMPILATION_REQUIRES_REVIEW", "Compiler returned nonzero; source/wrapper/toolchain attribution requires review",
                   diagnostic=diagnostics, returncode=compiled.get("returncode"))
        if not jar.is_file():
            raise RuntimeError("Compiler reported success without producing the requested JAR")
        result["jar"] = describe(jar)
        # Binding only: never connect to a service to test whether the port is free.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reservation:
            try:
                reservation.bind(("0.0.0.0", port))
            except OSError as exc:
                blocked("ENVIRONMENT", "Published test port is unavailable; no service contacted or stopped",
                        port=port, errno=exc.errno, error=str(exc))
        result["port_preflight"] = {"status": "PASS", "method": "IPv4 wildcard bind without listen/connect"}
        out_stream, err_stream = stdout_path.open("wb"), stderr_path.open("wb")
        argv = [str(java), "-Djava.net.preferIPv4Stack=true", "-jar", str(jar)]
        process = subprocess.Popen(argv, stdout=out_stream, stderr=err_stream, start_new_session=True)
        result["runtime_command"] = {"argv": argv, "started_at_utc": utc(), "pid": process.pid,
                                     "target": "Kotlin/JVM; not Kotlin/Native"}
        deadline = time.monotonic() + TIMEOUTS["startup"]
        while True:
            if process.poll() is not None:
                runtime_exit_record(process, stderr_path)
            observation = listener_ownership(process, port)
            if observation["foreign_listener"]:
                blocked("ENVIRONMENT", "Another listener appeared after preflight; no connection attempted", ownership=observation)
            if observation["owned_listener"]:
                result["ownership_observations"].append(observation)
                break
            if observation["listeners"]:
                blocked("ENVIRONMENT", "Another listener appeared after preflight; no connection attempted", ownership=observation)
            if time.monotonic() >= deadline:
                blocked("ENVIRONMENT_OR_STARTUP", "Owned JVM listener did not appear within the startup deadline")
            time.sleep(0.05)
        active_case = "empty_client"
        with connect_owned(process, port, stderr_path, result["ownership_observations"]) as connection:
            connection.shutdown(socket.SHUT_WR)
            receive_eof(connection)
        if process.poll() is not None:
            runtime_exit_record(process, stderr_path)
        result["cases"]["empty_client"] = {"status": "PASS", "sent_bytes": 0,
            "received_eof": True, "server_alive_after_client": True}
        active_case = "fragmented_echo"
        with connect_owned(process, port, stderr_path, result["ownership_observations"]) as connection:
            connection.sendall(PAYLOAD[:3])
            first = receive_exact(connection, 3)
            if first != PAYLOAD[:3]:
                failed("RUNTIME_CONTRACT", "First-fragment echo differs", actual_hex=first.hex())
            # The remaining writes occur only after the first echo was observed.
            connection.settimeout(TIMEOUTS["socket"])
            remainder = PAYLOAD[3:]
            write_sizes = [3]
            for start in range(0, len(remainder), 997):
                chunk = remainder[start:start + 997]
                connection.sendall(chunk)
                write_sizes.append(len(chunk))
            connection.shutdown(socket.SHUT_WR)
            echo = first + receive_exact(connection, len(remainder))
            receive_eof(connection)
        if echo != PAYLOAD:
            failed("RUNTIME_CONTRACT", "Echo stream differs from the binary payload",
                   expected_sha256=sha(PAYLOAD), actual_sha256=sha(echo))
        result["cases"]["fragmented_echo"] = {"status": "PASS", "sent_bytes": len(PAYLOAD),
            "received_bytes": len(echo), "payload_sha256": sha(PAYLOAD), "echo_sha256": sha(echo),
            "application_write_sizes": write_sizes, "first_three_echoed_before_rest_sent": True,
            "received_eof": True, "TCP_segment_or_read_boundaries_claimed": False}
        active_case = "following_client"
        with connect_owned(process, port, stderr_path, result["ownership_observations"]) as connection:
            connection.sendall(FOLLOWUP)
            connection.shutdown(socket.SHUT_WR)
            echo = receive_exact(connection, len(FOLLOWUP))
            receive_eof(connection)
        if echo != FOLLOWUP:
            failed("RUNTIME_CONTRACT", "Subsequent client received an incorrect echo")
        if process.poll() is not None:
            runtime_exit_record(process, stderr_path)
        result["cases"]["following_client"] = {"status": "PASS", "sent_bytes": len(FOLLOWUP),
            "echo_sha256": sha(echo), "received_eof": True, "server_alive_after_client": True}
        active_case = None
        result["status"] = "PASS"
    except StopProbe as exc:
        result.update(status=exc.record["status"], problem=exc.record)
    except (socket.timeout, TimeoutError) as exc:
        result.update(status="FAIL", problem={"status": "FAIL", "domain": "RUNTIME_DEADLINE",
            "error": repr(exc), "defect_attribution": "UNDETERMINED_REQUIRES_REVIEW"})
    except OSError as exc:
        status = "BLOCKED" if exc.errno in {errno.EPERM, errno.EACCES, errno.EADDRINUSE, errno.ENETUNREACH} else "FAIL"
        result.update(status=status, problem={"status": status, "domain": "ENVIRONMENT_OR_IO",
            "error": repr(exc), "defect_attribution": "UNDETERMINED_REQUIRES_REVIEW"})
    except Exception as exc:
        result.update(status="ERROR", problem={"status": "ERROR", "domain": "HARNESS",
            "error": repr(exc), "traceback": traceback.format_exc(), "source_defect_inferred": False})
    finally:
        if active_case is not None and result["cases"][active_case]["status"] != "PASS":
            result["cases"][active_case] = {"status": result["status"], "case_entered": True,
                "problem": result.get("problem", {"domain": "HARNESS_INTERRUPTED"})}
        if process is not None:
            result["cleanup"] = {**stop_owned(process), "process_started": True,
                "reason": "Intentional cleanup of this invocation's bounded teaching-server process"}
            if result["cleanup"]["status"] == "ERROR":
                result["status"] = "ERROR"
        for stream in [out_stream, err_stream]:
            if stream is not None:
                stream.close()
        for label, path in [("stdout", stdout_path), ("stderr", stderr_path)]:
            if path.exists():
                result["runtime_" + label] = describe(path)
        result["finished_at_utc"] = utc()
        (directory / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    raise_if_interrupted(result)
    return result


def aggregate(statuses):
    for value in ["ERROR", "FAIL", "BLOCKED", "NOT_RUN"]:
        if value in statuses:
            return value
    return "PASS"


def update_matrix(report):
    """Retain reached criteria even when interruption prevents a later variant."""
    by_name = {v["name"]: v for v in report["variants"]}
    compilation_statuses = []
    command_statuses = []
    for name in ["exact_8080", "derived_50081"]:
        variant = by_name.get(name)
        command_status = variant.get("compilation", {}).get("status", "NOT_RUN") if variant else "NOT_RUN"
        command_statuses.append(command_status)
        compilation_statuses.append("PASS" if command_status == "PASS" else variant["status"] if variant else "NOT_RUN")
    report["checks"]["K02"] = {"status": aggregate(compilation_statuses),
        "meaning": "Both Kotlin/JVM wrappers compile", "compiler_command_statuses": command_statuses}
    exact = by_name.get("exact_8080")
    if exact is not None:
        for key, case in [("K03", "empty_client"), ("K04", "fragmented_echo"), ("K05", "following_client")]:
            report["checks"][key] = {**exact["cases"][case], "variant": "exact_8080"}
    derived = by_name.get("derived_50081")
    if derived is not None:
        report["checks"]["K06"] = {"status": derived["status"], "meaning": "Derived high TCP socket port, not unsigned parsing"}
    if report["variants"]:
        report["checks"]["K07"] = {"status": aggregate([v["cleanup"]["status"] for v in report["variants"]]),
            "meaning": "Direct children reaped and no active owned-group members remain",
            "details": [v["cleanup"] for v in report["variants"]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--protocol-dir", required=True, type=Path)
    parser.add_argument("--kotlinc", required=True)
    parser.add_argument("--java", required=True)
    args = parser.parse_args()
    def interrupted(signum, frame):
        global _INTERRUPTION
        if _INTERRUPTION is None:
            _INTERRUPTION = {"signal": signum, "requested_at_utc": utc()}
        if _CLEANUP_DEPTH == 0:
            raise_if_interrupted()
    for signum in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(signum, interrupted)
    source_root, output = args.source_root.resolve(), args.output_dir.resolve()
    report = {"schema_version": 1, "started_at_utc": utc(), "status": "NOT_RUN",
        "expected_candidate_commit": COMMIT, "expected_candidate_tree": TREE,
        "expected_source_sha256": SOURCE_SHA256, "repository": "antonioclim/COMPNET-EN",
        "timeouts_seconds": TIMEOUTS, "python": sys.version, "platform": platform.platform(),
        "scope": "Kotlin/JVM Rosetta TCP echo component; IPv4 loopback only",
        "Kotlin_Native_tested": False, "Kotlin_binary_parser_exists_in_source": False,
        "source_repository_modified": False, "OVA_accessed": False,
        "VM_Docker_Mininet_Windows_browser_workbook_LMS_acceptance": "NOT_RUN",
        "checks": {"K" + str(i).zfill(2): {"status": "NOT_RUN"} for i in range(1, 8)},
        "variants": []}
    writable = False
    try:
        if output == source_root or source_root in output.parents:
            blocked("HARNESS_INPUT", "Output must be outside the source checkout")
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            blocked("HARNESS_INPUT", "Refusing to overwrite a nonempty output directory; JSON is emitted on stdout")
        output.mkdir(parents=True, exist_ok=True)
        writable = True
        verify_protocol(report, args.protocol_dir)
        for name in ["PROTOCOL_N08.md", "PROTOCOL_FREEZE.json"]:
            shutil.copy2(args.protocol_dir.resolve() / name, output / name)
        shutil.copy2(Path(__file__).resolve(), output / Path(__file__).name)
        if sys.platform != "linux" or not Path("/proc/net/tcp").is_file():
            blocked("ENVIRONMENT", "This frozen protocol requires Linux procfs for safe listener ownership")
        body = extract_source(source_root, output, report)
        kotlinc, java = resolve_tool(args.kotlinc), resolve_tool(args.java)
        env = os.environ.copy()
        env["JAVACMD"] = str(java)
        # This is the compiler's documented Java selection, not an unrelated HOME override.
        env["JAVA_HOME"] = str(java.parent.parent)
        report["tools"] = {"kotlinc_launcher": describe(kotlinc), "java_executable": describe(java),
                           "compiler_environment_overrides": {k: env[k] for k in ["JAVACMD", "JAVA_HOME"]}}
        for label, argv in [("java_version", [java, "-version"]), ("kotlinc_version", [kotlinc, "-version"])]:
            item, text = command(argv, output, label, TIMEOUTS["metadata"], env=env)
            report["tools"][label] = {"command": item, "text": text}
            require_command(item, text, label)
        version = re.search(r"kotlinc-jvm\s+(\S+)", report["tools"]["kotlinc_version"]["text"])
        if version is None or version.group(1) != EXPECTED_KOTLIN:
            blocked("PROVENANCE", "Compiler version differs from the frozen Kotlin/JVM version")
        compiler_jar = kotlinc.parent.parent / "lib" / "kotlin-compiler.jar"
        if compiler_jar.is_file():
            report["tools"]["compiler_jar"] = describe(compiler_jar)
        variants = [("exact_8080", 8080, body),
                    ("derived_50081", 50081, body.replace(b"ServerSocket(8080)", b"ServerSocket(50081)", 1))]
        for name, port, variant_body in variants:
            raise_if_interrupted()
            run_variant(name, port, variant_body, body, output, kotlinc, java, env, report["variants"])
        report["status"] = aggregate([v["status"] for v in report["variants"]])
    except StopProbe as exc:
        if (getattr(exc, "partial_variant", None) is not None
                and not any(v is exc.partial_variant for v in report["variants"])):
            report["variants"].append(exc.partial_variant)
        report.update(status=exc.record["status"], problem=exc.record)
    except Exception as exc:
        report.update(status="ERROR", problem={"status": "ERROR", "domain": "HARNESS_OR_INPUT",
            "error": repr(exc), "traceback": traceback.format_exc(), "source_defect_inferred": False})
    finally:
        update_matrix(report)
        report["finished_at_utc"] = utc()
        report["verdict"] = "PASS_KOTLIN_JVM_FRAGMENT_SCOPE_ONLY" if report["status"] == "PASS" else "N08_NOT_CLOSED"
        report["native_release_gates_all_passed"] = False
        report["F6_full_acceptance_completed"] = False
        report["check_counts"] = {status: sum(x["status"] == status for x in report["checks"].values())
                                  for status in ["PASS", "FAIL", "BLOCKED", "ERROR", "NOT_RUN"]}
        report_path = output / "N08_KOTLIN_RESULTS.json"
        report["report_path"] = str(report_path) if writable else None
        text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if writable:
            try:
                report_path.write_text(text)
            except OSError as exc:
                report["status"] = "ERROR"
                report["verdict"] = "N08_NOT_CLOSED"
                report["report_path"] = None
                report["report_write_error"] = repr(exc)
                text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        print(text, end="")
    return {"PASS": 0, "FAIL": 1, "BLOCKED": 2, "ERROR": 3, "NOT_RUN": 4}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
