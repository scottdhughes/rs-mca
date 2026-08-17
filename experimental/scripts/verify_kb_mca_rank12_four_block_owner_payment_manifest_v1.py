#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/kb-mca-rank12-four-block-owner-payment-v1"
MANIFEST = CERT / "manifest.json"


def main() -> None:
    data = json.loads(MANIFEST.read_text())
    result = json.loads((ROOT / data["result"]).read_text())
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    payload = hashlib.sha256(canonical).hexdigest()
    if payload != data["canonical_payload_sha256"]:
        raise AssertionError("canonical payload")
    if (CERT / "payload.txt").read_text().strip() != payload:
        raise AssertionError("payload note")
    for rel, expected in data["files"].items():
        path = ROOT / rel
        if not path.exists():
            raise AssertionError(f"missing {rel}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"hash {rel}")
    expected_claims = {
        "proper_rank2_drop_impossible_for_K_ge_662480": True,
        "whole_rank2_family_shortens_to_K_at_most_662479": True,
        "affine_error_rank_12_paid": False,
        "active_v4_ledger_movement": 0,
        "koalabear_closed": False,
    }
    if data["claims"] != expected_claims or result["claims"] != expected_claims:
        raise AssertionError("claims")
    print(
        "KB_MCA_RANK12_FOUR_BLOCK_MANIFEST_PASS "
        f"files={len(data['files'])} payload={payload}"
    )


if __name__ == "__main__":
    main()
