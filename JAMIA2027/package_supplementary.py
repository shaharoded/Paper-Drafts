"""Package current tracked repository files; leave source repositories untouched."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "jamia" / "supplementary-data" / "supplementary-code.zip"
manifest = {"repositories": {}, "files": {}}
payload = {}
for name in ("Mediator", "kineret-etl-repo"):
    source = ROOT.parent.parent / name
    files = subprocess.check_output(["git", "-C", str(source), "ls-files", "-z"]).decode().split("\0")
    revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    status = subprocess.check_output(["git", "-C", str(source), "status", "--porcelain"], text=True)
    manifest["repositories"][name] = {"revision": revision, "working_tree_clean": not bool(status.strip())}
    for relative in sorted(filter(None, files)):
        path = source / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Missing or unsupported tracked file: {path}")
        raw = path.read_bytes()
        packed = raw
        if path.suffix == ".ipynb":
            notebook = json.loads(raw)
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    cell["outputs"] = []
                    cell["execution_count"] = None
            notebook.get("metadata", {}).pop("widgets", None)
            packed = (json.dumps(notebook, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
        archive_name = name + "/" + relative
        payload[archive_name] = packed
        manifest["files"][archive_name] = {
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "archive_sha256": hashlib.sha256(packed).hexdigest(),
            "notebook_outputs_cleared": path.suffix == ".ipynb",
        }
payload["MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
payload["README.txt"] = b"""Supplementary code and curated concept indices

Mediator/: abstraction engine, knowledge base, analysis code, tests and setup.
kineret-etl-repo/: extraction/cohort notebooks and original curated index files.

Copies include all current Git-tracked files in both local repositories.
Git history, ignored local data/databases, environments, caches and logs are
excluded. Notebook outputs and execution counts are cleared in archive copies;
notebook source code is retained. Source repositories are not modified.
MANIFEST.json records source revisions and source/archive SHA-256 hashes.
No conversion of concept indices to CSV was performed.
Consult each project's README and license for setup and reuse. Repository
snapshots do not include the restricted patient-level data needed for analysis.
"""
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name, raw in sorted(payload.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, raw)
with zipfile.ZipFile(OUTPUT) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(payload)
    for name, expected in payload.items():
        assert archive.read(name) == expected, name
print(f"Validated {len(manifest['files'])} repository files; {OUTPUT.stat().st_size:,} bytes; {OUTPUT}")
print("Retained locally for editorial requests; ZIP upload is currently omitted due to portal errors.")
