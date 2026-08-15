#!/usr/bin/env python3
"""Verify hashes and payload for the factor-synchronization certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    manifest_path = root / "experimental/data/certificates/kb-mca-rank11-factor-synchronization-v1/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for entry in manifest["files"]:
        path = root / entry["path"]
        data = path.read_bytes()
        assert len(data) == entry["bytes"], entry["path"]
        assert sha256(data) == entry["sha256"], entry["path"]

    result_path = root / "experimental/data/certificates/kb-mca-rank11-factor-synchronization-v1/result.json"
    assert sha256(result_path.read_bytes()) == manifest["result_sha256"]

    payload = {
        "parent": manifest["parent"],
        "result_sha256": manifest["result_sha256"],
        "files": manifest["files"],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    assert sha256(canonical) == manifest["canonical_payload_sha256"]
    print(
        "KB_MCA_RANK11_FACTOR_SYNC_MANIFEST_PASS "
        f"files={len(manifest['files'])} payload={manifest['canonical_payload_sha256']}"
    )


if __name__ == "__main__":
    main()
