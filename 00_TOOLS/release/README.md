# Course kit release packaging

This maintainer helper creates a ZIP from a **committed full Git checkout**.
It uses the same `00_TOOLS/qa/run_checks.py` entry point as CI. It neither
changes executable modes nor silently skips missing test dependencies.

## Prepare and check

Run these commands from the repository root, in a Python environment used for QA:

```bash
python3 -m pip install -r 00_TOOLS/qa/requirements.txt
python3 00_TOOLS/qa/run_checks.py
```

The shared gates check Python syntax, executable permissions, relative Markdown
file targets, lexical integrity, lecture figure sources and pytest regressions.
The historical root `CHANGELOG.md` is explicitly excluded from the language
heuristic in both routes. This does not exclude it from the release archive.
The conservative `format-offline.js` helper is optional and is not a CI gate.

## Build the archive

Commit the reviewed changes first, then run:

```bash
bash 00_TOOLS/release/create_release_zip.sh ../COMPNET-EN-v1.5.0.zip
```

The output must not already exist. The helper refuses tracked working-tree or
index changes, runs the shared gates, archives `HEAD` with Git's recorded modes
and checks the ZIP CRC before creating the final file. Untracked files and ignored
results are not packaged. The default filename uses the current short commit ID.
Set `COMP_NET_PYTHON` to the required interpreter if `python3` is not suitable.

A sparse checkout or a downloaded source ZIP is not the supported maintainer
input. Use a full clone for QA and packaging. Students may use the GitHub release
source archive directly; GitHub's automatic source archives are produced by GitHub,
not by this helper.

## Scope of a successful result

Passing these gates verifies source and component properties. Docker start-up,
Mininet/OpenFlow behaviour, Windows/VirtualBox, LMS import and browser/Excel use
require their own acceptance evidence. The OVA is a separately versioned Zenodo
asset and is never included or re-exported here.

See [QA tools](../qa/) and the [main repository guide](../../README.md).
