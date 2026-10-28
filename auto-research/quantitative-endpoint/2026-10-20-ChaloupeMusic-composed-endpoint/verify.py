#!/usr/bin/env python3
"""Checks for the composed endpoint bound (PROOF.md). Not a formal proof.

Base: N1b head 8c2b34f (seven-eighths) on PR #12 head 029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5; lemmas A-E
of N1a (endpoint-constants, a8a9edc). Standard library only, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0 and standard output byte-identical to RESULT.json. Assertions are load-bearing; never -O.

1. Monomial certificates A t^j e^{-dt} <= B for every real t >= 512 (sign of j - dt; value at 512 with
   e >= 2); bounds with sqrt(t) are squared first.
2. Exact budgets for Sections 4-9 of PROOF.md with certified rational bounds for logarithms, separately
   for each of three tiers: Lemma D'' (45^(k/2), C = 71/20), Lemma D' alone (19^k, C = 403/100), and
   N1a's Lemma D alone (37^k, C = 35/8). budgets() takes the constants as parameters.
3. Exhaustive finite checks: the class products (19^k, 45^(k/2) on classes with K_a >= 2, 37^k), the
   canonical partition and the counting core of the short-block regularity lemma.
4. Negative controls that feed each decisive change back into budgets(), a 90-digit decimal replay on a
   grid of t for the three tiers, and file integrity.
"""
import hashlib
import json
import math
import sys
from decimal import Decimal as Dec, getcontext, MAX_EMAX, MIN_EMIN, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
T0 = 512
AD, BH, AS, AP = 22, 5, 4096, 36               # u = sqrt(k)/(AD t^{5/2}), h0 = BH D t^3, Ms = AS D t, p = AP t^{7/2}/sqrt(k)
E2 = Q(1, 64)                                   # eps_reg = E2/t, eta = eps_reg/(24 D)
G = 2 + E2 / 2                                  # gamma = 1/2 - G/t (single source)
RHO = Q(1, 2 ** 200)                            # rho = 1/u <= 2^-200
TAIL = Q(1)                                     # second-family tail exp(-TAIL (1 - eps_reg) h/t^2); 1/2 for threshold l/2
BASE = {"AD": AD, "BH": BH, "AS": AS, "AP": AP, "E2": E2, "G": G, "TAIL": TAIL}
# Three tiers, F = k (t/8 - (7/8) log t - C). The class product of PR #9 Section 8.3 step 4 is bounded by
# base^(exp k): D'' (collision classes have K_a >= 2) 45^(k/2); D' 19^k; N1a's Lemma D 37^k.
TIERS = [
    {"name": "D2", "label": "Lemma D'': 45^(k/2)", "C": Q(71, 20), "base": 45, "exp": Q(1, 2), "n9": 960,
     "coeff1024": Q(1119, 10000)},
    {"name": "D1", "label": "Lemma D': 19^k", "C": Q(403, 100), "base": 19, "exp": Q(1), "n9": 1015,
     "coeff1024": Q(1112, 10000)},
    {"name": "D0", "label": "N1a's Lemma D: 37^k", "C": Q(35, 8), "base": 37, "exp": Q(1), "n9": 1054,
     "coeff1024": Q(1107, 10000)},
]


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


def ln_up(y):
    """Upper bound for log y, y >= 1 rational: y = 2^e m with 1 <= m < 2."""
    y = Q(y)
    e = math.floor(math.log2(y.numerator) - math.log2(y.denominator))
    while pow2(e) > y:
        e -= 1
    while pow2(e + 1) <= y:
        e += 1
    return e * ln2_bounds()[1] + ln_bounds(y / pow2(e))[1]


def ln_lo(y):
    y = Q(y)
    e = math.floor(math.log2(y.numerator) - math.log2(y.denominator))
    while pow2(e) > y:
        e -= 1
    while pow2(e + 1) <= y:
        e += 1
    return e * ln2_bounds()[0] + ln_bounds(y / pow2(e))[0]


# ---------------------------------------------------------------- 1. monomials
def monomial(name, A, j, d, B, t0=T0):
    A, d, B = Q(A), Q(d), Q(B)
    require(A >= 0 and d > 0 and B > 0, f"{name}: bad parameters")
    require(j <= 0 or d * t0 - j >= 0, f"{name}: not monotone from t0")
    bound = A * Q(t0) ** j * pow2(-math.floor(d * t0))
    require(bound <= B, f"{name}: endpoint bound fails")
    return {"name": name, "A": str(A), "j": j, "d": str(d), "B": str(B), "t0": t0,
            "endpoint_upper": f"2^{-math.floor(d * t0)}*{A * Q(t0) ** j}"}


def monomials():
    L4 = ln_up(4)
    one = 1 + RHO
    specs = [
        ("u_at_least_8", (8 * AD) ** 2, 5, 1, 1),
        ("rho_below_2^-200", AD ** 2, 5, 1, RHO ** 2),
        ("M_at_least_k_over_33", 1056, 0, 1, 1),
        ("h0_plus_one_term", 1, -1, 1, (Q(1, 4) - Q(BH, AD) * one) ** 2),       # e^{-t/2} t^{-1/2}
        ("h0_below_2M", Q(33, 8) ** 2, 1, 1, Q(1, 2)),
        ("Ms_below_k", (Q(AS + 2, AD)) ** 2, -3, 1, 1),
        ("p_at_most_half", 4 * AP * AP, 7, 1, 1),
        ("log_t_below_t_over_32", 1, 1, Q(1, 32), 1),
        ("mesh_leading", 2, 1, 3, Q(1, 2)),
        ("mesh_rounding", 2, 0, 3, Q(1, 2)),
        ("Q_over_k", (6 * Q(AD, 8)) ** 2, 7, 1, Q(1, 10 ** 4)),                 # 6Q/k leading
        # first family small terms (units of 16 t^2/k), each <= 1/200
        ("F1_h0_plus_one", (64 * L4 * one / AD) ** 2, -1, 1, Q(1, 200) ** 2),
        ("F1_cube_root", (128 * L4 * one / (AD * Q(5, 2))) ** 2, 1, Q(1, 3), Q(1, 200) ** 2),
        ("F1_32Dt", (512 * one / AD) ** 2, 1, 1, Q(1, 200) ** 2),
        ("F1_2Dlog441", (32 * ln_up(441) * one / AD) ** 2, -1, 1, Q(1, 200) ** 2),
        ("F1_t3", 16, 3, 1, Q(1, 600)),
        ("F1_t2", 16 * ln_up(96) + 2, 2, 1, Q(1, 600)),
        ("F1_const", 32, 0, 1, Q(1, 600)),
        # rich: (5Q + D(23.25t + 10.81) + 16.5t + 18.1)/k, each term <= 1/1000
        ("rich_5Q", (5 * Q(AD, 8)) ** 2, 7, 1, Q(1, 1000) ** 2),
        ("rich_15t", 15, 1, 1, Q(1, 1000)),
        ("rich_D", ((Q(2325, 100) + Q(1081, 100 * T0)) * one / AD) ** 2, -3, 1, Q(1, 1000) ** 2),
        ("rich_lin", Q(165, 10) + Q(181, 10 * T0), 1, 1, Q(1, 1000)),
        # case (i): (log T_K + log 16)/k small; case (ii) residual terms
        ("caseI_6Q", (Q(33, 2)) ** 2, 7, 1, Q(1, 100) ** 2),
        ("caseI_lin", Q(225, 10) + 9, 1, 1, Q(1, 100)),
        ("caseI_D", (17 * one / AD) ** 2, -3, 1, Q(1, 100) ** 2),
        ("caseII_lin", (Q(245, 10) + Q(9, T0)) ** 2, -5, 1, Q(1, 100) ** 2),    # (24.5t+9)/(sqrt k t^{7/2})
    ]
    return [monomial(*s) for s in specs]


# ---------------------------------------------------------------- 2. exact budgets
def budgets(p, tier):
    """Every budget of PROOF.md Sections 4-9 for the parameter dict p and one tier (C, class product)."""
    AD, BH, AS, AP, E2, G, TAIL = (p[x] for x in ("AD", "BH", "AS", "AP", "E2", "G", "TAIL"))
    Cv, label = tier["C"], tier["name"]
    L2lo, L2up = ln2_bounds()
    L4, L9, L36 = ln_up(4), ln_up(9), ln_up(AP)
    one = 1 + RHO
    r = {}
    # scales
    require(Q(BH, AD) * one < Q(1, 4), "h0 <= sqrt(kt)/4 coefficient")
    require(Q(9 * T0, 64) >= L36, "L >= t/4")
    require(Q(17 * T0, 256) >= Cv, "F >= kt/32")
    require(math.ceil(24576 * T0 + 4) <= 24577 * T0, "B0 <= 24577 t")
    # geometry: D(12 eta + 3/h0) = 12 E2/(24 t) + 3/(BH t^3) <= E2/t, and 4MH/k <= eta (192 D t <= k^2: trivial)
    require(12 * E2 / 24 + Q(3, BH * T0 ** 2) <= E2, "short-block regularity budget")
    # dichotomy: A0 - 1/t - gamma = E2/t^2 exactly (rational identity in 1/t, checked at 3 points)
    for tt in (Q(T0), Q(1000), Q(10 ** 6)):
        A0 = (Q(1, 2) - 1 / tt) * (1 - E2 / tt)
        require(A0 - 1 / tt - (Q(1, 2) - G / tt) == E2 / tt ** 2, "dichotomy identity")
        require(A0 - 1 / tt > Q(1, 2) - G / tt, "dichotomy margin")
    # first family: main terms + five small terms (<= 1/200 each) <= 1; sqrt(t) >= 22.6 for t >= 512
    require(Q(226, 10) ** 2 <= T0, "sqrt(t0) >= 22.6")
    f1 = 64 * BH * L4 * (1 + 3 * RHO) / AD ** 2 + 16 * L4 * one / (AD * Q(226, 10)) + Q(5, 200)
    require(f1 <= 1, "first-family budget")
    r["first_family_total_upper"] = dec_ceil(f1, 5)
    # second family: phi(h0) <= -D((BH - 9/2) t + (7/2) log t - c2) + t + log t, where the entropy gives
    # (1/2 + 4) t per unit of D, the tail -(1 - E2/t) BH t, and c2 = 2 log 9 + 4 log 280 + BH E2;
    # B0 D h0 + 1 <= 280 k/t uses h0 <= sqrt(kt)/4 and B0 <= 24577 t.
    require(Q(24577, 4 * AD) * one <= 280 - Q(1, 100), "B0 D h0 coefficient")
    tail = BH * TAIL                                                      # tail = TAIL (1 - E2/t) h0/t^2 >= tail D t
    c2 = 2 * L9 + 4 * ln_up(280) + tail * E2
    require(tail > Q(9, 2), "second-family tail below its entropy")
    lt0_lo, lt0_up = ln_lo(T0), ln_up(T0)
    lhs2 = 8 * ((tail - Q(9, 2)) * T0 + Q(7, 2) * lt0_lo - c2)              # D >= 8; increasing in t
    require(lhs2 >= 3 * T0 + lt0_up + ln_up(192) + Q(1, 8), "second-family margin at t0")
    require(8 * (tail - Q(9, 2)) >= 3, "second-family margin is not increasing")
    require(5 * 8 + 2 <= (1 - E2 / T0) * tail * 8 * T0, "phi decreasing from h0")
    # third family: M_s/128 >= (AS/128) D t, log A_s <= D(18.5 t + (1/2) log t + 6.6) + 1.5 t + (1/2) log t;
    # need D((AS/128 - 37/2) t - (1/2) log t - 6.6) >= 2.5 t + (1/2) log t + log 96 + 1/8 with D >= 1
    require(3 * L9 <= Q(66, 10) + Q(1, 1000), "third-family constant")
    a3 = Q(AS, 128) - Q(37, 2)
    require(a3 >= 3 and a3 * T0 - lt0_up / 2 - Q(66, 10) >= Q(5, 2) * T0 + lt0_up / 2 + ln_up(96) + Q(1, 8),
            "third-family budget")
    # rich: gamma L / 2 identity on an interpolation grid (T, A = log t, B = log AP)
    for T in (Q(1), Q(2), Q(5)):
        for A in (Q(0), Q(1)):
            for B in (Q(0), Q(1)):
                gamma = Q(1, 2) - G / T
                Lx = T / 2 - Q(7, 2) * A - B
                rhs = T / 8 - Q(7, 8) * A - B / 4 - G / 4 + Q(7, 4) * G * A / T + G / 2 * B / T
                require(gamma * Lx / 2 == rhs, "gamma L / 2 expansion")
    # errors from PR #9's displayed factors, recomputed factor by factor (PROOF.md Section 7 table)
    ec, ep = error_bounds()
    require(ec == {"Q": 6, "Dt": Q(51, 2), "t": 30} | {x: ec[x] for x in ("D", "1")}, "E_c coefficients")
    require(ep == {"Q": 4, "Dt": 17, "t": 2} | {x: ep[x] for x in ("D", "1")}, "E_p coefficients")
    require(ec["D"] <= Q(1193, 100) and ec["1"] <= Q(231, 10), "E_c constants above the stated bound")
    require(ep["D"] <= Q(829, 100) and ep["1"] <= Q(461, 100), "E_p constants above the stated bound")
    k_class = tier["exp"] * ln_up(tier["base"])                          # class product <= base^(exp k)
    k_ebar = (L2up + k_class + ln_up(5)) / 2                              # E_c: log 2 + class + (1/2) log 5; E_p: (1/2) log 5
    kappa = Cv - L36 / 4 - G / 4 - k_ebar
    require(kappa > 6 * Q(1, 1000) + Q(1, 1000), f"rich budget ({label})")   # six monomials of <= 1/1000 above
    cut = Cv - L36 / 4 - G / 4 - (L2up + k_class) / 2
    require(cut >= Q(8, 10), f"rich cut ({label})")
    r["kappa_lower"] = dec_floor(kappa)
    r["cut_margin_lower"] = dec_floor(cut, 4)
    # cases (i) and (ii)
    require(1 >= L2up + 3 * Q(1, 100), "case (i) budget")                 # t/512 >= 1 at t0
    brun = Q(AS + 1, AD) * one * (3 + Q(1, T0))
    require(brun <= 560, "run coefficient")
    # residual terms over sqrt(k) t^{7/2}: 560 t^{-4}; D(16t+5) <= 17 (1+rho) u t gives 17 (1+rho)/(AD t^5);
    # (24.5 t + 9) t^{-7/2} e^{-t/2} is the monomial caseII_lin (<= 1/100)
    caseII_D = 17 * one / (AD * Q(T0) ** 5)
    require(6 * Q(AD, 8) + 560 * Q(1, T0 ** 4) + caseII_D + Q(1, 100) < Q(15, 32) * AP, "case (ii) budget")
    # Lemma C tail: 4(D+1) e^{-log 64 - t/2} <= 8 sqrt(k) e^{-t/2}/64 = 1/8, and 2 e^{-2 Gamma} <= 1/8 needs
    # Gamma >= log 4, which holds because Gamma >= Ebar + log 64 + t/2 >= log 64
    require(Q(8, 64) + Q(1, 8) <= Q(1, 4) and ln_lo(64) >= ln_up(4), "Lemma C tail")
    # thresholds
    require(739 * L2lo >= T0, "k >= 2^739 gives t >= 512")
    return r


def error_bounds():
    """PR #9 Sections 7.3, 7.12, 8.2, 8.3: each factor's logarithm as a linear form in Q = log q, D t, D, t
    and 1, using J <= k^6 (so 6 k^2 J + 1 <= 7 k^8), D <= sqrt(k), D + 4 <= 2 sqrt(k), s_G + 1 <= 3 k^2 q^2,
    s_phi + 1 <= 6 k^3, s_x + 1 <= 19 k^4. The k-linear terms (pairs, classes, subsets) are tier-dependent
    and handled in budgets()."""
    L2 = ln2_bounds()[1]

    def form(**c):
        return {x: Q(c.get(x, 0)) for x in ("Q", "Dt", "D", "t", "1")}

    discrete = form(Dt=1 + 16, D=ln_up(9) + 2 * ln_up(7), t=1)          # k^{D+1} T_aug: (D+1) t + D(log 9 + 2 log 7k^8)
    factors_c = {
        "discrete data (7.7)": discrete,
        "integer projections (8.8): D log(3Dk)": form(Dt=Q(3, 2), D=ln_up(3)),
        "first arrangement: 16 (s_G+1)^3": form(Q=6, t=6, **{"1": ln_up(16) + 3 * ln_up(3)}),
        "tail arrangement: (D+4)^2 (s_phi+1)^(D+3)": form(Dt=3, D=ln_up(6), t=1 + 9, **{"1": 2 * L2 + 3 * ln_up(6)}),
        "crossing arrangement: (D+4)^2 (s_x+1)^(D+3)": form(Dt=4, D=ln_up(19), t=1 + 12,
                                                            **{"1": 2 * L2 + 3 * ln_up(19)}),
    }
    factors_p = {
        "discrete data (7.7)": discrete,
        "cells (7.12): 100 D^2 q^4": form(Q=4, t=1, **{"1": ln_up(100)}),
        "second forms (8.5): 9^D": form(D=ln_up(9)),
    }

    def total(fs):
        out = form()
        for f in fs.values():
            for x in out:
                out[x] += f[x]
        return out

    return total(factors_c), total(factors_p)


def thresholds(tier):
    L2lo, L2up = ln2_bounds()
    # g(t) = t/72 - (7/8) log t - C increases for t > 63; k >= 2^n gives t >= n log 2 >= n L2lo
    Cv, n9 = tier["C"], tier["n9"]
    t9 = n9 * L2lo
    g9 = t9 / 72 - Q(7, 8) * ln_up(t9) - Cv
    require(g9 > 0 and t9 > 63, "1/9 threshold")
    tm = (n9 - 1) * L2up                                                  # k = 2^(n-1) has t <= (n-1) L2up
    require(tm / 72 - Q(7, 8) * ln_lo(tm) - Cv < 0, "1/9 threshold is not minimal in the exponent n")
    t1024 = 1024 * L2lo                                                   # coefficient increases in t
    coeff = Q(1, 8) - (Q(7, 8) * ln_up(t1024) + Cv) / t1024
    require(coeff >= tier["coeff1024"], "coefficient at 2^1024")
    return {"one_ninth_from": {"k": f"2^{n9}", "margin_lower": dec_floor(g9)},
            "coefficient_at_2^1024_lower": dec_floor(coeff, 5)}


# ---------------------------------------------------------------- 3. finite checks
def check_class_products(kmax=300):
    """Lemma D' (all classes, 19^k), Lemma D'' (classes with K_a >= 2, 45^(k/2)) and N1a's 37^k."""
    cases = 0
    for K in range(1, 3001):
        require(4 * K * K + 14 * K + 1 <= 19 ** K, "4K^2+14K+1 <= 19^K")
        if K >= 2:
            require((4 * K * K + 14 * K + 1) ** 2 <= 45 ** K, "4K^2+14K+1 <= 45^(K/2)")
    d2_needs_two = False
    for k in range(2, kmax + 1):
        for h in range(1, k):
            Kh = -(-k // h)
            prod_all, prod_two, sum_two = 1, 1, 0
            for a in range(h):
                Ka = -(-(k - a) // h)
                require(Ka >= 1 and Kh <= Ka + 1, "K_h <= K_a + 1")
                f = 2 * Ka * (2 * Kh + 5) + 1
                prod_all *= f
                if Ka >= 2:                        # a collision class has at least two positions
                    prod_two *= f
                    sum_two += Ka
            require(prod_all <= 19 ** k and prod_all <= 37 ** k, "class product above 19^k or 37^k")
            require(sum_two <= k and prod_two ** 2 <= 45 ** sum_two, "D'': product above 45^(sum K_a / 2)")
            d2_needs_two = d2_needs_two or prod_all ** 2 > 45 ** k
            cases += 1
    # control: with classes of length 1 allowed, the 45^(k/2) bound fails (factor 19 > sqrt 45)
    require(d2_needs_two, "control: K_a >= 2 is not load-bearing")
    return cases


def canonical_partition(k, h):
    n = -(-k // h)
    base, rho = divmod(k, n)
    return [base + 1] * rho + [base] * (n - rho)


def check_partition(kmax=300):
    cases = 0
    for k in range(2, kmax + 1):
        for h in range(1, k // 2 + 1):
            lengths = canonical_partition(k, h)
            require(sum(lengths) == k and all(-(-h // 2) <= ell <= h for ell in lengths), "partition")
            cases += 1
    return cases


def check_regularity_core(smax=14):
    cases = 0
    for s in range(1, smax + 1):
        for a in [x for x in range(1, s + 1) if math.gcd(x, s) == 1]:
            for ell in range(1, 2 * s + 3):
                visits = [0] * s
                for z in range(ell):
                    visits[(z * a) % s] += 1
                require(max(visits) <= -(-ell // s), "visit count")
                doubled = visits + visits
                for g in range(1, s + 1):
                    window = sum(doubled[:g])
                    worst = window
                    for c in range(1, s):
                        window += doubled[c + g - 1] - doubled[c - 1]
                        worst = max(worst, window)
                    require(worst <= g * -(-ell // s), "arc count")
                    cases += 1
    return cases


# ---------------------------------------------------------------- 4. negative controls
def negative_controls():
    """Each decisive change, fed back into budgets(), must make it fail."""
    by_name = {tier["name"]: tier for tier in TIERS}

    def fails(p_over, tier_name, tier_over=None):
        p = dict(BASE, **p_over)
        tier = dict(by_name[tier_name], **(tier_over or {}))
        try:
            budgets(p, tier)
        except AssertionError:
            return True
        return False

    rej = {
        "AD_21": fails({"AD": 21}, "D1"),
        "BH_4": fails({"BH": 4}, "D1"),
        "AS_1024": fails({"AS": 1024}, "D1"),
        "AP_35": fails({"AP": 35}, "D1"),
        "AP_37_under_D1": fails({"AP": 37}, "D1"),
        "C_7/2_under_D2": fails({}, "D2", {"C": Q(7, 2)}),
        "C_4.02_under_D1": fails({}, "D1", {"C": Q(402, 100)}),
        "C_4.35_under_D0": fails({}, "D0", {"C": Q(435, 100)}),
        "19k_at_C_3.55": fails({}, "D2", {"base": 19, "exp": Q(1)}),
        "37k_at_C_4.03": fails({}, "D1", {"base": 37}),
        "threshold_l/2": fails({"TAIL": Q(1, 2)}, "D1"),
        "G_2": fails({"G": Q(2)}, "D1"),
        "E2_1/2": fails({"E2": Q(1, 2), "G": 2 + Q(1, 4)}, "D1"),
    }
    require(not fails({}, "D1") and not fails({}, "D2") and not fails({}, "D0"), "delivered constants fail")
    try:
        monomial("control", (8 * AD) ** 2, 5, 1, 1, t0=30)
        rej["monomial_t0_30"] = False
    except AssertionError:
        rej["monomial_t0_30"] = True
    require(all(rej.values()), f"negative control not rejected: {rej}")
    return rej


# ---------------------------------------------------------------- 5. decimal replay
def decimal_replay():
    getcontext().prec = 90
    getcontext().Emax = MAX_EMAX
    getcontext().Emin = MIN_EMIN
    ONE = Dec(1)
    TOL = ONE - Dec(10) ** -60
    LN2, LN4, LN5, LN9 = (Dec(x).ln() for x in (2, 4, 5, 9))

    def ceil(x):
        return x.to_integral_value(rounding=ROUND_CEILING)

    def floor(x):
        return x.to_integral_value(rounding=ROUND_FLOOR)

    def dq(x):
        return Dec(x.numerator) / Dec(x.denominator)

    fails, checks, grid = 0, 0, list(range(512, 2001, 37)) + [5000, 10 ** 4, 10 ** 5]
    for tt in grid:
        for tier in TIERS:
            Cv = tier["C"]
            t = Dec(tt); k = t.exp(); lt = t.ln()
            u = (t / 2).exp() / (AD * t ** Dec("2.5")); D = ceil(u); M = floor(k / 32)
            h0, Ms = ceil(BH * D * t ** 3), ceil(AS * D * t)
            eps_reg = dq(E2) / t; eta = eps_reg / (24 * D); B0 = ceil(24576 * t + 4)
            gamma = ONE / 2 - dq(G) / t
            logp = Dec(AP).ln() + Dec("3.5") * lt - t / 2; p = logp.exp(); L = -logp
            F = k * (t / 8 - Dec("0.875") * lt - dq(Cv))
            logP = LN2 + 2 * t; Qh = F / D + logP
            A0 = (ONE / 2 - ONE / t) * (1 - eps_reg)
            Lam = LN4 * (h0 + (2 * M).sqrt() + 2 * t * (2 * M) ** (ONE / 3))
            logTglob = 4 * D * Lam + 32 * D * t + 2 * D * Dec(441).ln()
            phi = (D + 2) * h0.ln() + 2 * D * LN9 + 4 * D * (B0 * D * h0 + 1).ln() - (1 - eps_reg) * h0 / t ** 2
            logAs = t + (D + 1) * h0.ln() + D * (LN9 + 2 * (k * (4 * M + 4) + 1).ln()) + D * (LN9 + 2 * (3 * k ** 7).ln())
            Gamma = gamma * k * L / 2 - (F + D * logP)
            Ec = 6 * Qh + k * (LN2 + dq(tier["exp"]) * Dec(tier["base"]).ln() + LN5 / 2) + D * (Dec("25.5") * t + Dec("11.93")) + 30 * t + Dec("23.1")
            Ep = 4 * Qh + k * LN5 / 2 + D * (17 * t + Dec("8.29")) + 2 * t + Dec("4.61")
            logTK = 6 * Qh + D * (16 * t + 5) + Dec("4.5") * t + 6
            logBrun = h0.ln() + (Ms + 1).ln() + Ms * (LN2 + 3 * t)
            c = [u >= 8, p <= ONE / 2, L >= t / 4, h0 < 2 * M, 2 * M / k * TOL <= ONE / 16,
                 4 * M / k ** 3 <= eta, D * (12 * eta + 3 / h0) <= eps_reg, A0 - ONE / t > gamma,
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


# ---------------------------------------------------------------- 6. integrity
def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(name for name in manifest if name != "RESULT.json")


def main():
    report = {
        "base": {"n1b_head": "8c2b34f", "n1a_head": "a8a9edc",
                 "pr12_head": "029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5"},
        "parameters": {"u": f"sqrt(k)/({AD} t^(5/2))", "M": "floor(k/32)", "h0": f"ceil({BH} D t^3)",
                       "Ms": f"ceil({AS} D t)", "eps_reg": f"{E2}/t", "eta": "eps_reg/(24 D)",
                       "B0": "ceil(24576 t + 4)", "delta_s": "1/16", "gamma": f"1/2 - ({G})/t",
                       "p": f"{AP} t^(7/2)/sqrt(k)", "t0": T0},
        "monomial_certificates": monomials(),
        "tiers": {tier["name"]: {"assumption": tier["label"], "C": str(tier["C"]),
                                 "budgets": budgets(BASE, tier), "thresholds": thresholds(tier)} for tier in TIERS},
        "class_product_cases": check_class_products(),
        "partition_cases": check_partition(),
        "regularity_core_cases": check_regularity_core(),
        "negative_controls_rejected": negative_controls(),
        "decimal_replay": decimal_replay(),
        "integrity_files": integrity(),
        "conclusion": "W_r(k) > (k^(1/8) / (e^C (log k)^(7/8)))^(k floor(log2 r)) for k >= 2^739, with "
                      "C = 71/20 under Lemma D'' (c = 1/9 from 2^960), C = 403/100 under Lemma D' alone "
                      "(from 2^1015), C = 35/8 under N1a's Lemma D alone (from 2^1054); conditional on the "
                      "interfaces of PR #12, Section 2, and PR #9's displayed factors",
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
