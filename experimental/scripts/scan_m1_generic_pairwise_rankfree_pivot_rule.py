#!/usr/bin/env python3
"""Build the M1 generic-pairwise rank-free pivot-rule audit JSON."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import zlib
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")
OUTPUT_DATA = Path("experimental/data/m1_generic_pairwise_rankfree_pivot_rule.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
TARGET_BITS = 128
FIELD_DENOMINATOR = P**FIELD_DEGREE
PATTERN_CLASS = "generic_pairwise_rref_pivot"

EXPECTED_RULES = [
    "anchored_pair_proxy_first",
    "compressed_variable_block_order",
    "incidence_greedy_matching_v1",
    "nonanchored_difference_first",
    "pair_boundary_pressure_asc",
    "pair_boundary_pressure_desc",
    "pair_label_lexicographic_order",
    "rref_profile_pair_quota_mimic",
]

REQUIRED_NONCLAIMS = [
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
]

RANKFREE_RULE_RESULTS_ZLIB_B64 = """
eNrtXU2THLmNvc+vmNBZB4IAAdI3r0feUIQ/IuTxXhyODpIAZypGasndrbHljf3vC/Z3ZZVU6laPpmq3YkYtVXYWk5n5CD7gEeDf
vvn22//2P99++6zXU11pvbCTlT77zbfPWn1dT7vpSX+9+sd7O3kDJ2/Ds+fXJ7998+7Mzs/917p6Y6fnq7en5yftw8k/Vxenftwb
uGrWzwX/APT85mP0j3T3EefHePuR5ke4/Zj8Yyq3H3k2JZef/ue6J2oXdvZmdVpPL05O357+287e+kkXZ+/t+oQ39eJs9a+T8x/r
O/Pf/O26LYz5tt143ebfb76yOn17dvJjPf9xPoiENWsaxAatRq6dmS0aW8cckLlDyLnUMHrMpCM2iENHRjStww88W2v1rJ7+dDLe
v3693stTP7K6+OAHw/WRd6uf316c9Levz297gtCksJixhqyQGCJjSDXaaJlGV66BoopRjVVTLZpCkJ7VRs2QyrO1pt/V1Zm3//70
Yv11PZ9vKOXndwcW7wieL94SPF+8J3i+5U3dXfXujiTUCFootzRqCqP17o+xD2rZu104UU4dBwgRVUuS/CYxZ5NeRQjS+h2dvf3n
ycWHd7blrm7R7K/gBzu1s1W/7Mo/V+c2v+fnxq399d/ddVe1gcSAja2aqGgrIJZ65+wPWkbWFiJzqclhkjE3PyWMLFxHaJ1uuztB
cHXFewfGmXlX3r+2k3pxYW/eXd7ADVxvbuQWR3dYH/X1uT1f/v76Enfvcd7RfOM3uFo8oXvv/uZB3HsYvzAiP4oPH1JqJbWeEIpF
EgQByYOHcuyYBmaR5j1g41F7qb2RxaQVrakPv832197nU3Z/vrnZpsPsx7dnjrSrp3329l8fTobf08XyZDes9dJSPvvuxfcvXv3x
5Z9e/uX7l787+d2f//gfL//02+///Orlb/9w8uqvf3ix8c3353bujdprPalnq4sf39jFqm+Bwrm9tn7hfbnCxPnq33YfdlfnXNSL
95fd+MvLP/3nX//w21cn3pU/v7p/0U9e75sFUh4LVcKHQXUaIbgH7zu7U8q+4DcXNwajU0RiVL9UERyWU+wEPm0IYwVsROgTTClq
2Ho1Glpw2r7KO/BbW+SeRHxo+KBIrY6YaubWsiSjZn5pHEOnqersJghGhVq86Tawl8bb8Htvav/ZX3Ztjrf2+m3/yU2n2tkRxUcU
HwCKV6d9peYz/skPPq3qhxOngf3H1ekPJz/DEcKfhnDmh0A4XtLDPeIMlEuoJUQcxZx0qbcZQgoKohiDsJN0C46vqKOEDJUCamVz
KOlQorIDrXGYZaqUJhEdwgzkf1Pghj0NJ4PD3QNOTAN1YEJOShJixWYG0WwbWv3F3NIGXY1hZ5fQPdKGz0ArRHgYXNOlcYU1k4uX
JjfyvmA4JYpWg3US/24Tze58MnQ3eM0ta5yNuffZEwsYh+z+xei1uAEuwd2QsIv3OhQTCkREzgXcFR5VQlc36eT9k1HVfaWWDNw1
c6hPM0saTKVJb7CV914++ebPXOvZh5NLCvH+zH2Z835E8NHe7pe9/QhW1Y5gPQYU9i2gcPmQX9dmr09e279W/e0PZ/Xdj6t+9Mc+
ix5geThg09IhW4+Abo2Cbo2EbkZD92AMPFHQ9aNjIEMLrWAr4l5hUclmk01AnX8BSHHvrsdGZd5Z9lmgVMvsRp2psNK2MXB2ZmPG
0sbKcXr5Ev/x/u1FdQS+WX3CZL969eL3jrs/Ov4PB/FrUsSZvamr0+m32j/e14sbmWU+gs2gfUReRO0j8CJsHwMu4vYRYBm4L3eh
/Gu6ke4JOFftQLp3ZMGp/cglnw5yp/NsfAuvro5w78jV1e++Rdfn8L0jly3HuyPp6kiKa9H787fvz6YLVd+sXn/Yomc9Wz/vJ/tw
Y2svJQFd/bw6X7XVFGVOpjjzswNgvvoP5xf25je/+aQ6dt3mu9p/sosHNHv7/Vso/e7Fq+9f/v7li+9OLqH83YtXL//rxXfPvrm+
z8+V7uIXSHdY1qU7WJPuYlqT7lDWpLt15S6lJ1Lu5NY8x8CfUO66s0/WkrC6EVXA6rO/z/+a3OjEzuwGEGIbucXQRkuSoyKg9BKT
m8ZmT6fcpeRWT4qbahtFA02LOFTUXbVAOvkG0UjBZkcwTjmpxNBbTmVkKNgfoNzlsLQBaWEC7r2kKwuwFO4WL2orj6rF55As7iFW
Awh9pFSSjWxpzk7O0evQ7rTd76xHjs1nJ+IsMaaMEOqTCnfXIPiEcEdD/cHyCFr8+frjx5Tdl43EikTeb2Bw57Z1jTGiQdYaG2Tu
YjE6HpbCXeBfWrjLj+DZUHgLb4HwucTjiVD6ceIRa6itkXOW6mTamUZo3Kag6k+7Ny69V6iDMfqTD+7AQVBxF6+JUw/3MXcQj6fs
/gGpeYH3kXczPQy/eG8g7wFUkWQ4MTbhjMZBwBmwQ5Cku9soQ2Yco0t2IGejoNr8dB2D6+iWW6k7oCpd/VuJvKtV1GcbjuxEHqn0
kDN0TYwT/OR8371PdovJAu6d9ko+QdFBC3f7CVh8EGCvyev+ANbysJxTan0Iugc5dMbMIlEupWcpI1kPDTuM7H+qDKKCbn5Z3Pia
5F2AhS6peK9YpPkEn2F0djqVc4xFAg7TwJBjaT6DhlKKOFZDKkoMiSQerka3p+b1MTHj/UFrTBZScj4WpChqadB6yskqj+7G1GHj
PzWIVCeV1gqyt1/QrSMOrEF2oLWgeIfUsdmytxF8MMQeFIc3Gdx+5+5DQ0Oo4H5AqNhbz8n70TmO6Ob3cDW6/URrLl9OZq8CCPtD
ZsuQEqL/p+4upBZR2DElbk+xUAG3vLFTdoqrTmYJo5tI74F3yG20+eFdiyIyZXNkkrusY3SU6kzE++tEY4biconNb2kQtGQ5ZA5O
VUhQxM08uzN7qBLdfgJY8sPMLe2buQ2xBChFk6VE6k6Wz+S5IYcanXYGS25uK0TlViwXQb9E1VDchLqzZrvIgUjg0MIYtfRWehx5
aOngzECCsqi5Dfark5v1iiG6pY1SIjsRQdWoByvR7am1PYYO9iF0cCi63X6CGEgejuK72OfW+OfWGOi2OOhmLHQPhsAThVw/NgQ4
YhzJx1kD0RIotYre9xkHp9AhCMxZgxMQYKbAxb1IRpDu5/jIHIcj2/0ygH+8bHfP9t5AFvOGbMcbsl1ehO0j8VK2g7iU7daEvKt2
aCnbxbiQ7aDkpWx371u48S3aOIc2zrmW7cKvK9vFPZft4LGyHa3LdnE94y7KmmwX1zPu7qFmviPiJ9Lt0u1lQMondDuLzV0dThhG
d8JI0qIxOjeNvdXQk0qwEs3cEkkWaKHKNHajd/8C1vx0ul3XgjLjZB2xWkhaKZdmrRfQzjyCM44WMyT31cRNcFA3yk5IJKS5HC0+
QLcTXBoBWdqAZcYdxIUFIN4p3A0w5/kjcI3AINid7je2XlsckbBVLmQQo09VrEmdVUkPFCoTD0xFnlK4u0HBJ4Q7my9AVcERkPOA
6tNltDnxTHAIaCQp4tQPchs6/NeZ/GfI0X3ykdtCuPMr/tLCneAj2Ld8dq7HEyHy47keWll4jNKdavSgNEYiapb7zM3I3mrIqWeY
cmkJ5lQntIw5e7+6xLZrcdBTdv9wNLpb2O1ZVOMI1a8M1UPR6PYUsPggwF6x0D0CrM+hyhZ8rmLSJFi8XZ/HMDurEXfRrAcRI6o4
HUKsDmL3FrNCTeDA3QXY4CMhhdTmEs44fB5vIxrlbqHpZEZR6qxcQALITD5lciLu7uhhqrVXOliNbk/RmuDhGt0eodXPNnJUspPt
Xp0dWmcn2gZglHLj1EAaDQpYwZp0v5rhXF1FtaWAumuZsGowbMWxHVN3Wy0g0Il6LcWCZkdtDn5XGltUHDWGPiKL+pVbKDYOVqPb
VzIQHpG4vEe2NWehLAlqrbkDZpPpApTWiNyZcfiUqwU9fpU4XQN2VEnKKohMdZccJ0MKUKqjQCmCBGIBjbyZ2s28bQCHZsxSc74M
xiVhMW4V3SgL04HKcXuKVZaH8QDeL6zCxBDUpkrMNYm48YyZ3LqlHN27zdn/RW786hTURi45awwOuuzGD1rfgdU8/NROGUF8/ueg
7hO3kqLG2mw4w3Dw9mTgdANGzH6PLI7SWswZgbPnQ5Xjjl7W0cs6JOVtT/EKwA8H7H2Qb4lgbo1ibo1kbkYz94EKP03Q9GNjYBRn
uzmHeMkpApsOVkQzS8H7F51FBACE5MMLBmRo2e130lyk4+j1YKS3XwjxX5AxF2QjY24pvUHekN4wbUhvaUN6w6X0FsuG9BY3pDfe
yJgLS+ktpqX0BsuMObhbcXcjvd0ThNJ1nl34taU32FvpLX2B9JZgTXq7n/J4OQbWi12mdektr6fMladKmZO7lLn0CekNsDRKzgsD
hgHR/6HuvhRIKeS52lGELbtVgjwpZqcYeKZSdZ/+mdpITye9STL3z6hUdFvul0SbJU96DVqjswxhhMqWKEFpoBS6uOOHxiiD45Dw
AOmNl/o7LKU3SkvpbSm+p7JTejNFH7vm81GVUOsM8+UMwxo7s48p1ObeK1jEgeyTSZAGGTvXkbD50w5PmzOXdklvucS5dqrhIIyp
KqNC5OD8DmB6MO5LNCsRfZrjpr0YkZQ8BApGa7CZM5d+aemNH0Fcbh7EZ7CMJ0LkR/FRsxTtEXvPXJyu+MQ/SuqDtIh2smRqVZ1x
dKqszjvQaYlVck+vmVOcXSGMJ+z+IaXHpcPP3zhC9cuhejjpcXsJWEyPSY/bG8AmQGcrxT0+9/1KLFVDdoD2hFJ7TXVYVAILwacx
IBrVvSyOOTFMYO9cP5wTavfuQR8qpO4pimpLIfl0T1GqmPuG3CQlblBLnxVPLAeIvaXiDuUBp8ftJ1rLI6S3Qs83szgA9gXCrcWE
sZcS0ImjW1ixEkKc8pzT8NHQYkuxKmJxepaJUwzEvbDkJLuXwOtobKVwHmHG7rC2WhW6MmMhixUrFstNiVpv4bLIebdcp4PgZxse
cM7cXkKY4MshjHsGYYnDnYSB2N0ccyiQOSg193ZSzjM7qcmohO5UcHEmwcEPsmBHdcfJ/YpdS9hNYiN0LyWlGjCOalCj9uDEY7TU
Uu82Mz2jjxQ/N3UlAUauvQTrVQ42Z24/KW54TM7c3jAGba1hc183Yp5VApM7t2kGZUUzhjaLPbD/7bhNdZaIiMFNZCZoxSCR7sKq
m8/sw9XELXgOQu5Gu5XFpFKg+w1kHxFDrZUss1INZT/DyXOdYYFg43DLWh79saM/dlDpcWk/0+MekVLPW3M8t4l0lLaJdNu2KUhl
X8bAE4VXP5qQH3otzb1DGz1CnHv/GDRxMs4depkJK2MWtEyKrbmnqeBcWTD0hkK15wPKj0t7JtLdyyO7FunicjeqGGkp0kVcinSR
FiLdPb58Q0DuZd7FmyDGUqRD2siP4w2RTpYi3VoRy2XhzY+WtQz4q4p0aZ9FOv6CspZxTaPj8MkN6WhNo6N1jQ7yU21Ix3cb0tEn
NDrCHDIFbRB6sjJDSM5M/X+f+VN3/yrE6i4UxWFuS80ne+ZIxT2rwti4Pp1GZ0pQxkxu1t6kjlxipdZTgwTmTpi1VIXKXDnhrl13
ux6dvZaSC3Ch+JAN6Tju3JBuaQFoqdEt3tTWYvZNuIZZbwiHP1HGzKNwtS4WuAokzTKiu5WU1V1ZdwZqHIBazbl84PK0G9LRLo3O
zQNo5UQ0Z6VYc22jc+6deiqU3Dvp4FNhCbO8c84BRTSNqmGErAFpY0M6+sU1uviY+vH0uSTjiRD58SCcM5VQBgK5GxjqTIR3JBRn
McO9xVZ676juGWZOdUYxmKFrq3OFUOBYdpVZe8ruH9KGdLSPHDs+cEU87xdUldCtlBDP0mqhNSs1YXdjVbmJ2y53ErtRGHH4gVpC
9eti0u5XvNzQaxdU86wUb4ltLrGnWRVQxhi1E8wdL0WdOI2UwVm3X7Nhnsvnio5pU91bTYe999wRsEfAHs42c3uJVgjxMfse7Q1c
a3EqyFNUDurcT+fOHJHJch449yai1KGPGpCzUW+1WoQOba6cHyQ17oo3iGQHahf0UaAoczMjnDKyU46uISYaWAZEas5Jkbt0qpVj
q6M1AKAD3meO/i9sfHQVX1gvSHWzFHdfIJxniVTIveSKM/zWKIoz25piEoGoczu57JBiZbEOVmfRaxu1ONRLw12SslmuswKmYXQT
nWFuI6qtcY7ijkrtLaBN1iwxY8+M6EyZkpLirIkVx8FuM3e0t0d7ezj7zO0lWo9xgq8dJziYfeb207riI9I8OX72PnO0RZCjrfuG
530ZA08US/3omssuZGBOGlAVEcIICUIqEkbiS/Wwi3txEbs7d3OpmvRo0n02KIhW4ID2maN922duucfUPaJ7m+a5IcitlbBcloO8
2Wduo2Bl3ChYGfJSkINlwcp1iS5tnMOLvfGuBbn7us91jhwtBTn8dbPmeJ8LVvKXZM2tCXK4njRHuCbIpbAmyN3bQvAybxi+ctJc
Veuc3cNRiuZ+DDewlt3SCefEswxhYp9XTRl9og8ihcgpwJjLedkCHWTSHC1tAOHCBKSwsAC43Ghy8aa2TiJzTZ16530m0a4CYVb/
9vnE+ggtQB6Xi+o1GMCI5M+8TTcWq7OuysG+ctKcP96QS+oxaJKACmjDXVlpOixiC01KxgyDJdZEjUtq0Tub5t7q1ip+/aQ5CseV
b8ekucNYEp8eU0ll60q2vC/4LcN4ktK5yX3yn1SdIEObteHH4DbrWoCbFHQqjQLOnXsuNbIm1iAKu6Iao866bL302DMmIBtxbnfk
9JqHCubgvD7NbWTmLjI06+yWShFEm6pW0mMm3dOj+Ghwv7LBPWbSfb2dj3DP8j4pWOiIGDRAitmbnGVWS1PQFHppFv26be7EKakn
8YNaE5oTy8uqa7vQSs7eijn971kxWVH3M/sM/DXDFGNiVM0srcTpA5iFaWXbLF8OCVs7Js09sW19jEi35wyhE0MPUH3ad9C04Z+b
NYnicCbOUynTMsZIyqHkGEXn3rKgvUiV1ndB2MdGFq1zp8Uesrbig8AtvDcTYCYo5YGcUkakIHUAuDPD7Mxjdt9xzcekuacEcMGH
pdnvWdJcwuEgwiHgTXbWQQV05liqllRaDsMcvWOmuVnvtWSeW34awlz0QzsrXAMROpMdwLlRbZwN6pRUfBi4dWehNhzzfo8jZR80
uStVc3pSQlA39XhMmjsy2WPS3P/fpDmEhwOWtu0pR7hFo0thC5FA2FbZcm8y8p8ovPrR/AQYJP5FhiTOfSPGLtGZL86xxDEYRTfk
CQskqCkU9NPM0FSBtfZ0TJp7vEa3TJiJgTY2ldssa5d3a3SBlxodpKVGhxuVLUNeanT3KlLeJM1taHSRlhrdvbS+6+V0965+o9HF
X1uj+7pJc9/8/Zv/BeqcivU=
"""


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def exact_rows() -> list[dict[str, Any]]:
    raw = base64.b64decode("".join(RANKFREE_RULE_RESULTS_ZLIB_B64.split()))
    return json.loads(zlib.decompress(raw).decode())


def source_profiles(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["source_key"]: row
        for row in source["matrix_profiles"]
        if row["classification"] == PATTERN_CLASS
    }


def aggregate_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        value = str(item[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def add_counts(dst: dict[str, int], src: dict[str, int]) -> None:
    for key, value in src.items():
        dst[key] = dst.get(key, 0) + int(value)


def aggregate_pairs(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        add_counts(out, row["pivot_pair_counts"])
    return dict(sorted(out.items()))


def aggregate_rule_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_rule = {
        rule: {"tested": 0, "success": 0, "failed": 0}
        for rule in EXPECTED_RULES
    }
    by_class: dict[str, dict[str, int]] = {}
    total = 0
    success = 0
    best_failed = [-1, 1]
    best_failed_detail = None
    for row in rows:
        ncols = row["matrix_shape"][1]
        for attempt in row["rankfree_rule_attempts"]:
            total += 1
            rule = attempt["rule"]
            rule_class = attempt["rule_class"]
            assert rule in by_rule
            by_rule[rule]["tested"] += 1
            by_class.setdefault(rule_class, {"tested": 0, "success": 0, "failed": 0})
            by_class[rule_class]["tested"] += 1
            if attempt["minor_nonzero"]:
                success += 1
                by_rule[rule]["success"] += 1
                by_class[rule_class]["success"] += 1
            else:
                by_rule[rule]["failed"] += 1
                by_class[rule_class]["failed"] += 1
                if attempt["minor_rank"] * best_failed[1] > best_failed[0] * ncols:
                    best_failed = [attempt["minor_rank"], ncols]
                    best_failed_detail = {
                        "candidate_id": row["candidate_id"],
                        "rule": rule,
                        "minor_rank": attempt["minor_rank"],
                        "selected_minor_size": ncols,
                    }
    return {
        "rules_tested": len(EXPECTED_RULES),
        "rule_names": EXPECTED_RULES,
        "rank_free_attempts": total,
        "rank_free_successes": success,
        "rank_free_failures": total - success,
        "success_by_rule": dict(sorted(by_rule.items())),
        "success_by_rule_class": dict(sorted(by_class.items())),
        "best_failed_minor_rank_ratio": best_failed,
        "best_failed_minor": best_failed_detail,
        "status": "RREF_DERIVED_PATTERN_ONLY" if success == 0 else "CANDIDATE_THEOREM",
    }


def matrix_record(row: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    assert row["source_key"] == profile["source_key"]
    assert row["matrix_shape"] == profile["matrix_shape"]
    assert row["rank"] == profile["rank"]
    assert row["nullity"] == profile["nullity"] == 0
    assert row["pivot_pair_counts"] == profile["pivot_pattern"]["pair_pivot_counts"]
    matrix_cols = row["matrix_shape"][1]
    success_rules = [
        attempt["rule"]
        for attempt in row["rankfree_rule_attempts"]
        if attempt["minor_nonzero"]
    ]
    if success_rules:
        if any(
            attempt["minor_nonzero"]
            and attempt["rule_class"] == "DETERMINISTIC_COMBINATORIAL_RULE"
            for attempt in row["rankfree_rule_attempts"]
        ):
            best_status = "DETERMINISTIC_COMBINATORIAL_RULE"
        else:
            best_status = "RREF_MIMIC_RULE"
    else:
        best_status = "RREF_DERIVED_ONLY"
    return {
        "candidate_id": row["candidate_id"],
        "source_key": row["source_key"],
        "source_packet": row["source_packet"],
        "source_family": row["source_family"],
        "pattern_class": PATTERN_CLASS,
        "matrix_shape": row["matrix_shape"],
        "rank": row["rank"],
        "nullity": row["nullity"],
        "rref_certificate_status": "CERTIFIED",
        "rref_certificate": {
            "certificate_type": "RREF_PIVOT_MINOR",
            "minor_size": matrix_cols,
            "minor_rank_full": row["minor_rank_full"],
            "determinant_nonzero": row["determinant_nonzero"],
            "pivot_rows_hash": row["pivot_rows_hash"],
            "pivot_cols_hash": row["pivot_cols_hash"],
            "pivot_pairs_hash": row["pivot_pairs_hash"],
            "minor_hash": row["minor_hash"],
            "row_type_counts": row["pivot_row_type_counts"],
            "pair_pivot_counts": row["pivot_pair_counts"],
            "status": "CERTIFIED_FULL_RANK",
        },
        "rankfree_rules": row["rankfree_rule_attempts"],
        "rankfree_rule_successes": success_rules,
        "best_rule_status": best_status,
        "compressed_dimensions_by_witness": row["compressed_dimensions_by_witness"],
        "remaining_equations_by_pair": row["remaining_equations_by_pair"],
        "route_cut_status": "ROUTE_CUT_CERTIFIED_CANDIDATE",
    }


def build_result(source: dict[str, Any]) -> dict[str, Any]:
    assert threshold_floor() == 6
    profiles = source_profiles(source)
    rows = exact_rows()
    rows.sort(key=lambda item: item["source_key"])
    assert len(rows) == len(profiles) == 6
    matrices = [matrix_record(row, profiles[row["source_key"]]) for row in rows]
    rule_summary = aggregate_rule_summary(rows)
    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "denominator": "17^32",
        "field_denominator": str(FIELD_DENOMINATOR),
        "agreement": TARGET_AGREEMENT,
        "agreement_target": TARGET_AGREEMENT,
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "pattern_class": PATTERN_CLASS,
        "construction_mode": "generic_pairwise_rankfree_pivot_rule",
        "source_profile": {
            "path": str(SOURCE_DATA),
            "record_hash": source["record_hash"],
            "source_matrices": source["profile_summary"]["source_matrices"],
            "generic_pairwise_profiles": len(matrices),
            "status": source["global_status"]["status"],
        },
        "matrix_count": len(matrices),
        "source_family_counts": aggregate_by(matrices, "source_family"),
        "source_packet_counts": aggregate_by(matrices, "source_packet"),
        "aggregate_pair_pivot_counts": aggregate_pairs(rows),
        "rule_summary": rule_summary,
        "rref_derived_certificates_replayed": len(matrices),
        "rank_free_successes": rule_summary["rank_free_successes"],
        "matrices": matrices,
        "theorem_assessment": {
            "target_statement": (
                "For the generic_pairwise_rref_pivot class, a metadata-only "
                "row schedule selects a full column-rank minor over GF(17^32)."
            ),
            "rankfree_rules_tested": EXPECTED_RULES,
            "rankfree_rule_attempts": rule_summary["rank_free_attempts"],
            "rankfree_rule_successes": rule_summary["rank_free_successes"],
            "deterministic_schedule_proved": False,
            "reason_not_proved": (
                "All tested generic-pairwise metadata rules selected singular "
                "minors; the full-rank certificates remain RREF-derived."
            ),
            "status": rule_summary["status"],
        },
        "interpretation": {
            "a327_certificate_found": False,
            "candidate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "generic_pairwise_candidates_certified_full_rank": True,
            "rankfree_rule_found": rule_summary["rank_free_successes"] > 0,
            "deterministic_pivot_schedule_theorem_proved": False,
            "status": "AUDIT",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_generic_pairwise_rankfree_pivot_rule.sage",
            "checks_GF_17_32": True,
            "reconstructs_6_generic_pairwise_matrices": True,
            "replays_rref_derived_pivot_certificates": True,
            "tests_rankfree_rule_minors": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": REQUIRED_NONCLAIMS,
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": rule_summary["status"],
        },
        "status": "M1_GENERIC_PAIRWISE_RANKFREE_PIVOT_RULE_AUDIT",
    }
    result["record_hash"] = hash_payload(
        {
            "source_profile": result["source_profile"],
            "rule_summary": result["rule_summary"],
            "matrices": result["matrices"],
            "theorem_assessment": result["theorem_assessment"],
            "interpretation": result["interpretation"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE_DATA, type=Path)
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_result(load_json(args.source))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output, result)
        print(f"WROTE {args.output}")
        print(f"generic-pairwise matrices: {result['matrix_count']}")
        print(f"rank-free attempts: {result['rule_summary']['rank_free_attempts']}")
        print(f"rank-free successes: {result['rank_free_successes']}")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
