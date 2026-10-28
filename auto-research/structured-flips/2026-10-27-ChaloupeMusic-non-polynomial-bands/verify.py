"""Exact checks for the non-polynomial bands note (track S1a).

Standard library only, integer arithmetic. Bands follow the source:
y_i(n) = lambda*n / q^i mod 1, centered in [-1/2, 1/2), band = floor(q^2 * sum_i y_i^2).
"""
import hashlib
import json
import random
import sys
from fractions import Fraction
from math import comb, floor
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)


def centered(r, m):
    """Representative of r mod m in [-m/2, m/2)."""
    r %= m
    return r - m if 2 * r >= m else r


def band(n, lam, q, D):
    # q*y_i = c_i / q^(i-1), c_i the centered residue of lam*n mod q^i
    tot = 0
    for i in range(1, D + 1):
        c = centered(lam * n, q ** i)
        tot += c * c * q ** (2 * D - 2 * i)
    return tot // q ** (2 * D - 2)


def diff_coeffs(d):
    # Delta^{d+1} f(j) = sum_i c_i f(j+i)
    return [(-1) ** (d + 1 - i) * comb(d + 1, i) for i in range(d + 2)]


def poly_mod(seq, d, ell):
    """True when seq agrees mod ell with a polynomial of degree <= d."""
    c = diff_coeffs(d)
    return all(sum(ci * seq[j + i] for i, ci in enumerate(c)) % ell == 0
               for j in range(len(seq) - d - 1))


def poly_int(seq, d):
    c = diff_coeffs(d)
    return all(sum(ci * seq[j + i] for i, ci in enumerate(c)) == 0
               for j in range(len(seq) - d - 1))


# 1. Beatty lemma: round(Y + jB) is a polynomial of degree <= d on k >= 2d points
#    only if |B| <= 1/(k-1). (Its increments all lie in {0, 1} or all in {-1, 0}.)
beatty = {"cases": 0, "violations": 0}
for k in range(4, 15):
    for d in range(1, k // 2 + 1):
        for r in range(1, 41):
            for p in range(-r // 2, r // 2 + 1):
                B = Fraction(p, r)
                if not (-Fraction(1, 2) <= B < Fraction(1, 2)):
                    continue
                for y in range(0, 12):
                    Y = Fraction(y, 12) - Fraction(1, 2) + Fraction(1, 97)
                    w = [floor(Y + j * B + Fraction(1, 2)) for j in range(k)]
                    beatty["cases"] += 1
                    if poly_int(w, d) and abs(B) > Fraction(1, k - 1):
                        beatty["violations"] += 1
check(beatty["violations"] == 0, "Beatty lemma violated")
# control: with k <= 2d - 1 a non-affine polynomial wrap sequence exists
k, d = 5, 3
ctrl = False
for r in range(2, 41):
    for p in range(-r // 2, r // 2 + 1):
        B = Fraction(p, r)
        if abs(B) <= Fraction(1, k - 1) or B >= Fraction(1, 2):
            continue
        for y in range(48):
            Y = Fraction(y, 48) - Fraction(1, 2)
            w = [floor(Y + j * B + Fraction(1, 2)) for j in range(k)]
            if poly_int(w, d):
                ctrl = True
check(ctrl, "control: k <= 2d - 1 should allow a non-affine polynomial wrap sequence")
beatty["control_k_le_2d_minus_1_found"] = ctrl


# 2. Orbit lemma: along n0 + q^(D-1) m, m in [0, q), outside |B_D| <= 1/(k-1),
#    #{m : bands polynomial mod ell} <= (2^(d+1)+1)(q/ell + k + 1).
def orbit_case(q, D, lam, k, d, ell, rng, samples):
    N = q ** D
    out = {"orbits": 0, "excluded": 0, "max_bad": 0, "max_ratio": 0.0, "violations": 0}
    for _ in range(samples):
        dd = rng.randrange(1, N)
        r = rng.randrange(q ** (D - 1))
        BD = Fraction(centered(lam * dd, q ** D), q ** D)
        if abs(BD) <= Fraction(1, k - 1):
            out["excluded"] += 1
            continue
        out["orbits"] += 1
        bad = 0
        for m in range(q):
            n0 = r + q ** (D - 1) * m
            seq = [band(n0 + j * dd, lam, q, D) for j in range(k)]
            if poly_mod(seq, d, ell):
                bad += 1
        bound = (2 ** (d + 1) + 1) * (q / ell + k + 1)
        out["max_bad"] = max(out["max_bad"], bad)
        out["max_ratio"] = max(out["max_ratio"], bad / bound)
        if bad > bound:
            out["violations"] += 1
    return out


rng = random.Random(20261027)
orbit = {}
for (q, D, lam, k, d, ell, s) in [
    (1009, 2, 777, 12, 1, 31, 60),
    (1009, 2, 777, 12, 2, 101, 60),
    (1009, 2, 777, 12, 3, 2003, 60),
    (211, 3, 97, 10, 2, 13, 60),
    (211, 3, 97, 16, 3, 7, 40),
]:
    key = f"q={q},D={D},k={k},d={d},ell={ell}"
    orbit[key] = orbit_case(q, D, lam, k, d, ell, rng, s)
    check(orbit[key]["violations"] == 0, "orbit bound violated at " + key)
    check(orbit[key]["orbits"] > 0, "no orbit tested at " + key)


# 2b. Lemma 2 where it bites: one short window (m = 4) at a random start, small ell,
#     so that bad shifts exist. The count must stay within the bound, and bad
#     shifts must occur (otherwise the check proves nothing).
def window_case(q, D, lam, k, s, m, ell, rng, samples):
    N = q ** D
    out = {"orbits": 0, "bad_total": 0, "max_ratio": 0.0, "violations": 0}
    for _ in range(samples):
        dd = rng.randrange(1, N)
        if abs(Fraction(centered(lam * dd, N), N)) <= Fraction(1, m - 1):
            continue
        r = rng.randrange(q ** (D - 1))
        j0 = rng.randrange(k - m + 1)
        out["orbits"] += 1
        bad = sum(poly_mod([band(r + q ** (D - 1) * u + (j0 + j) * dd, lam, q, D)
                            for j in range(m)], s, ell) for u in range(q))
        bound = (2 ** (s + 1) + 1) * (q / ell + m + 1)
        out["bad_total"] += bad
        out["max_ratio"] = max(out["max_ratio"], round(bad / bound, 4))
        out["violations"] += bad > bound
    return out


window = {}
for (q, D, lam, k, s, m, ell, smp) in [(1009, 2, 777, 12, 2, 4, 29, 40),
                                       (1009, 2, 777, 12, 1, 4, 11, 40),
                                       (211, 3, 97, 10, 2, 4, 29, 40)]:
    key = f"q={q},D={D},s={s},m={m},ell={ell}"
    window[key] = window_case(q, D, lam, k, s, m, ell, rng, smp)
    check(window[key]["violations"] == 0, "window bound violated at " + key)
    check(window[key]["bad_total"] > 0, "window check never meets a bad shift at " + key)


# 3. The exceptional set is needed: the squares family of Proposition B3
#    (n_j = lam^{-1}(a + j)) has bands exactly (a + j)^2, polynomial of degree 2,
#    and |B_D| = 1/q^D <= 1/(k-1).
q, D, lam, k = 1009, 2, 777, 12
N = q ** D
inv = pow(lam, -1, N)
sq = {"progressions": 0, "polynomial": 0, "excluded": 0}
for a in range(-40, 40):
    seq = [band(inv * (a + j), lam, q, D) for j in range(k)]
    sq["progressions"] += 1
    sq["polynomial"] += poly_int(seq, 2) and all(seq[j] == (a + j) ** 2 for j in range(k))
    sq["excluded"] += abs(Fraction(centered(lam * inv, N), N)) <= Fraction(1, k - 1)
check(sq["polynomial"] == sq["progressions"], "squares family should be polynomial")
check(sq["excluded"] == sq["progressions"], "squares family should be in the exceptional set")


# 4. The identity behind the lemma, exactly. Along the orbit (mu = lam*m mod q), inside
#    one arc (fixed wraps of coordinate D on the window), W = -sum c_i y_D(n_i) is a
#    constant integer, the unfloored combination equals K - 2qW mu, and the floored
#    one differs from it by less than 2^{d+1}.
def arc_identity(q, D, lam, k, d, ell, rng, samples):
    N = q ** D
    c = diff_coeffs(d)
    stats = {"points": 0, "arcs": 0, "W_not_integer": 0, "W_varies_in_arc": 0,
             "slope_wrong": 0, "noise_too_wide": 0,
             "window_zero_mod_ell": 0, "window_bound": 0, "window_violations": 0}
    for _ in range(samples):
        dd = rng.randrange(1, N)
        r = rng.randrange(q ** (D - 1))
        j0 = rng.randrange(k - d - 1)
        arcs = {}
        for m in range(q):
            mu = (lam * m) % q
            n0 = r + q ** (D - 1) * m
            ns = [n0 + (j0 + i) * dd for i in range(d + 2)]
            wraps = tuple(1 if 2 * ((lam * n) % N) >= N else 0 for n in ns)
            W = -sum(Fraction(ci * centered(lam * n, N), N) for ci, n in zip(c, ns))
            real = sum(Fraction(ci * sum(centered(lam * n, q ** i) ** 2 * q ** (2 * D - 2 * i)
                                         for i in range(1, D + 1)), q ** (2 * D - 2))
                       for ci, n in zip(c, ns))
            X = sum(ci * band(n, lam, q, D) for ci, n in zip(c, ns))
            stats["points"] += 1
            stats["W_not_integer"] += W.denominator != 1
            stats["noise_too_wide"] += not (-2 ** (d + 1) < real - X < 2 ** (d + 1))
            arcs.setdefault(wraps, []).append((mu, W, real, X % ell == 0))
        for pts in arcs.values():
            stats["arcs"] += 1
            Ws = {W for _, W, _, _ in pts}
            stats["W_varies_in_arc"] += len(Ws) != 1
            W = pts[0][1]
            consts = {real + 2 * q * W * mu for mu, _, real, _ in pts}
            # one arc may hold two runs of mu (it wraps around q); allow the
            # shift by 2qW*q between them
            stats["slope_wrong"] += len({x % (2 * q * q * abs(W)) if W else x for x in consts}) != 1
            if W:
                zeros = sum(z for _, _, _, z in pts)
                bound = (2 ** (d + 1) + 1) * (len(pts) / ell + 2)
                stats["window_zero_mod_ell"] += zeros
                stats["window_bound"] += bound
                stats["window_violations"] += zeros > bound
    stats["window_bound"] = round(stats["window_bound"], 3)
    return stats


noise = {}
for (q, D, lam, k, d, ell, smp) in [(211, 2, 97, 10, 2, 13, 30), (1009, 2, 777, 12, 1, 31, 12),
                                    (211, 3, 97, 10, 1, 7, 12)]:
    key = f"q={q},D={D},k={k},d={d},ell={ell}"
    noise[key] = arc_identity(q, D, lam, k, d, ell, rng, smp)
for key in [f"{a}:{b}" for a in noise for b in ("W_not_integer", "W_varies_in_arc", "slope_wrong",
                                                  "noise_too_wide", "window_violations")]:
    a, b = key.split(":")
    check(noise[a][b] == 0, "arc identity: " + key)


# 5. Manifest.
manifest = json.loads((HERE / "MANIFEST.json").read_text())
for name, digest in manifest.items():
    got = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    check(got == digest, "hash mismatch: " + name)

summary = {"beatty": beatty, "orbit": orbit, "window": window, "squares_family": sq, "noise": noise,
           "fails": len(FAILS)}
print(json.dumps(summary, indent=1, sort_keys=True))
if FAILS:
    print("\n".join(FAILS))
    sys.exit(1)
expected = HERE / "RESULT.json"
if expected.exists() and json.loads(expected.read_text()) != summary:
    print("output differs from RESULT.json")
    sys.exit(1)
print("Test passé : all checks pass")
