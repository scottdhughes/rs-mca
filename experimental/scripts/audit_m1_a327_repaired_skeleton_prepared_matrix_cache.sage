#!/usr/bin/env sage
"""Sage-side cache manifest audit for the repaired M1 a=327 skeleton."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SCAN_PATH = Path("experimental/scripts/scan_m1_a327_repaired_skeleton_prepared_matrix_cache.py")
DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_prepared_matrix_cache.json")


def load_python_module(path, module_name):
    script_dir = str(path.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def audit_record():
    scan = load_python_module(SCAN_PATH, "prepared_matrix_cache_scan")
    return scan.build_record()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()
    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_REPAIRED_SKELETON_PREPARED_MATRIX_CACHE_OK")
        print("cache_type: %s" % record["prepared_state"]["cache_type"])
        print("replay_status: %s" % record["cache_replay"]["replay_status"])
        print("small_append_test_timeout: %s" % record["cache_replay"]["small_append_test_timeout"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
