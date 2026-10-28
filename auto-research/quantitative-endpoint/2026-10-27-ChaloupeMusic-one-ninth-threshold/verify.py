#!/usr/bin/env python3
"""Checks for "c = 1/9 from 2^940, and no template proof for e^256 <= k <= 2^934" (PROOF.md). Not a formal proof.

Base: the retuned endpoint (2026-10-26-ChaloupeMusic-retuned-endpoint, head 8916c20) and the template limit
(2026-10-26-ChaloupeMusic-template-limit). Standard library only, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0; standard output is RESULT.json followed by the line "Test passé". Assertions are load-bearing.

1. Monomial certificates A t^j e^{-dt} <= B for every real t >= T0 (T0 = floor(N0 log 2)).
2. Exact budgets of the retuned endpoint at the new constants and T0, except the rich inequality.
3. The rich inequality with F = kt/9, kept terms included, on a cover of [N0 log 2, oo) by intervals.
4. The smallest N0 for which 2 and 3 pass, per tier; N0 - 1 fails (this certificate goes no lower).
5. The floor: under (T1)-(T6) of template-limit, f >= t/9 is impossible for t in [256, n_low log 2]
   (plancher.py), and possible at (n_low + 1) log 2 for the bound used there.
6. Negative controls, a 90-digit decimal replay with F = kt/9, file integrity.
"""
import hashlib
import json
import math
import sys
from decimal import Decimal as Dec, getcontext, MAX_EMAX, MIN_EMIN, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from logs import L2_LO, L2_UP, ln_lo, ln_up, pow2           # noqa: E402
import plancher                                              # noqa: E402

AS = 4096                                       # Ms = AS D t, delta_s = 1/16 (unchanged)
E2 = Q(1, 64)                                   # eps_reg = E2/t (unchanged)
G = 2 + E2 / 2                                  # gamma = 1/2 - G/t (unchanged)
RHO = Q(1, 2 ** 100)                            # D >= u >= 2^100
RS = Q(101624, 100000)                          # Rosser-Schoenfeld (1962): theta(x) < 1.01624 x, x > 0
SMALL = Q(1, 10 ** 6)                           # each rich and case (ii) residual term, recertified at T0
T_SPAN = Q(64)                                  # beyond N0 log 2 + T_SPAN, the kept terms are not needed
# u = sqrt(k)/(AD t^{5/2}), h0 = ceil(BH D t^3), p = AP t^{7/2}/sqrt(k); F = kt/9
PARAMS = {"AD": Q(1805, 100), "BH": Q(451, 100), "AP": Q(2568, 100), "LA": RS, "E2": E2, "G": G}
CLASSES = {"D2": ("Lemma D'': 45^(k/2)", 45, Q(1, 2)), "D1": ("Lemma D': 19^k", 19, Q(1)),
           "D0": ("N1a's Lemma D: 37^k", 37, Q(1))}
TIERS = [{"cls": "D2", "N0": 940, "retuned": 950, "floor": 934},
         {"cls": "D1", "N0": 1000, "retuned": 1009, "floor": 994},
         {"cls": "D0", "N0": 1038, "retuned": 1048, "floor": 1032}]
N0_D2 = TIERS[0]["N0"]


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def dec_floor(x, digits=6):
    n = math.floor(x * 10 ** digits)
    s = "-" if n < 0 else ""
    n = abs(n)
    return f"{s}{n // 10 ** digits}.{n % 10 ** digits:0{digits}d}"


def dec_ceil(x, digits=6):
    return dec_floor(Q(math.ceil(x * 10 ** digits), 10 ** digits), digits)


def t0_of(n0):
    return math.floor(n0 * L2_LO)


# ---------------------------------------------------------------- 1. monomials
def monomial(name, A, j, d, B, t0):
    A, d, B = Q(A), Q(d), Q(B)
    require(A >= 0 and d > 0 and B > 0, f"{name}: bad parameters")
    require(j <= 0 or d * t0 - j >= 0, f"{name}: not monotone from t0")
    bound = A * Q(t0) ** j * pow2(-math.floor(d * t0))
    require(bound <= B, f"{name}: endpoint bound fails")
    return name


def monomials(P, t0):
    AD, BH, AP, LA = P["AD"], P["BH"], P["AP"], P["LA"]
    one = 1 + RHO
    specs = [
        ("u_at_least_2^100", (pow2(100) * AD) ** 2, 5, 1, 1),
        ("u_above_4t", 16 * AD ** 2, 7, 1, 1),
        ("M_at_least_k_over_33", 1056, 0, 1, 1),
        ("h0_plus_one_term", 1, -1, 1, (Q(1, 4) - BH * one / AD) ** 2),
        ("h0_below_2M", Q(33, 8) ** 2, 1, 1, Q(1, 2)),
        ("Ms_below_k", (Q(AS + 2) / AD) ** 2, -3, 1, 1),
        ("p_at_most_half", 4 * AP * AP, 7, 1, 1),
        ("log_t_below_t_over_32", 1, 1, Q(1, 32), 1),
        ("mesh_leading", 2, 1, 3, Q(1, 2)),
        ("mesh_rounding", 2, 0, 3, Q(1, 2)),
        ("Q_over_k", (6 * AD / 8) ** 2, 7, 1, Q(1, 10 ** 4)),
        ("F1_h0_plus_one", (64 * LA * one / AD) ** 2, -1, 1, Q(1, 200) ** 2),
        ("F1_cube_root", (128 * LA * one / (AD * Q(5, 2))) ** 2, 1, Q(1, 3), Q(1, 200) ** 2),
        ("F1_32Dt", (512 * one / AD) ** 2, 1, 1, Q(1, 200) ** 2),
        ("F1_2Dlog441", (32 * ln_up(441) * one / AD) ** 2, -1, 1, Q(1, 200) ** 2),
        ("F1_t3", 16, 3, 1, Q(1, 600)),
        ("F1_t2", 16 * ln_up(96) + 2, 2, 1, Q(1, 600)),
        ("F1_const", 32, 0, 1, Q(1, 600)),
        # rich: (5Q + D(23.25t + 10.81) + 16.5t + 18.1)/k, each term <= SMALL (was 1/1000)
        ("rich_5Q", (5 * AD / 8) ** 2, 7, 1, SMALL ** 2),
        ("rich_15t", 15, 1, 1, SMALL),
        ("rich_D", ((Q(2325, 100) + Q(1081, 100 * t0)) * one / AD) ** 2, -3, 1, SMALL ** 2),
        ("rich_lin", Q(165, 10) + Q(181, 10 * t0), 1, 1, SMALL),
        ("caseI_6Q", (6 * AD / 8) ** 2, 7, 1, Q(1, 100) ** 2),
        ("caseI_lin", Q(225, 10) + 9, 1, 1, Q(1, 100)),
        ("caseI_D", (17 * one / AD) ** 2, -3, 1, Q(1, 100) ** 2),
        ("caseII_lin", (Q(245, 10) + Q(9, t0)) ** 2, -5, 1, SMALL ** 2),     # was 1/100
    ]
    return [monomial(*s, t0=t0) for s in specs]


# ---------------------------------------------------------------- 2. budgets (all but rich)
def error_bounds():
    """PR #9 Sections 7.3, 7.12, 8.2, 8.3, as in the composed and retuned endpoints (unchanged)."""
    def form(**c):
        return {x: Q(c.get(x, 0)) for x in ("Q", "Dt", "D", "t", "1")}

    discrete = form(Dt=1 + 16, D=ln_up(9) + 2 * ln_up(7), t=1)
    fc = [discrete, form(Dt=Q(3, 2), D=ln_up(3)), form(Q=6, t=6, **{"1": ln_up(16) + 3 * ln_up(3)}),
          form(Dt=3, D=ln_up(6), t=1 + 9, **{"1": 2 * L2_UP + 3 * ln_up(6)}),
          form(Dt=4, D=ln_up(19), t=1 + 12, **{"1": 2 * L2_UP + 3 * ln_up(19)})]
    fp = [discrete, form(Q=4, t=1, **{"1": ln_up(100)}), form(D=ln_up(9))]

    def total(fs):
        out = form()
        for f in fs:
            for x in out:
                out[x] += f[x]
        return out
    return total(fc), total(fp)


def budgets(P, n0):
    AD, BH, AP, LA, E2_, G_ = (P[x] for x in ("AD", "BH", "AP", "LA", "E2", "G"))
    T0 = t0_of(n0)
    LAP, L9 = ln_up(AP), ln_up(9)
    lt0_lo, lt0_up = ln_lo(T0), ln_up(T0)
    one = 1 + RHO
    r = {"T0": T0}
    require(n0 * L2_LO >= T0, "k >= 2^N0 gives t >= T0")
    require(BH * one / AD < Q(1, 4), "h0 <= sqrt(kt)/4 coefficient")
    require(Q(9 * T0, 64) >= LAP, "L >= t/4")
    require(Q(1, 9) >= Q(1, 32), "F = kt/9 >= kt/32")
    require(math.ceil(24576 * T0 + 4) <= 24577 * T0, "B0 <= 24577 t")
    require(12 * E2_ / 24 + Q(3) / (BH * T0 ** 2) <= E2_, "short-block regularity budget")
    for tt in (Q(T0), Q(1000), Q(10 ** 6)):
        A0 = (Q(1, 2) - 1 / tt) * (1 - E2_ / tt)
        require(A0 - 1 / tt - (Q(1, 2) - G_ / tt) == E2_ / tt ** 2, "dichotomy identity")
    # first family; sqrt(t) >= 25 for t >= T0
    require(25 ** 2 <= T0, "sqrt(T0) >= 25")
    f1 = 64 * BH * LA * (1 + 3 * RHO) / AD ** 2 + 16 * LA * one / (AD * 25) + Q(5, 200)
    require(f1 <= 1, "first-family budget")
    r["first_family_total_upper"] = dec_ceil(f1, 5)
    # second family
    cB = Q(24577) * one / (4 * AD) + Q(1, 100)
    c2 = 2 * L9 + 4 * ln_up(cB) + BH * E2_
    require(BH >= Q(9, 2), "second-family tail below its entropy")
    m0 = (BH - Q(9, 2)) * T0 + Q(7, 2) * lt0_lo - c2
    require(m0 >= 1, "second-family margin at T0")
    require(4 * T0 >= 3 * T0 + lt0_up + ln_up(192) + Q(1, 8), "4t covers the second-family right side")
    require(7 <= (1 - E2_ / T0) * BH * T0, "phi decreasing from h0")
    r["second_family_margin_at_T0_lower"] = dec_floor(m0, 3)
    # third family (unchanged)
    require(3 * L9 <= Q(66, 10) + Q(1, 1000), "third-family constant")
    a3 = Q(AS, 128) - Q(37, 2)
    require(a3 * T0 - lt0_up / 2 - Q(66, 10) >= Q(5, 2) * T0 + lt0_up / 2 + ln_up(96) + Q(1, 8),
            "third-family budget")
    ec, ep = error_bounds()
    require(ec["Q"] == 6 and ec["Dt"] == Q(51, 2) and ec["t"] == 30, "E_c coefficients")
    require(ep["Q"] == 4 and ep["Dt"] == 17 and ep["t"] == 2, "E_p coefficients")
    require(ec["D"] <= Q(1193, 100) and ec["1"] <= Q(231, 10), "E_c constants")
    require(ep["D"] <= Q(829, 100) and ep["1"] <= Q(461, 100), "E_p constants")
    # case (i)
    l0 = Q(T0, 2) - Q(7, 2) * lt0_up - LAP
    require(l0 / 128 >= L2_UP + Q(3, 100), "case (i) budget")
    r["caseI_margin_lower"] = dec_floor(l0 / 128 - L2_UP - Q(3, 100), 4)
    # case (ii): log T_K <= 6 F/D + ..., and F/D = (kt/9)/u = (AD/9) sqrt(k) t^{7/2} (was AD/8 with F <= kt/8)
    brun = Q(AS + 1) * one * (3 + Q(1, T0)) / AD
    lhs = 6 * AD / 9 + brun / Q(T0) ** 4 + 17 * one / (AD * Q(T0) ** 5) + SMALL
    require(lhs < Q(15, 32) * AP, "case (ii) budget")
    r["caseII_ratio_upper"] = dec_ceil(lhs / (Q(15, 32) * AP), 6)
    require(Q(8, 64) + Q(1, 8) <= Q(1, 4) and ln_lo(64) >= ln_up(4), "Lemma C tail")
    r["monomials"] = len(monomials(P, T0))
    return r


# ---------------------------------------------------------------- 3. the rich inequality, F = kt/9
def k_ebar(cls):
    _, base, expo = CLASSES[cls]
    return (L2_UP + expo * ln_up(base) + ln_up(5)) / 2


def rich_interval(P, cls, a, b, keep=True):
    """Lower bound, for t in [a, b], of gamma L/2 - t/9 - kbar - S (S <= 4 SMALL).

    gamma L/2 - t/9 = h(t) - LAP/4 - G/4 + (7/4) G log t / t + (G/2) LAP / t, h(t) = t/72 - (7/8) log t,
    with h increasing (t > 63), log t / t decreasing (t > e), and LAP (G/(2t) - 1/4) decreasing in t (derivative
    -G LAP/(2t^2)) and in LAP: on [a, b], h at a and both t-dependent terms at b. keep = False drops the two kept terms, as the retuned endpoint does."""
    G_ = P["G"]
    LAP = ln_up(P["AP"])
    h = a / 72 - Q(7, 8) * ln_up(a)
    if b is None:                                   # [a, oo)
        kept = -LAP / 4
    elif keep:
        kept = Q(7, 4) * G_ * ln_lo(b) / b + LAP * (G_ / (2 * b) - Q(1, 4))
    else:
        kept = -LAP / 4
    return h + kept - G_ / 4 - k_ebar(cls) - 4 * SMALL


def rich_cover(P, cls, n0, keep=True):
    """Cover [n0 log 2, oo); every interval must have a positive lower bound. Returns (intervals, min)."""
    a = n0 * L2_LO
    t_big = a + T_SPAN
    require(a > 63, "h increasing")
    worst, n = None, 0
    while a < t_big:
        step = Q(8)
        while True:
            b = min(a + step, t_big)
            v = rich_interval(P, cls, a, b, keep)
            if v > 0:
                break
            step /= 2
            require(step >= Q(1, 2 ** 24), f"rich inequality fails near t = {float(a)} ({cls}, N0 = {n0})")
        worst = v if worst is None else min(worst, v)
        a, n = b, n + 1
    v = rich_interval(P, cls, t_big, None, keep)
    require(v > 0, "rich inequality beyond N0 log 2 + T_SPAN")
    # the second rich inequality, Gamma > (E_c - E_p)/2, has the same left side and loses log(5)/2 less
    require(ln_lo(5) / 2 > 4 * SMALL, "second rich inequality follows from the first")
    return n + 1, min(worst, v)


def threshold(P, tier):
    cls, n0 = tier["cls"], tier["N0"]
    b = budgets(P, n0)
    nint, worst = rich_cover(P, cls, n0)
    try:
        budgets(P, n0 - 1)
        rich_cover(P, cls, n0 - 1)
        lower_fails = False
    except AssertionError:
        lower_fails = True
    require(lower_fails, f"N0 - 1 also passes ({cls}): N0 is not the smallest for this certificate")
    require(n0 < tier["retuned"], "no gain over the retuned endpoint")
    return {"one_ninth_from": f"2^{n0}", "retuned_endpoint": f"2^{tier['retuned']}", "budgets": b,
            "rich_intervals": nint, "rich_margin_lower": dec_floor(worst, 7),
            "N0_minus_1_fails": lower_fails}


# ---------------------------------------------------------------- 5. the floor
def exp_neg_up(x, N=200):
    """Upper bound for e^{-x}, x > 0 rational: e^x >= sum_{n <= N} x^n/n!."""
    x, term, s = Q(x), Q(1), Q(1)
    for n in range(1, N + 1):
        term = term * x / n
        s += term
    return 1 / s


def delta_check():
    """m_0 of Broadbent et al., Theorem 1 (k = 0), at X_0 = e^45, with eps(45) of Table 8 (valid for all
    x >= e^45 by their Theorem 2), is below 1.1084e-8 < delta = 2e-8 (plancher.DELTA)."""
    eps45 = Q(109073, 10 ** 13)
    m0 = eps45 + Q(103883, 10 ** 5) * (exp_neg_up(Q(45, 2)) + exp_neg_up(30) + exp_neg_up(36))
    require(m0 < Q(11084, 10 ** 12) < plancher.DELTA, "m_0 at X_0 = e^45 not below delta")
    return {"m0_upper": f"{float(m0):.6e}", "delta": str(plancher.DELTA)}


def floor_check(tier):
    cls, nl = tier["cls"], tier["floor"]
    n = plancher.floor_cover(256, nl * L2_UP, cls)
    m_in = plancher.margin_at(nl * L2_LO, cls)
    m_out = plancher.margin_at((nl + 1) * L2_LO, cls)
    require(m_in < 0 and m_out > 0, f"floor is not at 2^{nl} ({cls})")
    require(nl < tier["N0"], "floor above the proved threshold")
    return {"no_template_proof_for_k_in": f"[e^256, 2^{nl}]", "intervals": n,
            "margin_at_2^floor_upper": dec_ceil(m_in, 5), "margin_at_2^(floor+1)": dec_floor(m_out, 5),
            "gap_proved_minus_floor": tier["N0"] - nl}


# ---------------------------------------------------------------- 6. controls, replay, integrity
def negative_controls():
    d2 = TIERS[0]

    def fails(f):
        try:
            f()
        except AssertionError:
            return True
        return False

    rej = {
        "AD_18.03_h0_constraint": fails(lambda: budgets(dict(PARAMS, AD=Q(1803, 100)), N0_D2)),
        "BH_4.505_second_family": fails(lambda: budgets(dict(PARAMS, BH=Q(4505, 1000)), N0_D2)),
        "AP_25.66_case_ii": fails(lambda: budgets(dict(PARAMS, AP=Q(2566, 100)), N0_D2)),
        "N0_minus_1_rich": fails(lambda: rich_cover(PARAMS, "D2", N0_D2 - 1)),
        "kept_terms_dropped_at_N0": fails(lambda: rich_cover(PARAMS, "D2", N0_D2, keep=False)),
        "case_ii_with_F_at_most_kt_over_8": fails(lambda: budgets_case_ii_eighth()),
        "class_D1_at_N0": fails(lambda: rich_cover(PARAMS, "D1", N0_D2)),
        "G_2.1": fails(lambda: rich_cover(dict(PARAMS, G=Q(21, 10)), "D2", N0_D2)),
        "floor_at_935": fails(lambda: plancher.floor_cover(900 * L2_LO, 935 * L2_UP, "D2")),
    }
    require(not fails(lambda: threshold(PARAMS, d2)), "delivered constants fail")
    bad = {k: v for k, v in rej.items() if not v}
    require(not bad, f"negative control not rejected: {bad}")
    return rej


def budgets_case_ii_eighth():
    """Control: the case (ii) budget with the retuned endpoint's 6 AD/8 (F <= kt/8) fails at AP = 25.68."""
    AD, AP, T0 = PARAMS["AD"], PARAMS["AP"], t0_of(N0_D2)
    brun = Q(AS + 1) * (1 + RHO) * (3 + Q(1, T0)) / AD
    lhs = 6 * AD / 8 + brun / Q(T0) ** 4 + 17 * (1 + RHO) / (AD * Q(T0) ** 5) + SMALL
    require(lhs < Q(15, 32) * AP, "case (ii) budget with 6 AD/8")


def decimal_replay():
    """The retuned endpoint's 16 inequalities, with F = kt/9, on a grid of t from N0 log 2 (D'' tier)."""
    getcontext().prec = 90
    getcontext().Emax = MAX_EMAX
    getcontext().Emin = MIN_EMIN
    ONE = Dec(1)
    TOL = ONE - Dec(10) ** -60
    LN2, LN5, LN9 = (Dec(x).ln() for x in (2, 5, 9))

    def dq(x):
        return Dec(x.numerator) / Dec(x.denominator)

    def ceil(x):
        return x.to_integral_value(rounding=ROUND_CEILING)

    def floor(x):
        return x.to_integral_value(rounding=ROUND_FLOOR)

    AD, BH, AP, LA = (dq(PARAMS[x]) for x in ("AD", "BH", "AP", "LA"))
    t_s = Dec(N0_D2) * LN2
    grid = [t_s + Dec(i) / 10 for i in range(0, 60)] + [Dec(x) for x in (700, 800, 1000, 2000, 10 ** 4)]
    fails = checks = 0
    for t in grid:
        k = t.exp()
        lt = t.ln()
        u = (t / 2).exp() / (AD * t ** Dec("2.5"))
        D = ceil(u)
        M = floor(k / 32)
        h0, Ms = ceil(BH * D * t ** 3), ceil(AS * D * t)
        eps_reg = dq(E2) / t
        eta = eps_reg / (24 * D)
        B0 = ceil(24576 * t + 4)
        gamma = ONE / 2 - dq(G) / t
        logp = AP.ln() + Dec("3.5") * lt - t / 2
        p = logp.exp()
        L = -logp
        F = k * t / 9
        logP = LN2 + 2 * t
        Qh = F / D + logP
        A0 = (ONE / 2 - ONE / t) * (1 - eps_reg)
        Lam = LA * (h0 + (2 * M).sqrt() + 2 * t * (2 * M) ** (ONE / 3))
        logTglob = 4 * D * Lam + 32 * D * t + 2 * D * Dec(441).ln()
        phi = (D + 2) * h0.ln() + 2 * D * LN9 + 4 * D * (B0 * D * h0 + 1).ln() - (1 - eps_reg) * h0 / t ** 2
        logAs = t + (D + 1) * h0.ln() + D * (LN9 + 2 * (k * (4 * M + 4) + 1).ln()) + D * (LN9 + 2 * (3 * k ** 7).ln())
        Gamma = gamma * k * L / 2 - (F + D * logP)
        Ec = 6 * Qh + k * (LN2 + Dec(45).ln() / 2 + LN5 / 2) + D * (Dec("25.5") * t + Dec("11.93")) + 30 * t + Dec("23.1")
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
    # control: at (N0 - 1) log 2 the rich inequality fails in the replay too
    t = Dec(N0_D2 - 1) * LN2
    k = t.exp()
    lt = t.ln()
    L = t / 2 - Dec("3.5") * lt - AP.ln()
    D = ceil((t / 2).exp() / (AD * t ** Dec("2.5")))
    rich_below = (ONE / 2 - dq(G) / t) * L / 2 - t / 9 - (LN2 + Dec(45).ln() / 2 + LN5) / 2 \
        - (5 * (k * t / 9 / D + LN2 + 2 * t) + D * (Dec("23.25") * t + Dec("10.81")) + Dec("16.5") * t + Dec("18.1")) / k
    require(fails == 0, "decimal replay found a failing inequality")
    require(rich_below < 0, "decimal replay: the rich inequality should fail at 2^(N0 - 1)")
    return {"t_values": len(grid), "checks": checks, "failures": fails, "rich_at_2^(N0-1)_negative": True}


def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(manifest)


def main():
    report = {
        "base": {"retuned_endpoint_head": "8916c20", "template_limit": "2026-10-26-ChaloupeMusic-template-limit"},
        "parameters": {"u": f"sqrt(k)/({PARAMS['AD']} t^(5/2))", "h0": f"ceil({PARAMS['BH']} D t^3)",
                       "p": f"{PARAMS['AP']} t^(7/2)/sqrt(k)", "F": "kt/9", "lemma_A": "Rosser-Schoenfeld 1.01624",
                       "unchanged": "M, Ms, eps_reg, eta, B0, delta_s, gamma, q as in the retuned endpoint"},
        "tiers": {t["cls"]: {"class_product": CLASSES[t["cls"]][0], "threshold": threshold(PARAMS, t),
                             "floor": floor_check(t)} for t in TIERS},
        "floor_delta": delta_check(),
        "negative_controls": negative_controls(),
        "decimal_replay": decimal_replay(),
        "integrity_files": integrity(),
        "conclusion": "W_r(k) > k^((k/9) floor(log2 r)) for every k >= 2^940 (D''; 2^1000 under D', 2^1038 under D), "
                      "conditional on the interfaces of PR #12, Section 2, and PR #9's factors, as the retuned "
                      "endpoint; under (T1)-(T6) of template-limit no proof in this chain gives it for e^256 <= k <= 2^934",
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    stored = HERE / "RESULT.json"
    if "--write" in sys.argv:
        stored.write_text(text)
    require(stored.read_text() == text, "output differs from RESULT.json")
    sys.stdout.write(text)
    print("Test passé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
