"""Regression tests for capture measurement, independent of a native tshark install.

Run: python -m pytest 02_PROJECTS/00_common/tests
Native dissector/capture acceptance is a separate lab gate.
"""
import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
SPEC = importlib.util.spec_from_file_location("project_validate_pcap", TOOLS / "validate_pcap.py")
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def manifest(**overrides):
    rule = {"id": "R1", "filter": "tcp", "condition": ">= 1", "description": "TCP frames"}
    rule.update(overrides)
    return {"project": "S00", "rules": [rule]}


def fields(parts, stream="0"):
    return [[stream, str(seq), payload.hex()] for seq, payload in parts]


@pytest.mark.parametrize("parts", [
    [(1, b"BID item 10\nBID item 20\r\n")],
    [(1, b"B"), (2, b"ID item 10\nBI"), (15, b"D item 20\r\n")],
    [(14, b"ID item 20\r\n"), (1, b"BID item 10\nB")],
    [(1, b"BID item 10\n"), (1, b"BID item 10\n"), (13, b"BID item 20\r\n")],
])
def test_logical_bid_count_is_independent_of_segment_boundaries(parts):
    assert validator.count_tcp_commands(fields(parts), ["BID"]) == 2


def test_substrings_responses_and_control_characters_are_not_commands():
    payload = b"UNSUBSCRIBE x\nTOP_BID x 20\nERROR BID was rejected\nTEXT x\vBID x 30\nSUBSCRIBE x\n"
    assert validator.count_tcp_commands(fields([(1, payload)]), ["SUBSCRIBE"]) == 1
    assert validator.count_tcp_commands(fields([(1, payload)]), ["BID"]) == 0


def test_identical_overlaps_are_deduplicated():
    assert validator.reassemble_segments([(1, b"BID x "), (5, b"x 10\n"), (1, b"BID x ")]) == b"BID x 10\n"


@pytest.mark.parametrize("parts", [[(2, b"BID x\n")], [(1, b"BI"), (4, b"D x\n")], [(1, b"BID x\n"), (1, b"BID y\n")]])
def test_missing_or_conflicting_tcp_bytes_are_rejected(parts):
    with pytest.raises(ValueError):
        validator.count_tcp_commands(fields(parts), ["BID"])


def test_incomplete_last_command_is_rejected():
    with pytest.raises(ValueError, match="Incomplete"):
        validator.count_tcp_commands(fields([(1, b"BID x")]), ["BID"])


def test_http_messages_in_one_stream_not_frames(monkeypatch):
    rule = manifest(measurement="field_occurrences", field="http.request.method", value="GET", aggregation="max_per_stream", condition=">= 2")
    for rows in ([["0", "GET,GET"]], [["0", "GET"], ["0", "GET"]]):
        monkeypatch.setattr(validator, "_tshark_fields", lambda *args: rows)
        result = validator.validate(Path("synthetic.pcap"), rule)[0]
        assert result.passed and result.observed == 2
    monkeypatch.setattr(validator, "_tshark_fields", lambda *args: [["0", "GET"], ["1", "GET"]])
    assert not validator.validate(Path("synthetic.pcap"), rule)[0].passed


def test_distinct_port_count_does_not_count_retransmissions(monkeypatch):
    monkeypatch.setattr(validator, "_tshark_fields", lambda *args: [["0", "80"], ["0", "80"], ["1", "443"]])
    result = validator.validate(Path("synthetic.pcap"), manifest(measurement="distinct_values", field="tcp.dstport", condition=">= 3"))[0]
    assert result.observed == 2 and not result.passed


@pytest.mark.parametrize("mutator", [
    lambda d: d.update(rules=[]),
    lambda d: d["rules"].append(copy.deepcopy(d["rules"][0])),
    lambda d: d["rules"][0].update(filter=3),
    lambda d: d["rules"][0].update(condition="approximately one"),
    lambda d: d.update(manual_checks="not a list"),
    lambda d: d["rules"][0].update(measurement="tcp_commands", commands=[]),
])
def test_invalid_manifest_cannot_certify_capture(mutator):
    data = manifest()
    mutator(data)
    with pytest.raises(ValueError):
        validator.validate_manifest(data)


def test_all_canonical_manifests_validate_and_preserve_direction():
    paths = sorted((TOOLS / "pcap_rules").glob("*.json"))
    assert len(paths) == 30
    for path in paths:
        data = json.loads(path.read_text())
        validator.validate_manifest(data, path.stem)
        for rule in data["rules"]:
            if rule.get("measurement") == "tcp_commands":
                assert "tcp.dstport==" in rule["filter"] or "tcp.srcport==" in rule["filter"]
    with pytest.raises(ValueError, match="do not agree"):
        validator.validate_manifest(manifest(), "S01")


@pytest.mark.parametrize("mode,expected", [("empty", 2), ("pass", 0), ("criterion", 1), ("tool", 2)])
def test_cli_exit_codes(tmp_path, monkeypatch, mode, expected):
    pcap = tmp_path / "capture.pcap"
    pcap.write_bytes(b"synthetic test input; tshark is replaced in this unit test")
    rules = manifest()
    if mode == "empty":
        rules["rules"] = []
    (tmp_path / "S00.json").write_text(json.dumps(rules))
    calls = []
    def count(*args):
        calls.append(args)
        if mode == "tool":
            raise RuntimeError("synthetic tshark failure")
        return 0 if mode == "criterion" else 1
    monkeypatch.setattr(validator, "_run_tshark_count", count)
    monkeypatch.setattr(sys, "argv", ["validate_pcap.py", "--project", "S00", "--rules-dir", str(tmp_path), "--pcap", str(pcap)])
    assert validator.main() == expected
    assert bool(calls) == (mode != "empty")
