#!/usr/bin/env python3
"""Verify the M31 fixed-G universal base-field RS embedding packet.

The packet certifies an exact counterexample adapter from ordinary
Reed--Solomon lists on deployed boundary shortenings to one fixed-``G``
boundary slice of the M31 code.  It is a route cut, not an ordinary-list
upper bound, a varying-``G`` census, a v4 payment, or row closure.

All gates use explicit exceptions and remain active under ``python -O``.
The verifier checks canonical JSON, a closed top-level schema, fresh source
hashes, the sealed parent payload, theorem-note anchors, primary normal and
optimized replays, primary hostile mutations, an independent Sage replay,
the sealed parent packet, scalar-descent scope, and hostile packet mutations.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Sequence


SCHEMA_DOC_ID = "rs-mca-m31-fixed-g-universal-rs-embedding-v1"
SCHEMA_ID = "m31-fixed-g-universal-rs-embedding-summary-v1"
THEOREM_ID = "M31_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_V1"
ARCHITECTURE_ID = "M31_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_V1"
ARTIFACT_KIND = "EXACT_FIXED_G_BASE_FIELD_RS_EMBEDDING_COUNTEREXAMPLE_ADAPTER"
STATUS = "PROVED_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_ORDINARY_LIST_BOUND_OPEN"
TERMINAL = "UNPAID_UNIFORM_DETERMINISTIC_PUNCTURED_RS_LIST_BOUND"

PARENT_PAYLOAD = "006cde59ee0a9fc23f8f13c3dc9955c26732bdee86b4af943f06fffeb5dd572e"
PARENT_THEOREM = "M31_COMMON_V_SPLIT_FLAT_PAIRWISE_CRT_EQUIVALENCE_V1"
PARENT_STATUS = "PROVED_PAIRWISE_CRT_EQUIVALENCE_SPLIT_FLAT_ATLAS_GLOBAL_INCIDENCE_OPEN"

P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
FORBIDDEN_LIST_SIZE = B_STAR + 1
ORDINARY_REQUIRED_UPPER = B_STAR - 1
ALLOWED_CONSTANT_LOWER = P - R
DEPLOYED_NUMERATOR = B_STAR * A
DEPLOYED_BAD_UPPER, DEPLOYED_REMAINDER = divmod(DEPLOYED_NUMERATOR, ALLOWED_CONSTANT_LOWER)
DEPLOYED_GOOD_LOWER = A - DEPLOYED_BAD_UPPER
GOOD_MARGIN_OVER_R = DEPLOYED_GOOD_LOWER - R
UNIFORM_LMAX = 259_450_259
UNIFORM_LMAX_SUCCESSOR = UNIFORM_LMAX + 1
UNIFORM_BAD_UPPER = (UNIFORM_LMAX * A) // ALLOWED_CONSTANT_LOWER
UNIFORM_SUCCESSOR_BAD_UPPER = (UNIFORM_LMAX_SUCCESSOR * A) // ALLOWED_CONSTANT_LOWER
U_PAID = 3_730
ATOM_ORDER = ("U_paid", "U_Q", "U_list_int", "U_ext", "U_new")

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_fixed_g_universal_rs_embedding_v1.schema.json"
DEFAULT_MANIFEST = ROOT / "experimental/data/certificates/m31-fixed-g-universal-rs-embedding-v1/manifest.json"
README_PATH = ROOT / "experimental/data/certificates/m31-fixed-g-universal-rs-embedding-v1/README.md"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md"
PRIMARY_PATH = ROOT / "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.sage"
PARENT_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/manifest.json"
PARENT_PACKET_PATH = ROOT / "experimental/scripts/verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py"
PARENT_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_common_v_split_flat_pairwise_crt_equivalence_v1.md"
SCALAR_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_scalar_descent_equivalence.md"
SCALAR_REPLAY_PATH = ROOT / "experimental/scripts/verify_m31_scalar_descent_equivalence.py"


class VerificationError(RuntimeError):
    """Raised whenever an exact packet gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity JSON forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_decode(raw: bytes, *, canonical: bool) -> dict[str, Any]:
    require(len(raw) <= 64 * 1024 * 1024, "JSON size cap")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise VerificationError("invalid JSON") from exc
    require(type(value) is dict, "top-level JSON object")
    if canonical:
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def strict_load(path: Path, *, canonical: bool = True) -> dict[str, Any]:
    require(path.exists() and path.is_file(), f"JSON source exists: {path}")
    return strict_decode(path.read_bytes(), canonical=canonical)


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def canonical_repo_path(value: str) -> Path:
    require(type(value) is str and value.isascii(), "source path ASCII string")
    pure = PurePosixPath(value)
    require(not pure.is_absolute(), "source path relative")
    require(len(pure.parts) > 0, "source path nonempty")
    require("." not in pure.parts and ".." not in pure.parts, "source path canonical")
    path = ROOT.joinpath(*pure.parts)
    require(path.exists() and path.is_file(), f"source exists: {value}")
    require(not path.is_symlink(), f"source is not symlink: {value}")
    require(path.resolve().is_relative_to(ROOT.resolve()), f"source contained: {value}")
    return path


def strict_payload_pin(path: Path, expected: str, label: str) -> dict[str, Any]:
    value = strict_load(path)
    require(value.get("payload_sha256") == expected, f"{label}: payload pin")
    require(payload_sha256(value) == expected, f"{label}: payload seal")
    return value


def source_binding(
    binding_id: str,
    path_text: str,
    role: str,
    scope: str,
    *,
    internal_payload_sha256: str | None = None,
) -> dict[str, Any]:
    path = canonical_repo_path(path_text)
    if internal_payload_sha256 is not None:
        strict_payload_pin(path, internal_payload_sha256, binding_id)
    return {
        "binding_id": binding_id,
        "internal_payload_sha256": internal_payload_sha256,
        "path": path_text,
        "role": role,
        "scope": scope,
        "sha256": sha256_path(path),
    }


def validate_schema() -> None:
    schema = strict_load(SCHEMA_PATH, canonical=False)
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft")
    require(schema.get("$id") == SCHEMA_DOC_ID, "schema document id")
    require(schema.get("type") == "object", "schema object")
    require(schema.get("additionalProperties") is False, "schema top closed")
    required = {
        "architecture_id",
        "artifact_kind",
        "dependency_contract",
        "deployed_parameters",
        "fixed_g_embedding",
        "ledger_state",
        "nonclaims",
        "payload_sha256",
        "row_contract",
        "schema",
        "source_bindings",
        "status",
        "terminal",
        "theorem_id",
        "threshold_equivalence",
        "translation_avoidance",
        "toy_replays",
    }
    require(set(schema.get("required", [])) == required, "schema required keys")
    require(set(schema.get("properties", {})) == required, "schema property keys")


def arithmetic() -> None:
    require(P == 2_147_483_647, "M31 prime")
    require((N, K, A, R, W) == (2_097_152, 1_048_576, 1_116_023, 981_129, 67_447), "deployed parameters")
    require(B_STAR == 16_777_215 and FORBIDDEN_LIST_SIZE == 16_777_216, "budget/list size")
    require(ORDINARY_REQUIRED_UPPER == 16_777_214, "ordinary forced upper")
    require(ALLOWED_CONSTANT_LOWER == 2_146_502_518, "allowed constant lower")
    require(DEPLOYED_NUMERATOR == 18_723_757_815_945, "deployed incidence numerator")
    require((DEPLOYED_BAD_UPPER, DEPLOYED_REMAINDER) == (8_722, 1_962_853_949), "deployed division")
    require(DEPLOYED_GOOD_LOWER == 1_107_301, "deployed good-root lower")
    require(GOOD_MARGIN_OVER_R == 126_172, "good-root reserve")
    require(A - R == 134_894, "uniform bad-root allowance")
    require(UNIFORM_BAD_UPPER == 134_894, "Lmax bad-root floor")
    require(UNIFORM_SUCCESSOR_BAD_UPPER == 134_895, "Lmax successor floor")
    require(A - UNIFORM_BAD_UPPER == R, "Lmax uniform endpoint")
    require(A - UNIFORM_SUCCESSOR_BAD_UPPER == R - 1, "Lmax successor fails")
    require((W + 1, R, R - W) == (67_448, 981_129, 913_682), "degree intervals")


def run_process(
    command: list[str],
    *,
    timeout: int,
    label: str,
    env: dict[str, str] | None = None,
) -> bytes:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationError(f"{label}: execution failed") from exc
    require(completed.returncode == 0, f"{label}: exit status")
    require(completed.stderr == b"", f"{label}: stderr empty")
    require(completed.stdout.endswith(b"\n"), f"{label}: final newline")
    return completed.stdout


def verify_primary_summary(summary: dict[str, Any]) -> None:
    require(summary.get("schema") == SCHEMA_ID, "primary schema")
    require(summary.get("theorem_id") == THEOREM_ID, "primary theorem")
    require(summary.get("architecture") == ARCHITECTURE_ID, "primary architecture")
    require(summary.get("status") == STATUS, "primary status")
    require(summary.get("terminal") == TERMINAL, "primary terminal")

    params = summary["parameters"]
    require((params["p"], params["n"], params["K"], params["a"], params["R"], params["w"]) == (P, N, K, A, R, W), "primary deployed tuple")
    require(params["B_star"] == B_STAR and params["forbidden_list_size"] == FORBIDDEN_LIST_SIZE, "primary budget/list")
    require(params["allowed_constant_lower_p_minus_R"] == ALLOWED_CONSTANT_LOWER, "primary allowed denominator")
    require(params["deployed_division"] == {
        "denominator_p_minus_R": ALLOWED_CONSTANT_LOWER,
        "numerator_L_times_a": DEPLOYED_NUMERATOR,
        "quotient": DEPLOYED_BAD_UPPER,
        "remainder": DEPLOYED_REMAINDER,
    }, "primary exact division")
    require(params["good_S0_root_lower"] == DEPLOYED_GOOD_LOWER, "primary good-root lower")
    require(params["good_root_margin_over_R"] == GOOD_MARGIN_OVER_R, "primary good-root reserve")
    require(params["uniform_Lmax"] == UNIFORM_LMAX, "primary Lmax")
    require(params["Lmax_bad_root_upper"] == UNIFORM_BAD_UPPER, "primary Lmax floor")
    require(params["Lmax_successor_bad_root_upper"] == UNIFORM_SUCCESSOR_BAD_UPPER, "primary successor floor")
    require(params["legal_d_interval"] == [1, R - W], "primary d interval")
    require(params["legal_m_interval"] == [W + 1, R], "primary m interval")

    averaging = summary["averaging_lemma"]
    require(averaging["allowed_constants"] == "C=F_p\\{-r(x):x in E0}", "primary allowed constants")
    require(averaging["allowed_constant_count"] == "p-|r(E0)|>=p-R", "primary allowed count")
    require(averaging["uses_union_not_pair_multiplicity"] is True, "primary incidence/union scope")
    require(averaging["bad_object"] == "union of S0 points where some b_i(x)+c=0", "primary bad object")
    require(averaging["deployed_worst_case_gate"] == "a-floor(L*a/(p-R))>=m", "primary deployed gate")
    require(averaging["general_gate"] == "a-floor(L*a/(p-|r(E0)|))>=m=d+w", "primary exact general gate")
    require(averaging["deployed_B_star_bad_union_upper"] == DEPLOYED_BAD_UPPER, "primary deployed bad union")
    require(averaging["deployed_B_star_good_root_lower"] == DEPLOYED_GOOD_LOWER, "primary deployed good roots")

    embedding = summary["embedding"]
    require(embedding["all_nonanchors_share_one_G"] is True, "primary one fixed G")
    require(embedding["fixed_locator"] == "G=L_T divides A0 and deg(G)=m", "primary fixed locator")
    require(embedding["translation"] == "b_i'=b_i+c and r'=r+c, with r' nowhere zero", "primary translation")
    require(embedding["common_unit"] == "V(x)=G(x)/(r(x)+c) on E0", "primary common unit")
    require(embedding["full_gcd"] == "H_i=gcd(L0,G-b_i'V)=agreement locator of b_i with r", "primary exact full gcd")
    require(embedding["maximum_codeword_degree"] == K - 1, "primary codeword degree")
    require(embedding["exact_agreement_support"] == "(S0\\Z(G)) disjoint_union Agr_E0(b_i,r)", "primary support")
    require(embedding["translated_polynomials_distinct"] is True, "primary distinctness")
    require(embedding["zero_anchor_is_boundary"] is True, "primary zero anchor")
    require(embedding["target_field_embedding_valid"] is True, "primary target-field embedding")

    threshold = summary["threshold_consequence"]
    require(threshold["ordinary_companions"] == B_STAR, "primary ordinary companions")
    require(threshold["boundary_anchor"] == 1, "primary anchor count")
    require(threshold["M31_list_size"] == FORBIDDEN_LIST_SIZE, "primary forbidden list")
    require(threshold["M_ord_required_upper_if_M31_safe"] == ORDINARY_REQUIRED_UPPER, "primary forced ordinary upper")
    require(threshold["ordinary_RS_upper_proved"] is False, "primary ordinary upper open")
    require(threshold["global_varying_G_converse"] is False, "primary varying-G converse absent")
    require("E0 subset of deployed D" in threshold["M_ord_statement"], "primary pinned-domain scope")

    uniform = summary["uniform_range"]
    require(uniform["works_for_all_legal_m_through_L"] == UNIFORM_LMAX, "primary uniform Lmax")
    require(uniform["successor"] == UNIFORM_LMAX_SUCCESSOR, "primary Lmax successor")
    require(uniform["at_Lmax_good_roots"] == R, "primary Lmax roots")
    require(uniform["successor_good_roots"] == R - 1, "primary successor roots")
    require(uniform["successor_fails_uniform_m_equals_R_gate"] is True, "primary sharp conservative gate")

    row = summary["row"]
    require(row["evaluation_domain"] == "every partition D=S0 disjoint_union E0 of the deployed D", "primary deployed-domain scope")
    require(row["coefficient_field"] == "F_p embedded in F_(p^4)", "primary field scope")

    johnson = summary["johnson_middle"]
    require(johnson["nonpositive_m_interval"] == [[72_859, 908_270]], "primary Johnson m interval")
    require(johnson["nonpositive_d_interval"] == [[5_412, 840_823]], "primary Johnson d interval")

    toy = summary["small_prime_control"]
    require(toy["field"] == "GF(11)" and toy["q"] == 11, "primary toy field")
    require(toy["averaging_bad_union_upper"] == 1, "primary toy averaging")
    require(toy["allowed_translation_count"] == 8, "primary toy allowed translations")
    require(toy["exhaustive_fixed_G_constructions"] == 20, "primary toy exhaustive constructions")
    require(toy["selected_construction"]["all_nonanchors_share_one_G"] is True, "primary toy fixed G")
    require(toy["selected_construction"]["list_size_including_anchor"] == 3, "primary toy list off-by-one")

    ledger = summary["ledger"]
    require(ledger["U_paid"] == U_PAID, "primary parent payment")
    require(all(ledger[atom] is None for atom in ATOM_ORDER[1:]), "primary null atoms")
    require(ledger["movement"] == 0 and ledger["official_endpoint_movement"] == 0, "primary zero movement")
    require(ledger["row_closed"] is False, "primary row open")
    require("no deterministic ordinary RS list upper is proved" in summary["nonclaims"], "primary upper nonclaim")


def replay_primary() -> tuple[dict[str, Any], dict[str, Any]]:
    normal_raw = run_process([sys.executable, str(PRIMARY_PATH)], timeout=300, label="primary normal")
    optimized_raw = run_process([sys.executable, "-O", str(PRIMARY_PATH)], timeout=300, label="primary optimized")
    normal = strict_decode(normal_raw, canonical=True)
    optimized = strict_decode(optimized_raw, canonical=True)
    deep_exact(optimized, normal, "primary optimized replay")
    verify_primary_summary(normal)

    tamper_raw = run_process(
        [sys.executable, str(PRIMARY_PATH), "--tamper-selftest"],
        timeout=300,
        label="primary tamper",
    )
    tamper = strict_decode(tamper_raw, canonical=True)
    require(tamper.get("schema") == SCHEMA_ID, "primary tamper schema")
    require(tamper.get("theorem_id") == THEOREM_ID, "primary tamper theorem")
    require(tamper.get("mutation_selftest") == "PASS", "primary tamper pass")
    require(type(tamper.get("mutations_detected")) is int and tamper["mutations_detected"] >= 37, "primary mutation count")
    require(len(tamper.get("mutation_names", [])) == tamper["mutations_detected"], "primary mutation names")
    require(tamper.get("ordinary_RS_upper_proved") is False, "primary tamper upper open")
    require(tamper.get("row_closed") is False, "primary tamper row open")
    return normal, {
        "normal_output_sha256": sha256_bytes(normal_raw),
        "optimized_output_sha256": sha256_bytes(optimized_raw),
        "normal_equals_optimized": normal_raw == optimized_raw,
        "tamper_output_sha256": sha256_bytes(tamper_raw),
        "mutations_detected": tamper["mutations_detected"],
        "mutation_names": tamper["mutation_names"],
    }


def replay_sage() -> dict[str, Any]:
    sage_env = dict(os.environ)
    sage_env["HOME"] = "/tmp/rs-mca-sage-home"
    raw = run_process(
        ["/usr/local/bin/sage", str(SAGE_PATH)],
        timeout=900,
        label="Sage replay",
        env=sage_env,
    )
    summary = strict_decode(raw, canonical=True)
    require(summary.get("schema") == "m31-fixed-g-universal-rs-embedding-sage-v1", "Sage schema")
    require(summary.get("theorem_id") == THEOREM_ID, "Sage theorem")
    require(summary.get("architecture_id") == ARCHITECTURE_ID, "Sage architecture")
    require(summary.get("status") == STATUS, "Sage status")
    require(summary.get("terminal") == TERMINAL, "Sage terminal")
    avoidance = summary["avoidance_control"]
    require(avoidance["field"] == "GF(11)", "Sage field")
    require(avoidance["allowed_constant_count"] == 8, "Sage allowed constants")
    require(avoidance["conservative_allowed_count_q_minus_E"] == 6, "Sage conservative denominator")
    require(avoidance["conservative_bad_union_cap"] == 1, "Sage bad-union cap")
    require(avoidance["summed_bad_union"] <= avoidance["summed_incidences"] <= 2 * 4, "Sage union/incidence gate")
    require(avoidance["witness_kappa"] == 3, "Sage witness translation")
    exhaustive = summary["exhaustive_embedding_control"]
    require(exhaustive["allowed_translations"] == 8, "Sage exhaustive translations")
    require(exhaustive["exhaustive_translation_locator_constructions"] == 20, "Sage exhaustive constructions")
    require(exhaustive["exact_codeword_support_checks"] == 40, "Sage exact supports")
    require(exhaustive["ordinary_table_to_fixed_G_and_back"] is True, "Sage forward/reverse")
    require(exhaustive["witness"]["G_degree"] == 3, "Sage fixed-G degree")
    require(len(exhaustive["witness"]["nonanchors"]) == 2, "Sage nonanchor count")
    require(exhaustive["witness"]["zero_anchor_support"] == [5, 6, 7, 8], "Sage anchor support")
    require(exhaustive["witness"]["lift_invariance"] is True, "Sage lift invariance")
    scope = summary["deployed_scope"]
    require(scope["ordinary_list_upper_16777214_proved"] is False, "Sage ordinary upper open")
    require(scope["global_split_rational_incidence_upper_proved"] is False, "Sage global residual open")
    require(scope["arbitrary_ambient_Fp4_received_word_equivalence_proved"] is False, "Sage field scope")
    require(scope["ledger_movement"] == 0 and scope["row_closed"] is False, "Sage row open")
    require(scope["toy_controls_are_deployed_evidence"] is False, "Sage evidence scope")
    return {
        "independent_finite_field_control": True,
        "output_sha256": sha256_bytes(raw),
        "summary": summary,
    }


def replay_parent_packet() -> dict[str, Any]:
    raw = run_process(
        [sys.executable, str(PARENT_PACKET_PATH), "--check"],
        timeout=1200,
        label="parent packet replay",
    )
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("parent packet ASCII") from exc
    require("M31 common-V split-flat pairwise-CRT packet v1: PASS" in text, "parent packet PASS")
    require("global split rational-function/divisor incidence: OPEN; v4 ledger movement: 0" in text, "parent packet residual open")
    return {"output_sha256": sha256_bytes(raw), "verified": True}


def replay_scalar_descent() -> dict[str, Any]:
    raw = run_process([sys.executable, str(SCALAR_REPLAY_PATH)], timeout=180, label="scalar descent replay")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("scalar replay ASCII") from exc
    lines = text.splitlines()
    require(lines and lines[-1] == "VERIFIED", "scalar descent VERIFIED")
    values: dict[str, str] = {}
    for line in lines[:-1]:
        require(line.count("=") == 1, "scalar descent key-value line")
        key, value = line.split("=", 1)
        require(key and value and key not in values, "scalar descent unique field")
        values[key] = value
    require(values.get("p") == str(P), "scalar descent p")
    require(values.get("B_star") == str(B_STAR), "scalar descent B_star")
    require(values.get("threshold_equivalence") == "PASS", "scalar descent equivalence")
    require(values.get("semantic_mutations") == "8/8", "scalar descent mutations")
    return {"fields": values, "output_sha256": sha256_bytes(raw)}


def verify_parent() -> dict[str, Any]:
    parent = strict_payload_pin(PARENT_MANIFEST_PATH, PARENT_PAYLOAD, "parent packet")
    require(parent.get("theorem_id") == PARENT_THEOREM, "parent theorem")
    require(parent.get("status") == PARENT_STATUS, "parent status")
    require(parent["pairwise_crt_equivalence"]["exact_boundary_list_realization"]["degree_gate"] == "deg(c_i)<K", "parent reconstruction degree")
    require(parent["pairwise_crt_equivalence"]["exact_boundary_list_realization"]["boundary_anchor"] == "zero_codeword", "parent zero anchor")
    require(parent["ledger_state"]["movement_from_this_packet"] == 0, "parent zero movement")
    require(parent["ledger_state"]["row_closed"] is False, "parent row open")
    return parent


def verify_text_contracts() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# M31 fixed-G universal base-field RS embedding",
        "### Lemma 2.1",
        "C=F\\setminus\\{-r(x):x\\in E\\}",
        "The proof uses incidences only as an upper bound on bad points.",
        "p-R=2,146,502,518",
        "a-8,722=1,107,301",
        "=R+126,172",
        "L_{\\max}",
        "=259,450,259",
        "### Theorem 4.1",
        "q_r=p-|r(E_0)|\\ge p-R",
        "a-\\left\\lfloor\\frac{La}{q_r}\\right\\rfloor\\ge m",
        "G=L_Z",
        "b_i=f_i+kappa",
        "V(x)=G(x)/\\widetilde r(x)",
        "H_i=gcd(L_0,G-b_iV)",
        "(S_0\\setminus Z)\\mathbin{\\dot\\cup}Z(H_i)",
        "B_*-1=16,777,214",
        "Only R-subsets E_0 of the deployed domain D are asserted.",
        "does not pay U_{\\mathrm{list-int}}",
    ):
        require(anchor in note, f"theorem-note anchor: {anchor}")

    parent_note = PARENT_NOTE_PATH.read_text(encoding="utf-8")
    require("# M31 common-V split-flat and pairwise CRT equivalence" in parent_note, "parent note title")
    require("fixed-G slice is exactly an ordinary Reed--Solomon list census" in parent_note, "parent fixed-G source")

    scalar_note = SCALAR_NOTE_PATH.read_text(encoding="utf-8")
    require("Its evaluation domain is contained in `F_p`." in scalar_note, "scalar pinned base-field domain")
    require("threshold_equivalence" not in scalar_note or "PASS" in scalar_note, "scalar note equivalence")

    readme = README_PATH.read_text(encoding="utf-8")
    for anchor in (
        "floor(B_star*a/(p-R))                    = 8,722",
        "1,107,301-R                              = 126,172",
        "B_star-1=16,777,214",
        "`L <= 259,450,259`",
        "subsets of the pinned deployed domain",
        TERMINAL,
    ):
        require(anchor in readme, f"README anchor: {anchor}")


def source_bindings() -> list[dict[str, Any]]:
    return [
        source_binding(
            "M31_FIXED_G_RS::packet_schema",
            "experimental/data/schemas/m31_fixed_g_universal_rs_embedding_v1.schema.json",
            "packet_schema",
            "Closed top-level schema for the fixed-G RS embedding packet.",
        ),
        source_binding(
            "M31_FIXED_G_RS::packet_verifier",
            "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_packet_v1.py",
            "packet_verifier",
            "Canonical manifest, dependency replay, source hashes, and hostile mutations.",
        ),
        source_binding(
            "M31_FIXED_G_RS::primary_exact_replay",
            "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.py",
            "primary_exact_replay",
            "Standard-library deployed arithmetic, finite-table construction, and mutations.",
        ),
        source_binding(
            "M31_FIXED_G_RS::sage_exact_replay",
            "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_v1.sage",
            "sage_exact_replay",
            "Independent Sage finite-field interpolation, gcd, support, and degree replay.",
        ),
        source_binding(
            "M31_FIXED_G_RS::theorem_note",
            "experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md",
            "theorem_note",
            "Avoidance lemma, exact construction, threshold equivalence, scope, and route cut.",
        ),
        source_binding(
            "M31_FIXED_G_RS::packet_readme",
            "experimental/data/certificates/m31-fixed-g-universal-rs-embedding-v1/README.md",
            "packet_readme",
            "Replay commands, exact margins, dependency, and nonclaims.",
        ),
        source_binding(
            "M31_FIXED_G_RS::parent_manifest",
            "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/manifest.json",
            "parent_manifest",
            "Sealed common-V split-flat and pairwise CRT parent packet.",
            internal_payload_sha256=PARENT_PAYLOAD,
        ),
        source_binding(
            "M31_FIXED_G_RS::parent_packet_verifier",
            "experimental/scripts/verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py",
            "parent_packet_verifier",
            "Fail-closed replay of the sealed parent packet.",
        ),
        source_binding(
            "M31_FIXED_G_RS::scalar_descent_note",
            "experimental/notes/thresholds/m31_scalar_descent_equivalence.md",
            "scalar_descent_note",
            "Prime-field threshold equivalence and pinned-domain scope.",
        ),
        source_binding(
            "M31_FIXED_G_RS::scalar_descent_replay",
            "experimental/scripts/verify_m31_scalar_descent_equivalence.py",
            "scalar_descent_replay",
            "Exact deployed scalar-descent arithmetic and semantic mutations.",
        ),
    ]


def build_template() -> dict[str, Any]:
    arithmetic()
    verify_text_contracts()
    parent = verify_parent()
    primary, primary_replay = replay_primary()
    sage_replay = replay_sage()
    parent_replay = replay_parent_packet()
    scalar_replay = replay_scalar_descent()
    bindings = source_bindings()

    payload: dict[str, Any] = {
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "dependency_contract": {
            "parent": {
                "path": "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/manifest.json",
                "payload_sha256": PARENT_PAYLOAD,
                "status": PARENT_STATUS,
                "theorem_id": PARENT_THEOREM,
            },
            "stacked_dependency": True,
            "subprocess_replays": {
                "parent_packet": True,
                "parent_packet_output_sha256": parent_replay["output_sha256"],
                "primary_mutations_detected": primary_replay["mutations_detected"],
                "primary_normal": True,
                "primary_normal_equals_optimized": primary_replay["normal_equals_optimized"],
                "primary_normal_output_sha256": primary_replay["normal_output_sha256"],
                "primary_optimized": True,
                "primary_optimized_output_sha256": primary_replay["optimized_output_sha256"],
                "primary_tamper_output_sha256": primary_replay["tamper_output_sha256"],
                "sage": True,
                "sage_output_sha256": sage_replay["output_sha256"],
                "scalar_descent": True,
                "scalar_descent_output_sha256": scalar_replay["output_sha256"],
            },
        },
        "deployed_parameters": {
            **copy.deepcopy(primary["parameters"]),
            "ordinary_required_upper_if_M31_safe": ORDINARY_REQUIRED_UPPER,
            "target_epsilon": "2^-100",
        },
        "fixed_g_embedding": {
            **copy.deepcopy(primary["embedding"]),
            "johnson_middle": copy.deepcopy(primary["johnson_middle"]),
            "same_G_for_every_nonanchor": True,
            "G_may_depend_on_the_input_list": True,
            "G_predeclared_independently_of_the_list": False,
        },
        "ledger_state": {
            "atoms": [
                {"atom_id": atom, "value": primary["ledger"][atom]}
                for atom in ATOM_ORDER
            ],
            "movement_from_this_packet": primary["ledger"]["movement"],
            "official_endpoint_or_score_movement": primary["ledger"]["official_endpoint_movement"],
            "ordinary_RS_upper_proved": False,
            "row_closed": primary["ledger"]["row_closed"],
            "route_cut_is_not_payment": True,
        },
        "nonclaims": {
            "arbitrary_evaluation_sets_outside_pinned_D_covered_by_deployed_consequence": False,
            "complete_M31_list_bound_proved": False,
            "deterministic_ordinary_RS_list_upper_proved": False,
            "fixed_G_predeclared_independently_of_input_list": False,
            "global_varying_G_converse_proved": False,
            "ledger_atom_paid_by_this_packet": False,
            "official_endpoint_or_score_changed": False,
            "row_closed": False,
            "small_prime_controls_are_deployed_evidence": False,
            "stable_paper_modified": False,
            "v4_owner_transport_proved": False,
        },
        "payload_sha256": "",
        "row_contract": {
            **copy.deepcopy(primary["row"]),
            "anchor_codewords_added": 1,
            "ordinary_companion_input_at_deployed_threshold": B_STAR,
            "projection_unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "scope": "EVERY_R_SUBSET_E0_OF_THE_PINNED_DEPLOYED_DOMAIN_D_AND_S0_EQUALS_D_MINUS_E0",
        },
        "schema": SCHEMA_ID,
        "source_bindings": bindings,
        "status": STATUS,
        "terminal": TERMINAL,
        "theorem_id": THEOREM_ID,
        "threshold_equivalence": {
            "deployed": copy.deepcopy(primary["threshold_consequence"]),
            "fixed_G_subclass_only": True,
            "general_varying_G_row_equivalence": False,
            "uniform_range": copy.deepcopy(primary["uniform_range"]),
        },
        "translation_avoidance": copy.deepcopy(primary["averaging_lemma"]),
        "toy_replays": {
            "parent_packet": parent_replay,
            "primary_mutation_names": primary_replay["mutation_names"],
            "primary_small_prime_control": copy.deepcopy(primary["small_prime_control"]),
            "sage": sage_replay,
            "scalar_descent": scalar_replay,
        },
    }
    require(parent["payload_sha256"] == PARENT_PAYLOAD, "template parent payload")
    return seal(payload)


def verify_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list and len(bindings) == 10, "source bindings list")
    ids: set[str] = set()
    paths: set[str] = set()
    pins = 0
    for index, binding in enumerate(bindings):
        require(type(binding) is dict, f"binding {index}: object")
        require(set(binding) == {"binding_id", "internal_payload_sha256", "path", "role", "scope", "sha256"}, f"binding {index}: exact keys")
        require(type(binding["binding_id"]) is str and binding["binding_id"].isascii(), f"binding {index}: id")
        require(binding["binding_id"] not in ids, f"binding {index}: unique id")
        ids.add(binding["binding_id"])
        path = canonical_repo_path(binding["path"])
        require(binding["path"] not in paths, f"binding {index}: unique path")
        paths.add(binding["path"])
        require(type(binding["role"]) is str and binding["role"].isascii(), f"binding {index}: role")
        require(type(binding["scope"]) is str and binding["scope"].isascii(), f"binding {index}: scope")
        digest = binding["sha256"]
        require(type(digest) is str and len(digest) == 64 and set(digest) <= set("0123456789abcdef"), f"binding {index}: hash")
        require(digest == sha256_path(path), f"binding {index}: fresh hash")
        pin = binding["internal_payload_sha256"]
        if pin is not None:
            pins += 1
            require(type(pin) is str and len(pin) == 64, f"binding {index}: pin shape")
            strict_payload_pin(path, pin, f"binding {index}")
    require(pins == 1, "one internal predecessor pin")


def validate(payload: dict[str, Any], expected: dict[str, Any] | None = None) -> None:
    arithmetic()
    require(payload.get("schema") == SCHEMA_ID, "payload schema")
    require(payload.get("theorem_id") == THEOREM_ID, "payload theorem")
    require(payload.get("architecture_id") == ARCHITECTURE_ID, "payload architecture")
    require(payload.get("artifact_kind") == ARTIFACT_KIND, "payload artifact kind")
    require(payload.get("status") == STATUS, "payload status")
    require(payload.get("terminal") == TERMINAL, "payload terminal")
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")

    params = payload["deployed_parameters"]
    require(params["p"] == P and params["B_star"] == B_STAR, "payload p/B_star")
    require(params["allowed_constant_lower_p_minus_R"] == ALLOWED_CONSTANT_LOWER, "payload allowed denominator")
    require(params["deployed_division"]["quotient"] == DEPLOYED_BAD_UPPER, "payload deployed floor")
    require(params["deployed_division"]["remainder"] == DEPLOYED_REMAINDER, "payload deployed remainder")
    require(params["good_S0_root_lower"] == DEPLOYED_GOOD_LOWER, "payload good roots")
    require(params["good_root_margin_over_R"] == GOOD_MARGIN_OVER_R, "payload reserve")
    require(params["uniform_Lmax"] == UNIFORM_LMAX, "payload Lmax")
    require(params["ordinary_required_upper_if_M31_safe"] == ORDINARY_REQUIRED_UPPER, "payload ordinary cap")

    averaging = payload["translation_avoidance"]
    require(averaging["allowed_constant_count"] == "p-|r(E0)|>=p-R", "payload allowed count")
    require(averaging["uses_union_not_pair_multiplicity"] is True, "payload incidence/union")
    require(averaging["bad_object"] == "union of S0 points where some b_i(x)+c=0", "payload bad object")
    require(averaging["deployed_worst_case_gate"] == "a-floor(L*a/(p-R))>=m", "payload deployed gate")
    require(averaging["general_gate"] == "a-floor(L*a/(p-|r(E0)|))>=m=d+w", "payload general gate")

    embedding = payload["fixed_g_embedding"]
    require(embedding["all_nonanchors_share_one_G"] is True, "payload fixed G")
    require(embedding["same_G_for_every_nonanchor"] is True, "payload same G")
    require(embedding["G_may_depend_on_the_input_list"] is True, "payload G dependence")
    require(embedding["G_predeclared_independently_of_the_list"] is False, "payload no predeclared G")
    require(embedding["maximum_codeword_degree"] == K - 1, "payload degree")
    require(embedding["translated_polynomials_distinct"] is True, "payload distinctness")
    require(embedding["exact_agreement_support"] == "(S0\\Z(G)) disjoint_union Agr_E0(b_i,r)", "payload support")
    require(embedding["johnson_middle"]["nonpositive_m_interval"] == [[72_859, 908_270]], "payload Johnson middle")

    threshold = payload["threshold_equivalence"]
    require(threshold["fixed_G_subclass_only"] is True, "payload fixed-G scope")
    require(threshold["general_varying_G_row_equivalence"] is False, "payload no global converse")
    require(threshold["deployed"]["M31_list_size"] == FORBIDDEN_LIST_SIZE, "payload list off-by-one")
    require(threshold["deployed"]["M_ord_required_upper_if_M31_safe"] == ORDINARY_REQUIRED_UPPER, "payload ordinary upper")
    require(threshold["deployed"]["ordinary_RS_upper_proved"] is False, "payload ordinary upper open")
    require(threshold["uniform_range"]["works_for_all_legal_m_through_L"] == UNIFORM_LMAX, "payload uniform Lmax")
    require(threshold["uniform_range"]["successor_fails_uniform_m_equals_R_gate"] is True, "payload successor failure")

    row = payload["row_contract"]
    require(row["evaluation_domain"] == "every partition D=S0 disjoint_union E0 of the deployed D", "payload pinned domain")
    require(row["scope"] == "EVERY_R_SUBSET_E0_OF_THE_PINNED_DEPLOYED_DOMAIN_D_AND_S0_EQUALS_D_MINUS_E0", "payload exact scope")
    require(row["anchor_codewords_added"] == 1, "payload anchor count")
    require(row["ordinary_companion_input_at_deployed_threshold"] == B_STAR, "payload companion count")

    ledger = payload["ledger_state"]
    require([row["atom_id"] for row in ledger["atoms"]] == list(ATOM_ORDER), "payload atom order")
    require(ledger["atoms"][0]["value"] == U_PAID, "payload parent payment")
    require(all(row["value"] is None for row in ledger["atoms"][1:]), "payload null atoms")
    require(ledger["movement_from_this_packet"] == 0, "payload zero movement")
    require(ledger["official_endpoint_or_score_movement"] == 0, "payload zero official movement")
    require(ledger["ordinary_RS_upper_proved"] is False, "payload upper open")
    require(ledger["row_closed"] is False and ledger["route_cut_is_not_payment"] is True, "payload row open")
    require(all(value is False for value in payload["nonclaims"].values()), "all nonclaims false")

    dependency = payload["dependency_contract"]
    require(dependency["stacked_dependency"] is True, "payload stacked dependency")
    require(dependency["parent"]["payload_sha256"] == PARENT_PAYLOAD, "payload parent pin")
    require(dependency["parent"]["theorem_id"] == PARENT_THEOREM, "payload parent theorem")
    replays = dependency["subprocess_replays"]
    require(replays["primary_normal"] is True and replays["primary_optimized"] is True, "payload primary modes")
    require(replays["primary_normal_equals_optimized"] is True, "payload optimized equality")
    require(replays["primary_mutations_detected"] >= 37, "payload primary mutations")
    require(replays["sage"] is True and replays["parent_packet"] is True and replays["scalar_descent"] is True, "payload dependency replays")

    toy = payload["toy_replays"]
    require(toy["primary_small_prime_control"]["exhaustive_fixed_G_constructions"] == 20, "payload primary toy exhaustion")
    require(toy["primary_small_prime_control"]["selected_construction"]["list_size_including_anchor"] == 3, "payload toy off-by-one")
    require(toy["sage"]["independent_finite_field_control"] is True, "payload Sage independence")
    require(toy["parent_packet"]["verified"] is True, "payload parent replay")
    verify_source_bindings(payload["source_bindings"])

    if expected is not None:
        deep_exact(payload, expected)


def mutate(path: Sequence[Any], value: Any) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def apply(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        cursor: Any = out
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        return seal(out)

    return apply


def tamper_selftest(expected: dict[str, Any]) -> int:
    def drop_source(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["source_bindings"].pop()
        return seal(out)

    def duplicate_source(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["source_bindings"][1]["binding_id"] = out["source_bindings"][0]["binding_id"]
        return seal(out)

    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("schema", mutate(("schema",), "wrong")),
        ("theorem", mutate(("theorem_id",), "WRONG")),
        ("architecture", mutate(("architecture_id",), "WRONG")),
        ("status", mutate(("status",), "CLOSED")),
        ("terminal", mutate(("terminal",), "PAID")),
        ("p", mutate(("deployed_parameters", "p"), P - 2)),
        ("B_star", mutate(("deployed_parameters", "B_star"), B_STAR + 1)),
        ("allow denominator", mutate(("deployed_parameters", "allowed_constant_lower_p_minus_R"), P)),
        ("division quotient", mutate(("deployed_parameters", "deployed_division", "quotient"), DEPLOYED_BAD_UPPER - 1)),
        ("division remainder", mutate(("deployed_parameters", "deployed_division", "remainder"), DEPLOYED_REMAINDER + 1)),
        ("good roots", mutate(("deployed_parameters", "good_S0_root_lower"), DEPLOYED_GOOD_LOWER - 1)),
        ("reserve", mutate(("deployed_parameters", "good_root_margin_over_R"), GOOD_MARGIN_OVER_R - 1)),
        ("Lmax", mutate(("deployed_parameters", "uniform_Lmax"), UNIFORM_LMAX + 1)),
        ("ordinary upper", mutate(("deployed_parameters", "ordinary_required_upper_if_M31_safe"), B_STAR)),
        ("allowed count", mutate(("translation_avoidance", "allowed_constant_count"), "p")),
        ("incidence equals union", mutate(("translation_avoidance", "uses_union_not_pair_multiplicity"), False)),
        ("bad object", mutate(("translation_avoidance", "bad_object"), "incidence pairs")),
        ("general gate", mutate(("translation_avoidance", "general_gate"), "a-floor(L*a/p)>=m")),
        ("fixed G", mutate(("fixed_g_embedding", "all_nonanchors_share_one_G"), False)),
        ("separate G", mutate(("fixed_g_embedding", "same_G_for_every_nonanchor"), False)),
        ("predeclared G", mutate(("fixed_g_embedding", "G_predeclared_independently_of_the_list"), True)),
        ("degree", mutate(("fixed_g_embedding", "maximum_codeword_degree"), K)),
        ("distinctness", mutate(("fixed_g_embedding", "translated_polynomials_distinct"), False)),
        ("support", mutate(("fixed_g_embedding", "exact_agreement_support"), "Z(G) union Z(H)")),
        ("Johnson middle", mutate(("fixed_g_embedding", "johnson_middle", "nonpositive_m_interval"), [[72_858, 908_270]])),
        ("not fixed-G subclass", mutate(("threshold_equivalence", "fixed_G_subclass_only"), False)),
        ("false global converse", mutate(("threshold_equivalence", "general_varying_G_row_equivalence"), True)),
        ("anchor off-by-one", mutate(("threshold_equivalence", "deployed", "M31_list_size"), B_STAR)),
        ("false ordinary upper", mutate(("threshold_equivalence", "deployed", "ordinary_RS_upper_proved"), True)),
        ("successor gate", mutate(("threshold_equivalence", "uniform_range", "successor_fails_uniform_m_equals_R_gate"), False)),
        ("arbitrary domain", mutate(("row_contract", "scope"), "EVERY_R_SUBSET_OF_F_P")),
        ("anchor count", mutate(("row_contract", "anchor_codewords_added"), 0)),
        ("companion count", mutate(("row_contract", "ordinary_companion_input_at_deployed_threshold"), B_STAR - 1)),
        ("ledger movement", mutate(("ledger_state", "movement_from_this_packet"), 1)),
        ("official movement", mutate(("ledger_state", "official_endpoint_or_score_movement"), 1)),
        ("row closure", mutate(("ledger_state", "row_closed"), True)),
        ("route cut payment", mutate(("ledger_state", "route_cut_is_not_payment"), False)),
        ("U_list_int", mutate(("ledger_state", "atoms", 2, "value"), 0)),
        ("false nonclaim", mutate(("nonclaims", "deterministic_ordinary_RS_list_upper_proved"), True)),
        ("parent pin", mutate(("dependency_contract", "parent", "payload_sha256"), "0" * 64)),
        ("unstack", mutate(("dependency_contract", "stacked_dependency"), False)),
        ("skip optimized", mutate(("dependency_contract", "subprocess_replays", "primary_optimized"), False)),
        ("optimized mismatch", mutate(("dependency_contract", "subprocess_replays", "primary_normal_equals_optimized"), False)),
        ("skip Sage", mutate(("dependency_contract", "subprocess_replays", "sage"), False)),
        ("skip parent", mutate(("dependency_contract", "subprocess_replays", "parent_packet"), False)),
        ("replay hash", mutate(("dependency_contract", "subprocess_replays", "primary_normal_output_sha256"), "0" * 64)),
        ("toy exhaustion", mutate(("toy_replays", "primary_small_prime_control", "exhaustive_fixed_G_constructions"), 19)),
        ("toy anchor", mutate(("toy_replays", "primary_small_prime_control", "selected_construction", "list_size_including_anchor"), 2)),
        ("source hash", mutate(("source_bindings", 0, "sha256"), "0" * 64)),
        ("source traversal", mutate(("source_bindings", 0, "path"), "../schema.json")),
        ("source internal pin", mutate(("source_bindings", 6, "internal_payload_sha256"), "0" * 64)),
        ("drop source", drop_source),
        ("duplicate source", duplicate_source),
    ]
    rejected = 0
    for name, apply in mutations:
        candidate = apply(expected)
        try:
            validate(candidate, expected)
        except (VerificationError, KeyError, IndexError, TypeError):
            rejected += 1
        else:
            raise VerificationError(f"mutation escaped: {name}")

    malformed = [
        b'{"a":1,"a":2}\n',
        b'{"x":1.5}\n',
        b'{"x":NaN}\n',
        b'[]\n',
        b'{"x":"\xff"}\n',
        b'{"x":1}',
    ]
    for raw in malformed:
        try:
            strict_decode(raw, canonical=True)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("malformed JSON accepted")
    require(rejected == len(mutations) + len(malformed), "all packet mutations rejected")
    return rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.check or args.tamper_selftest or args.print_template):
        args.check = True
    require(sum((args.check, args.tamper_selftest, args.print_template)) == 1, "select exactly one mode")
    validate_schema()
    expected = build_template()
    validate(expected, expected)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
        return
    if args.tamper_selftest:
        count = tamper_selftest(expected)
        print(f"M31 fixed-G universal RS embedding packet mutations: {count}/{count} rejected PASS")
        return

    actual = strict_load(args.manifest)
    validate(actual, expected)
    print("M31 fixed-G universal base-field RS embedding packet v1: PASS")
    print("constant translation: allowed-set averaging and common-good-root reserve PASS")
    print("fixed-G embedding: degree, support, unit, gcd, distinctness, and anchor gates PASS")
    print("deployed arithmetic: bad=8722; good=1107301; reserve=126172 PASS")
    print("ordinary punctured RS upper: OPEN; varying-G residual: OPEN; v4 ledger movement: 0")
    print(f"checks={CHECKS}")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
