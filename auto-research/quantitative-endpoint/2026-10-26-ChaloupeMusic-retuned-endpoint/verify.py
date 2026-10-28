#!/usr/bin/env python3
"""Checks for the retuned endpoint bound (PROOF.md). Not a formal proof.

Base: the composed endpoint (2026-10-20-ChaloupeMusic-composed-endpoint, head ebfae63) and the template
limit (2026-10-26-ChaloupeMusic-template-limit). Standard library only, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0 and standard output byte-identical to RESULT.json. Assertions are load-bearing; never -O.

1. Monomial certificates A t^j e^{-dt} <= B for every real t >= 256 (sign of j - dt; value at 256 with
   e >= 2); bounds with sqrt(t) are squared first. One list per Lemma A tier.
2. Exact budgets for every inequality of PROOF.md, with certified rational bounds for logarithms, for each
   of the six tiers (Lemma A: Erdos or Rosser-Schoenfeld; class product: D'', D', D).
3. Each delivered C against the template floor C* of the template-limit package, recomputed here.
4. Negative controls that feed each decisive change back into budgets(), a 90-digit decimal replay on a
   grid of t from 256, and file integrity.
"""
import hashlib
import json
import math
import sys
from decimal import Decimal as Dec, getcontext, MAX_EMAX, MIN_EMIN, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
T0 = 256                                        # k >= 2^370 gives t >= 256
N0 = 370
AS = 4096                                       # Ms = AS D t, delta_s = 1/16 (unchanged)
E2 = Q(1, 64)                                   # eps_reg = E2/t, eta = eps_reg/(24 D)
G = 2 + E2 / 2                                  # gamma = 1/2 - G/t
RHO = Q(1, 2 ** 100)                            # rho = 1/u <= 2^-100, so D >= u >= 2^100
RS = Q(101624, 100000)                          # Rosser-Schoenfeld (1962), (3.16): theta(x) < 1.01624 x, x > 0
# Lemma A tiers: u = sqrt(k)/(AD t^{5/2}), h0 = ceil(BH D t^3), p = AP t^{7/2}/sqrt(k), log lambda < LA (...)
LEMMA_A = {
    "RS": {"label": "Rosser-Schoenfeld: theta(x) < 1.01624 x", "AD": Q(73, 4), "BH": Q(91, 20), "AP": Q(59, 2)},
    "E": {"label": "Erdos: theta(x) < x log 4", "AD": Q(85, 4), "BH": Q(227, 50), "AP": Q(69, 2)},
}
CLASSES = {"D2": ("Lemma D'': 45^(k/2)", 45, Q(1, 2)), "D1": ("Lemma D': 19^k", 19, Q(1)),
           "D0": ("N1a's Lemma D: 37^k", 37, Q(1))}
# F = k (t/8 - (7/8) log t - C); n9: c = 1/9 from 2^n9
TIERS = [
    {"name": "RS-D2", "A": "RS", "cls": "D2", "C": Q(173, 50), "n9": 950, "coeff1024": Q(1120, 10000)},
    {"name": "RS-D1", "A": "RS", "cls": "D1", "C": Q(199, 50), "n9": 1009, "coeff1024": Q(1112, 10000)},
    {"name": "RS-D0", "A": "RS", "cls": "D0", "C": Q(108, 25), "n9": 1048, "coeff1024": Q(1108, 10000)},
    {"name": "E-D2", "A": "E", "cls": "D2", "C": Q(7, 2), "n9": 954, "coeff1024": Q(1119, 10000)},
    {"name": "E-D1", "A": "E", "cls": "D1", "C": Q(201, 50), "n9": 1014, "coeff1024": Q(1112, 10000)},
    {"name": "E-D0", "A": "E", "cls": "D0", "C": Q(109, 25), "n9": 1053, "coeff1024": Q(1107, 10000)},
]
COMPOSED_C = {"D2": Q(71, 20), "D1": Q(403, 100), "D0": Q(35, 8)}


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def pow2(n):
    return Q(1 << n) if n >= 0 else Q(1, 1 << (-n))


def dec_floor(x, digits=6):
    n = math.floor(x * 10 ** digits)
    return f"{n // 10 ** digits}.{n % 10 ** digits:0{digits}d}" if n >= 0 else str(float(x))


def dec_ceil(x, digits=6):
    n = math.ceil(x * 10 ** digits)
    return f"{n // 10 ** digits}.{n % 10 ** digits:0{digits}d}"


# ---------------------------------------------------------------- logarithms
def ln2_bounds(N=60):
    s = sum(Q(1, n * 2 ** n) for n in range(1, N + 1))
    return s, s + Q(1, (N + 1) * 2 ** N)


def ln_bounds(y, N=60):
    y = Q(y)
    if y == 1:
        return Q(0), Q(0)
    z = (y - 1) / (y + 1)
    s = 2 * sum(z ** (2 * m + 1) / (2 * m + 1) for m in range(N))
    return s, s + 2 * z ** (2 * N + 1) / ((2 * N + 1) * (1 - z * z))


def _split(y):
    y = Q(y)
    e = math.floor(math.log2(y.numerator) - math.log2(y.denominator))
    while pow2(e) > y:
        e -= 1
    while pow2(e + 1) <= y:
        e += 1
    return e, y / pow2(e)


def ln_up(y):
    """Upper bound for log y, y >= 1 rational."""
    e, m = _split(y)
    return e * ln2_bounds()[1] + ln_bounds(m)[1]


def ln_lo(y):
    e, m = _split(y)
    return e * ln2_bounds()[0] + ln_bounds(m)[0]


def lemma_a_constant(name):
    return RS if name == "RS" else ln_up(4)


# ---------------------------------------------------------------- 1. monomials
def monomial(name, A, j, d, B, t0=T0):
    A, d, B = Q(A), Q(d), Q(B)
    require(A >= 0 and d > 0 and B > 0, f"{name}: bad parameters")
    require(j <= 0 or d * t0 - j >= 0, f"{name}: not monotone from t0")
    bound = A * Q(t0) ** j * pow2(-math.floor(d * t0))
    require(bound <= B, f"{name}: endpoint bound fails")
    return {"name": name, "A": str(A), "j": j, "d": str(d), "B": str(B), "t0": t0,
            "endpoint_upper": f"2^{-math.floor(d * t0)}*{A * Q(t0) ** j}"}


def monomials(a):
    P = LEMMA_A[a]
    AD, BH, AP = P["AD"], P["BH"], P["AP"]
    LA = lemma_a_constant(a)
    one = 1 + RHO
    specs = [
        ("u_at_least_2^100", (pow2(100) * AD) ** 2, 5, 1, 1),                   # also rho <= 2^-100
        ("u_above_4t", 16 * AD ** 2, 7, 1, 1),                                  # D >= u >= 4t
        ("M_at_least_k_over_33", 1056, 0, 1, 1),
        ("h0_plus_one_term", 1, -1, 1, (Q(1, 4) - BH * one / AD) ** 2),         # BH D t^3 + 1 <= sqrt(kt)/4
        ("h0_below_2M", Q(33, 8) ** 2, 1, 1, Q(1, 2)),
        ("Ms_below_k", (Q(AS + 2) / AD) ** 2, -3, 1, 1),
        ("p_at_most_half", 4 * AP * AP, 7, 1, 1),
        ("log_t_below_t_over_32", 1, 1, Q(1, 32), 1),
        ("mesh_leading", 2, 1, 3, Q(1, 2)),
        ("mesh_rounding", 2, 0, 3, Q(1, 2)),
        ("Q_over_k", (6 * AD / 8) ** 2, 7, 1, Q(1, 10 ** 4)),
        # first family small terms (units of 16 t^2/k), each <= 1/200
        ("F1_h0_plus_one", (64 * LA * one / AD) ** 2, -1, 1, Q(1, 200) ** 2),
        ("F1_cube_root", (128 * LA * one / (AD * Q(5, 2))) ** 2, 1, Q(1, 3), Q(1, 200) ** 2),
        ("F1_32Dt", (512 * one / AD) ** 2, 1, 1, Q(1, 200) ** 2),
        ("F1_2Dlog441", (32 * ln_up(441) * one / AD) ** 2, -1, 1, Q(1, 200) ** 2),
        ("F1_t3", 16, 3, 1, Q(1, 600)),
        ("F1_t2", 16 * ln_up(96) + 2, 2, 1, Q(1, 600)),
        ("F1_const", 32, 0, 1, Q(1, 600)),
        # rich: (5Q + D(23.25t + 10.81) + 16.5t + 18.1)/k, each term <= 1/1000
        ("rich_5Q", (5 * AD / 8) ** 2, 7, 1, Q(1, 1000) ** 2),
        ("rich_15t", 15, 1, 1, Q(1, 1000)),
        ("rich_D", ((Q(2325, 100) + Q(1081, 100 * T0)) * one / AD) ** 2, -3, 1, Q(1, 1000) ** 2),
        ("rich_lin", Q(165, 10) + Q(181, 10 * T0), 1, 1, Q(1, 1000)),
        # case (i): (log T_K + log 16)/k small; case (ii) residual terms
        ("caseI_6Q", (6 * AD / 8) ** 2, 7, 1, Q(1, 100) ** 2),
        ("caseI_lin", Q(225, 10) + 9, 1, 1, Q(1, 100)),
        ("caseI_D", (17 * one / AD) ** 2, -3, 1, Q(1, 100) ** 2),
        ("caseII_lin", (Q(245, 10) + Q(9, T0)) ** 2, -5, 1, Q(1, 100) ** 2),
    ]
    return [monomial(*s) for s in specs]


# ---------------------------------------------------------------- 2. exact budgets
def budgets(P, tier):
    """Every budget of PROOF.md for the parameters P (AD, BH, AP, LA, E2, G, TAIL) and one tier."""
    AD, BH, AP, LA, E2_, G_, TAIL = (P[x] for x in ("AD", "BH", "AP", "LA", "E2", "G", "TAIL"))
    Cv = tier["C"]
    _, base, expo = CLASSES[tier["cls"]]
    L2lo, L2up = ln2_bounds()
    L9, LAP = ln_up(9), ln_up(AP)
    lt0_lo, lt0_up = ln_lo(T0), ln_up(T0)
    one = 1 + RHO
    r = {}
    # scales
    require(BH * one / AD < Q(1, 4), "h0 <= sqrt(kt)/4 coefficient")
    require(Q(9 * T0, 64) >= LAP, "L >= t/4")
    require(Q(17 * T0, 256) >= Cv, "F >= kt/32")
    require(math.ceil(24576 * T0 + 4) <= 24577 * T0, "B0 <= 24577 t")
    require(12 * E2_ / 24 + Q(3) / (BH * T0 ** 2) <= E2_, "short-block regularity budget")
    for tt in (Q(T0), Q(1000), Q(10 ** 6)):
        A0 = (Q(1, 2) - 1 / tt) * (1 - E2_ / tt)
        require(A0 - 1 / tt - (Q(1, 2) - G_ / tt) == E2_ / tt ** 2, "dichotomy identity")
    # first family: main terms + five small terms (<= 1/200 each) <= 1; sqrt(t) >= 16 for t >= 256
    require(16 ** 2 <= T0, "sqrt(t0) >= 16")
    f1 = 64 * BH * LA * (1 + 3 * RHO) / AD ** 2 + 16 * LA * one / (AD * 16) + Q(5, 200)
    require(f1 <= 1, "first-family budget")
    r["first_family_total_upper"] = dec_ceil(f1, 5)
    # second family: B0 D h0 + 1 <= cB k/t (h0 <= sqrt(kt)/4, B0 <= 24577 t, D <= (1+rho) u);
    # phi(h0) <= -D m(t) + t + log t with m(t) = (tail - 9/2) t + (7/2) log t - c2, nondecreasing;
    # m(t0) >= 1 and D >= u >= 4t give D m >= 4t >= 3t + log t + log 192 + 1/8
    cB = Q(24577) * one / (4 * AD) + Q(1, 100)
    tail = BH * TAIL
    c2 = 2 * L9 + 4 * ln_up(cB) + tail * E2_
    require(tail >= Q(9, 2), "second-family tail below its entropy")
    m0 = (tail - Q(9, 2)) * T0 + Q(7, 2) * lt0_lo - c2
    require(m0 >= 1, "second-family margin at t0")
    require(4 * T0 >= 3 * T0 + lt0_up + ln_up(192) + Q(1, 8), "4t covers the second-family right side")
    require(7 <= (1 - E2_ / T0) * tail * T0, "phi decreasing from h0")
    r["second_family_margin_at_t0_lower"] = dec_floor(m0, 3)
    # third family (unchanged): D((AS/128 - 37/2) t - (1/2) log t - 6.6) >= 2.5 t + (1/2) log t + log 96 + 1/8
    require(3 * L9 <= Q(66, 10) + Q(1, 1000), "third-family constant")
    a3 = Q(AS, 128) - Q(37, 2)
    require(a3 >= 3 and a3 * T0 - lt0_up / 2 - Q(66, 10) >= Q(5, 2) * T0 + lt0_up / 2 + ln_up(96) + Q(1, 8),
            "third-family budget")
    # rich: gamma L / 2 identity
    for T in (Q(1), Q(2), Q(5)):
        for A in (Q(0), Q(1)):
            for B in (Q(0), Q(1)):
                gamma = Q(1, 2) - G_ / T
                Lx = T / 2 - Q(7, 2) * A - B
                rhs = T / 8 - Q(7, 8) * A - B / 4 - G_ / 4 + Q(7, 4) * G_ * A / T + G_ / 2 * B / T
                require(gamma * Lx / 2 == rhs, "gamma L / 2 expansion")
    ec, ep = error_bounds()
    require(ec == {"Q": 6, "Dt": Q(51, 2), "t": 30} | {x: ec[x] for x in ("D", "1")}, "E_c coefficients")
    require(ep == {"Q": 4, "Dt": 17, "t": 2} | {x: ep[x] for x in ("D", "1")}, "E_p coefficients")
    require(ec["D"] <= Q(1193, 100) and ec["1"] <= Q(231, 10), "E_c constants above the stated bound")
    require(ep["D"] <= Q(829, 100) and ep["1"] <= Q(461, 100), "E_p constants above the stated bound")
    k_class = expo * ln_up(base)
    k_ebar = (L2up + k_class + ln_up(5)) / 2
    kappa = Cv - LAP / 4 - G_ / 4 - k_ebar
    require(kappa > 7 * Q(1, 1000), f"rich budget ({tier['name']})")
    cut = Cv - LAP / 4 - G_ / 4 - (L2up + k_class) / 2
    require(cut >= Q(8, 10), f"rich cut ({tier['name']})")
    r["kappa_lower"] = dec_floor(kappa)
    r["cut_margin_lower"] = dec_floor(cut, 4)
    # case (i): L/128 >= log 2 + 3/100; L/t = 1/2 - ((7/2) log t + log AP)/t increases for t >= 3
    l0 = Q(T0, 2) - Q(7, 2) * lt0_up - LAP
    require(l0 / 128 >= L2up + Q(3, 100), "case (i) budget")
    r["caseI_margin_lower"] = dec_floor(l0 / 128 - L2up - Q(3, 100), 4)
    # case (ii): log B_run <= 2t + brun sqrt(k) t^{-1/2}
    brun = Q(AS + 1) * one * (3 + Q(1, T0)) / AD
    caseII_D = 17 * one / (AD * Q(T0) ** 5)
    lhs = 6 * AD / 8 + brun / Q(T0) ** 4 + caseII_D + Q(1, 100)
    require(lhs < Q(15, 32) * AP, "case (ii) budget")
    r["caseII_ratio_upper"] = dec_ceil(lhs / (Q(15, 32) * AP), 5)
    require(Q(8, 64) + Q(1, 8) <= Q(1, 4) and ln_lo(64) >= ln_up(4), "Lemma C tail")
    require(N0 * L2lo >= T0 and (N0 - 1) * L2up < T0, "k >= 2^370 gives t >= 256, and 2^369 does not")
    return r


def error_bounds():
    """PR #9 Sections 7.3, 7.12, 8.2, 8.3, as in the composed endpoint (unchanged)."""
    L2 = ln2_bounds()[1]

    def form(**c):
        return {x: Q(c.get(x, 0)) for x in ("Q", "Dt", "D", "t", "1")}

    discrete = form(Dt=1 + 16, D=ln_up(9) + 2 * ln_up(7), t=1)
    factors_c = [discrete, form(Dt=Q(3, 2), D=ln_up(3)),
                 form(Q=6, t=6, **{"1": ln_up(16) + 3 * ln_up(3)}),
                 form(Dt=3, D=ln_up(6), t=1 + 9, **{"1": 2 * L2 + 3 * ln_up(6)}),
                 form(Dt=4, D=ln_up(19), t=1 + 12, **{"1": 2 * L2 + 3 * ln_up(19)})]
    factors_p = [discrete, form(Q=4, t=1, **{"1": ln_up(100)}), form(D=ln_up(9))]

    def total(fs):
        out = form()
        for f in fs:
            for x in out:
                out[x] += f[x]
        return out

    return total(factors_c), total(factors_p)


def thresholds(tier):
    L2lo, L2up = ln2_bounds()
    Cv, n9 = tier["C"], tier["n9"]
    t9 = n9 * L2lo
    g9 = t9 / 72 - Q(7, 8) * ln_up(t9) - Cv
    require(g9 > 0 and t9 > 63, "1/9 threshold")
    tm = (n9 - 1) * L2up
    require(tm / 72 - Q(7, 8) * ln_lo(tm) - Cv < 0, "1/9 threshold is not minimal in the exponent n")
    t1024 = 1024 * L2lo
    coeff = Q(1, 8) - (Q(7, 8) * ln_up(t1024) + Cv) / t1024
    require(coeff >= tier["coeff1024"], "coefficient at 2^1024")
    return {"one_ninth_from": {"k": f"2^{n9}", "margin_lower": dec_floor(g9)},
            "coefficient_at_2^1024_lower": dec_floor(coeff, 5)}


def params(a):
    P = dict(LEMMA_A[a])
    P.update({"LA": lemma_a_constant(a), "E2": E2, "G": G, "TAIL": Q(1)})
    return P


# ---------------------------------------------------------------- 3. the template floor
def cstar(cls):
    """C* = (1/2)(log 10 + l_cls) + 1/2 + (1/4)(log 18 + (1/2) log 2) (template-limit, Theorem B)."""
    _, base, expo = CLASSES[cls]
    lo = (ln_lo(10) + expo * ln_lo(base)) / 2 + Q(1, 2) + (ln_lo(18) + ln2_bounds()[0] / 2) / 4
    up = (ln_up(10) + expo * ln_up(base)) / 2 + Q(1, 2) + (ln_up(18) + ln2_bounds()[1] / 2) / 4
    return lo, up


def floor_check(tier):
    lo, up = cstar(tier["cls"])
    require(tier["C"] > up, "delivered C below the template floor")
    require(tier["C"] < COMPOSED_C[tier["cls"]], "no gain over the composed endpoint")
    return {"C_star_upper": dec_ceil(up, 5), "gap_to_floor_lower": dec_floor(tier["C"] - up, 4),
            "gain_over_composed": str(COMPOSED_C[tier["cls"]] - tier["C"])}


# ---------------------------------------------------------------- 4. controls, replay, integrity
def negative_controls():
    by = {t["name"]: t for t in TIERS}

    def fails(a, p_over, tier_name, tier_over=None):
        P = dict(params(a), **p_over)
        tier = dict(by[tier_name], **(tier_over or {}))
        try:
            budgets(P, tier)
        except AssertionError:
            return True
        return False

    rej = {
        "RS_AD_18": fails("RS", {"AD": Q(18)}, "RS-D2"),
        "RS_BH_4.53": fails("RS", {"BH": Q(453, 100)}, "RS-D2"),
        "RS_AP_29": fails("RS", {"AP": Q(29)}, "RS-D2"),
        "RS_C_3.45": fails("RS", {}, "RS-D2", {"C": Q(69, 20)}),
        "RS_params_with_log4": fails("RS", {"LA": ln_up(4)}, "RS-D2"),
        "E_AD_21": fails("E", {"AD": Q(21)}, "E-D2"),
        "E_C_3.49": fails("E", {}, "E-D2", {"C": Q(349, 100)}),
        "RS_C_3.97_under_D1": fails("RS", {}, "RS-D1", {"C": Q(397, 100)}),
        "E_C_4.35_under_D0": fails("E", {}, "E-D0", {"C": Q(435, 100)}),
        "G_2": fails("RS", {"G": Q(2)}, "RS-D2"),
    }
    require(all(not fails(t["A"], {}, t["name"]) for t in TIERS), "delivered constants fail")
    for a in LEMMA_A:
        try:
            monomial("control", (pow2(100) * LEMMA_A[a]["AD"]) ** 2, 5, 1, 1, t0=200)
            rej[f"monomial_t0_200_{a}"] = False
        except AssertionError:
            rej[f"monomial_t0_200_{a}"] = True
    try:
        floor_check(dict(TIERS[0], C=Q(341, 100)))
        rej["C_below_floor"] = False
    except AssertionError:
        rej["C_below_floor"] = True
    require(all(rej.values()), f"negative control not rejected: {rej}")
    return rej


def decimal_replay():
    getcontext().prec = 90
    getcontext().Emax = MAX_EMAX
    getcontext().Emin = MIN_EMIN
    ONE = Dec(1)
    TOL = ONE - Dec(10) ** -60
    LN2, LN5, LN9 = (Dec(x).ln() for x in (2, 5, 9))

    def ceil(x):
        return x.to_integral_value(rounding=ROUND_CEILING)

    def floor(x):
        return x.to_integral_value(rounding=ROUND_FLOOR)

    def dq(x):
        return Dec(x.numerator) / Dec(x.denominator)

    fails, checks, grid = 0, 0, list(range(256, 520, 11)) + list(range(520, 2001, 37)) + [5000, 10 ** 4, 10 ** 5]
    for tt in grid:
        for tier in TIERS:
            P = params(tier["A"])
            AD, BH, AP, LA = (dq(P[x]) for x in ("AD", "BH", "AP", "LA"))
            _, base, expo = CLASSES[tier["cls"]]
            Cv = dq(tier["C"])
            t = Dec(tt); k = t.exp(); lt = t.ln()
            u = (t / 2).exp() / (AD * t ** Dec("2.5")); D = ceil(u); M = floor(k / 32)
            h0, Ms = ceil(BH * D * t ** 3), ceil(AS * D * t)
            eps_reg = dq(E2) / t; eta = eps_reg / (24 * D); B0 = ceil(24576 * t + 4)
            gamma = ONE / 2 - dq(G) / t
            logp = AP.ln() + Dec("3.5") * lt - t / 2; p = logp.exp(); L = -logp
            F = k * (t / 8 - Dec("0.875") * lt - Cv)
            logP = LN2 + 2 * t; Qh = F / D + logP
            A0 = (ONE / 2 - ONE / t) * (1 - eps_reg)
            Lam = LA * (h0 + (2 * M).sqrt() + 2 * t * (2 * M) ** (ONE / 3))
            logTglob = 4 * D * Lam + 32 * D * t + 2 * D * Dec(441).ln()
            phi = (D + 2) * h0.ln() + 2 * D * LN9 + 4 * D * (B0 * D * h0 + 1).ln() - (1 - eps_reg) * h0 / t ** 2
            logAs = t + (D + 1) * h0.ln() + D * (LN9 + 2 * (k * (4 * M + 4) + 1).ln()) + D * (LN9 + 2 * (3 * k ** 7).ln())
            Gamma = gamma * k * L / 2 - (F + D * logP)
            Ec = 6 * Qh + k * (LN2 + dq(expo) * Dec(base).ln() + LN5 / 2) + D * (Dec("25.5") * t + Dec("11.93")) + 30 * t + Dec("23.1")
            Ep = 4 * Qh + k * LN5 / 2 + D * (17 * t + Dec("8.29")) + 2 * t + Dec("4.61")
            logTK = 6 * Qh + D * (16 * t + 5) + Dec("4.5") * t + 6
            logBrun = h0.ln() + (Ms + 1).ln() + Ms * (LN2 + 3 * t)
            c = [u >= 2 ** 100, p <= ONE / 2, L >= t / 4, h0 < 2 * M, 2 * M / k * TOL <= ONE / 16,
                 4 * M / k ** 3 <= eta, D * (12 * eta + 3 / h0) <= eps_reg, A0 - ONE / t > gamma,
                 h0 <= (k * t).sqrt() / 4,
                 logTglob + Dec(96).ln() + ONE / 8 + t <= 2 * M / t ** 2,
                 phi <= -2 * t - Dec(192).ln() - ONE / 8,
                 logAs + Dec(96).ln() + ONE / 8 + t <= Ms / 128,
                 Gamma - (Ec + Ep) / 2 >= Dec(64).ln() + t / 2, Gamma > (Ec - Ep) / 2,
                 Dec(16).ln() + logTK + k * LN2 <= k * L / 128,
                 logTK + logBrun + Dec(16).ln() <= Dec(15) / 32 * p * k]
            checks += len(c)
            fails += sum(1 for ok in c if not ok)
    require(fails == 0, "decimal replay found a failing inequality")
    return {"t_values": len(grid), "tiers": len(TIERS), "checks": checks, "failures": fails}


def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(name for name in manifest if name != "RESULT.json")


def main():
    report = {
        "base": {"composed_head": "ebfae63", "template_limit": "2026-10-26-ChaloupeMusic-template-limit",
                 "pr12_head": "029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5"},
        "parameters": {a: {"lemma_A": P["label"], "u": f"sqrt(k)/({P['AD']} t^(5/2))", "h0": f"ceil({P['BH']} D t^3)",
                           "p": f"{P['AP']} t^(7/2)/sqrt(k)"} for a, P in LEMMA_A.items()}
                      | {"common": {"M": "floor(k/32)", "Ms": f"ceil({AS} D t)", "eps_reg": f"{E2}/t",
                                    "delta_s": "1/16", "gamma": f"1/2 - ({G})/t", "t0": T0, "k_from": f"2^{N0}"}},
        "monomial_certificates": {a: monomials(a) for a in LEMMA_A},
        "tiers": {t["name"]: {"lemma_A": LEMMA_A[t["A"]]["label"], "class_product": CLASSES[t["cls"]][0],
                              "C": str(t["C"]), "budgets": budgets(params(t["A"]), t),
                              "thresholds": thresholds(t), "template_floor": floor_check(t)} for t in TIERS},
        "negative_controls_rejected": negative_controls(),
        "decimal_replay": decimal_replay(),
        "integrity_files": integrity(),
        "conclusion": "W_r(k) > (k^(1/8) / (e^C (log k)^(7/8)))^(k floor(log2 r)) for k >= 2^370, with C = 173/50 "
                      "(Rosser-Schoenfeld, D''; c = 1/9 from 2^950) or C = 7/2 (Erdos, D''; from 2^954); "
                      "D' and D tiers in RESULT; conditional on the interfaces of PR #12, Section 2, and PR #9's "
                      "displayed factors",
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(text)
    stored = HERE / "RESULT.json"
    if "--write" in sys.argv:
        stored.write_text(text)
    else:
        require(stored.read_text() == text, "output differs from RESULT.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
