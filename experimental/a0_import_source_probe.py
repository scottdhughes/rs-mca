#!/usr/bin/env python3
"""Probe external sources needed for the A0 import audit.

Status: AUDIT.

This script records whether the exact public source URLs used by the A0 audit
are reachable from the current environment.  It does not prove or disprove any
theorem and does not upgrade the Crites--Stewart or ABF imports.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
CLAIM = (
    "source availability probe only; no theorem verification; "
    "no import status upgrade"
)


@dataclass(frozen=True)
class Source:
    key: str
    url: str
    role: str


SOURCES = (
    Source(
        "cs25_eprint_pdf",
        "https://eprint.iacr.org/2025/2046.pdf",
        "CS25 Theorem 2 primary ePrint PDF",
    ),
    Source(
        "abf26_eprint_pdf",
        "https://eprint.iacr.org/2026/680.pdf",
        "ABF26 Theorems 5.2 and 5.3 restatement PDF",
    ),
    Source(
        "bchks25_eprint_pdf",
        "https://eprint.iacr.org/2025/2055.pdf",
        "BCHKS25 Theorem 1.9 ePrint PDF",
    ),
    Source(
        "bchks25_eccc_pdf",
        "https://eccc.weizmann.ac.il/report/2025/169/download/",
        "BCHKS25 ECCC TR25-169 PDF mirror",
    ),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def current_repo_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def probe_url(source: Source, *, timeout: float) -> dict[str, Any]:
    curl = shutil.which("curl")
    if curl is None:
        return {
            "key": source.key,
            "url": source.url,
            "role": source.role,
            "reachable": False,
            "status_code": None,
            "content_type": None,
            "content_length": None,
            "server": None,
            "error": "curl not found on PATH",
        }

    try:
        result = subprocess.run(
            [
                curl,
                "-L",
                "-I",
                "-sS",
                "--max-time",
                str(max(1, int(timeout))),
                source.url,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return {
            "key": source.key,
            "url": source.url,
            "role": source.role,
            "reachable": False,
            "status_code": None,
            "content_type": None,
            "content_length": None,
            "server": None,
            "error": f"OSError: {exc}",
        }

    status_code: int | None = None
    headers: dict[str, str] = {}
    for block in result.stdout.replace("\r\n", "\n").split("\n\n"):
        lines = [line for line in block.splitlines() if line]
        if not lines or not lines[0].startswith("HTTP/"):
            continue
        parts = lines[0].split()
        if len(parts) >= 2 and parts[1].isdigit():
            status_code = int(parts[1])
        headers = {}
        for line in lines[1:]:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

    return {
        "key": source.key,
        "url": source.url,
        "role": source.role,
        "reachable": status_code is not None and 200 <= status_code < 400,
        "status_code": status_code,
        "content_type": headers.get("content-type"),
        "content_length": headers.get("content-length"),
        "server": headers.get("server"),
        "error": None if result.returncode == 0 else result.stderr.strip(),
    }


def build_report(timeout: float) -> dict[str, Any]:
    probes = [probe_url(source, timeout=timeout) for source in SOURCES]
    return {
        "schema_version": "a0-import-source-probe-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "provenance": {
            "created_at_utc": utc_now(),
            "generator": "experimental/a0_import_source_probe.py",
            "repo_commit": current_repo_commit(),
        },
        "tools": {
            "pdftotext": shutil.which("pdftotext"),
        },
        "summary": {
            "sources": len(probes),
            "reachable": sum(1 for probe in probes if probe["reachable"]),
            "blocked_or_unreachable": sum(1 for probe in probes if not probe["reachable"]),
        },
        "sources": probes,
    }


def print_text_report(report: dict[str, Any]) -> None:
    print("A0 import source probe")
    print(f"Status: {report['status']}")
    print(f"Reachable sources: {report['summary']['reachable']}/{report['summary']['sources']}")
    print(f"pdftotext: {report['tools']['pdftotext']}")
    for probe in report["sources"]:
        outcome = "reachable" if probe["reachable"] else "blocked/unreachable"
        print(
            "{key}: {outcome}, status={status}, type={content_type}, url={url}".format(
                key=probe["key"],
                outcome=outcome,
                status=probe["status_code"],
                content_type=probe["content_type"],
                url=probe["url"],
            )
        )
    print(f"claim: {report['claim']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    report = build_report(timeout=args.timeout)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
