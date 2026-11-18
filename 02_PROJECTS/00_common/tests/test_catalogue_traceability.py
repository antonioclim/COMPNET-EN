"""Keep the 30 project briefs, rule tables and assessment workbook aligned."""
import json
from pathlib import Path
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile

PROJECTS = Path(__file__).resolve().parents[2]
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def briefs():
    return {p.name[:3]: p for p in PROJECTS.glob("0[12]_*/*.md") if re.fullmatch(r"[AS]\d{2}", p.name[:3])}


def bullets(text, heading):
    level = len(heading.split()[0])
    match = re.search(r"^" + re.escape(heading) + r"\s*\n(.*?)(?=^#{1," + str(level) + r"} |\Z)", text, re.M | re.S)
    assert match, heading
    result = []
    for line in match.group(1).splitlines():
        if line.startswith("- "):
            result.append(line[2:])
        elif line.strip() and result and not line.startswith("#"):
            result[-1] += " " + line.strip()
    return result


def test_brief_capture_tables_match_machine_readable_rules():
    for code, path in briefs().items():
        manifest = json.loads((PROJECTS / f"00_common/tools/pcap_rules/{code}.json").read_text())
        text = path.read_text()
        for rule in manifest["rules"]:
            filt = rule["filter"].replace("|", r"\|")
            description = rule["description"]
            if rule.get("measurement") not in (None, "frames"):
                description += f" Measurement: `{rule['measurement']}`."
            expected = f"| {rule['id']} | `{filt}` | `{rule['condition']}` | {description} |"
            assert expected in text, (code, rule["id"])
        assert manifest.get("manual_checks"), code


def test_workbook_matches_all_canonical_must_and_nonfunctional_requirements():
    with zipfile.ZipFile(PROJECTS / "RC2026_VERIFICATION_INDEX.xlsx") as archive:
        strings = ["".join(item.itertext()) for item in ET.fromstring(archive.read("xl/sharedStrings.xml"))] if "xl/sharedStrings.xml" in archive.namelist() else []
        rels = {item.attrib["Id"]: item.attrib["Target"] for item in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))}
        sheets = {}
        for item in ET.fromstring(archive.read("xl/workbook.xml")).find("m:sheets", NS):
            target = rels[item.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
            sheets[item.attrib["name"]] = ET.fromstring(archive.read(target))
        assert set(sheets) == set(briefs()) | {"RULES", "INDEX"}
        for code, path in briefs().items():
            text = path.read_text()
            expected = {f"M{i:02}": value for i, value in enumerate(bullets(text, "### MUST (mandatory)"), 1)}
            expected.update({f"NF{i:02}": value for i, value in enumerate(bullets(text, "## Non-functional requirements"), 1)})
            cells = {}
            for cell in sheets[code].findall(".//m:sheetData/m:row/m:c", NS):
                value = cell.findtext("m:v", None, NS)
                if cell.attrib.get("t") == "s":
                    value = strings[int(value)]
                elif cell.attrib.get("t") == "inlineStr":
                    node = cell.find("m:is", NS)
                    value = "".join(node.itertext()) if node is not None else None
                cells[cell.attrib["r"]] = value
            actual = {value: cells.get("C" + address[1:]) for address, value in cells.items() if address.startswith("B") and re.fullmatch(r"(?:M|NF)\d+", value or "")}
            assert actual == expected, code
            validations = sheets[code].findall(".//m:dataValidation", NS)
            assert validations and all(v.findtext("m:formula1", None, NS) == '"OK,NO,N/A"' for v in validations), code
