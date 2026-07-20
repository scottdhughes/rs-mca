"""Independent exact controls for the carrier-incidence splice.

This Sage companion checks the load-bearing deployed endpoints and constructs
sharp finite-field moving-zero pencils for both signs of x.  It is not a
deployed selector census and does not replace the symbolic proof.
"""

import json


SCHEMA = "rs-mca-m1-kb-rank9-full-outside-carrier-incidence-splice-v1-sage"
SCALE = "EXACT_ENDPOINT_AND_TOY_CONTROL_NOT_DEPLOYED_SELECTOR_OR_PROOF"

N = 2_097_152
J = 981_104
T = 67_472
D = 18_014
B_REMAINING = 274_980_305_756_664_755
CORE_RANK = 8
SELECTOR_RANK = 9
C0 = binomial(T + CORE_RANK, CORE_RANK)
MU0 = ceil(C0 / 9)
MUH = ceil(binomial(T + CORE_RANK + D + 1, CORE_RANK) / 9)
GAIN = MUH - MU0


class ContractError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def ceil_div(a, b):
    require(b > 0, "ceil_div denominator")
    return -((-a) // b)


def source_size(r):
    return T + r + 1


def carrier(r):
    return N - source_size(r)


def x_floor(r):
    return ceil(source_size(r) / 2) - r


def line_cap(r):
    x0 = x_floor(r)
    return 1 + J // x0 if x0 >= 1 else J + 1


def coarse_cap(r):
    return binomial(carrier(r), SELECTOR_RANK) // MU0


def tail(r):
    ambient = binomial(carrier(r), SELECTOR_RANK)
    require(ambient // MU0 > B_REMAINING, "tail called on coarse-paid row")
    needed = ambient + 1 - (B_REMAINING + 1) * MU0
    required_high = max(0, ceil_div(needed, GAIN))
    return B_REMAINING + 1 - required_high


def h_cap(r):
    return line_cap(r) * binomial(carrier(r), CORE_RANK) // C0


def max_count(r, low):
    ambient = binomial(carrier(r), SELECTOR_RANK)
    cheap = min(low, ambient // MU0)
    return cheap + (ambient - cheap * MU0) // MUH


require(
    C0 == 10_658_592_438_443_717_273_371_372_062_592_575,
    "C0 drift",
)
require(
    MU0 == 1_184_288_048_715_968_585_930_152_451_399_175,
    "mu0 drift",
)
require(
    MUH == 7_863_582_775_712_820_188_422_356_536_857_430,
    "mu high drift",
)
require(J - T - 1 == 913_631, "source slack maximum drift")


expected = {
    196: (67_669, 2_029_483, 33_639, 30,
          82_763_872_360_106_809, 20_089_920_852_688),
    67_466: (134_939, 1_962_213, 4, 245_277,
             145_820_857_871_608_193, 125_429_426_992_548_046),
    67_467: (134_940, 1_962_212, 3, 327_035,
             145_821_673_909_059_329, 167_238_042_774_200_802),
    236_097: (303_570, 1_793_582, -84_312, 981_105,
              244_488_250_573_176_944, 244_488_380_605_515_372),
    236_098: (303_571, 1_793_581, -84_312, 981_105,
              244_488_648_231_472_350, 244_487_290_102_240_448),
    330_335: (397_808, 1_699_344, -131_431, 981_105,
              274_980_243_816_664_215, 158_759_006_821_237_606),
}

endpoint_rows = []
for r, values in expected.items():
    actual = (
        source_size(r),
        carrier(r),
        x_floor(r),
        line_cap(r),
        tail(r),
        h_cap(r),
    )
    require(actual == values, "endpoint drift at r=%s" % r)
    require(max_count(r, tail(r)) == B_REMAINING, "Tstar sharpness drift")
    require(max_count(r, tail(r) + 1) == B_REMAINING + 1, "Tstar+1 sharpness drift")
    endpoint_rows.append(
        {
            "r": int(r),
            "tail": str(tail(r)),
            "H_cap": str(h_cap(r)),
            "margin": str(tail(r) - h_cap(r)),
        }
    )

require(tail(67_466) >= h_cap(67_466), "first paid endpoint failed")
require(tail(67_467) < h_cap(67_467), "first gap endpoint unexpectedly paid")
require(tail(236_097) < h_cap(236_097), "last gap endpoint unexpectedly paid")
require(tail(236_098) >= h_cap(236_098), "second paid endpoint failed")
require(coarse_cap(330_335) > B_REMAINING, "last one-cut row became coarse paid")
require(
    coarse_cap(330_336) == 274_979_198_751_652_213 <= B_REMAINING,
    "first coarse endpoint drift",
)
require(coarse_cap(913_631) == 6_250_452_705_118_696, "top coarse cap drift")


def packing_control(r):
    H = tail(r) + 1
    L = ceil_div(H, line_cap(r))
    used = L * C0
    available = binomial(carrier(r), CORE_RANK)
    chosen_x = x_floor(r) if x_floor(r) >= 1 else 1
    common_zero_size = carrier(r) - (J + chosen_x)
    local_capacity = binomial(common_zero_size, CORE_RANK)
    require(used <= available, "abstract packing capacity failed")
    require(local_capacity >= C0, "local common-zero basis capacity failed")
    require(r - (D + 1) > 195, "high-deficit scalar layer hits degree-195 owner")
    return {
        "r": int(r),
        "low_count": str(H),
        "line_count": str(L),
        "chosen_x": int(chosen_x),
        "common_zero_size": int(common_zero_size),
        "local_basis_capacity": str(local_capacity),
        "basis_margin": str(available - used),
    }


first_packing = packing_control(67_467)
last_packing = packing_control(236_097)
require(first_packing["line_count"] == "445890115459", "first packing line count")
require(last_packing["line_count"] == "249196824574", "last packing line count")


# Sharp positive-x moving-zero pencil: j=20, x=2, J=11.
F = GF(101)
j_toy = 20
x_positive = 2
positive_slopes = [F(i) for i in range(1, 12)]
positive_labels = [eta for eta in positive_slopes for _ in range(x_positive)]
a_positive = vector(F, [-eta for eta in positive_labels])
b_positive = vector(F, [1 for _ in positive_labels])
positive_deficits = []
positive_zero_sets = []
for eta in positive_slopes:
    word = a_positive + eta * b_positive
    zeros = tuple(i for i, value in enumerate(word) if value == 0)
    support = sum(1 for value in word if value != 0)
    positive_zero_sets.append(zeros)
    positive_deficits.append(j_toy - support)
require(len(a_positive) == j_toy + x_positive == 22, "positive W size")
require(all(len(zeros) == x_positive for zeros in positive_zero_sets), "positive zeros")
require(all(delta == 0 for delta in positive_deficits), "positive deficits")
require(len(set(positive_zero_sets)) == len(positive_zero_sets), "positive zero overlap")
require(
    len(positive_slopes) * x_positive + sum(positive_deficits)
    == j_toy + x_positive,
    "positive moving-zero equality",
)
require(len(positive_slopes) == 1 + j_toy // x_positive, "positive cap not sharp")


# Sharp negative-x branch: j=20, x=-2, delta=3, J=18.
x_negative = -2
negative_slopes = [F(i) for i in range(1, 19)]
a_negative = vector(F, [-eta for eta in negative_slopes])
b_negative = vector(F, [1 for _ in negative_slopes])
negative_deficits = []
negative_zero_sets = []
for eta in negative_slopes:
    word = a_negative + eta * b_negative
    zeros = tuple(i for i, value in enumerate(word) if value == 0)
    support = sum(1 for value in word if value != 0)
    negative_zero_sets.append(zeros)
    negative_deficits.append(j_toy - support)
require(len(a_negative) == j_toy + x_negative == 18, "negative W size")
require(all(len(zeros) == 1 for zeros in negative_zero_sets), "negative zeros")
require(all(delta == 3 for delta in negative_deficits), "negative deficits")
require(len(set(negative_zero_sets)) == len(negative_zero_sets), "negative zero overlap")
require(
    len(negative_slopes) * x_negative + sum(negative_deficits)
    == j_toy + x_negative,
    "negative moving-zero equality",
)
require(len(negative_slopes) == j_toy + x_negative, "negative cap not sharp")


print(
    json.dumps(
        {
            "schema": SCHEMA,
            "scale": SCALE,
            "endpoint_rows": endpoint_rows,
            "first_coarse_r": int(330_336),
            "top_slack_r": int(913_631),
            "first_gap_packing": first_packing,
            "last_gap_packing": last_packing,
            "positive_x_fixture": {
                "field": "GF(101)",
                "j": int(j_toy),
                "x": int(x_positive),
                "J": int(len(positive_slopes)),
                "moving_zero_equality": True,
            },
            "negative_x_fixture": {
                "field": "GF(101)",
                "j": int(j_toy),
                "x": int(x_negative),
                "delta": int(3),
                "J": int(len(negative_slopes)),
                "moving_zero_equality": True,
            },
            "deployed_selector_constructed": False,
            "koalabear_closed": False,
            "status": "PASS",
        },
        sort_keys=True,
    )
)
