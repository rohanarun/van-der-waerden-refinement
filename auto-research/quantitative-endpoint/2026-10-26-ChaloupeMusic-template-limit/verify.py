#!/usr/bin/env python3
"""Checks for the template limit (PROOF.md). Not a formal proof.

Base: the composed endpoint (2026-10-20-ChaloupeMusic-composed-endpoint, head ebfae63) on PR #12 head
029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5. Standard library only, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0 and standard output byte-identical to RESULT.json. Assertions are load-bearing; never -O.

1. C* of Theorem B in each tier, enclosed by certified rational bounds for logarithms, and its gap to the
   delivered constants.
2. The exact identities of the proof: (1/2) log 288 + log(3/2) = log(18 sqrt 2), the expansion (7), and
   the minimum of x/4 + (B/2) e^{-x}.
3. Evidence only: a numerical optimisation of (T1)-(T6) at finite t (40-digit decimals). The best constant
   the template allows at t increases towards C* from below, and the optimal tolerances are near 1/t.
4. Negative controls and file integrity.
"""
import hashlib
import json
import math
import sys
from decimal import Decimal as Dec, getcontext, MAX_EMAX, MIN_EMIN
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = {}
TIERS = [
    {"name": "D2", "label": "Lemma D'': 45^(k/2)", "base": 45, "exp": Q(1, 2), "C": Q(71, 20)},
    {"name": "D1", "label": "Lemma D': 19^k", "base": 19, "exp": Q(1), "C": Q(403, 100)},
    {"name": "D0", "label": "N1a's Lemma D: 37^k", "base": 37, "exp": Q(1), "C": Q(35, 8)},
]


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def pow2(n):
    return Q(1 << n) if n >= 0 else Q(1, 1 << (-n))


def dec_floor(x, digits=6):
    n = math.floor(x * 10 ** digits)
    return f"{n // 10 ** digits}.{n % 10 ** digits:0{digits}d}"


def dec_ceil(x, digits=6):
    n = math.ceil(x * 10 ** digits)
    return f"{n // 10 ** digits}.{n % 10 ** digits:0{digits}d}"


# ---------------------------------------------------------------- certified logarithms
def ln2_bounds(N=80):
    s = sum(Q(1, n * 2 ** n) for n in range(1, N + 1))
    return s, s + Q(1, (N + 1) * 2 ** N)


def ln_bounds(y, N=80):
    """Enclosure of log y for 1 <= y < 2: atanh series with a geometric tail."""
    y = Q(y)
    z = (y - 1) / (y + 1)
    s = 2 * sum(z ** (2 * m + 1) / (2 * m + 1) for m in range(N))
    return s, s + 2 * z ** (2 * N + 1) / ((2 * N + 1) * (1 - z * z))


def ln_enclose(y):
    y = Q(y)
    require(y >= 1, "ln_enclose needs y >= 1")
    e = 0
    while pow2(e + 1) <= y:
        e += 1
    lo2, up2 = ln2_bounds()
    lo, up = ln_bounds(y / pow2(e))
    return e * lo2 + lo, e * up2 + up


def cstar_enclosure(tier):
    """C* = (1/2)(log 10 + l_cls) + 1/2 + (1/4)(log 18 + (1/2) log 2), with l_cls = exp * log(base)."""
    l10, lb, l18, l2 = (ln_enclose(x) for x in (10, tier["base"], 18, 2))
    lo = (l10[0] + tier["exp"] * lb[0]) / 2 + Q(1, 2) + (l18[0] + l2[0] / 2) / 4
    up = (l10[1] + tier["exp"] * lb[1]) / 2 + Q(1, 2) + (l18[1] + l2[1] / 2) / 4
    require(up - lo < Q(1, 10 ** 15), "enclosure too wide")
    return lo, up


def part1():
    out = {}
    for tier in TIERS:
        lo, up = cstar_enclosure(tier)
        gap = tier["C"] - up
        require(gap > 0, f"delivered C below C* ({tier['name']})")
        out[tier["name"]] = {"assumption": tier["label"], "C_star_lower": dec_floor(lo, 8),
                             "C_star_upper": dec_ceil(up, 8), "delivered_C": str(tier["C"]),
                             "gap_lower": dec_floor(gap, 4)}
    return out


# ---------------------------------------------------------------- 2. identities
def part2():
    # (1/2) log 288 + log(3/2) = log(18 sqrt 2)  <=>  288 (3/2)^2 = (18 sqrt 2)^2 = 648
    require(288 * Q(3, 2) ** 2 == 648 == 18 ** 2 * 2, "log(18 sqrt 2) identity")
    # (7): (1/2)(1/2 - e1 - e2)(B - x1 - x2) = B/4 - sum_i (x_i/4 + (e_i/2)(B - x1 - x2)), as polynomials
    pts = 0
    for B in (Q(7), Q(-3, 2), Q(100)):
        for e1 in (Q(1, 3), Q(1, 50)):
            for e2 in (Q(0), Q(1, 7)):
                for x1 in (Q(0), Q(2)):
                    for x2 in (Q(1, 2), Q(5)):
                        lhs = Q(1, 2) * (Q(1, 2) - e1 - e2) * (B - x1 - x2)
                        rhs = B / 4 - sum(x / 4 + e / 2 * (B - x1 - x2) for x, e in ((x1, e1), (x2, e2)))
                        require(lhs == rhs, "expansion (7)")
                        pts += 1
    # min_x x/4 + (B/2) e^{-x} = (1 + log 2B)/4 at e^{-x} = 1/(2B): checked against a dense grid
    getcontext().prec = 50
    mins = 0
    for B in (Dec(10), Dec(256), Dec(10 ** 6)):
        xs = (2 * B).ln()
        val = xs / 4 + B / 2 * (-xs).exp()
        require(abs(val - (1 + (2 * B).ln()) / 4) < Dec(10) ** -40, "closed form of the minimum")
        for j in range(-400, 401):
            x = xs + Dec(j) / 100
            require(x / 4 + B / 2 * (-x).exp() >= val - Dec(10) ** -40, "minimum is global on the grid")
            mins += 1
    return {"expansion_points": pts, "minimum_grid_points": mins}


# ---------------------------------------------------------------- 3. finite-t optimisation (evidence)
def template_fmax(t, estar, lines=4, tol_grid=None):
    """Largest f = F/k allowed by (T1)-(T6), maximised over tolerances eps_i = s_i/t on a grid and D by
    bisection. Uses theta(x) >= x (1 - 1/(2 log x)) (Rosser-Schoenfeld) as the weakest form of (T2), and
    the entropy (D+1) log h + 4D log(Dh) of (T3); lines != 4 is a control."""
    t = Dec(t)
    k = t.exp()
    grid = tol_grid or [Dec(x) / 10 for x in range(8, 14)]
    best = None
    for s1 in grid:
        for s2 in grid:
            e1, e2 = s1 / t, s2 / t
            lo, hi = Dec(1), k.sqrt()
            for _ in range(70):
                D = (lo * hi).sqrt()
                h = D * 4 * t / e2 ** 2
                for _ in range(12):
                    lh = h.ln()
                    h = ((D + 1) * lh + lines * D * (D * h).ln()) / e2 ** 2 - 1      # least h = h_0 + 1 in (T3)
                theta = (h - 1) * (1 - 1 / (2 * (h - 1).ln()))
                if 4 * D * theta <= k * e1 ** 2 / 16:
                    lo = D
                else:
                    hi = D
            D = lo
            gamma = Dec(1) / 2 - e1 - e2
            f = t / 8
            for _ in range(30):
                f = gamma * (D / (12 * f)).ln() / 2 - estar
            if best is None or f > best[0]:
                best = (f, s1, s2)
    return best


def part3():
    getcontext().prec = 40
    getcontext().Emax = MAX_EMAX
    getcontext().Emin = MIN_EMIN
    tier = TIERS[0]
    lo, up = cstar_enclosure(tier)
    cs = Dec(lo.numerator) / Dec(lo.denominator)
    estar = ((Dec(10).ln() + Dec(tier["exp"].numerator) / Dec(tier["exp"].denominator) * Dec(tier["base"]).ln())
             / 2)
    rows, prev = {}, None
    for tt in (256, 512, 1000, 10 ** 4, 10 ** 6):
        f, s1, s2 = template_fmax(tt, estar)
        c = Dec(tt) / 8 - Dec(7) / 8 * Dec(tt).ln() - f
        require(c < cs, "finite-t constant above C*")
        require(prev is None or c > prev, "finite-t constant not increasing")
        require(Dec("0.8") <= s1 <= Dec("1.3") and Dec("0.8") <= s2 <= Dec("1.3"), "optimal tolerances far from 1/t")
        require(Dec(tier["C"].numerator) / tier["C"].denominator >= c, "delivered C below the template's best")
        CACHE[tt] = f
        rows[str(tt)] = {"best_C_at_t": f"{c:.5f}", "eps1_times_t": str(s1), "eps2_times_t": str(s2)}
        prev = c
    require(cs - prev < Dec("0.001"), "no convergence to C* by t = 10^6")
    return {"tier": tier["name"], "C_star": f"{cs:.6f}", "rows": rows}, estar


# ---------------------------------------------------------------- 4. controls and integrity
def part4(estar):
    getcontext().prec = 40
    tt = 10 ** 6
    f = CACHE[tt]
    c = Dec(tt) / 8 - Dec(7) / 8 * Dec(tt).ln() - f
    rej = {}
    # C* with 12 sqrt 2 (dropping the factor 3/2 of Step 1) or with 18 (dropping sqrt 2) misses the limit
    for name, const in (("C*_with_12sqrt2", 12 * Dec(2).sqrt()), ("C*_with_18", Dec(18))):
        alt = estar + Dec(1) / 2 + const.ln() / 4
        rej[name] = abs(alt - c) > Dec("0.01")
    # tolerances held at 2/t: the best constant moves by more than 0.05 (the 1/t balance is load-bearing)
    f2, _, _ = template_fmax(tt, estar, tol_grid=[Dec(2)])
    rej["tolerances_2/t"] = (f - f2) > Dec("0.05")
    # an entropy with 2 comparison-line factors instead of 4 moves the limit (the 18 sqrt 2 is the entropy's)
    f3, _, _ = template_fmax(tt, estar, lines=2)
    rej["entropy_2_lines"] = (f3 - f) > Dec("0.05")
    require(all(rej.values()), f"negative control not rejected: {rej}")
    return rej


def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(name for name in manifest if name != "RESULT.json")


def main():
    p3, estar = part3()
    report = {
        "base": {"composed_head": "ebfae63", "pr12_head": "029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5"},
        "C_star": part1(),
        "identities": part2(),
        "finite_t_evidence": p3,
        "negative_controls_rejected": part4(estar),
        "integrity_files": integrity(),
        "conclusion": "Within the template (T1)-(T6) of PR #12, N1b and the composed endpoint, F/k <= t/8 - "
                      "(7/8) log t - C* + o(1): no theta < 7/8, and C >= C* = (1/2)(log 10 + l_cls) + 1/2 + "
                      "(1/4) log(18 sqrt 2), that is 3.41219 under Lemma D''",
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
