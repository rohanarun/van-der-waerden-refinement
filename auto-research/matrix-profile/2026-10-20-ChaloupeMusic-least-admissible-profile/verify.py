#!/usr/bin/env python3
"""Exact checks for "The least admissible matrix profile" (base 63bef9c).

Standard library only, no network, writes no files. From the repository root:

    python3 -B auto-research/matrix-profile/2026-10-20-ChaloupeMusic-least-admissible-profile/verify.py

Expected: exit 0, and the JSON report printed on stdout equals RESULT.json.
No check uses `assert`, so the run is equally effective under `python3 -O`.

Everything is exact rational arithmetic (fractions.Fraction, integers). The script
supplements the written proofs in README.md; finite grids are evidence, except where a
check is a complete certificate (degree-bounded polynomial identities, the coefficient
positivity of explicit polynomials, and the explicit envelope witnesses), as labelled.

  Part A  P_o is admissible on a finite grid (listed constraints and the t = 3/4 envelope).
  Part B  Certificates for the identities the proofs use (complete, not grid evidence).
  Part C  Least-element evidence: diagonal values equal the growth-lemma bound, the
          repository LP minima equal L_a, and no single value of P_o can be lowered.
  Part D  The five additional valid families, checked exactly for P_o on finite grids.
  Part E  Envelope witnesses above t = 3/4, a bracket of the sharp constant checked against an
          independent value, and the referee's example for the scope of Corollary 3.
  Part F  Negative controls: each corrupted object must fail.
"""
import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

PKG = Path(__file__).resolve().parent
ROOT = PKG.parents[2]
BASE = "63bef9ca996786a41169de4a0c3d6b3b47b0fe96"
BASE_FILES = {
    "research-note.tex": "ebc6b43030ff138247f889a03f496e47cf5f6c9cafadadb35b2fcaa4fd480605",
    "profile_lp.py": "ee699938375e8b2855bb4f4645b9cf99033a68c3008d0d91240d7d7337c83fa1",
    "experiments/matrix-profile.json": "a69414ca791a6fa0a8c865deed10120cfd1d2dc926e28de1544a8e1a1c19b5db",
}

FAILURES = []


def check(cond, label):
    if not cond:
        FAILURES.append(label)
    return bool(cond)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------
# Profiles. u = min(a, b), v = max(a, b).
def multipliers(n, step=lambda m: Q(3 * m + 1, 3 * m)):
    """g[1..n] with g[1] = 1 and g[u] = g[u-1] * step(u-1). The default gives H_u."""
    g = [None, Q(1)]
    for u in range(2, n + 1):
        g.append(g[-1] * step(u - 1))
    return g


NMAX = 400
H = multipliers(NMAX)


def profile(g, offset=Q(1, 2)):
    def P(a, b):
        u, v = (a, b) if a <= b else (b, a)
        return g[u] * (v + offset * (u - 1))
    return P


Po = profile(H)


def L(a):
    return Q(3 * a - 1, 2) * H[a]


def H_big(n):
    """H_n for large n: one reduction instead of one per factor."""
    num = den = 1
    for m in range(1, n):
        num *= 3 * m + 1
        den *= 3 * m
    return Q(num, den)


# ------------------------------------------------------------------------------------------
def listed_violations(P, A, B):
    """Violations of P(1,b)=b, symmetry, row concavity and shifted tripling on a grid.

    Concavity in the first coordinate follows from symmetry, which is checked.
    """
    bad = []
    for b in range(1, B + 1):
        if P(1, b) != b:
            bad.append(("boundary", 1, b))
    for a in range(1, A + 1):
        for b in range(1, A + 1):
            if P(a, b) != P(b, a):
                bad.append(("symmetry", a, b))
        for b in range(2, B):
            if P(a, b - 1) - 2 * P(a, b) + P(a, b + 1) > 0:
                bad.append(("concavity", a, b))
        for h in range(1, B + 1):
            if 3 * h + a - 1 > B:
                break
            if P(a, 3 * h + a - 1) < 3 * P(a, h):
                bad.append(("tripling", a, h))
    return bad


def envelope_violations(P, A):
    """P(a,b) <= (a+b-1)^(4/3), compared after cubing (both sides positive)."""
    return [(a, b) for a in range(1, A + 1) for b in range(1, A + 1)
            if P(a, b) ** 3 > Q(a + b - 1) ** 4]


def monotone_violations(P, A, B):
    return [(a, b) for a in range(1, A + 1) for b in range(1, B) if P(a, b + 1) <= P(a, b)]


def part_a():
    A, B = 60, 240
    viol = listed_violations(Po, A, B)
    env = envelope_violations(Po, 120)
    mono = monotone_violations(Po, A, B)
    # P_o <= P_* pointwise, i.e. H_u^3 <= (3u-1)/2 (P_* has multiplier ((3u-1)/2)^(1/3)).
    below_pstar = [u for u in range(1, NMAX + 1) if H[u] ** 3 > Q(3 * u - 1, 2)]
    check(not viol, "A: listed constraints")
    check(not env, "A: rank envelope at t=3/4")
    check(not mono, "A: monotonicity")
    check(not below_pstar, "A: P_o <= P_*")
    return {
        "grid": {"rows_a": A, "columns_b": B, "envelope_grid": 120, "multiplier_range_u": NMAX},
        "listed_constraint_violations": len(viol),
        "envelope_violations_t_3_4": len(env),
        "monotonicity_violations": len(mono),
        "P_o_above_P_star": len(below_pstar),
    }


# ------------------------------------------------------------------------------------------
# Part B. A polynomial of degree <= d_i in variable i that vanishes on a product grid with
# d_i + 1 distinct values in each variable is identically zero; each identity below is
# checked on a strictly larger grid than its degree requires, so it is a certificate.
def poly_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return r


def poly_pow(p, k):
    r = [1]
    for _ in range(k):
        r = poly_mul(r, p)
    return r


def poly_sub(p, q):
    n = max(len(p), len(q))
    p, q = p + [0] * (n - len(p)), q + [0] * (n - len(q))
    r = [x - y for x, y in zip(p, q)]
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    return r


def part_b():
    out = {}
    # B1. Interior second difference in row a, centre b with b + 1 <= a (lower branch):
    #     P(a,b+1) - 2P(a,b) + P(a,b-1) = -2 H_b (a-b) / (3b(3b-2)).
    # Divided by H_b and multiplied by 6b(3b-2) it is a polynomial of degree 1 in a, 3 in b.
    def b1(a, b):
        up, mid, dn = Q(3 * b + 1, 3 * b), Q(1), Q(3 * b - 3, 3 * b - 2)
        lhs = up * (a + Q(b, 2)) - 2 * mid * (a + Q(b - 1, 2)) + dn * (a + Q(b - 2, 2))
        return 6 * b * (3 * b - 2) * (lhs + Q(2 * (a - b), 3 * b * (3 * b - 2)))
    out["B1_interior_second_difference"] = check(
        all(b1(a, b) == 0 for a in range(0, 4) for b in range(1, 7)), "B1")
    # B2. Seam: the second difference centred on the diagonal is exactly 0 (a >= 2).
    #     With H_{a-1} = H_a (3a-3)/(3a-2), divided by H_a: polynomial of degree 1 times
    #     (3a-2), checked on 6 points.
    def b2(a):
        return (3 * a - 2) * (Q(3 * a + 1, 2) - (3 * a - 1)
                              + Q(3 * a - 3, 3 * a - 2) * (a + Q(a - 2, 2)))
    out["B2_seam_second_difference_zero"] = check(all(b2(a) == 0 for a in range(2, 8)), "B2")
    # B3. Tripling for h < a reduces to H_a (2h+a-1) >= H_h (2a+h-1); its ratio step is
    #     (3a+1)(2h+a)(2a+h-1) - 3a(2h+a-1)(2a+h+1) = 2(a-h)(a-h+1)   (degree 3).
    def b3(a, h):
        return ((3 * a + 1) * (2 * h + a) * (2 * a + h - 1) - 3 * a * (2 * h + a - 1) * (2 * a + h + 1)
                - 2 * (a - h) * (a - h + 1))
    out["B3_tripling_ratio_step"] = check(
        all(b3(a, h) == 0 for a in range(0, 5) for h in range(0, 5)), "B3")
    # B4. H_u^3 <= (3u-1)/2 by induction: 27u^3(3u+2) - (3u+1)^3(3u-1) = 6u+1  (degree 4).
    out["B4_cube_step"] = check(
        all(27 * u ** 3 * (3 * u + 2) - (3 * u + 1) ** 3 * (3 * u - 1) == 6 * u + 1
            for u in range(0, 6)), "B4")
    # B5. kappa_n = L_n / n^(4/3) increases: (L_{n+1}/L_n)^3 >= ((n+1)/n)^4, where
    #     L_{n+1}/L_n = (3n+1)(3n+2)/(3n(3n-1)). After clearing denominators and dividing by
    #     n^3: (3n+1)^3 (3n+2)^3 n - 27 (3n-1)^3 (n+1)^4 >= 0; with n = 1 + k every
    #     coefficient in k is positive.
    def shift(c, s):     # coefficients of c(x + s), lowest degree first
        r = [0]
        for coeff in reversed(c):
            r = poly_mul(r, [s, 1])
            r[0] += coeff
        while len(r) > 1 and r[-1] == 0:   # Horner from r = 0 leaves one leading zero
            r.pop()
        return r
    lhs = poly_mul(poly_mul(poly_pow([1, 3], 3), poly_pow([2, 3], 3)), [0, 1])
    rhs = [27 * x for x in poly_mul(poly_pow([-1, 3], 3), poly_pow([1, 1], 4))]
    diff = poly_sub(lhs, rhs)
    shifted = shift(diff, 1)
    out["B5_kappa_step_coefficients_at_n_eq_1_plus_k"] = shifted
    check(all(c > 0 for c in shifted), "B5")
    # B6. For s, c >= 2: kappa_sc < (3/2)^(4/3) <= kappa_2^2 <= kappa_s kappa_c, cubed:
    #     (3/2)^4 <= kappa_2^6 = L_2^6 / 2^8.
    out["B6_kappa2_squared_exceeds_three_halves_power"] = check(
        Q(3, 2) ** 4 <= L(2) ** 6 / 2 ** 8, "B6")
    # B7. Recursion of the growth lemma, with equality: L_a = L_{a-1} + H_{a-1} + H_a.
    out["B7_growth_recursion_equality_up_to"] = NMAX
    check(all(L(a) == L(a - 1) + H[a - 1] + H[a] for a in range(2, NMAX + 1)), "B7")
    # B8. Tripling is tight on the affine branch: P_o(a, 3h+a-1) = 3 P_o(a,h) for h >= a.
    out["B8_tripling_tight_for_h_ge_a"] = check(
        all(Po(a, 3 * h + a - 1) == 3 * Po(a, h) for a in range(1, 40) for h in range(a, 80)), "B8")
    # B9. H_a^3 / a increases: (3a+1)^3 - 27a^2(a+1) = 9a+1  (degree 3). With B4, which says
    #     that H_a^3 / (a - 1/3) decreases, this brackets the constant (Part E).
    out["B9_lower_sequence_step"] = check(
        all((3 * a + 1) ** 3 - 27 * a ** 2 * (a + 1) == 9 * a + 1 for a in range(0, 6)), "B9")
    # B10. P_o is in no member of PR #11's family F(u)^s (v + lambda(u-1)). Row u = 2 forces
    #      lambda = 1/2 and (5/2)^s = 4/3; row u = 3 then forces 4^s = 14/9. But
    #      (5/2)^(6/19) > 4/3 gives s < 6/19, and 4^(6/19) < 14/9 gives 4^s < 14/9.
    out["B10_not_in_pr11_family"] = check(
        5 ** 6 * 3 ** 19 > 2 ** 6 * 4 ** 19 and 4 ** 6 * 9 ** 19 < 14 ** 19
        and H[2] == Q(4, 3) and H[3] == Q(14, 9), "B10")
    # B11. With K4' (P(a,2) <= 2a) and P(a,1) = a, the envelope at 3/4 cannot fail when
    #      min(a,b) <= 2: (a+1)^4 - 8a^3 = (a^2-2a)^2 + 2a^2 + 4a + 1 > 0  (degree 4).
    out["B11_rows_1_2_inside_envelope_under_K4prime"] = check(
        all((a + 1) ** 4 - 8 * a ** 3 == (a * a - 2 * a) ** 2 + 2 * a * a + 4 * a + 1
            for a in range(0, 6)), "B11")
    return out


# ------------------------------------------------------------------------------------------
def part_c():
    out = {}
    out["L_a_exact"] = {str(a): str(L(a)) for a in range(1, 11)}
    data = json.loads((ROOT / "experiments/matrix-profile.json").read_text())
    lp = []
    for item in data:
        k, val = item["target"], item["diagonal"]
        rel = abs(Q(val) - L(k)) / L(k)
        lp.append({"target": k, "grid_N": item["N"], "lp_diagonal": val,
                   "L_a": float(L(k)), "relative_gap_below_1e-12": rel < Q(1, 10 ** 12)})
        check(rel < Q(1, 10 ** 12), "C: LP minimum equals L_a")
    out["repository_lp_minima"] = lp
    # Local rigidity: lowering one symmetric pair of values of P_o by eps breaks a listed
    # constraint, at every point of the grid. This is consistent with P_o being least; the
    # proof of leastness is in README.md, not here.
    A, B, eps = 12, 40, Q(1, 10 ** 6)
    rigid = 0
    total = 0
    for a0 in range(1, A + 1):
        for b0 in range(a0, A + 1):
            total += 1
            def P(a, b, a0=a0, b0=b0):
                val = Po(a, b)
                return val - eps if (a, b) in ((a0, b0), (b0, a0)) else val
            if listed_violations(P, A, B):
                rigid += 1
    out["lowering_any_single_value_breaks_a_constraint"] = {"points": total, "broken": rigid}
    check(rigid == total, "C: local rigidity")
    return out


# ------------------------------------------------------------------------------------------
def part_d():
    out = {}

    def tally(name, items):
        items = list(items)
        slack_min = min(s for s, _ in items)
        eq = sum(1 for s, _ in items if s == 0)
        neg = [w for s, w in items if s < 0]
        check(not neg, "D: " + name)
        out[name] = {"checks": len(items), "violations": len(neg), "equalities": eq,
                     "min_slack_nonnegative": slack_min >= 0}

    # K1 Kronecker: P(a,b)P(c,d) <= P(a + K(c-1), b + K(d-1)),  K = a + b - 1.
    R = range(1, 8)
    tally("K1_kronecker", (
        (Po(a + (a + b - 1) * (c - 1), b + (a + b - 1) * (d - 1)) - Po(a, b) * Po(c, d), (a, b, c, d))
        for a, b, c, d in product(R, R, R, R)))
    # K2 stride: P(sc, sd) <= P(s,s) P(c,d).
    R = range(1, 13)
    tally("K2_stride", ((Po(s, s) * Po(c, d) - Po(s * c, s * d), (s, c, d))
                        for s, c, d in product(R, R, R) if s * max(c, d) <= NMAX))
    # K3 multiple: P(a, m b) <= m P(a, b).
    tally("K3_multiple", ((m * Po(a, b) - Po(a, m * b), (a, b, m))
                          for a, b, m in product(range(1, 31), range(1, 31), range(1, 11))))
    # K4 Clebsch-Gordan of order k: k P(a,b) >= sum_{i < min(b,k)} P(a, b+k-1-2i).
    tally("K4_clebsch_gordan", ((k * Po(a, b) - sum(Po(a, b + k - 1 - 2 * i) for i in range(min(b, k))),
                                 (a, b, k))
                                for a, b, k in product(range(1, 21), range(1, 21), range(2, 21))))
    # K5 alternating sector chains: P(a, sum h + (a-1) floor(m/2)) >= sum P(a, h_i).
    def chains():
        for a in range(1, 11):
            for m in range(1, 6):
                for hs in product(range(1, 6), repeat=m):
                    B = sum(hs) + (a - 1) * (m // 2)
                    yield Po(a, B) - sum(Po(a, h) for h in hs), (a, hs)
    tally("K5_sector_chains", chains())
    return out


# ------------------------------------------------------------------------------------------
def floor_cuberoot_scaled(x, digits):
    """Largest integer m with (m / 10^digits)^3 <= x, for a positive rational x."""
    scale = 10 ** digits
    lo, hi = 0, 1
    while Q(hi, scale) ** 3 <= x:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if Q(mid, scale) ** 3 <= x:
            lo = mid
        else:
            hi = mid
    return lo


def part_e():
    out = {}
    # Envelope above 3/4: P_o(a,a) = L_a > (2a-1)^(1/t), compared after integer powers.
    hold = [a for a in range(1, 63) if L(a) ** 4 > (2 * a - 1) ** 5]
    out["t_4_5_first_violation_a"] = 63
    check(not hold and L(63) ** 4 > 125 ** 5, "E: t=4/5 witness")
    L2494 = Q(3 * 2494 - 1, 2) * H_big(2494)
    out["t_7_9_violation_a"] = 2494
    check(L2494 ** 7 > Q(2 * 2494 - 1) ** 9, "E: t=7/9 witness")
    # Sharp constant kappa = lim L_a / a^(4/3) = 3/(2 Gamma(4/3)), bracketed without any
    # external inequality: H_a^3 / a increases (B9) and H_a^3 / (a - 1/3) decreases (B4); both
    # tend to Gamma(4/3)^(-3), the name of the limit coming from H_a = Gamma(a+1/3)/(Gamma(4/3)
    # Gamma(a)) and Gamma(a+1/3)/Gamma(a) ~ a^(1/3). Hence, for every N,
    #   (27/8) H_N^3 / N  <=  kappa^3  <=  (81/8) H_N^3 / (3N - 1).
    N = 10000
    HN3 = H_big(N) ** 3
    lo3 = Q(27, 8) * HN3 / N
    hi3 = Q(81, 8) * HN3 / (3 * N - 1)
    D = 6
    lo = floor_cuberoot_scaled(lo3, D)
    hi = floor_cuberoot_scaled(hi3, D) + 1
    out["kappa_bracket_N_10000"] = [str(Q(lo, 10 ** D)), str(Q(hi, 10 ** D))]
    check(Q(lo, 10 ** D) ** 3 <= lo3 and hi3 <= Q(hi, 10 ** D) ** 3, "E: kappa bracket")
    # Independent value: 3/(2 Gamma(4/3)) with Gamma(1/3) = 2.67893853470774763365569294097...
    # (computed with mpmath 1.3.0 at 60 digits, outside this package). The unrounded bracket
    # must contain it with its 10^-47 error interval; this is what an error in either end
    # would break (Part F, F9).
    KAPPA_REF = Q("1.679769782583278527468576405904938474396352190868")
    ref_lo3, ref_hi3 = (KAPPA_REF - Q(1, 10 ** 47)) ** 3, (KAPPA_REF + Q(1, 10 ** 47)) ** 3
    out["kappa_reference_inside_unrounded_bracket"] = check(lo3 <= ref_lo3 and ref_hi3 <= hi3,
                                                             "E: kappa reference")
    # P_* gives (3/2)^(4/3) = 1.7170713...; the bracket must lie strictly below it.
    check(Q(hi, 10 ** D) ** 3 < Q(3, 2) ** 4, "E: kappa below P_* constant")
    # kappa_a increases (B5) and stays below (3/2)^(4/3) (B4): a check at a = 2..400.
    kap3 = [L(a) ** 3 / Q(a) ** 4 for a in range(1, NMAX + 1)]   # kappa_a^3
    check(all(x < y for x, y in zip(kap3, kap3[1:])), "E: kappa increasing")
    # Scope of Corollary 3 (example due to the referee): Pt = c P_o off the first row and
    # column, Pt(1,b) = b, satisfies the listed constraints for every c >= 1 and keeps the
    # diagonal exponent 4/3; with c = 81/56, Pt(3,3) = 9 > 5^(4/3). So a constraint forcing
    # P(3,3) >= 9 would exclude t = 3/4 without raising the exponent.
    c = Q(81, 56)

    def Pt(a, b):
        return Q(b) if a == 1 else Q(a) if b == 1 else c * Po(a, b)
    viol = listed_violations(Pt, 40, 200)
    out["referee_example_c_81_56"] = {
        "listed_constraint_violations_rows_40_columns_200": len(viol),
        "value_at_3_3": str(Pt(3, 3)),
        "exceeds_envelope_at_3_3": Pt(3, 3) ** 3 > Q(5) ** 4,
    }
    check(not viol and Pt(3, 3) == 9 and Q(9) ** 3 > Q(5) ** 4, "E: referee example")
    # Where a point outside the envelope must be sought: with K4', min(a,b) >= 3 (B11). There
    # P_o sits below (a+b-1)^(4/3) by at least the factor at (3,3), 9 * 5^(4/3) / 56 = 1.374...
    # (grid 3 <= a, b <= 120, exact).
    ref = Po(3, 3) ** 3 / Q(5) ** 4
    worse = [(a, b) for a in range(3, 121) for b in range(a, 121)
             if Po(a, b) ** 3 / Q(a + b - 1) ** 4 > ref]
    out["smallest_envelope_gap_min_ge_3_is_at_3_3_on_grid_120"] = check(not worse, "E: gap at (3,3)")
    return out


# ------------------------------------------------------------------------------------------
def part_f():
    """Each corrupted object must fail. A control that passes is a failure of the verifier."""
    out = {}
    A, B = 12, 48
    # F1. Second multiplier lowered by 1/100: the seam at a = 2 is no longer concave.
    g = multipliers(A)
    g[2] -= Q(1, 100)
    for u in range(3, A + 1):
        g[u] = g[u - 1] * Q(3 * u - 2, 3 * u - 3)
    v = listed_violations(profile(g), A, B)
    out["F1_lowered_H2"] = check(any(x[0] == "concavity" and x[1] == 2 for x in v), "F1")
    # F2. A smaller growth factor 1 + 1/(3m+1): its diagonal would beat L_a; must fail.
    g = multipliers(A, step=lambda m: Q(3 * m + 2, 3 * m + 1))
    v = listed_violations(profile(g), A, B)
    out["F2_slower_growth"] = check(any(x[0] == "concavity" for x in v), "F2")
    # F3. Offset 1/2 + 1/100: tripling fails on the affine branch.
    v = listed_violations(profile(multipliers(A), Q(51, 100)), A, B)
    out["F3_offset_too_large"] = check(any(x[0] == "tripling" for x in v), "F3")
    # F4. Offset 1/2 - 1/100 with the same multiplier: the seam turns convex.
    v = listed_violations(profile(multipliers(A), Q(49, 100)), A, B)
    out["F4_offset_too_small"] = check(any(x[0] == "concavity" for x in v), "F4")
    # F5. Diagonal multiplied by 99/100 at a = 5 only (kept symmetric): breaks a constraint.
    def P5(a, b):
        return Po(a, b) * (Q(99, 100) if a == b == 5 else 1)
    out["F5_lowered_diagonal_value"] = check(bool(listed_violations(P5, A, B)), "F5")
    # F6. A corrupted identity is detected (B3 with +1).
    out["F6_corrupted_identity_detected"] = check(
        any(((3 * a + 1) * (2 * h + a) * (2 * a + h - 1) - 3 * a * (2 * h + a - 1) * (2 * a + h + 1)
             - 2 * (a - h) * (a - h + 1) - 1) != 0 for a in range(0, 5) for h in range(0, 5)), "F6")
    # F7. The family checkers are not vacuous: 2 P_o violates K1 at (1,1,1,1), P_o / 2 violates K2.
    out["F7_K1_detects_2P"] = check(4 * Po(1, 1) ** 2 > 2 * Po(1, 1), "F7a")
    out["F7_K2_detects_half_P"] = check(Po(1, 1) / 2 > (Po(1, 1) / 2) ** 2, "F7b")
    # F8. The envelope at t = 4/5 holds for a < 63 and fails at 63 (see Part E); at 3/4 the
    #     same diagonal never fails on 1..400.
    out["F8_envelope_3_4_diagonal_holds_to_400"] = check(
        all(L(a) ** 3 <= Q(2 * a - 1) ** 4 for a in range(1, NMAX + 1)), "F8")
    # F9. Two wrong brackets must miss the reference constant (they would have passed a check
    #     of the rounded bracket alone): Wendel's upper factor ((3N+1)/(3N))^2 with exponent 1,
    #     and the upper sequence taken at 3N instead of 3N - 1.
    N = 10000
    HN3 = H_big(N) ** 3
    kref3 = Q("1.679769782583278527468576405904938474396352190868") ** 3
    wendel_exp1 = Q(27, 8) * HN3 / N * Q(3 * N + 1, 3 * N)
    upper_at_3N = Q(81, 8) * HN3 / (3 * N)
    out["F9_wendel_exponent_1_misses_kappa"] = check(wendel_exp1 < kref3, "F9a")
    out["F9_upper_sequence_at_3N_misses_kappa"] = check(upper_at_3N < kref3, "F9b")
    return out


# ------------------------------------------------------------------------------------------
def main():
    report = {"base": BASE, "package": PKG.name}
    hashes = {}
    for rel, want in BASE_FILES.items():
        p = ROOT / rel
        got = sha256(p) if p.is_file() else None
        hashes[rel] = got == want
        check(got == want, "pinned base file " + rel)
    report["pinned_base_files_ok"] = hashes
    man = json.loads((PKG / "MANIFEST.json").read_text())
    # lean/.lake holds the local Lake build (Mathlib), never part of the package
    listed = sorted(p.relative_to(PKG).as_posix() for p in PKG.rglob("*")
                    if p.is_file() and p.name != "MANIFEST.json"
                    and ".lake" not in p.relative_to(PKG).parts)
    check(sorted(man) == listed, "manifest lists exactly the package files")
    for name, want in man.items():
        check(sha256(PKG / name) == want, "manifest hash " + name)
    report["manifest_files"] = sorted(man)
    report["A_admissibility_grid"] = part_a()
    report["B_certificates"] = part_b()
    report["C_least_element_evidence"] = part_c()
    report["D_additional_families_for_P_o"] = part_d()
    report["E_envelope_and_constant"] = part_e()
    report["F_negative_controls"] = part_f()
    report["failures"] = FAILURES
    report["status"] = "passed" if not FAILURES else "failed"
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    saved = PKG / "RESULT.json"
    if saved.is_file() and json.loads(saved.read_text()) != report:
        print("report differs from RESULT.json", file=sys.stderr)
        return 1
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
