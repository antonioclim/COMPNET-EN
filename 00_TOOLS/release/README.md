# Release tooling

This folder contains small utilities for producing a distributable ZIP archive.

The release script:

* runs the repository QA checks
* applies executable permission bits based on `00_TOOLS/qa/executable_manifest.txt`
* packages a ZIP while excluding development artefacts

## Create a ZIP archive

From the repository root:

```bash
bash 00_TOOLS/release/create_release_zip.sh
```

To choose an explicit output name:

```bash
bash 00_TOOLS/release/create_release_zip.sh compnet-course-kit.zip
```
