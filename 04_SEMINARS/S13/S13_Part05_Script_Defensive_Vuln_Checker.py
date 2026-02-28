"""
S13 — Defensive vulnerability checker (lab helper)

Important safety note
---------------------
This script is designed for *defensive identification* only:

- banner collection
- simple HTTP GET to read the landing page
- no exploitation attempts

It is intended for the seminar Docker lab in S13 (DVWA, WebGoat, vsftpd).

Why this exists (pedagogy)
--------------------------
Tools like Nmap/Nikto are powerful, but students often need a smaller artefact
that shows *exactly* what “detection” means:

- what is being checked
- why the check indicates a specific vulnerable service
- what a safe next step would be (in a controlled lab)

Examples (host execution)
-------------------------
DVWA (published on host port 8888 by default; can be overridden via `.env`):
  python3 S13_Part05_Script_Defensive_Vuln_Checker.py --service dvwa --target 127.0.0.1

WebGoat (published on host port 8080 by default; can be overridden via `.env`):
  python3 S13_Part05_Script_Defensive_Vuln_Checker.py --service webgoat --target 127.0.0.1

vsftpd 2.3.4 (published on host port 2121 by default; can be overridden via `.env`):
  python3 S13_Part05_Script_Defensive_Vuln_Checker.py --service vsftpd --target 127.0.0.1

Outputs
-------
- Human-readable summary is printed to stdout.
- JSON report is written to `04_SEMINARS/S13/artifacts/` by default.

This script uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os

from s13_env import load_local_env
import socket
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


_ENV = load_local_env()

def _env_int(key: str, default: int) -> int:
    raw = os.getenv(key) or _ENV.get(key)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default

DVWA_PORT = _env_int("DVWA_HOST_PORT", 8888)
WEBGOAT_PORT = _env_int("WEBGOAT_HOST_PORT", 8080)
VSFTPD_PORT = _env_int("VSFTPD_HOST_PORT", 2121)
VSFTPD_BACKDOOR_PORT = _env_int("VSFTPD_BACKDOOR_HOST_PORT", 6200)

DEFAULTS = {
    "dvwa": {"port": DVWA_PORT, "scheme": "http"},
    "webgoat": {"port": WEBGOAT_PORT, "scheme": "http"},
    "vsftpd": {"port": VSFTPD_PORT, "scheme": "tcp"},
}

@dataclass
class Finding:
    kind: str
    evidence: str
    severity: str  # "info" | "low" | "medium" | "high"
    recommendation: str


@dataclass
class Report:
    service: str
    target: str
    port: int
    timestamp_utc: str
    reachable: bool
    observations: Dict[str, object]
    findings: List[Finding]


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def tcp_connect(host: str, port: int, timeout: float) -> Tuple[bool, Optional[str]]:
    """
    Attempt a TCP connection and optionally read an initial banner.

    Returns:
      (reachable, banner_or_none)
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            try:
                banner = s.recv(4096)
                if banner:
                    return True, banner.decode("utf-8", errors="replace").strip()
            except Exception:
                pass
            return True, None
    except Exception as exc:
        return False, str(exc)


def http_probe(url: str, timeout: float) -> Tuple[bool, Dict[str, str], str, Optional[str]]:
    """
    Perform a conservative HTTP GET (no auth, no forms).
    Returns:
      (ok, headers, sample_body, error)
    """
    try:
        req = Request(url, headers={"User-Agent": "COMPNET-EN DefensiveChecker/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            body = resp.read(20000)  # sample only
            sample = body.decode("utf-8", errors="replace")
            return True, headers, sample, None
    except HTTPError as e:
        return False, {}, "", f"HTTPError: {e.code} {e.reason}"
    except URLError as e:
        return False, {}, "", f"URLError: {e.reason}"
    except Exception as e:
        return False, {}, "", f"Error: {e}"


def detect_dvwa(sample: str, headers: Dict[str, str]) -> Optional[Finding]:
    text = sample.lower()
    if "damn vulnerable web application" in text or "dvwa" in text:
        return Finding(
            kind="DVWA detected",
            evidence="Landing page contains 'Damn Vulnerable Web Application' / 'DVWA'.",
            severity="high",
            recommendation="This is intentionally vulnerable (lab). Treat it as hostile in real deployments.",
        )
    # Some DVWA containers show a distinctive PHPSESSID + security cookie.
    if "php" in headers.get("server", "").lower() and "dvwa" in text:
        return Finding(
            kind="Possible DVWA",
            evidence="Server/header pattern and page content suggest DVWA.",
            severity="medium",
            recommendation="Confirm by navigating to the login page and checking the application banner.",
        )
    return None


def detect_webgoat(sample: str, headers: Dict[str, str]) -> Optional[Finding]:
    text = sample.lower()
    if "webgoat" in text:
        return Finding(
            kind="WebGoat detected",
            evidence="Landing page contains 'WebGoat'.",
            severity="high",
            recommendation="This is intentionally vulnerable (lab). Use only in an isolated environment.",
        )
    # Heuristic: many WebGoat deployments run on Spring Boot with common headers.
    server = headers.get("server", "").lower()
    if "jetty" in server or "tomcat" in server:
        if "webgoat" in headers.get("set-cookie", "").lower():
            return Finding(
                kind="Possible WebGoat",
                evidence="Header patterns suggest a Java web app; cookie hints at WebGoat.",
                severity="medium",
                recommendation="Confirm by opening the service URL and identifying the application.",
            )
    return None


def detect_vsftpd(host: str, banner: Optional[str], reachable: bool) -> List[Finding]:
    findings: List[Finding] = []
    if not reachable:
        return findings

    if banner:
        if "vsftpd 2.3.4" in banner.lower():
            findings.append(
                Finding(
                    kind="vsftpd 2.3.4 banner",
                    evidence=f"FTP banner: {banner!r}",
                    severity="high",
                    recommendation="This version is intentionally vulnerable in many training labs. Do not deploy.",
                )
            )
        else:
            findings.append(
                Finding(
                    kind="FTP banner",
                    evidence=f"FTP banner: {banner!r}",
                    severity="info",
                    recommendation="Banner identified. Validate versioning and patch status in real systems.",
                )
            )
    else:
        findings.append(
            Finding(
                kind="FTP reachable (no banner captured)",
                evidence="TCP connect succeeded but no banner was captured within timeout.",
                severity="info",
                recommendation="Re-run with higher timeout or use a dedicated FTP client for a full banner.",
            )
        )

    # Non-invasive check: is the classic backdoor port open? (presence only)
    # In lab scenarios it may be used to illustrate why banner-based risk is meaningful.
    backdoor_open, _ = tcp_connect(host, VSFTPD_BACKDOOR_PORT, timeout=0.3)
    if backdoor_open:
        findings.append(
            Finding(
                kind=f"Port {VSFTPD_BACKDOOR_PORT} reachable (lab observation)",
                evidence=f"TCP connect to port {VSFTPD_BACKDOOR_PORT} succeeded.",
                severity="medium",
                recommendation="Treat as lab-only evidence. Do not attempt to exploit; isolate and patch.",
            )
        )
    return findings


def write_json_report(report: Report, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(report)
    payload["findings"] = [asdict(f) for f in report.findings]
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="S13 defensive vuln checker (lab)")
    ap.add_argument("--service", choices=["dvwa", "webgoat", "vsftpd"], required=True)
    ap.add_argument("--target", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=None, help="Override the default service port")
    ap.add_argument("--timeout", type=float, default=2.0)
    ap.add_argument("--json-out", default=None, help="Write JSON report to this path (optional)")
    args = ap.parse_args()

    service = args.service
    port = args.port if args.port is not None else int(DEFAULTS[service]["port"])
    target = args.target

    findings: List[Finding] = []
    observations: Dict[str, object] = {}

    # Reachability test
    reachable, banner_or_err = tcp_connect(target, port, timeout=args.timeout)
    observations["tcp_connect"] = {"reachable": reachable, "banner_or_error": banner_or_err}

    if service in {"dvwa", "webgoat"}:
        scheme = "http"
        url = f"{scheme}://{target}:{port}/"
        ok, headers, body_sample, err = http_probe(url, timeout=args.timeout)
        observations["http_probe"] = {
            "url": url,
            "ok": ok,
            "error": err,
            "headers_sample": {k: headers[k] for k in sorted(headers) if k in {"server", "content-type", "set-cookie", "location"}},
            "body_sample_first_400": body_sample[:400],
        }

        if not reachable:
            findings.append(
                Finding(
                    kind="Service unreachable",
                    evidence=f"TCP connect failed: {banner_or_err}",
                    severity="high",
                    recommendation="Start the Docker lab (S13) and verify the published port mapping.",
                )
            )
        elif not ok:
            findings.append(
                Finding(
                    kind="HTTP probe failed",
                    evidence=str(err),
                    severity="medium",
                    recommendation="Check container logs and confirm the correct URL/port.",
                )
            )
        else:
            if service == "dvwa":
                f = detect_dvwa(body_sample, headers)
                if f:
                    findings.append(f)
            if service == "webgoat":
                f = detect_webgoat(body_sample, headers)
                if f:
                    findings.append(f)

            if not findings:
                findings.append(
                    Finding(
                        kind="Service reachable (no strong signature)",
                        evidence="HTTP responded but the page did not match the expected lab fingerprint.",
                        severity="info",
                        recommendation="Verify you are targeting the intended container/port.",
                    )
                )

    else:  # vsftpd
        if not reachable:
            findings.append(
                Finding(
                    kind="Service unreachable",
                    evidence=f"TCP connect failed: {banner_or_err}",
                    severity="high",
                    recommendation="Start the Docker lab and verify port 2121 is published.",
                )
            )
        else:
            findings.extend(detect_vsftpd(target, banner_or_err if reachable else None, reachable))

    report = Report(
        service=service,
        target=target,
        port=port,
        timestamp_utc=now_utc_iso(),
        reachable=reachable,
        observations=observations,
        findings=findings,
    )

    # Human-readable output
    print("=" * 72)
    print(f"S13 Defensive vuln checker — {service}")
    print("=" * 72)
    print(f"Target:     {target}")
    print(f"Port:       {port}")
    print(f"Reachable:  {reachable}")
    if reachable and service == "vsftpd":
        if banner_or_err:
            print(f"Banner:     {banner_or_err}")
    print("-" * 72)
    if findings:
        for i, f in enumerate(findings, start=1):
            print(f"[{i}] {f.kind} (severity={f.severity})")
            print(f"    Evidence: {f.evidence}")
            print(f"    Next:     {f.recommendation}")
            print("")
    else:
        print("No findings.")
    print("=" * 72)

    # JSON output path
    if args.json_out:
        out = Path(args.json_out)
    else:
        out = Path(__file__).resolve().parent / "artifacts" / f"vulncheck_{service}_{target.replace(':','_')}_{port}.json"

    write_json_report(report, out)
    print(f"[OK] JSON report written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
