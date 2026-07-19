#!/usr/bin/env python3
"""Exact replay for the dense-shell FOLD weighted-curvature certificate.

No grid or cascade census is run.  The verifier expands the universal linear
identities coefficientwise, checks the oriented third-difference convention
and the exact quadratic-profile arithmetic, binds public statement markers,
and supplies fail-closed mutations.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = (
    ROOT
    / "experimental/notes/thresholds/dense_shell_fold_curvature_certificate.md"
)
SOURCE = ROOT / "experimental/notes/thresholds/dense_shell_prop_tail_reduction.md"
LEAN = (
    ROOT
    / "experimental/lean/dense_shell_fold_curvature_certificate/"
    / "DenseShellFoldCurvatureCertificate.lean"
)

FAILED: list[str] = []
PASSED = 0
DIM_P = 17
DIM_L = 18


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASSED
    if ok:
        PASSED += 1
    else:
        FAILED.append(name)
    suffix = f" ({detail})" if detail else ""
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def zero(size: int) -> tuple[int, ...]:
    return (0,) * size


def basis(size: int, index: int) -> tuple[int, ...]:
    return tuple(1 if i == index else 0 for i in range(size))


def add(*vectors: tuple[int, ...]) -> tuple[int, ...]:
    if not vectors:
        raise ValueError("add requires at least one vector")
    size = len(vectors[0])
    if any(len(vector) != size for vector in vectors):
        raise ValueError("coefficient dimension mismatch")
    return tuple(sum(vector[i] for vector in vectors) for i in range(size))


def scale(coefficient: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * value for value in vector)


def sub(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return add(left, scale(-1, right))


def symbolic_data(tamper: str | None):
    p = tuple(basis(DIM_P, i) for i in range(DIM_P))
    S = add(*p[:16])
    kappas = tuple(add(p[j + 2], scale(-2, p[j + 1]), p[j]) for j in range(15))
    weights = tuple((j + 1) * (15 - j) for j in range(15))
    if tamper == "endpoint-weight":
        weights = weights[:-1] + (weights[-1] - 1,)
    K = add(*(scale(weight, curvature) for weight, curvature in zip(weights, kappas)))
    return p, S, kappas, weights, K


def third_difference(j: int) -> tuple[int, ...]:
    """Delta^3 L_j = L_(j+3)-3L_(j+2)+3L_(j+1)-L_j."""

    return add(
        basis(DIM_L, j + 3),
        scale(-3, basis(DIM_L, j + 2)),
        scale(3, basis(DIM_L, j + 1)),
        scale(-1, basis(DIM_L, j)),
    )


def oriented_curvature(j: int, orientation: int) -> tuple[int, ...]:
    """Second difference of p_i=orientation*(L_i-L_(i+1))."""

    drops = tuple(
        scale(
            orientation,
            sub(basis(DIM_L, i), basis(DIM_L, i + 1)),
        )
        for i in range(17)
    )
    return add(drops[j + 2], scale(-2, drops[j + 1]), drops[j])


def gate_sources(tamper: str | None) -> bool:
    if tamper == "source-marker":
        return False
    note = NOTE.read_text(encoding="utf-8")
    source = SOURCE.read_text(encoding="utf-8")
    lean = LEAN.read_text(encoding="utf-8")
    note_markers = (
        "Theorem 1 (weighted curvature identity)",
        "7K <= 119p_0+5p_16",
        "The full (FOLD) clause remains open.",
        "Missing realized-profile lemma",
    )
    source_markers = (
        "**(FOLD) — the 57/50 child-window fold.**",
        "measured max `1.1322` at `n=48`",
    )
    lean_markers = (
        "theorem weighted_curvature_identity",
        "theorem fold_iff_weighted_curvature",
        "theorem fold_17_15_from_curvature_sum",
        "theorem quadratic_window_sums",
    )
    return (
        all(marker in note for marker in note_markers)
        and all(marker in source for marker in source_markers)
        and all(marker in lean for marker in lean_markers)
    )


def run(tamper: str | None = None) -> bool:
    print("INPUT: one monotone 18-value window; exact integer coefficient arithmetic")
    print("OBJECT: 18-over-17 spread fold and weighted drop curvature")
    print("THEOREM: dense-shell-fold-curvature-certificate")
    print("STATUS: PROVED PARTIAL (full realized-profile FOLD remains open)")

    p, S, kappas, weights, K = symbolic_data(tamper)
    expected_weights = (15, 28, 39, 48, 55, 60, 63, 64, 63, 60, 55, 48, 39, 28, 15)
    weight_target = 681 if tamper == "weight-sum" else 680
    weights_ok = weights == expected_weights and all(weight > 0 for weight in weights)
    weights_ok &= sum(weights) == weight_target
    check("F1 exact positive curvature weights", weights_ok, f"sum={sum(weights)}")

    identity_lhs = scale(2, S)
    identity_rhs = sub(add(scale(17, p[0]), scale(15, p[16])), K)
    check(
        "F2 weighted summation-by-parts identity coefficientwise",
        identity_lhs == identity_rhs,
        f"variables={DIM_P}",
    )

    fold_tail = 49 if tamper == "fold-constant" else 50
    fold_margin_twice = scale(2, sub(scale(7, S), scale(fold_tail, p[16])))
    curvature_margin = sub(add(scale(119, p[0]), scale(5, p[16])), scale(7, K))
    check(
        "F3 57/50 fold iff exact weighted-curvature certificate",
        fold_margin_twice == curvature_margin,
    )

    sign_ok = True
    for j in range(15):
        delta3 = third_difference(j)
        decreasing_expected = scale(-1, delta3)
        if tamper == "curvature-sign" and j == 0:
            decreasing_expected = delta3
        sign_ok &= oriented_curvature(j, 1) == decreasing_expected
        sign_ok &= oriented_curvature(j, -1) == delta3
    check(
        "F4 oriented curvature sign: decreasing kappa=-Delta^3 L",
        sign_ok,
        "indices=0..14; both orientations",
    )

    concave_decomposition = sub(scale(2, S), scale(15, p[16]))
    concave_rhs = sub(scale(17, p[0]), K)
    ratio_ok = concave_decomposition == concave_rhs
    ratio_ok &= 17 * 50 < 57 * 15
    check(
        "F5 concave-drop subfamily gives 17/15 < 57/50",
        ratio_ok,
        "850<855",
    )

    quadratic_p = tuple(2 * i + 1 for i in range(17))
    if tamper == "quadratic-tail":
        quadratic_p = quadratic_p[:-1] + (32,)
    quadratic_kappa = tuple(
        quadratic_p[j + 2] - 2 * quadratic_p[j + 1] + quadratic_p[j]
        for j in range(15)
    )
    quadratic_S = sum(quadratic_p[:16])
    quadratic_full = sum(quadratic_p)
    quadratic_ok = all(value == 0 for value in quadratic_kappa)
    quadratic_ok &= quadratic_S == 256 and quadratic_full == 289
    quadratic_ok &= 289 * 50 < 57 * 256
    check(
        "F6 quadratic profile has exact ratio 289/256",
        quadratic_ok,
        f"spreads={quadratic_S},{quadratic_full}",
    )

    defect_constant = 4759 if tamper == "defect-constant" else 4760
    defect_ok = sum(weights) == 680
    defect_ok &= 7 * sum(weights) == defect_constant
    defect_ok &= curvature_margin == scale(2, sub(scale(7, S), scale(50, p[16])))
    check(
        "F7 uniform positive-curvature defect certificate",
        defect_ok,
        f"7*680={7 * sum(weights)}",
    )

    check("F8 required source markers present in source, note, and Lean", gate_sources(tamper))

    total = PASSED + len(FAILED)
    print(f"CERTIFICATE: exact checks={PASSED}/{total}; deterministic seed=none")
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} ({PASSED}/{total})")
    return not FAILED


def tamper_selftest() -> bool:
    tampers = (
        "endpoint-weight",
        "weight-sum",
        "fold-constant",
        "curvature-sign",
        "quadratic-tail",
        "defect-constant",
        "source-marker",
    )
    runs = [
        (
            tamper,
            subprocess.Popen(
                [sys.executable, __file__, "--tamper", tamper],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            ),
        )
        for tamper in tampers
    ]
    caught = 0
    for tamper, process in runs:
        stdout, _ = process.communicate()
        detected = process.returncode != 0 and "RESULT: FAIL" in stdout
        caught += int(detected)
        print(f"tamper {tamper}: {'caught' if detected else 'MISSED'}")
    print(f"TAMPER SELFTEST: {caught}/{len(tampers)} caught")
    return caught == len(tampers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tamper",
        choices=(
            "endpoint-weight",
            "weight-sum",
            "fold-constant",
            "curvature-sign",
            "quadratic-tail",
            "defect-constant",
            "source-marker",
        ),
    )
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return 0 if tamper_selftest() else 1
    return 0 if run(args.tamper) else 1


if __name__ == "__main__":
    raise SystemExit(main())
