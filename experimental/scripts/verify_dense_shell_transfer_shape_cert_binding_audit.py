#!/usr/bin/env python3
"""Self-contained transcript audit for the PR #905 Arb certificate.

The audited tree is PR #905 head 0000964180a4a809ca5ddb46d02bc91220c2a8ac.
The transfer-shape packet is byte-identical at integration commit 3404d21 for
its proof, Arb verifier, replay wrapper, contract, and certificate.  This
script deliberately does not import flint.  Its default mode reads no
repository file: it checks the pinned SHA-256 observations and the resulting
provenance logic.  The optional ``--verify-tree`` mode recomputes those
observations from the two pinned Git objects.

Reproduction commands for the embedded observations are printed by
``--reproduction``.  A PASS means that the audit finding is internally
consistent; it does not certify TS1--TS3 or replay the Arb computation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass


PR_NUMBER = 905
PR_HEAD = "0000964180a4a809ca5ddb46d02bc91220c2a8ac"
INTEGRATION = "3404d21b64c876c6d9b995ad3e29d7120ab27a54"
UPSTREAM_BASE = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
CERT_SHA256 = "80c8dfc072977d4ea6359086f7dedf4eaa67a5a56b6064634299a933f02d4e09"
PR_BODY_CERT_SHA256 = (
    "80c8dfc072977d4ea6359086f7dedf4eaa67a5a56b6064634299a933f02d4e09"
)
PR_BODY_UPDATED_AT = "2026-07-18T10:13:57Z"
PR_BODY_CLI_SHA256 = (
    "40be2b98b36423d5037871e4b915f3d746fae78b41e8544d87a728951890dce9"
)

MANIFEST_PATH = (
    "experimental/data/certificates/dense-shell-transfer-shape/SHA256SUMS.txt"
)
CERTIFICATE_PATH = (
    "experimental/data/certificates/dense-shell-transfer-shape/"
    "dense_shell_transfer_shape.json"
)
WRAPPER_PATH = "experimental/scripts/replay_dense_shell_transfer_shape.py"


@dataclass(frozen=True)
class HashRow:
    name: str
    recorded: str
    actual_at_head: str
    actual_at_integration: str | None = None

    @property
    def head_mismatch(self) -> bool:
        return self.recorded != self.actual_at_head

    @property
    def integration_mismatch(self) -> bool:
        actual = self.actual_at_integration or self.actual_at_head
        return self.recorded != actual


MANIFEST_ROWS = (
    HashRow(
        "experimental/notes/thresholds/dense_shell_transfer_shape.md",
        "0cf65b76e6a788310ced83c9400aa0ef17b07747c8c509054d3149b7115a0509",
        "5fc9f180b69fe87f5d2b055355577511672aff8ef222beb42ab9d2e628354368",
    ),
    HashRow(
        "experimental/scripts/verify_dense_shell_transfer_shape_arb.py",
        "1fd9d8bbacc79905842837c910e22c8f5cf4079c620fff23eb970150378e4b77",
        "9eac9446b74b50641ee9f7c661de0da656701b5902aba521ba2936f6b50e0c1c",
    ),
    HashRow(
        "experimental/scripts/replay_dense_shell_transfer_shape.py",
        "47e818c40caa974b31bdfc6a2d963d8d9cf4e32d3caab8e62a375ecf46adccef",
        "32b45f42bc694d0daa9271e6223e43060bab8327d5437882616c35732e0a09fa",
    ),
    HashRow(
        "experimental/scripts/README.md",
        "fb457506a1facbf3f8a45c840338079d4a0a67d8739a51c69f5380c2b68f3917",
        "f85c7cff4fc647e8be00c35c8d62588ecb753605235d35befb9dfa0757cfe54f",
        "bae6a2ebb25db39466f47d487b2d8586e770f4555355122a2293e19ccfbb15cd",
    ),
    HashRow(
        "experimental/data/certificates/dense-shell-transfer-shape/dense_shell_transfer_shape.json",
        "5a731c8839e613d36f767596429ea83867940eb6230eeb142a1a684038792512",
        CERT_SHA256,
    ),
    HashRow(
        "experimental/data/certificates/dense-shell-transfer-shape/consumer_contract.json",
        "3a3f1558e21418cec6bdab4e3c9ad370648bee9e8d7477b38aad1d861e40d702",
        "a0cfa97b006f316812ea4e8c9f7384e745a980691cdc91c14b35fe68a200dacb",
    ),
    HashRow(
        "experimental/data/certificates/dense-shell-transfer-shape/README.md",
        "1408d25ae535aa1a6295b6af46b4f06c65cd083a1d70ff92d7264f3cf3e55efd",
        "042a8045e09c9f56de4431edcd1e5a9bb800a791c0cfad7d3a721fe36c8096d3",
    ),
    HashRow(
        "experimental/notes/thresholds/dense_shell_class_charges.md",
        "6ebb6f6eaf23665cb3ae23d82c6e6e9ba4057869561fcaf0d8066b36ba9f2879",
        "e92c61aaffb3ab382789bee8b8ba00db809fb9b7cfc969dff7918a7904951c4f",
        "e13be4f164ac741329c98e174b2261970c368081a1f725bd4b9ae7249e4e7270",
    ),
    HashRow(
        "experimental/scripts/verify_dense_shell_class_charges.py",
        "5fbe9ef774420324b7e22cdf512ee394c0df584c5101bc948acc19103fe2cdeb",
        "561bcf5d536a853296c1ddf9def9067d0ec7616fd63e458c52b7d2f68420b7fc",
        "23703024a296ff6c94ec9b2d4b652310e7e0e8b858dcc4677a28f3bd6c598212",
    ),
    HashRow(
        "experimental/data/certificates/dense-shell-class-charges/dense_shell_class_charges.json",
        "613ca0f25ccd22eb9f86feedbb4b337d46a0571c332f239aecd4726f0cc27586",
        "719879447b4ff15d01703b713c493879f40adff63e894a1aa2ffa9bc59a612e3",
        "4c19880fb876126fb4ae1cd3f9abd3fabe268c431d3dcb7718326b0b1005f901",
    ),
)


BINDING_ROWS = (
    HashRow(
        "proof_sha256",
        "0cf65b76e6a788310ced83c9400aa0ef17b07747c8c509054d3149b7115a0509",
        "5fc9f180b69fe87f5d2b055355577511672aff8ef222beb42ab9d2e628354368",
    ),
    HashRow(
        "source_sha256",
        "1fd9d8bbacc79905842837c910e22c8f5cf4079c620fff23eb970150378e4b77",
        "9eac9446b74b50641ee9f7c661de0da656701b5902aba521ba2936f6b50e0c1c",
    ),
    HashRow(
        "replay_source_sha256",
        "47e818c40caa974b31bdfc6a2d963d8d9cf4e32d3caab8e62a375ecf46adccef",
        "32b45f42bc694d0daa9271e6223e43060bab8327d5437882616c35732e0a09fa",
    ),
    HashRow(
        "consumer_contract_sha256",
        "3a3f1558e21418cec6bdab4e3c9ad370648bee9e8d7477b38aad1d861e40d702",
        "a0cfa97b006f316812ea4e8c9f7384e745a980691cdc91c14b35fe68a200dacb",
    ),
    HashRow(
        "consumed_note_sha256",
        "6ebb6f6eaf23665cb3ae23d82c6e6e9ba4057869561fcaf0d8066b36ba9f2879",
        "e92c61aaffb3ab382789bee8b8ba00db809fb9b7cfc969dff7918a7904951c4f",
        "e13be4f164ac741329c98e174b2261970c368081a1f725bd4b9ae7249e4e7270",
    ),
    HashRow(
        "consumer_script_sha256",
        "5fbe9ef774420324b7e22cdf512ee394c0df584c5101bc948acc19103fe2cdeb",
        "561bcf5d536a853296c1ddf9def9067d0ec7616fd63e458c52b7d2f68420b7fc",
        "23703024a296ff6c94ec9b2d4b652310e7e0e8b858dcc4677a28f3bd6c598212",
    ),
)

EXPECTED_MANIFEST_NAMES = (
    "experimental/notes/thresholds/dense_shell_transfer_shape.md",
    "experimental/scripts/verify_dense_shell_transfer_shape_arb.py",
    "experimental/scripts/replay_dense_shell_transfer_shape.py",
    "experimental/scripts/README.md",
    "experimental/data/certificates/dense-shell-transfer-shape/dense_shell_transfer_shape.json",
    "experimental/data/certificates/dense-shell-transfer-shape/consumer_contract.json",
    "experimental/data/certificates/dense-shell-transfer-shape/README.md",
    "experimental/notes/thresholds/dense_shell_class_charges.md",
    "experimental/scripts/verify_dense_shell_class_charges.py",
    "experimental/data/certificates/dense-shell-class-charges/dense_shell_class_charges.json",
)
EXPECTED_BINDING_NAMES = (
    "proof_sha256",
    "source_sha256",
    "replay_source_sha256",
    "consumer_contract_sha256",
    "consumed_note_sha256",
    "consumer_script_sha256",
)


CERTIFICATE_STATIC = {
    "schema": "dense-shell-transfer-shape-arb/v3",
    "pass": True,
    "python_flint_tested": "0.9.0",
    "arb_precision_bits": 448,
    "chebyshev_degree": 320,
    "two_state_base_level": 25,
    "curvature_base_level": 26,
    "finite_target_levels_n": [5, 26],
    "upstream_base": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
}
EXPECTED_STATIC = {
    "schema": "dense-shell-transfer-shape-arb/v3",
    "pass": True,
    "python_flint_tested": "0.9.0",
    "arb_precision_bits": 448,
    "chebyshev_degree": 320,
    "two_state_base_level": 25,
    "curvature_base_level": 26,
    "finite_target_levels_n": [5, 26],
    "upstream_base": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
}

CERTIFICATE_FIELDS = frozenset(
    {
        "arb_precision_bits",
        "base_interval_cells",
        "bernstein_rho",
        "chebyshev_degree",
        "consumed_note_sha256",
        "consumer_contract_sha256",
        "consumer_script_sha256",
        "curvature_C",
        "curvature_base_level",
        "epsilon_interval_cells",
        "finite_target_levels_n",
        "interpolation_operator_bound",
        "lambda",
        "parameter_neighborhood_radius",
        "pass",
        "proof_sha256",
        "python_flint_tested",
        "replay_source_sha256",
        "results",
        "scalar_interval_cells",
        "schema",
        "source_sha256",
        "two_state_base_level",
        "upstream_base",
    }
)

WRAPPER_STEPS = (
    "Arb --check",
    "Arb --tamper-selftest",
    "py_compile",
    "class-charge --deep",
    "JSON parse",
    "SHA256SUMS check",
)

CHECKED_IN_TRANSCRIPTS: tuple[str, ...] = ()
PR_BODY_CLAIMS_ARTIFACT_HASHES_PASS = True


def summarize(
    manifest_rows: tuple[HashRow, ...] = MANIFEST_ROWS,
    binding_rows: tuple[HashRow, ...] = BINDING_ROWS,
    cert_sha256: str = CERT_SHA256,
    pr_body_cert_sha256: str = PR_BODY_CERT_SHA256,
    certificate_fields: frozenset[str] = CERTIFICATE_FIELDS,
    wrapper_steps: tuple[str, ...] = WRAPPER_STEPS,
) -> dict[str, object]:
    manifest_head = sum(row.head_mismatch for row in manifest_rows)
    manifest_integration = sum(row.integration_mismatch for row in manifest_rows)
    binding_head = sum(row.head_mismatch for row in binding_rows)
    binding_integration = sum(row.integration_mismatch for row in binding_rows)
    manifest_rows_complete = tuple(row.name for row in manifest_rows) == EXPECTED_MANIFEST_NAMES
    binding_rows_complete = tuple(row.name for row in binding_rows) == EXPECTED_BINDING_NAMES
    return {
        "manifest_rows_complete": manifest_rows_complete,
        "binding_rows_complete": binding_rows_complete,
        "manifest_mismatches_at_head": manifest_head,
        "manifest_mismatches_at_integration": manifest_integration,
        "binding_mismatches_at_head": binding_head,
        "binding_mismatches_at_integration": binding_integration,
        "certificate_hash_matches_pr_body": cert_sha256 == pr_body_cert_sha256,
        "artifact_pass_claim_contradicted": (
            PR_BODY_CLAIMS_ARTIFACT_HASHES_PASS and manifest_head > 0
        ),
        "current_check_payload_must_differ": (
            binding_rows_complete and binding_head == len(EXPECTED_BINDING_NAMES)
        ),
        "producer_head_pinned": "producer_commit" in certificate_fields,
        "checked_in_transcript_count": len(CHECKED_IN_TRANSCRIPTS),
        "static_fields_coherent": CERTIFICATE_STATIC == EXPECTED_STATIC,
        "hash_check_runs_after_arb": wrapper_steps == WRAPPER_STEPS,
    }


def audit_checks(summary: dict[str, object]) -> tuple[tuple[str, bool, str], ...]:
    return (
        (
            "manifest-stale-at-head",
            (
                bool(summary["manifest_rows_complete"])
                and summary["manifest_mismatches_at_head"]
                == len(EXPECTED_MANIFEST_NAMES)
            ),
            (
                f"{summary['manifest_mismatches_at_head']}/"
                f"{len(EXPECTED_MANIFEST_NAMES)} mismatch; "
                f"complete={summary['manifest_rows_complete']}"
            ),
        ),
        (
            "manifest-stale-at-integration",
            (
                bool(summary["manifest_rows_complete"])
                and summary["manifest_mismatches_at_integration"]
                == len(EXPECTED_MANIFEST_NAMES)
            ),
            (
                f"{summary['manifest_mismatches_at_integration']}/"
                f"{len(EXPECTED_MANIFEST_NAMES)} mismatch; "
                f"complete={summary['manifest_rows_complete']}"
            ),
        ),
        (
            "certificate-self-binding-stale-at-head",
            (
                bool(summary["binding_rows_complete"])
                and summary["binding_mismatches_at_head"]
                == len(EXPECTED_BINDING_NAMES)
            ),
            (
                f"{summary['binding_mismatches_at_head']}/"
                f"{len(EXPECTED_BINDING_NAMES)} mismatch; "
                f"complete={summary['binding_rows_complete']}"
            ),
        ),
        (
            "certificate-self-binding-stale-at-integration",
            (
                bool(summary["binding_rows_complete"])
                and summary["binding_mismatches_at_integration"]
                == len(EXPECTED_BINDING_NAMES)
            ),
            (
                f"{summary['binding_mismatches_at_integration']}/"
                f"{len(EXPECTED_BINDING_NAMES)} mismatch; "
                f"complete={summary['binding_rows_complete']}"
            ),
        ),
        (
            "frozen-certificate-payload-identified",
            bool(summary["certificate_hash_matches_pr_body"]),
            f"sha256={CERT_SHA256}",
        ),
        (
            "frozen-transcript-artifact-pass-contradicted",
            bool(summary["artifact_pass_claim_contradicted"]),
            (
                "PR body snapshot says PASS while pinned manifest is 0/10; "
                f"body_cli_sha256={PR_BODY_CLI_SHA256[:16]}"
            ),
        ),
        (
            "current-verifier-check-cannot-match-certificate",
            bool(summary["current_check_payload_must_differ"]),
            "certificate_payload recomputes all six mismatching hashes",
        ),
        (
            "producer-head-not-pinned",
            not bool(summary["producer_head_pinned"]),
            f"only upstream_base={UPSTREAM_BASE[:8]} is recorded",
        ),
        (
            "no-hash-bound-stdout-transcript",
            summary["checked_in_transcript_count"] == 0,
            "checked-in transcript count=0",
        ),
        (
            "static-certificate-parameters-coherent",
            bool(summary["static_fields_coherent"]),
            "schema/precision/degree/base levels agree internally",
        ),
        (
            "wrapper-order-recorded-correctly",
            bool(summary["hash_check_runs_after_arb"]),
            "Arb --check and tamper run before SHA256SUMS",
        ),
    )


def print_rows(title: str, rows: tuple[HashRow, ...]) -> None:
    print(title)
    for row in rows:
        integrated = row.actual_at_integration or row.actual_at_head
        print(
            f"  {row.name}: recorded={row.recorded[:16]} "
            f"head={row.actual_at_head[:16]} integrated={integrated[:16]}"
        )


def run_audit() -> bool:
    summary = summarize()
    print(f"TARGET: PR #{PR_NUMBER} head {PR_HEAD[:8]} integrated at {INTEGRATION[:8]}")
    print("SCOPE: transcript and SHA-256 provenance only; Arb not replayed")
    print_rows("MANIFEST:", MANIFEST_ROWS)
    print_rows("CERTIFICATE BINDINGS:", BINDING_ROWS)
    checks = audit_checks(summary)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}")
    passed = all(ok for _, ok, _ in checks)
    report = {
        "schema": "dense-shell-transfer-shape-cert-binding-audit/v1",
        "status": "AUDIT",
        "verdict": "OPEN GAP",
        "finding": "SHOULD_CERT_BINDING_STALENESS",
        "arb_replayed": False,
        "target_pr": PR_NUMBER,
        "target_head": PR_HEAD,
        "integration": INTEGRATION,
        "pr_body_updated_at": PR_BODY_UPDATED_AT,
        "pr_body_cli_sha256": PR_BODY_CLI_SHA256,
        **summary,
        "pass": passed,
    }
    print("AUDIT_JSON=" + json.dumps(report, sort_keys=True, separators=(",", ":")))
    print(f"RESULT: {'PASS' if passed else 'FAIL'} ({sum(ok for _, ok, _ in checks)}/{len(checks)})")
    return passed


def run_tamper_selftest() -> bool:
    tests: tuple[tuple[str, dict[str, object], str], ...] = (
        (
            "omit-manifest-row",
            {"manifest_rows": MANIFEST_ROWS[1:]},
            "manifest-stale-at-head",
        ),
        (
            "omit-binding-row",
            {"binding_rows": BINDING_ROWS[1:]},
            "certificate-self-binding-stale-at-head",
        ),
        (
            "certificate-hash-drift",
            {"cert_sha256": "0" * 64},
            "frozen-certificate-payload-identified",
        ),
        (
            "invent-producer-pin",
            {"certificate_fields": frozenset(set(CERTIFICATE_FIELDS) | {"producer_commit"})},
            "producer-head-not-pinned",
        ),
        (
            "omit-arb-check-step",
            {"wrapper_steps": WRAPPER_STEPS[1:]},
            "wrapper-order-recorded-correctly",
        ),
    )

    baseline = {name: ok for name, ok, _ in audit_checks(summarize())}
    caught = 0
    for name, kwargs, target_gate in tests:
        tampered = {gate: ok for gate, ok, _ in audit_checks(summarize(**kwargs))}
        ok = baseline.get(target_gate) is True and tampered.get(target_gate) is False
        caught += int(ok)
        print(
            f"{'PASS' if ok else 'FAIL'} | tamper {name} | "
            f"{target_gate}={tampered.get(target_gate)!r}"
        )
    passed = caught == len(tests)
    print(f"TAMPER RESULT: {'PASS' if passed else 'FAIL'} ({caught}/{len(tests)})")
    return passed


def git_blob(revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def blob_sha256(revision: str, path: str) -> str:
    return hashlib.sha256(git_blob(revision, path)).hexdigest()


def parse_manifest(revision: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in git_blob(revision, MANIFEST_PATH).decode("utf-8").splitlines():
        digest, path = line.split("  ", 1)
        rows[path] = digest
    return rows


def wrapper_steps_from_blob(revision: str) -> tuple[str, ...]:
    source = git_blob(revision, WRAPPER_PATH).decode("utf-8")
    markers = {
        "Arb --check": 'run(VERIFY, "--check")',
        "Arb --tamper-selftest": 'run(VERIFY, "--tamper-selftest")',
        "py_compile": 'run("-m", "py_compile"',
        "class-charge --deep": 'run(CLASS_VERIFY, "--deep")',
        "JSON parse": 'json.loads((CERT_DIR / "dense_shell_transfer_shape.json")',
        "SHA256SUMS check": "\n    replay_hashes()\n",
    }
    positions = {name: source.index(marker) for name, marker in markers.items()}
    return tuple(sorted(positions, key=positions.get))


def run_tree_verification() -> bool:
    """Recompute the embedded observations when the two Git objects exist."""

    head_manifest = parse_manifest(PR_HEAD)
    integration_manifest = parse_manifest(INTEGRATION)
    head_certificate = json.loads(git_blob(PR_HEAD, CERTIFICATE_PATH))
    integration_certificate = json.loads(git_blob(INTEGRATION, CERTIFICATE_PATH))
    binding_targets = dict(zip(EXPECTED_BINDING_NAMES, (
        EXPECTED_MANIFEST_NAMES[0],
        EXPECTED_MANIFEST_NAMES[1],
        EXPECTED_MANIFEST_NAMES[2],
        EXPECTED_MANIFEST_NAMES[5],
        EXPECTED_MANIFEST_NAMES[7],
        EXPECTED_MANIFEST_NAMES[8],
    )))

    manifest_by_name = {row.name: row for row in MANIFEST_ROWS}
    binding_by_name = {row.name: row for row in BINDING_ROWS}
    checks = (
        (
            "manifest-records-reloaded",
            set(head_manifest) == set(EXPECTED_MANIFEST_NAMES)
            and set(integration_manifest) == set(EXPECTED_MANIFEST_NAMES)
            and all(
                head_manifest[name] == manifest_by_name[name].recorded
                and integration_manifest[name] == manifest_by_name[name].recorded
                for name in EXPECTED_MANIFEST_NAMES
            ),
            "10 entries at both revisions",
        ),
        (
            "head-blob-hashes-recomputed",
            all(
                blob_sha256(PR_HEAD, name) == manifest_by_name[name].actual_at_head
                for name in EXPECTED_MANIFEST_NAMES
            ),
            "10/10 embedded actuals",
        ),
        (
            "integration-blob-hashes-recomputed",
            all(
                blob_sha256(INTEGRATION, name)
                == (
                    manifest_by_name[name].actual_at_integration
                    or manifest_by_name[name].actual_at_head
                )
                for name in EXPECTED_MANIFEST_NAMES
            ),
            "10/10 embedded actuals",
        ),
        (
            "certificate-binding-fields-reloaded",
            all(
                head_certificate[field] == binding_by_name[field].recorded
                and integration_certificate[field] == binding_by_name[field].recorded
                for field in EXPECTED_BINDING_NAMES
            ),
            "6 fields at both revisions",
        ),
        (
            "certificate-binding-targets-recomputed",
            all(
                blob_sha256(PR_HEAD, binding_targets[field])
                == binding_by_name[field].actual_at_head
                and blob_sha256(INTEGRATION, binding_targets[field])
                == (
                    binding_by_name[field].actual_at_integration
                    or binding_by_name[field].actual_at_head
                )
                for field in EXPECTED_BINDING_NAMES
            ),
            "6 targets at both revisions",
        ),
        (
            "certificate-file-hash-recomputed",
            blob_sha256(PR_HEAD, CERTIFICATE_PATH) == CERT_SHA256
            and blob_sha256(INTEGRATION, CERTIFICATE_PATH) == CERT_SHA256,
            CERT_SHA256,
        ),
        (
            "certificate-schema-reloaded",
            set(head_certificate) == set(CERTIFICATE_FIELDS)
            and set(integration_certificate) == set(CERTIFICATE_FIELDS)
            and all(
                head_certificate[key] == value
                and integration_certificate[key] == value
                for key, value in CERTIFICATE_STATIC.items()
            ),
            f"{len(head_certificate)} fields at both revisions",
        ),
        (
            "wrapper-order-derived",
            wrapper_steps_from_blob(PR_HEAD) == WRAPPER_STEPS
            and wrapper_steps_from_blob(INTEGRATION) == WRAPPER_STEPS,
            "Arb checks precede SHA256SUMS at both revisions",
        ),
        (
            "primary-transfer-payload-byte-identical",
            all(
                git_blob(PR_HEAD, path) == git_blob(INTEGRATION, path)
                for path in (
                    EXPECTED_MANIFEST_NAMES[0],
                    EXPECTED_MANIFEST_NAMES[1],
                    EXPECTED_MANIFEST_NAMES[2],
                    EXPECTED_MANIFEST_NAMES[4],
                    EXPECTED_MANIFEST_NAMES[5],
                )
            ),
            "proof/verifier/wrapper/certificate/contract: 5/5",
        ),
    )
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} | tree {name} | {detail}")
    passed = all(ok for _, ok, _ in checks)
    print(f"TREE RESULT: {'PASS' if passed else 'FAIL'} ({sum(ok for _, ok, _ in checks)}/{len(checks)})")
    return passed


def print_reproduction() -> None:
    print("git fetch upstream pull/905/head:refs/remotes/upstream/pr-905")
    print("gh pr view 905 --repo przchojecki/rs-mca --json body,headRefOid,updatedAt")
    print("gh pr view 905 --repo przchojecki/rs-mca --json body --jq .body | sha256sum")
    print("sha256sum -c experimental/data/certificates/dense-shell-transfer-shape/SHA256SUMS.txt")
    print("git show upstream/pr-905:<PATH> | sha256sum")
    print("python3 experimental/scripts/verify_dense_shell_transfer_shape_audit.py")
    print("python3 experimental/scripts/verify_dense_shell_class_charges.py")
    print("Do not run the Arb verifier or replay wrapper in a stdlib-only environment.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--verify-tree", action="store_true")
    parser.add_argument("--reproduction", action="store_true")
    args = parser.parse_args()
    if args.reproduction:
        print_reproduction()
        return 0
    if args.verify_tree:
        return 0 if run_tree_verification() else 1
    return 0 if (run_tamper_selftest() if args.tamper_selftest else run_audit()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
