#!/usr/bin/env python3
"""Checks for the seven-eighths endpoint transfer (PROOF.md). Not a formal proof.

Base: PR #12 head 029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5 (on 63bef9ca996786a41169de4a0c3d6b3b47b0fe96).
Standard library only, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0 and standard output byte-identical to RESULT.json. Assertions are load-bearing; never -O.

1. Monomial certificates A t^j e^{-dt} <= B for every real t >= 512 (sign of j - dt, value at 512 with
   e >= 2), for every scale bound of PROOF.md Sections 4-9. Bounds with sqrt(t) are squared first.
2. Exact rational budgets: every constant comparison of Sections 4-10, with certified rational
   bounds for log 2 and log 1735 (alternating-free series with explicit tails).
3. Exhaustive finite checks of Lemma 5.1 (canonical partition) and of the counting core of Lemma 5.2.
4. Negative controls: each decisive change must break a stated inequality.
5. A 90-digit decimal replay of the main inequalities on a grid of t (corroboration only).
6. Integrity of the package files against MANIFEST.json.
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
AD, AH, AS, AP = 4096, 256, 4096, 16384      # u = sqrt(k)/(AD t^{5/2}), h0 = AH D t^3, Ms = AS D t, p = AP t^{7/2}/sqrt(k)
C = Q(35, 2)                                  # F = k (t/8 - (7/8) log t - C)
G = 3                                         # gamma = 1/2 - G/t (single source for every check)


def dec_floor(x, digits=6):
    """Decimal string of a rational rounded down (safe for lower bounds)."""
    n = math.floor(x * 10 ** digits)
    return f"{n // 10 ** digits}.{n % 10 ** digits:0{digits}d}" if n >= 0 else str(float(x))


def dec_ceil(x, digits=6):
    """Decimal string of a positive rational rounded up (safe for upper bounds)."""
    n = math.ceil(x * 10 ** digits)
    return f"{n // 10 ** digits}.{n % 10 ** digits:0{digits}d}"


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def pow2(n):
    return Q(1 << n) if n >= 0 else Q(1, 1 << (-n))


# ---------------------------------------------------------------- 1. monomials
def monomial(name, A, j, d, B, t0=T0):
    """Certify A t^j e^{-d t} <= B for all real t >= t0 (A >= 0, d > 0)."""
    A, d, B = Q(A), Q(d), Q(B)
    require(A >= 0 and d > 0 and B > 0, f"{name}: bad parameters")
    require(j <= 0 or d * t0 - j >= 0, f"{name}: not monotone from t0")   # derivative sign j/t - d
    bound = A * Q(t0) ** j * pow2(-math.floor(d * t0))                    # e^{-x} <= 2^{-floor x}
    require(bound <= B, f"{name}: endpoint bound fails")
    return {"name": name, "A": str(A), "j": j, "d": str(d), "B": str(B), "t0": t0,
            "endpoint_upper": f"2^{-math.floor(d * t0)}*{A * Q(t0) ** j}"}


MONOMIALS = [
    # (4.1) u >= 1: AD t^{5/2} e^{-t/2} <= 1, squared
    ("u_at_least_one", AD * AD, 5, 1, 1),
    # (4.2) M >= k/33
    ("M_at_least_k_over_33", 1056, 0, 1, 1),
    # (4.5) h0 < 2M: (33/14) t^{1/2} e^{-t/2} < 1, squared (with margin 1/2)
    ("h0_below_2M", Q(33, 14) ** 2, 1, 1, Q(1, 2)),
    # (4.6) Ms <= 8194 u t <= k
    ("Ms_below_k", Q(2 * AS + 2, AD) ** 2, -3, 1, 1),
    # (4.7) D <= 2u <= k/64
    ("D_below_k_over_64", Q(128, AD) ** 2, -5, 1, 1),
    # (4.8) p <= 1/2
    ("p_at_most_half", 4 * AP * AP, 7, 1, 1),
    # (4.9) log t <= t/32
    ("log_t_below_t_over_32", 1, 1, Q(1, 32), 1),
    # (4.13) 6Q + 100 D t <= k: three terms, each <= 1/3
    ("sixQ_leading", (6 * AD // 8) ** 2, 7, 1, Q(1, 9)),
    ("sixQ_rounding", 18, 1, 1, Q(1, 3)),
    ("hundred_Dt", Q(200, AD) ** 2, -3, 1, Q(1, 9)),
    # (4.14) J <= k^6: (2t + 2) e^{-3t} <= 1
    ("mesh_leading", 2, 1, 3, Q(1, 2)),
    ("mesh_rounding", 2, 0, 3, Q(1, 2)),
    # (5) first family: each of three terms <= 1/200 after dividing by k/t^2
    ("first_family_sqrt", Q(84, AD) ** 2, 1, 1, Q(1, 200) ** 2),
    ("first_family_t3", 1, 3, 1, Q(1, 200)),
    ("first_family_t2", 4, 2, 1, Q(1, 200)),
    # (8) 20t + 3 <= 23 t <= sqrt(k) t^{7/2} / 2, squared: 4 * 23^2 t^{-5} e^{-t} <= 1
    ("run_linear_terms", 4 * 23 * 23, -5, 1, 1),
]


def monomial_certificates():
    out = [monomial(*m) for m in MONOMIALS]
    # rich tail: 32 k e^{-3k} <= 1 for every real k >= 2 (variable k, not t)
    out.append(monomial("rich_tail_in_k", 32, 1, 3, 1, t0=2))
    return out


# ---------------------------------------------------------------- 2. exact budgets
def ln2_bounds(N=60):
    s = sum(Q(1, n * 2 ** n) for n in range(1, N + 1))
    return s, s + Q(1, (N + 1) * 2 ** N)           # tail <= sum_{n>N} 2^{-n}/(N+1)


def ln_bounds(y, N=60):
    """Rational bounds for log y, y > 1, by 2 artanh((y-1)/(y+1))."""
    y = Q(y)
    z = (y - 1) / (y + 1)
    s = 2 * sum(z ** (2 * m + 1) / (2 * m + 1) for m in range(N))
    tail = 2 * z ** (2 * N + 1) / ((2 * N + 1) * (1 - z * z))
    return s, s + tail


def ln_upper_int(y):
    """Rational upper bound for log y, y a positive integer: y = 2^e m with 1 <= m < 2."""
    e = y.bit_length() - 1
    m = Q(y, 1 << e)
    return e * ln2_bounds()[1] + (ln_bounds(m)[1] if m > 1 else 0)


def e_lower(N=20):
    return sum(Q(1, math.factorial(n)) for n in range(N + 1))


def exact_budgets():
    L2lo, L2up = ln2_bounds()
    require(L2up - L2lo < Q(1, 10 ** 15) and L2lo < Q(693148, 10 ** 6) and L2up > Q(693147, 10 ** 6),
            "log 2 bounds inconsistent")
    r = {}
    # (4.3) h0 coefficients: 256 u t^3 = sqrt(kt)/16 and 514 u t^3 <= sqrt(kt)/7
    #       h0 >= (AH/AD) sqrt(kt) and h0 <= (2(AH+1)/AD) sqrt(kt) <= sqrt(kt)/7
    require(AD >= AH and Q(2 * (AH + 1), AD) <= Q(1, 7), "h0 upper coefficient")
    # (4.4) log h0 >= t/2 + (1/2) log t - log(AD/AH) >= t/3, implied by t/6 >= log(AD/AH)
    log_ratio_up = ln_bounds(Q(AD, AH))[1] if AD > AH else 0
    require(Q(T0, 6) >= log_ratio_up, "log h0 >= t/3 fails at t0")
    # (4.10) L = t/2 - (7/2) log t - log AP >= t/4: with log t <= t/32, 9t/64 >= log AP at t0
    logAP_up = ln_upper_int(AP)
    require(Q(9 * T0, 64) >= logAP_up, "L >= t/4 fails")
    # (4.11) F >= kt/32: 17 t/256 >= 35/2 at t0 (increasing)
    require(Q(17 * T0, 256) >= C, "F >= kt/32 fails")
    # (4.12) Q <= (AD/8) sqrt(k) t^{7/2} + 3t is used through the monomial sixQ_leading = (6 AD/8)^2
    # (I1) B0 = ceil(384 t + 4) <= 385 t <= 512 t for t >= 4
    require(math.ceil(384 * T0 + 4) <= 385 * T0 <= 512 * T0, "B0 bound")
    # (5) global entropy: 240 * 257 * 4 / AD^2 below 1/33 - 3/200
    g = Q(240 * (AH + 1) * 4, AD * AD)
    margin = Q(1, 33) - g - Q(3, 200)
    require(margin > 0, "first-family budget fails")
    r["first_family_margin_lower"] = dec_floor(margin, 9)
    # log 48 <= 4 (used as -t-4 <= -log 48k)
    require(e_lower() ** 4 >= 48, "log 48 <= 4 fails")
    # Family 2: h0/(4t^2) >= (AH/4) D t; 2t + 15 D t - (AH/4) D t <= -t - 4 needs AH/4 - 15 >= 4 (D >= 1, t >= 4)
    require(Q(AH, 4) - 15 >= 4, "second-family budget")
    # Family 3: Ms/32 >= (AS/32) D t; 40 D t - (AS/32) D t <= -t - 4 needs AS/32 - 40 >= 2
    require(Q(AS, 32) - 40 >= 2, "third-family budget")
    # local lemma criterion: log 2 + 1/8 < 1 <= w
    require(L2up + Q(1, 8) < 1, "local lemma criterion")
    # Lemma 5.2 bookkeeping: D(12 eta + 3/h0) = 1/(2t) + 3D/h0 <= 1/(2t) + 3/(256 t^3) <= 1/t
    require(Q(12, 24) == Q(1, 2) and Q(1, 2 * T0) + Q(3, AH * T0 ** 3) <= Q(1, T0), "regularity budget")
    # (6) dichotomy: (1/2 - 1/t)(1 - 1/t) - 1/t - (1/2 - 5/(2t)) = 1/t^2 >= 0 and 5/2 < 3
    for tt in (Q(T0), Q(1000), Q(10 ** 6)):
        A0 = (Q(1, 2) - 1 / tt) * (1 - 1 / tt)
        require(A0 - 1 / tt - (Q(1, 2) - Q(5, 2) / tt) == 1 / tt ** 2, "dichotomy identity")
        require(A0 - 1 / tt > Q(1, 2) - Q(G) / tt, "dichotomy margin: A0 - 1/t > gamma")
        require(A0 <= Q(1, 2), "A0 <= 1/2")
    # (7) gamma L / 2 identity, checked on a full interpolation grid (T * both sides is a polynomial of
    # degree 2 in T and 1 in A = log t, B = log AP, so a 3 x 2 x 2 grid proves it)
    for T in (Q(1), Q(2), Q(5)):
        for A in (Q(0), Q(1)):
            for B in (Q(0), Q(1)):
                gamma = Q(1, 2) - Q(G) / T
                L = T / 2 - Q(7, 2) * A - B
                rhs = T / 8 - Q(7, 8) * A - B / 4 - Q(G, 4) + Q(7 * G, 4) * A / T + Q(G, 2) * B / T
                require(gamma * L / 2 == rhs, "gamma L / 2 expansion")
    # Gamma >= k (C - log(AP)/4 - G/4) - 3Dt with 3Dt <= 3k/100 must give Gamma >= 14k (E <= 11k)
    rich = C - logAP_up / 4 - Q(G, 4)
    require(rich - Q(3, 100) >= 14 and 14 - 11 == 3, "rich budget: Gamma < 14k")
    r["Gamma_over_k_lower"] = dec_floor(rich)
    # E <= 11 k from 6Q + 100 D t <= k
    require(10 + 1 == 11, "E budget")
    # (29) many s-light: kt/64 - 2k >= 6k at t0, and 6 >= log 8 (log 8 <= 3 log 2 up)
    require(Q(T0, 64) - 2 >= 6 and 6 > 3 * L2up, "many s-light budget")
    # (8) run budget: Ms(3t+1) <= 8194 (3 + 1/512) u t^2 and 8194 (3 + 1/512)/AD <= 7
    require(Q(2 * AS + 2, 1) * (3 + Q(1, T0)) / AD <= 7, "run coefficient")
    require(Q(7) + Q(1, 64) <= Q(T0) ** 4 / 2, "run t^{-1/2} term")
    require(Q(6 * AD, 8) + 1 < Q(AP, 4), "few s-light budget: 6Q + rest >= pk/4")
    r["few_s_light_coefficients"] = f"{Q(6 * AD, 8) + 1} < {Q(AP, 4)}"
    # main threshold: 739 log 2 > 512
    require(739 * L2lo > T0, "k >= 2^739 does not give t >= 512")
    # (2) the 1/9 threshold: g(t) = t/72 - (7/8) log t - 35/2 increases for t > 63, g(1735) > 0
    l1735lo, l1735up = ln_bounds(Q(1735, 1024))
    log1735_up = 10 * L2up + l1735up
    require(log1735_up <= Q(74593, 10 ** 4), "log 1735 upper bound")
    g1735 = Q(1735, 72) - Q(7, 8) * log1735_up - C
    require(g1735 > 0 and 63 < 1735, "1/9 threshold fails at t = 1735")
    require(2504 * L2lo >= 1735, "k >= 2^2504 does not give t >= 1735")
    r["one_ninth_margin_at_t_1735_lower"] = dec_floor(g1735)
    r["log2_interval"] = [dec_floor(L2lo, 15), dec_ceil(L2up, 15)]
    r["log1735_upper"] = dec_ceil(log1735_up, 9)
    return r


# ---------------------------------------------------------------- 3. finite lemma checks
def canonical_partition(k, h):
    n = -(-k // h)
    base, rho = divmod(k, n)
    return [base + 1] * rho + [base] * (n - rho)


def check_partition(kmax=400):
    cases = 0
    for k in range(2, kmax + 1):
        for h in range(1, k // 2 + 1):
            lengths = canonical_partition(k, h)
            require(sum(lengths) == k, "partition does not cover")
            require(all(-(-h // 2) <= ell <= h for ell in lengths), f"partition length out of range k={k} h={h}")
            cases += 1
    # control: the old partition (full blocks of length h plus a remainder) has a block shorter
    # than h/2 for some k, h <= k/2, e.g. k = 9, h = 4 gives 4, 4, 1.
    def old_partition(k, h):
        return [h] * (k // h) + ([k % h] if k % h else [])
    require(old_partition(9, 4) == [4, 4, 1] and any(min(old_partition(k, h)) < -(-h // 2)
            for k in range(2, 60) for h in range(2, k // 2 + 1)), "partition control not detected")
    return cases


def check_regularity_core(smax=16):
    """Counting core of Lemma 5.2: for a rotation of exact period s, over z < ell the number of z whose
    grid point falls in an arc containing g grid points is <= g * ceil(ell/s); and the resulting
    fraction (g)(1/s + 1/ell) with g <= 4 eta s + 1 is <= 12 eta + 3/h0 when h0 < s <= h <= 2 ell."""
    cases = 0
    for s in range(1, smax + 1):
        steps = [a for a in range(1, s + 1) if math.gcd(a, s) == 1]
        for a in steps:
            for ell in range(1, 2 * s + 3):
                visits = [0] * s
                for z in range(ell):
                    visits[(z * a) % s] += 1
                require(max(visits) <= -(-ell // s), "visit count exceeds ceil(ell/s)")
                doubled = visits + visits
                for g in range(1, s + 1):            # arc = g consecutive grid points (circular window)
                    window = sum(doubled[:g])
                    worst = window
                    for c in range(1, s):
                        window += doubled[c + g - 1] - doubled[c - 1]
                        worst = max(worst, window)
                    require(worst <= g * -(-ell // s), "arc count exceeds g ceil(ell/s)")
                    cases += 1
    # algebra: (4 eta s + 1)(1/s + 1/ell) <= 12 eta + 3/h0 for h0 < s <= h <= 2 ell
    for h0 in (3, 7, 20):
        for h in range(h0 + 1, h0 + 30):
            for s in [d for d in range(h0 + 1, h + 1) if h % d == 0]:
                for ell in range(-(-h // 2), h + 1):
                    for eta in (Q(1, 1000), Q(1, 97), Q(1, 24)):
                        require((4 * eta * s + 1) * (Q(1, s) + Q(1, ell)) <= 12 * eta + Q(3, h0),
                                "fraction bound fails")
                        cases += 1
    return cases


# ---------------------------------------------------------------- 4. negative controls
def negative_controls():
    rejected = {}
    L2lo, L2up = ln2_bounds()
    # (a) full blocks + remainder with M = floor(k/32): #12 (25) loses up to h <= 2M = k/16 positions,
    #     A0 (k - k/16) - k/t < gamma k at t0, so the dichotomy fails without Lemma 5.1.
    tt = Q(T0)
    A0 = (Q(1, 2) - 1 / tt) * (1 - 1 / tt)
    require(A0 * (1 - Q(1, 16)) - 1 / tt < Q(1, 2) - Q(G) / tt, "control (a) not rejected")
    rejected["remainder_with_M_k_over_32"] = True
    # (b) keeping #12's M = floor(k/t) with D ~ sqrt(k)/t^{5/2}: M/t^2 = k/t^3 < 246720/AD^2 * k/t^2
    require(Q(1, T0) < Q(240 * (AH + 1) * 4, AD * AD), "control (b) not rejected")
    rejected["M_k_over_t_with_new_D"] = True
    # (c) AD = 2048 with the crude bound D <= 2u: 246720/2048^2 > 1/33
    require(Q(240 * (AH + 1) * 4, 2048 * 2048) > Q(1, 33), "control (c) not rejected")
    rejected["AD_2048"] = True
    # (d) AP = 8192: 3073 >= 8192/4
    require(not (3073 < Q(8192, 4)), "control (d) not rejected")
    rejected["AP_8192"] = True
    # (e) C = 14: Gamma/k lower bound 14 - (7/2) log 2 - 3/4 does not exceed E/k = 11
    require(Q(14) - Q(7, 2) * L2lo - Q(3, 4) < 11, "control (e) not rejected")
    rejected["C_14"] = True
    # (f) theta = 3/4 (p ~ t^3/sqrt(k)): 6Q ~ 3072 sqrt(k) t^{7/2} exceeds pk/4 = 4096 sqrt(k) t^3 at t0
    require(3072 ** 2 * T0 > 4096 ** 2, "control (f) not rejected")   # 3072 t^{1/2} > 4096, squared
    rejected["theta_three_quarters"] = True
    # (g) blocks shorter than h/2: for a block of length ell = 4 eta s at step 1/s next to the cut, every
    #     position has its grid value within 2 eta of the cut (the quantity Lemma 5.2 bounds), so that
    #     count reaches ell, above (12 eta + 3/h0) ell.
    s, h0 = 960, 100
    eta = Q(1, 96)
    ell = int(4 * eta * s)                 # 40 consecutive grid points fit in the arc of length 4 eta
    start = Q(1, 2) - 2 * eta               # step 1/s from the left end of the cut neighbourhood
    nonregular = sum(1 for z in range(ell) if abs(start + Q(z, s) - Q(1, 2)) <= 2 * eta)   # rho <= 2 eta
    require(ell < s // 2 and nonregular == ell and Q(nonregular, ell) > 12 * eta + Q(3, h0),
            "control (g) not rejected")
    rejected["block_shorter_than_half"] = True
    # (h) a wrong monomial must be refused: AD t^{5/2} e^{-t/2} <= 1 with AD = 4096 fails at t0 = 30
    try:
        monomial("control", AD * AD, 5, 1, 1, t0=30)
        raise RuntimeError("control (h) not rejected")
    except AssertionError:
        rejected["monomial_t0_30"] = True
    return rejected


# ---------------------------------------------------------------- 5. decimal replay
def decimal_replay():
    getcontext().prec = 90
    getcontext().Emax = MAX_EMAX
    getcontext().Emin = MIN_EMIN
    ONE = Dec(1)
    TOL = ONE - Dec(10) ** -60

    def ceil(x):
        return x.to_integral_value(rounding=ROUND_CEILING)

    def floor(x):
        return x.to_integral_value(rounding=ROUND_FLOOR)

    LN2, LN3, LN9 = Dec(2).ln(), Dec(3).ln(), Dec(9).ln()
    fails, checks, grid = 0, 0, list(range(512, 4097, 31)) + [10 ** 4, 10 ** 5]
    for tt in grid:
        t = Dec(tt)
        k, sk = t.exp(), (t / 2).exp()
        u = sk / (AD * t ** Dec("2.5"))
        D, M = ceil(u), floor(k / 32)
        h0, Ms = ceil(AH * D * t ** 3), ceil(AS * D * t)
        eta, gamma = ONE / (24 * D * t), ONE / 2 - G / t
        A0 = (ONE / 2 - ONE / t) * (ONE - ONE / t)
        logp = Dec(AP).ln() + Dec("3.5") * t.ln() - t / 2
        Cd = Dec(C.numerator) / Dec(C.denominator)
        p, L = logp.exp(), -logp
        F = k * (t / 8 - Dec("0.875") * t.ln() - Cd)
        logP = LN2 + 2 * t
        Qh = F / D + logP
        logJ = LN2 + 2 * t + ((D + 1) * Qh).ln() + Dec(10) ** -40
        hi = 2 * t + 60 * h0
        logTglob = 2 * D * (LN9 + 2 * (LN3 + 2 * t + hi + (ONE + (6 * t - hi).exp()).ln() + Dec(10) ** -40))
        logAs = t + (D + 1) * h0.ln() + D * (LN9 + 2 * (k * (4 * M + 4) + 1).ln()) \
            + D * (LN9 + 2 * (LN2 + t + logJ + Dec(10) ** -40))
        logTK_noq = D * (LN9 + 2 * (LN3 + 2 * t + logJ + Dec(10) ** -40)) + Dec(16).ln() + 3 * (t + D.ln() + 3 / k ** 2)
        logTK = logTK_noq + 6 * Qh
        logBrun = h0.ln() + (Ms + 1).ln() + Ms * (LN2 + 3 * t)
        Gamma = gamma * k * L / 2 - (F + D * logP)
        c = [u >= 1, D <= k / 64, p <= ONE / 2, L >= t / 4, h0 < 2 * M, logJ <= 6 * t,
             2 * M / k * TOL <= ONE / 16, 4 * M / k ** 3 <= eta, D * (12 * eta + 3 / h0) <= ONE / t,
             logTglob - M / t ** 2 <= -Dec(48).ln() - t,
             logAs - Ms / 32 <= -Dec(48).ln() - t,
             A0 * k - k / t > gamma * k,
             Gamma >= 14 * k, 10 * k + 100 * D * t + 6 * Qh <= 11 * k,
             logTK <= k, LN2 + logTK + logBrun - p * k / 4 < -Dec(4).ln()]
        checks += len(c)
        fails += sum(1 for ok in c if not ok)
    require(fails == 0, "decimal replay found a failing inequality")
    return {"t_values": len(grid), "checks": checks, "failures": fails}


# ---------------------------------------------------------------- 6. integrity
def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue                       # RESULT.json is checked by comparison with stdout
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(name for name in manifest if name != "RESULT.json")


def main():
    report = {
        "base": {"pr12_head": "029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5",
                 "repository_base": "63bef9ca996786a41169de4a0c3d6b3b47b0fe96"},
        "parameters": {"u": f"sqrt(k)/({AD} t^(5/2))", "M": "floor(k/32)", "h0": f"ceil({AH} D t^3)",
                       "Ms": f"ceil({AS} D t)", "eta": "1/(24 D t)", "gamma": f"1/2 - {G}/t",
                       "p": f"{AP} t^(7/2)/sqrt(k)", "F": f"k (t/8 - (7/8) log t - {C})", "t0": T0},
        "monomial_certificates": monomial_certificates(),
        "exact_budgets": exact_budgets(),
        "partition_lemma_cases": check_partition(),
        "regularity_core_cases": check_regularity_core(),
        "negative_controls_rejected": negative_controls(),
        "decimal_replay": decimal_replay(),
        "integrity_files": integrity(),
        "conclusion": "W_r(k) > (k^(1/8) / (e^(35/2) (log k)^(7/8)))^(k floor(log2 r)) for k >= 2^739; "
                      "c = 1/9 for k >= 2^2504; conditional on the interfaces of PR #12, Section 2",
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
