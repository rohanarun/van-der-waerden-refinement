#!/usr/bin/env python3
"""Checks accompanying an adversarial audit of the short-period note (PR #7) and of PR #12.

Base commit 63bef9ca996786a41169de4a0c3d6b3b47b0fe96; PR #12 head 029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5;
PR #9 head 89660352f5dfcf1180a47b224610d444b2ce8701. Standard library only, no network.
Run with `python3 -B verify.py` (assertions are load-bearing; never run with -O).

Part A, exact (fractions): every asymptotic side condition that the c = 1/9 chain uses
(source, sharpened region, repeated-key, digit-rank and short-period notes), written as
a strict linear inequality in the exponents (a, m, b). Each one is checked at the explicit
1/9 tuple, and shown to hold on the whole open region 0 < b < a, 2a < m < 1 by maximising
its left side over the vertices of the closed region. Negative controls: each condition
fails somewhere outside the region.

Part B, finite numeric (decimal, 90 digits, log space): the 35 explicit inequalities of
PR #12, Sections 4 to 9, recomputed from its definitions (ceilings and floors included) at
every integer t = log k in [512, 4096] and at five larger t. This is a finite replay; PR #12's
own verify.py carries the all-larger-t monomial certificates.

Part C, finite numeric: PR #12's Appendix A error E = 10k + 100Dt + 6 log q against the
explicit factor formulas of PR #9, Sections 7 and 8, at PR #12's variable scales, on the
same grid. The encodings that produce those factors are not re-proved here.
"""
from decimal import Decimal as Dec, getcontext, MAX_EMAX, MIN_EMIN, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Q
from itertools import combinations
import json
import sys

# --------------------------------------------------------------------------------------
# Part A. Side-condition ledger in exponent form.
# A condition is (label, origin, coefficients (ca, cm, cb), rhs) meaning ca*a+cm*m+cb*b < rhs.
LEDGER = [
    ("a<m", "source Sec. 2 and sharpened Change 1: h_0 = D L^2 < 2M", (1, -1, 0), 0),
    ("2a<m", "first local-lemma family: log T_glob = O(k^{2a} log^3 k) = o(M)", (2, -1, 0), 0),
    ("m<1", "drift lemma m_*-1 >= k/(2M); 2M/k <= 1/16; coverage k-h-delta k", (0, 1, 0), 1),
    ("m<2", "path lemma (1-2MH)/(2M) > H; heavy-width 2H+4MH/h < 1; 4MH/h < 1/2; Lemma 1 2MH_x < 1/2", (0, 1, 0), 2),
    ("m<3", "drift lemma |v - lambda u| <= 6MH/k < 1", (0, 1, 0), 3),
    ("a+m<3", "long periods: rotating drift 4MH/k < eta = eps_reg/(8D)", (1, 1, 0), 3),
    ("a<1", "Lemma C/C*: 4D(k+2)q/k^2 < q/8 and 3|v|_1/k^2 < 1; errors O(D log k) = o(k log k)", (1, 0, 0), 1),
    ("-a<0", "errors O(log q) = O(c k^{1-a} log k) = o(k log k); case (i) key words", (-1, 0, 0), 0),
    ("b<a", "short period, case (ii): 6 log q = O(k^{1-a} log k) = o(pk)", (-1, 0, 1), 0),
    ("a+b<1", "short period, case (ii): V-box word O(D log k) and run code O(D log^3 k) = o(pk)", (1, 0, 1), 1),
    ("-b<0", "p = k^{-b} <= 1/2 eventually", (0, 0, -1), 0),
]
# Closed region: 0 <= b <= a, 2a <= m <= 1 (a >= 0 follows). As cons: alpha.(a,m,b) <= r.
REGION = [((0, 0, -1), 0), ((-1, 0, 1), 0), ((2, -1, 0), 0), ((0, 1, 0), 1)]
TUPLE_1_9 = {"a": Q(49, 100), "m": Q(99, 100), "b": Q(97, 200)}


def solve3(rows, rhs):
    """Exact solution of a 3x3 system by Cramer's rule, or None if singular."""
    def det(M):
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    M = [[Q(x) for x in r] for r in rows]
    d = det(M)
    if d == 0:
        return None
    sol = []
    for j in range(3):
        Mj = [r[:] for r in M]
        for i in range(3):
            Mj[i][j] = Q(rhs[i])
        sol.append(det(Mj) / d)
    return sol


def vertices(cons):
    out = set()
    for trio in combinations(cons, 3):
        x = solve3([c for c, _ in trio], [r for _, r in trio])
        if x is not None and all(sum(Q(ci) * xi for ci, xi in zip(c, x)) <= r for c, r in cons):
            out.add(tuple(x))
    return sorted(out)


def part_a():
    vs = vertices(REGION)
    assert len(vs) >= 4, vs
    rows = []
    for label, origin, (ca, cm, cb), rhs in LEDGER:
        a, m, b = TUPLE_1_9["a"], TUPLE_1_9["m"], TUPLE_1_9["b"]
        margin = Q(rhs) - (ca * a + cm * m + cb * b)
        assert margin > 0, (label, margin)
        sup = max(ca * x[0] + cm * x[1] + cb * x[2] for x in vs)
        # A non-constant linear function attains its supremum over the open region only on
        # the boundary, so sup <= rhs over the closure gives the strict inequality inside.
        assert sup <= rhs, (label, sup)
        rows.append({"condition": label, "origin": origin, "margin_at_1_9": str(margin),
                     "sup_over_region": str(sup), "rhs": str(rhs)})
    # Negative controls: each condition except the two that define the region itself
    # (b<a and 2a<m) and the trivially-implied ones has a violating point just outside.
    controls = {
        "b<a": {"a": Q(1, 4), "m": Q(3, 4), "b": Q(1, 4)},
        "2a<m": {"a": Q(1, 2), "m": Q(1), "b": Q(1, 4)},
        "a+b<1": {"a": Q(1, 2), "m": Q(1), "b": Q(1, 2)},
        "a<1": {"a": Q(1), "m": Q(1), "b": Q(1, 2)},
    }
    rejected = 0
    for label, pt in controls.items():
        ca, cm, cb = next(c for lab, _, c, _ in LEDGER if lab == label)
        rhs = next(r for lab, _, _, r in LEDGER if lab == label)
        assert not (ca * pt["a"] + cm * pt["m"] + cb * pt["b"] < rhs), label
        rejected += 1
    # The region's own supremum of b is 1/2, hence c < gamma*b/2 < 1/8 (PR #7).
    assert max(x[2] for x in vs) == Q(1, 2)
    return {"conditions": rows, "region_vertices": [[str(c) for c in v] for v in vs],
            "negative_controls_rejected": rejected}


# --------------------------------------------------------------------------------------
# Part B and C. PR #12 at its variable scales.
getcontext().prec = 90
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN
ONE, TWO = Dec(1), Dec(2)
LN2, LN3, LN9 = TWO.ln(), Dec(3).ln(), Dec(9).ln()
TOL = ONE - Dec(10) ** -60  # one-ulp slack for exact identities evaluated at 90 digits


def ceil(x):
    return x.to_integral_value(rounding=ROUND_CEILING)


def floor(x):
    return x.to_integral_value(rounding=ROUND_FLOOR)


def ln(x):
    return x.ln()


def lse(x, y):
    """log(e^x + e^y)."""
    hi, lo = (x, y) if x >= y else (y, x)
    return hi + (ONE + (lo - hi).exp()).ln()


def pr12_scales(t):
    t = Dec(t)
    k = t.exp()
    sk = (t / 2).exp()
    u = sk / (4096 * t**3)
    D = ceil(u)
    M = floor(k / t)
    h0 = ceil(256 * D * t**3)
    Ms = ceil(4096 * D * t)
    logp = ln(Dec(65536)) + 4 * ln(t) - t / 2
    F = k * (t / 8 - ln(t) - 20)
    logP = LN2 + 2 * t                      # worst source prime P <= 2k^2
    Q_hi = F / D + logP                      # q least power of P with D log q >= F
    return dict(t=t, k=k, sk=sk, u=u, D=D, M=M, h0=h0, Ms=Ms, eta=ONE / (8 * D * t),
                gamma=ONE / 2 - 4 / t, logp=logp, L=-logp, F=F, logP=logP, Q=Q_hi,
                DlogQ=F + D * logP)


def part_b(t):
    s = pr12_scales(t)
    t, k, sk, u, D, M, h0, Ms = (s[x] for x in ("t", "k", "sk", "u", "D", "M", "h0", "Ms"))
    eta, gamma, L, F, Qh = s["eta"], s["gamma"], s["L"], s["F"], s["Q"]
    p = s["logp"].exp()
    c = {}
    c["(14) u>=1"] = u >= 1
    c["(14) D<=2u"] = D <= 2 * u
    c["(14) M>=k/(2t)"] = M >= k / (2 * t)
    c["(14) sqrt(k)/16<=h0<=sqrt(k)/4"] = sk / 16 * TOL <= h0 <= sk / 4
    c["(14) Ms<=4097Dt<=k"] = Ms <= 4097 * D * t <= k
    c["(15) D<=k/64"] = D <= k / 64
    c["(15) p<=1/2"] = p <= ONE / 2
    c["(15) Q<=512sqrt(k)t^4+3t"] = Qh <= 512 * sk * t**4 + 3 * t
    c["(15) 6Q+100Dt<=k"] = 6 * Qh + 100 * D * t <= k
    c["(13) log P<=3t"] = s["logP"] <= 3 * t
    c["(16) L>=t/4"] = L >= t / 4
    c["(16) F>=kt/32"] = F >= k * t / 32
    logJ = LN2 + 2 * t + ln((D + 1) * Qh) + Dec(10) ** -40   # J <= 2k^2 (D+1) log q + 2
    c["(4) J<=k^6"] = logJ <= 6 * t
    c["(17) 2M/k<=1/16"] = 2 * M / k <= ONE / 16
    c["(17) 4MH/k<=eta"] = 4 * M / k**3 <= eta
    c["(17) D(4eta+1/h0)<=1/t"] = D * (4 * eta + ONE / h0) <= ONE / t
    loglam = 10 * h0 / ln(h0) * ln(2 * M)                       # (9)-(10)
    c["(11) log lambda<=60h0"] = loglam <= 60 * h0
    logTglob = 2 * D * (LN9 + 2 * (LN3 + 2 * t + lse(2 * t + loglam, 6 * t) + Dec(10) ** -40))
    c["(18) log T_glob<=k/(16t^3)"] = logTglob <= k / (16 * t**3)
    B0 = ceil(128 * t + 4)
    h = 2 * M
    logAh = (D + 1) * ln(h) + 2 * D * (LN9 + 2 * ln(B0 * D * h + 1))
    c["(19) log A_h<=15Dt at h=2M"] = logAh <= 15 * D * t
    logAs = t + (D + 1) * ln(h0) + D * (LN9 + 2 * ln(k * (4 * M + 4) + 1)) \
        + D * (LN9 + 2 * (LN2 + t + logJ + Dec(10) ** -40))
    c["(20) log A_s<=40Dt"] = logAs <= 40 * D * t
    c["(23) I1<=1/(48k)"] = logTglob - M / t**2 <= -ln(Dec(48)) - t
    c["(23) 15Dt<=h0/(16t^2)"] = 15 * D * t <= h0 / (16 * t**2)
    c["(23) I2=k e^{-112Dt}<=1/(48k)"] = t - 112 * D * t <= -ln(Dec(48)) - t
    c["(23) I3<=1/(48k)"] = logAs - Ms / 32 <= -ln(Dec(48)) - t
    Gamma = gamma * k * L / 2 - s["DlogQ"]
    E = 10 * k + 100 * D * t + 6 * Qh
    c["(26) Gamma>=14k"] = Gamma >= 14 * k
    c["(28) E<=11k"] = E <= 11 * k
    c["(28) 4(D+1)e^{E-Gamma}<1/4"] = ln(4 * (D + 1)) + E - Gamma < -ln(Dec(4))
    logTK_noq = D * (LN9 + 2 * (LN3 + 2 * t + logJ + Dec(10) ** -40)) + ln(Dec(16)) \
        + 3 * (t + ln(D) + 3 / k**2)                                   # log T_K - 6 log q
    logTK = logTK_noq + 6 * Qh
    c["(8) log T_K<=6Q+32Dt"] = logTK_noq <= 32 * D * t
    c["(8) log T_K<=k"] = logTK <= k
    c["(29) 2 T_K 2^k p^{k/16}<1/4"] = LN2 + logTK + k * LN2 - k * L / 16 < -ln(Dec(4))
    logBrun = ln(h0) + ln(Ms + 1) + Ms * (LN2 + 3 * t)
    c["(31) log B_run<=3t+4Ms t"] = logBrun <= 3 * t + 4 * Ms * t
    c["(31) log T_K+log B_run+log 8<pk/16"] = logTK + logBrun + ln(Dec(8)) < p * k / 16
    c["(31) total<1/4"] = LN2 + logTK + logBrun - p * k / 4 < -ln(Dec(4))
    if t >= 2048:
        c["(2) F>=kt/9"] = F >= k * t / 9
    return c


def part_c(t):
    """PR #9 Sections 7.3, 7.12, 8.2, 8.3 factors against PR #12 Appendix A, at PR #12 scales."""
    s = pr12_scales(t)
    t, k, D, Qh = s["t"], s["k"], s["D"], s["Q"]
    logJ = LN2 + 2 * t + ln((D + 1) * Qh) + Dec(10) ** -40
    logTaug = D * (LN9 + 2 * (ln(Dec(6)) + 2 * t + logJ + Dec(10) ** -40))      # (7.6)
    logBdisc = (D + 1) * t + logTaug + k * 2 * LN2                               # (7.7)
    Kh = k                                    # K_h = ceil(k/h) <= k for h >= 1
    # s_G + 1 <= kDq^2 (1 + 32/k) since (8Dk+4k+20)/(D q^2) <= 32/k for q > k
    # log(s_G + 1) <= t + log D + 2 log q + 32/k, used below with 2 log q cancelled
    log_sphi1 = ln(k * (4 * D * k + 7) + 1)
    log_sx1 = ln(2 * k**2 * (2 * Kh + 5) ** 2 + 1)
    # Terms in log q are cancelled exactly on both sides before comparing: 6 log q has
    # about 120 digits at t = 512, so a residual 9t would fall below 90-digit precision.
    # Each row is (left side minus its q-term, right side minus the same q-term).
    rows = {
        "discrete data <= 21Dt+2k": (logBdisc, 21 * D * t + 2 * k),
        "integer projections D log(3Dk) <= 3Dt": (D * ln(3 * D * k), 3 * D * t),
        "first arrangement 16(s_G+1)^3 <= 6log q+9t": (ln(Dec(16)) + 3 * (t + ln(D) + 32 / k), 9 * t),
        "tail arrangement (D+4)^2(s_phi+1)^(D+3) <= 20Dt": (2 * ln(D + 4) + (D + 3) * log_sphi1, 20 * D * t),
        "crossing arrangement (D+4)^2(s_x+1)^(D+3) <= 28Dt": (2 * ln(D + 4) + (D + 3) * log_sx1, 28 * D * t),
        "classes and subsets 256^k 2^k <= 7k": (9 * k * LN2, 7 * k),
    }
    c = {name: lhs <= rhs for name, (lhs, rhs) in rows.items()}
    # E - 6 log q = 10k + 100Dt; the certificate excess minus 6 log q must stay below it.
    cert_excess_noq = sum(lhs for lhs, _ in rows.values())
    c["certificate excess <= 6log q+81Dt+9k < E"] = cert_excess_noq <= 81 * D * t + 9 * k < 10 * k + 100 * D * t
    prog_excess_noq = logBdisc + ln(Dec(100)) + 2 * ln(D) + D * LN9                # (8.6) minus 4 log q
    c["progression excess <= 4log q+26Dt+2k < E"] = prog_excess_noq <= 26 * D * t + 2 * k \
        and 4 * Qh + 26 * D * t + 2 * k < 10 * k + 100 * D * t + 6 * Qh
    return c


def main():
    out = {"part_a_short_period_ledger": part_a()}
    grid = list(range(512, 4097)) + [5000, 10**4, 3 * 10**4, 10**5, 10**6]
    fails_b, fails_c, nb, nc = [], [], 0, 0
    for t in grid:
        cb, cc = part_b(t), part_c(t)
        nb += len(cb)
        nc += len(cc)
        fails_b += [(t, name) for name, ok in cb.items() if not ok]
        fails_c += [(t, name) for name, ok in cc.items() if not ok]
    assert not fails_b, fails_b[:10]
    assert not fails_c, fails_c[:10]
    # Negative control for Part B: PR #12's scale D ~ sqrt(k)/(4096 t^3) is needed; with the
    # constant 4096 replaced by 64 the global-word inequality (18) must fail at t = 512.
    s = pr12_scales(512)
    D64 = ceil(s["sk"] / (64 * s["t"] ** 3))
    h064 = ceil(256 * D64 * s["t"] ** 3)
    assert not (240 * D64 * h064 + 42 * D64 * s["t"] <= s["k"] / (16 * s["t"] ** 3))
    # Negative control for Part C: the 6 log q term of E is load-bearing, since the
    # first arrangement factor alone exceeds the whole 100Dt budget.
    s = pr12_scales(512)
    first_arrangement = ln(Dec(16)) + 3 * (s["t"] + ln(s["D"]) + 2 * s["Q"])
    assert first_arrangement > 100 * s["D"] * s["t"]
    out["part_b_pr12_inequalities"] = {"t_values": len(grid), "t_range": "every integer in [512,4096] and 5000, 1e4, 3e4, 1e5, 1e6",
                                       "checks": nb, "failures": 0}
    out["part_c_pr12_appendix_a_vs_pr9"] = {"t_values": len(grid), "checks": nc, "failures": 0}
    out["negative_controls"] = {"part_a": out["part_a_short_period_ledger"]["negative_controls_rejected"],
                                "part_b_scale_4096_needed": 1, "part_c_6logq_needed": 1}
    json.dump(out, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
