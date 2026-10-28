#!/usr/bin/env python3
"""Rich-cover barrier: exact checks and scoped measurements.

Base commit: 63bef9ca996786a41169de4a0c3d6b3b47b0fe96 (on review/binding-lever).
Standard library only. Run:  python3 -B verify.py      (assertions are load-bearing; never -O)
Regenerate RESULT.json:      python3 -B verify.py --write

Notation (README.md): a progression has y-representatives A + tB - w_t with
w_t = round(A + tB) in Z^D (wrap vectors); its relaxed band rows are
    r_t = (-2 w_t, -2 t w_t, 1, 2t, t^2)  in Z^(2D+3),
so that |A + tB - w_t|^2 = <r_t, z> + |w_t|^2 for z = (A, B, |A|^2, <A,B>, |B|^2).

Checks:
 1. linear rigidity fails, with an exact certificate (Dirichlet mechanism);
 2. along the certified null direction the true bands still move (first order);
 3. rank deficits of the rows on s0-sets: two positive controls (affine,
    quasi-affine) and generic progressions (searched and random sets);
 4. elementary bounds used by the proposition on small exact instances
    (box fibres, lattice separation, Gram determinant >= 1);
 5. the bookkeeping of the proposition at one sample parameter point.
"""
import itertools, json, math, random, sys
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path

P61 = (1 << 61) - 1
HERE = Path(__file__).resolve().parent

def frac_vec(rng, D, lo=Q(-1, 2), width=Q(1)):
    den = 1 << 30
    return [lo + width * Q(rng.randrange(den), den) for _ in range(D)]

def wraps(A, B, k):
    return [[math.floor(a + t * b + Q(1, 2)) for a, b in zip(A, B)] for t in range(k)]

def rows(W):
    return [[-2 * x for x in w] + [-2 * t * x for x in w] + [1, 2 * t, t * t]
            for t, w in enumerate(W)]

def rank_mod(R):
    """Rank modulo 2^61-1: a lower bound for the rational rank (equal unless an
    accidental cancellation mod P61 occurs)."""
    M = [[x % P61 for x in r] for r in R]
    r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = pow(M[r][c], P61 - 2, P61)
        M[r] = [x * inv % P61 for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(x - f * y) % P61 for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r

def dirichlet_g(B):
    """g in {-1,0,1}^D, g != 0, with |<g,B>| <= D 2^-D (pigeonhole on {0,1}^D sums)."""
    D = len(B)
    sums = sorted((sum(b for b, e in zip(B, eps) if e), eps)
                  for eps in itertools.product((0, 1), repeat=D))
    best = min(range(len(sums) - 1), key=lambda i: sums[i + 1][0] - sums[i][0])
    g = [x - y for x, y in zip(sums[best + 1][1], sums[best][1])]
    gap = sums[best + 1][0] - sums[best][0]
    assert any(g) and gap <= Q(D, 2 ** D) + Q(1, 2 ** 25)
    return g, gap

# ---------------------------------------------------------------- check 1, 2
def check_linear_rigidity_fails(D, k, seed):
    rng = random.Random(seed)
    A, B = frac_vec(rng, D), frac_vec(rng, D)
    W = wraps(A, B, k)
    R = rows(W)
    g, gap = dirichlet_g(B)
    vals = [sum(x * y for x, y in zip(g, w)) for w in W]
    distinct = sorted(set(vals))
    m = max(distinct, key=vals.count)
    J = [t for t in range(k) if vals[t] == m]
    n = 2 * D + 3
    # exact certificate: two independent null vectors on J
    for u, v in ((1, 0), (0, 1)):
        h = [u * x for x in g] + [v * x for x in g] + [2 * u * m, v * m, 0]
        assert all(sum(x * y for x, y in zip(R[t], h)) == 0 for t in J)
    # first-order band change along (dA, dB) = (u g, v g): 2(u + v t)<phi_t, g>,
    # <phi_t, g> = <g,A> - m + t<g,B> on J: vanishes at most once
    gA = sum(x * a for x, a in zip(g, A))
    gB = sum(x * b for x, b in zip(g, B))
    zeros = sum(1 for t in J if gA - m + t * gB == 0)
    assert zeros <= 1
    return {"D": D, "k": k, "seed": seed, "g": g, "|<g,B>|": str(abs(gap)),
            "values_of_<g,w_t>": len(distinct), "|J_m|": len(J),
            "k/(D+2)": round(k / (D + 2), 2), "rank_on_J_at_most": n - 2,
            "first_order_band_zeros_on_J": zeros,
            "pigeonhole_guaranteed": 2 ** D > D * k}

# ---------------------------------------------------------------- check 3
def deficit_search(D, k, s0, seed, mode, ntop=40, rmax=6, cap=400):
    rng = random.Random(seed)
    n = 2 * D + 3
    A, B = frac_vec(rng, D), frac_vec(rng, D)
    if mode != "generic":
        r = int(mode.split("=")[1])
        for i in range(r, D):     # non-wrapping coordinates: tiny step, far from the cut
            B[i] = Q(rng.randrange(-400, 401), 1000 * k)
            A[i] = Q(rng.randrange(-50, 51), 1000)
    W = wraps(A, B, k)
    R = rows(W)
    out = {"D": D, "k": k, "s0": s0, "seed": seed, "mode": mode,
           "rank_all_positions": rank_mod(R)}
    rand_def = max(n - rank_mod([R[t] for t in rng.sample(range(k), s0)]) for _ in range(20))
    out["max_deficit_20_random_sets"] = rand_def
    if mode != "generic":
        out["expected_deficit_at_least"] = 2 * (D - int(mode.split("=")[1]))
        assert rand_def >= out["expected_deficit_at_least"]
        return out
    G = [g for g in itertools.product((-1, 0, 1), repeat=D) if any(g)]
    G.sort(key=lambda g: abs(sum(x * b for x, b in zip(g, B))))
    G = G[:3000]
    lev = []
    for g in G:
        vals = [sum(x * y for x, y in zip(g, w)) for w in W]
        best = max(set(vals), key=vals.count)
        lev.append((vals.count(best), [t for t in range(k) if vals[t] == best]))
    lev.sort(key=lambda x: -x[0])
    lev = lev[:ntop]
    worst, tried = 0, 0
    for r in range(1, rmax + 1):
        cands = 0
        for combo in itertools.combinations(range(len(lev)), r):
            J = set(lev[combo[0]][1])
            for i in combo[1:]:
                J &= set(lev[i][1])
            if len(J) >= s0:
                Js = sorted(J)[:s0]
                worst = max(worst, n - rank_mod([R[t] for t in Js]))
                tried += 1
                cands += 1
                if cands >= cap:
                    break
        if tried >= cap:
            break
    out["searched_sets"] = tried
    out["max_deficit_searched_sets"] = worst
    return out

# ---------------------------------------------------------------- check 4
def ytilde(nn, q, D):
    return [((Q(nn, q ** i) + Q(1, 2)) % 1) - Q(1, 2) for i in range(1, D + 1)]

def check_small_instances(q=29, D=3, seed=7):
    rng = random.Random(seed)
    N = q ** D
    Y = [ytilde(nn, q, D) for nn in range(N)]
    # box fibres: #{n : y~(n) in prod I_i} <= prod (q|I_i| + 1)
    worst_ratio = Q(0)
    for _ in range(200):
        boxes = []
        for _ in range(D):
            lo = Q(rng.randrange(-500, 400), 1000)
            boxes.append((lo, lo + Q(rng.randrange(1, 100), 1000)))
        cnt = sum(1 for y in Y if all(lo <= c < hi for c, (lo, hi) in zip(y, boxes)))
        bound = 1
        for lo, hi in boxes:
            bound *= math.floor(q * (hi - lo)) + 1
        assert cnt <= bound
        worst_ratio = max(worst_ratio, Q(cnt, bound))
    # lattice separation: |y~(n) - y~(n')| >= 1/q for n != n' (squared, exact)
    minsq = min(sum((a - b) ** 2 for a, b in zip(Y[i], Y[j]))
                for i in range(N) for j in rng.sample(range(N), 30) if i != j)
    assert minsq >= Q(1, q * q)
    # Gram determinant of independent integer rows is an integer >= 1 (Cauchy-Binet)
    def bareiss_det(M):
        M = [r[:] for r in M]; n = len(M); prev = 1; sign = 1
        for c in range(n - 1):
            p = next((i for i in range(c, n) if M[i][c]), None)
            if p is None:
                return 0
            if p != c:
                M[c], M[p] = M[p], M[c]; sign = -sign
            for i in range(c + 1, n):
                for j in range(c + 1, n):
                    M[i][j] = (M[i][j] * M[c][c] - M[i][c] * M[c][j]) // prev
            prev = M[c][c]
        return sign * M[n - 1][n - 1]
    grams = []
    for s in range(5):
        A, B = frac_vec(rng, 4), frac_vec(rng, 4)
        R = rows(wraps(A, B, 60))
        sel = rng.sample(range(60), 9)
        Rs = [R[t] for t in sel]
        if rank_mod(Rs) < 9:
            continue
        Gm = [[sum(x * y for x, y in zip(a, b)) for b in Rs] for a in Rs]
        d = bareiss_det(Gm)
        assert d >= 1
        grams.append(d.bit_length())
    return {"q": q, "D": D, "box_fibre_max_count_over_bound": str(worst_ratio),
            "min_sq_separation_times_q2": str(minsq * q * q), "gram_det_bits": grams}

# ---------------------------------------------------------------- check 5
def check_bookkeeping(a=Q(49, 100), b=Q(97, 200), c=Q(13, 100), theta=Q(13, 100), log10k=400):
    """The three regimes of the proposition at one sample point, in exact-enough
    Decimal arithmetic on logarithms (no huge integers are formed)."""
    assert c > b / 4 and theta < 2 - b / (2 * c)
    getcontext().prec = 60
    L = Decimal(log10k) * Decimal(10).ln()                    # log k
    k = Decimal(10) ** log10k
    D = (Decimal(a.numerator) / a.denominator * L).exp()     # k^a
    bb, cc, th = (Decimal(x.numerator) / x.denominator for x in (b, c, theta))
    logq = cc * k / D * L + (2 * k * k).ln()                 # q <= 2k^2 k^{ck/D}
    logN = cc * k * L                                        # N >= k^{ck}
    logp = -bb * L
    s0 = int((4 - 2 / L) * D / bb)
    # ln(2/k^2 + 1/q) = ln(2/k^2) + ln(1 + k^2/(2q)) <= ln(2/k^2) + k^2/(2q), and
    # k^2/(2q) <= e^{-230} < 1e-99 here (checked), so 1e-99 is a safe stand-in
    assert logq - 2 * L - Decimal(2).ln() > 230
    box = (Decimal(2) / (k * k)).ln() + Decimal("1e-99")      # >= ln(2/k^2 + 1/q)
    # regime 1: 4k (2/k^2 + 1/q)^D <= p
    r1 = (4 * k).ln() + D * box <= logp
    # regime 2: 4k^2 (2/k^2 + 1/q)^{2D} <= p^{s0-1}
    r2 = (4 * k * k).ln() + 2 * D * box <= (s0 - 1) * logp
    # support of nu: progressions with a repeated V-box are at most
    # k N^2 (4/k^2 + 1/q)^D, a fraction far below 3/4
    rep = L + D * ((Decimal(4) / (k * k)).ln() + Decimal("1e-99"))   # log of the fraction
    r0 = rep <= (Decimal(3) / 4).ln()
    # regime 3: 4 k^{s0}(k+2)^{D s0}(1+4q sqrt D)^{theta D} / N^2 <= p^{k/2}
    lhs3 = Decimal(4).ln() + s0 * L + D * s0 * (k + 2).ln() \
        + th * D * (logq + (4 * D.sqrt()).ln() + Decimal(1)) - 2 * logN
    r3 = lhs3 <= k / 2 * logp
    assert r0 and r1 and r2 and r3
    return {"a": str(a), "b": str(b), "c": str(c), "theta": str(theta), "log10_k": log10k,
            "repeated_box_fraction_below_3/4": r0, "regime1": r1, "regime2": r2, "regime3": r3,
            "regime3_margin_in_units_of_k_log_k": str(((k / 2 * logp - lhs3) / (k * L)).quantize(Decimal("1e-6")))}

# ---------------------------------------------------------------- check 6
def check_flat_reduction(a=Q(49, 100), b=Q(97, 200), c=Q(13, 100), theta=Q(13, 100),
                         delta=Q(1, 2000), log10k=400):
    """Proposition 5' (weaker hypothesis): bookkeeping at one sample point.
    For |S| >= s0 the count uses S0 subset S of size sigma = min(|S|, floor(delta k)),
    positions k^sigma, wrap patterns <= (4 sigma^2 (k+4)^2)^D (faces of a line
    arrangement, one per coordinate), and the tube (1 + 4q sqrt D)^d. Checks:
    (i)  rank >= 4 + floor((1+b+delta) sigma D/(c k)) suffices for s0 <= sigma < delta k;
    (ii) deficit <= theta D on sets of size floor(delta k) suffices for |S| >= delta k;
    (iii) (i) asks only rank >= 4 up to sigma4 = ck/((1+b+delta)D), and the rank-3 exceptions
         (some g <= k/(s0-1) with ||g y~(d)|| < 1/(s0-1)) are a vanishing fraction."""
    assert c > b / 4 and theta < 2 - (delta + b / 2) / c
    getcontext().prec = 500
    L = Decimal(log10k) * Decimal(10).ln()
    k = Decimal(10) ** log10k
    D = (Decimal(a.numerator) / a.denominator * L).exp()
    bb, cc, th, de = (Decimal(x.numerator) / x.denominator for x in (b, c, theta, delta))
    logq_lo = cc * k / D * L                                 # q >= k^{ck/D}
    logq_hi = logq_lo + (2 * k * k).ln()                     # q <= 2k^2 k^{ck/D}
    tube = logq_hi + (4 * D.sqrt()).ln() + 1                 # >= ln(1 + 4q sqrt D)
    s0 = int((4 - 2 / L) * D / bb)
    sig1 = (de * k).to_integral_value(rounding="ROUND_FLOOR")
    def margin(sigma, s, d):                                 # RHS - LHS, must be >= 0
        lhs = Decimal(4).ln() + sigma * L + D * (4 * sigma * sigma * (k + 4) ** 2).ln() \
            + d * tube - 2 * D * logq_lo
        return -bb * s * L - lhs
    x = (1 + bb + de) * D / (cc * k)
    def need_i(sigma):
        return 2 * D - 1 - (x * sigma).to_integral_value(rounding="ROUND_FLOOR")
    grid = [Decimal(s0)]
    while grid[-1] * 2 < sig1:
        grid.append(grid[-1] * 2)
    grid.append(sig1 - 1)
    worst_i = min(margin(sg, sg, need_i(sg)) / (k * L) for sg in grid)
    ok_i = all(margin(sg, sg, need_i(sg)) >= 0 for sg in grid)
    # (ii): worst |S| = k/2 with S0 of size sig1 and deficit theta D
    m2 = margin(sig1, k / 2, (th * D).to_integral_value(rounding="ROUND_FLOOR"))
    ok_ii = m2 >= 0
    # (iii): largest sigma for which deficit 2D-1 (rank 4) passes: bisection
    sigma4 = (cc * k / ((1 + bb + de) * D)).to_integral_value(rounding="ROUND_FLOOR")
    assert need_i(sigma4) == 2 * D - 1 and margin(sigma4, sigma4, 2 * D - 1) >= 0
    # rank-3 exceptions: fraction <= (k/(s0-1)) (2/(s0-1) + 1/q)^D
    exc = (k / (s0 - 1)).ln() + D * ((Decimal(2) / (s0 - 1)).ln() + Decimal("1e-99"))
    ok_iii = sigma4 >= s0 and exc < -L
    assert ok_i and ok_ii and ok_iii
    return {"a": str(a), "b": str(b), "c": str(c), "theta": str(theta), "delta": str(delta),
            "log10_k": log10k, "regime_i_on_dyadic_grid": ok_i, "regime_ii": ok_ii,
            "rank4_suffices_up_to_sigma4": ok_iii,
            "sigma4_times_D_over_ck": str((sigma4 * D / (cc * k)).quantize(Decimal("1e-6"))),
            "log10_rank3_exception_fraction_below": "%.4e" % float(exc / Decimal(10).ln()),
            "regime_i_min_margin_in_units_of_k_log_k": "%.3e" % float(worst_i),
            "regime_ii_margin_in_units_of_k_log_k": str((m2 / (k * L)).quantize(Decimal("1e-6")))}

def main():
    res = {
        "1_linear_rigidity_fails": [check_linear_rigidity_fails(4, 120, 1),
                                    check_linear_rigidity_fails(12, 300, 2),
                                    check_linear_rigidity_fails(12, 300, 3)],
        "3_deficits": [deficit_search(8, 400, 40, 11, "affine wrap=0"),
                       deficit_search(8, 400, 40, 12, "quasi wrap=3"),
                       deficit_search(8, 400, 40, 13, "generic"),
                       deficit_search(8, 400, 40, 14, "generic")],
        "4_small_instances": check_small_instances(),
        "5_bookkeeping": check_bookkeeping(),
        "6_flat_reduction": check_flat_reduction(),
    }
    for d in res["3_deficits"]:
        if d["mode"] == "generic":
            assert d["rank_all_positions"] == 2 * d["D"] + 3
            assert d["max_deficit_20_random_sets"] == 0
    text = json.dumps(res, indent=2, sort_keys=True) + "\n"
    if "--write" in sys.argv:
        (HERE / "RESULT.json").write_text(text)
        print("RESULT.json written")
        return 0
    stored = (HERE / "RESULT.json").read_text()
    assert stored == text, "output differs from RESULT.json"
    print("OK: all checks pass and match RESULT.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
