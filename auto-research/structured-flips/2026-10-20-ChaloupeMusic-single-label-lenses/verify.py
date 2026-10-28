"""Exact checks for "Structured flips on single-label progressions: lenses".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json).

Notation is that of the source (OpenAI, pinned commit fd4aeeb, Sections 2 and
6) as restated in short-period-runs-proof.md: q a prime power, N = q^D, the
dilation lam, y_i(n) = (lam n mod q^i)/q^i, y~ its centred value in
[-1/2, 1/2), band(n) = floor(||q y~(n)||^2), key = (V-box of y~(n), band).

What is checked:

  1. Lens identity (Lemma 1).  On n_j = r + q^(D-1)(m + j e), e a signed
     step whose real segment s + j lam e stays in [-q/2, q/2):
       band(n_j) = floor(theta + v j) + lam^2 e^2 j^2,
       theta = C + s^2, v = 2 s lam e, frac(s) = y_{D-1}(r),
     with C = sum_{i<D} (q y~_i(r))^2 and s = q y~_D(n_0).  Fractions.
     Control: the unsigned step q - e (same points as -e) breaks it.
  2. Shifted squares (Lemma 2).  For D >= 3, 0 <= u < q/2 and
     r = u lam^{-1} mod q^(D-1): band(n_j) = x_j^2 + u^2 exactly, with
     x_j = floor(s) + j lam e.  Negative control: false for D = 2.
  3. Blocking sets for translates of the squares mod a prime ell (Lemma 3):
     stored R' meet every translate (exhaustive); the counting bound
     ell * C((ell-1)/2, s) < C(ell, s) at s = ceil(log2 ell) + 1 for every odd prime
     ell < 5000 (exact).  Control: a single residue never blocks.
  4. Theorem A at lens level: with k = (ell-1)^2 + 1, R = R' + {-1, 0, 1},
     every lens floor(theta + v j) + L j^2 with L a nonzero square mod ell
     meets R mod ell; the Dirichlet witness of the proof is recomputed on each
     lens.  A tight lens forces the witness index (ell-1)^2, so the
     hypothesis k >= (ell-1)^2 + 1 is exercised.  Control: L = 0 mod ell
     (that is, ell | e) with v = 0 mod ell misses.
  5. Measured, exhaustive (not a proof for general ell): with k = 2 ell, the
     stored R of size <= 5 meets EVERY lens (all real theta, v, all nonzero
     squares L) for ell in {13, 17, 19}; the enumeration of mechanical words
     of length k is complete (Farey points and midpoints).  Control: no
     3-element set does it for ell = 13, so |R| = 4 is minimal there.
  6. The real construction (q = 2^61 - 1, D = 3, lam = 840, k = 145, ell = 13,
     the source's U mesh and adaptive V mesh with 200-digit decimals):
       * P3 blocks (random r, e = 1) and P1 blocks (r = 0) with 13 not
         dividing e stay in one full label, meet X = (band mod 13 in R),
         and are not saturated by it (fewer than k keys in X);
       * saturation control, Proposition B with u = 0 (P2): on P1 blocks
         with 13 | e the rule is constant; some are missed and some have
         all k keys in X, which freezes them monochromatic;
       * the killer: a single-label block of the shifted family u = 1 with
         e = 13 has no key in X and no perfect-square band, so no patch
         on squares can reach it (Proposition B).
  7. Rich side, typical behaviour only (II): on 2000 uniformly random
     progressions of Z/N the number of keys in X has the binomial mean and
     variance of density |R|/13 within 5 standard errors.  The tail that
     matters for (II) is NOT tested (see README).
"""
import json
import math
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations
from pathlib import Path

getcontext().prec = 200
FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL', msg)


def centered(fr):
    r = fr - math.floor(fr)
    if r >= Fraction(1, 2):
        r -= 1
    return r


def ytilde(n, q, D, lam):
    return [centered(Fraction(lam * n, q ** i)) for i in range(1, D + 1)]


def xhat(n, q, D):
    return [Fraction(n % q ** i, q ** i) for i in range(1, D + 1)]


def band(n, q, D, lam):
    return math.floor(sum((q * v) ** 2 for v in ytilde(n, q, D, lam)))


def squares(ell):
    return {(z * z) % ell for z in range(ell)}


rng = random.Random(20261020)

# ------------------------------------------------------------ 1. lens identity
tests = 0
for trial in range(400):
    q = rng.choice([101, 1009, 11 ** 3, 10007, 2 ** 31 - 1])
    D = rng.randint(2, 4)
    lam = rng.choice([6, 60, 840])
    if math.gcd(lam, q) != 1:
        continue
    k = rng.randint(3, 10)
    r = rng.randrange(q ** (D - 1))
    e = rng.randint(1, 5)
    m = rng.randrange(q)
    n0 = r + q ** (D - 1) * m
    y0 = ytilde(n0, q, D, lam)
    s = q * y0[-1]
    if not (s >= 0 and s + (k - 1) * lam * e < Fraction(q, 2)):
        continue
    C = sum((q * v) ** 2 for v in y0[:-1])
    yD1 = Fraction((lam * r) % q ** (D - 1), q ** (D - 1))
    check(s - math.floor(s) == yD1 - math.floor(yD1), f'lens: frac(s) != y_(D-1)(r), trial {trial}')
    theta, v = C + s * s, 2 * s * lam * e
    for j in range(k):
        n = r + q ** (D - 1) * (m + j * e)
        tests += 1
        check(band(n, q, D, lam) == math.floor(theta + v * j) + lam ** 2 * e ** 2 * j ** 2,
              f'lens: identity fails, trial {trial} j {j}')
OUT['lens_identity_positions'] = tests
# control: the step must be read as a signed e with (k-1) lam |e| < q/2.  The step
# e' = q - e gives the same points as -e in Z/N, and the identity read with e' fails.
q, D, lam, k, e = 10007, 3, 60, 8, 2
r = 12345
bad = 0
for m in range(5000, 9000, 37):
    s = q * ytilde(r + q ** (D - 1) * m, q, D, lam)[-1]
    C = sum((q * v) ** 2 for v in ytilde(r + q ** (D - 1) * m, q, D, lam)[:-1])
    ep = q - e
    for j in range(k):
        if band(r + q ** (D - 1) * (m + j * ep), q, D, lam) != \
                math.floor(C + s * s + 2 * s * lam * ep * j) + lam ** 2 * ep ** 2 * j ** 2:
            bad += 1
check(bad > 0, 'control: an unsigned wrapped step should break the lens identity')
print(f'1. lens identity: band = floor(theta + v j) + lam^2 e^2 j^2 on {tests} positions; '
      f'the wrapped step q - e breaks it on {bad} positions')

# ---------------------------------------------------------- 2. shifted squares
tests = 0
for trial in range(400):
    q = rng.choice([10007, 2 ** 31 - 1, 2 ** 61 - 1])
    D = rng.randint(3, 4)
    lam = rng.choice([60, 840])
    k = rng.randint(3, 10)
    u = rng.randrange(0, q // 2)
    r = (u * pow(lam, -1, q ** (D - 1))) % q ** (D - 1)
    e = rng.randint(1, 5)
    m = rng.randrange(q)
    s = q * ytilde(r + q ** (D - 1) * m, q, D, lam)[-1]
    if not (s >= 0 and s + (k - 1) * lam * e < Fraction(q, 2)):
        continue
    x0 = math.floor(s)
    for j in range(k):
        tests += 1
        x = x0 + j * lam * e
        check(band(r + q ** (D - 1) * (m + j * e), q, D, lam) == x * x + u * u,
              f'shifted squares: fails, trial {trial}')
OUT['shifted_squares_positions'] = tests
# control: D = 2 (the fractional part of s is u/q, not negligible)
q, D, lam, u = 10007, 2, 840, 1234
r = (u * pow(lam, -1, q)) % q
bad = 0
for m in range(0, 2000, 7):
    n = r + q * m
    s = q * ytilde(n, q, D, lam)[-1]
    if s >= 0 and band(n, q, D, lam) != math.floor(s) ** 2 + u * u:
        bad += 1
check(bad > 0, 'control: D = 2 should break the shifted-squares identity')
print(f'2. shifted squares: band = x^2 + u^2 on {tests} positions (D >= 3); '
      f'D = 2 control breaks it on {bad} positions')

# ------------------------------------------------------- 3. blocking sets mod ell
BLOCK = {11: (0, 1, 5), 13: (0, 1, 7), 17: (0, 3, 6), 19: (0, 1, 2, 4),
         23: (0, 1, 2, 4), 29: (0, 1, 2, 3), 31: (0, 1, 2, 14), 37: (0, 1, 2, 8),
         41: (0, 1, 4, 5), 43: (0, 1, 2, 26)}
for ell, Rp in BLOCK.items():
    S = squares(ell)
    check(all(any((rr - c) % ell in S for rr in Rp) for c in range(ell)),
          f'blocking: R\' fails for ell = {ell}')
    check(not any(all(any((rr - c) % ell in S for rr in (x,)) for c in range(ell)) for x in range(ell)),
          f'blocking control: a single residue blocks for ell = {ell}')


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


cnt = 0
for ell in range(3, 5000, 2):
    if not is_prime(ell):
        continue
    s_ = math.ceil(math.log2(ell)) + 1
    if s_ > (ell - 1) // 2:
        continue
    check(ell * math.comb((ell - 1) // 2, s_) < math.comb(ell, s_), f'counting bound fails at ell = {ell}')
    cnt += 1
OUT['counting_bound_primes'] = cnt
print(f'3. blocking sets: stored R\' block every translate of the squares for '
      f'{len(BLOCK)} primes; counting bound holds for {cnt} odd primes < 5000')

# ------------------------------------------------- 4. Theorem A at lens level


def dirichlet(v, Q):
    """1 <= beta <= Q and integer a with |beta v - a| <= 1/(Q+1)."""
    best = None
    for beta in range(1, Q + 1):
        a = round(beta * v)
        d = abs(beta * v - a)
        if d <= Fraction(1, Q + 1):
            return beta, a
        if best is None or d < best[0]:
            best = (d, beta, a)
    raise AssertionError('Dirichlet failed')


ell = 13
Rp = BLOCK[ell]
RR = {(x + d) % ell for x in Rp for d in (-1, 0, 1)}
kA = (ell - 1) ** 2 + 1
SQ = squares(ell)
nonzero_sq = sorted(SQ - {0})
lens_ok = 0
for trial in range(1500):
    den = rng.choice([10 ** 9 + 7, 2 ** 61 - 1, 3 ** 40])
    theta = Fraction(rng.randrange(10 ** 6 * den), den)
    v = Fraction(rng.randrange(10 ** 6 * den), den)
    L = rng.choice(nonzero_sq) + ell * rng.randrange(10 ** 6)
    bands = [math.floor(theta + v * j) + L * j * j for j in range(kA)]
    hit = any(b % ell in RR for b in bands)
    check(hit, f'Theorem A: lens missed, trial {trial}')
    beta, a = dirichlet(v, ell - 1)
    g = [(math.floor(theta) + a * i + L * beta * beta * i * i) % ell for i in range(ell)]
    i0 = next((i for i in range(ell) if g[i] in Rp), None)
    check(i0 is not None, f'Theorem A: g(i) misses R\', trial {trial}')
    if i0 is not None:
        check(beta * i0 < kA and bands[beta * i0] % ell in RR,
              f'Theorem A: witness index fails, trial {trial}')
    lens_ok += hit
# control: ell | e makes L = 0 mod ell; with v an integer multiple of ell the residue is constant
theta = Fraction(13, 3)
bands = [math.floor(theta + 13 * 7 * j) + (13 * 4) * j * j for j in range(kA)]
check(len({b % ell for b in bands}) == 1 and bands[0] % ell not in RR,
      'control: ell | e lens should be constant mod ell and miss R')
# a lens on which the proof needs the largest index (ell-1)^2: v = n + 1/(ell-1) forces
# beta = ell - 1, and floor(theta), n are chosen so that g meets R' only at i = ell - 1
tight = None
for n_int in range(ell):
    for th0 in range(ell):
        v = n_int + Fraction(1, ell - 1)
        theta = th0 + Fraction(1, 2)
        L = 840 ** 2
        beta, a = dirichlet(v, ell - 1)
        g = [(th0 + a * i + L * beta * beta * i * i) % ell for i in range(ell)]
        hits = [i for i in range(ell) if g[i] in Rp]
        if beta == ell - 1 and hits == [ell - 1]:
            tight = (n_int, th0)
            break
    if tight:
        break
check(tight is not None, 'tight lens not found')
if tight:
    v, theta = tight[0] + Fraction(1, ell - 1), tight[1] + Fraction(1, 2)
    bands = [math.floor(theta + v * j) + 840 ** 2 * j * j for j in range(kA)]
    check((ell - 1) ** 2 < kA and bands[(ell - 1) ** 2] % ell in RR,
          'tight lens: the witness index (ell-1)^2 must lie below k')
    OUT['theoremA_tight_lens'] = {'v': str(v), 'theta': str(theta), 'witness_index': (ell - 1) ** 2}
OUT['theoremA_lenses'] = lens_ok
OUT['theoremA_R'] = sorted(RR)
print(f'4. Theorem A (k = {kA}, ell = {ell}, |R| = {len(RR)}): {lens_ok} random lenses hit, '
      f'Dirichlet witness recomputed; the tight lens uses index (ell-1)^2; the ell | e control misses')

# ------------------------------------- 5. measured: k = 2l, exhaustive lenses


def farey(n):
    a, b, c, d = 0, 1, 1, n
    out = [Fraction(0)]
    while c <= n:
        t = (n + b) // d
        a, b, c, d = c, d, t * c - a, t * d - b
        out.append(Fraction(a, b))
    return out


def mechanical_words(k):
    W = set()
    fs = farey(k)
    phis = set(fs) | {(fs[i] + fs[i + 1]) / 2 for i in range(len(fs) - 1)}
    for phi in phis:
        if phi >= 1:
            continue
        bps = sorted({(-phi * j) % 1 for j in range(k)} | {Fraction(0)})
        ths = set(bps) | {(bps[i] + bps[i + 1]) / 2 for i in range(len(bps) - 1)}
        ths.add((bps[-1] + 1) / 2)
        for th in ths:
            W.add(tuple(math.floor(th + phi * j) for j in range(k)))
    return W


MEASURED = {13: (0, 1, 3, 4), 17: (0, 1, 2, 3), 19: (0, 1, 2, 3, 4)}
measured = {}
for ell, Rm in MEASURED.items():
    k2 = 2 * ell
    W = mechanical_words(k2)
    masks = set()
    minpat = ell
    for L in sorted(squares(ell) - {0}):
        for w in W:
            for nn in range(ell):
                pat = {(L * j * j + nn * j + w[j]) % ell for j in range(k2)}
                minpat = min(minpat, len(pat))
                pm = sum(1 << p for p in pat)
                for t in range(ell):
                    masks.add(((pm << t) | (pm >> (ell - t))) & ((1 << ell) - 1))
    rm = sum(1 << x for x in Rm)
    check(all(mk & rm for mk in masks), f'measured: R fails for ell = {ell}')
    if ell == 13:
        check(not any(all(mk & sum(1 << x for x in T) for mk in masks)
                      for T in combinations(range(ell), 3)),
              'measured control: a 3-element set blocks every lens for ell = 13')
    measured[str(ell)] = {'k': k2, 'words': len(W), 'min_pattern_size': minpat, 'R': list(Rm)}
OUT['measured_k_equals_2l'] = measured
print('5. measured (exhaustive over all real lenses, k = 2l): ' +
      ', '.join(f'ell={ell}: |R|={len(v["R"])}, min pattern {v["min_pattern_size"]} '
                f'over {v["words"]} words' for ell, v in ((int(a), b) for a, b in measured.items())))

# ----------------------------------------------- 6. the real construction


def mesh(q, D, k):
    alpha = Decimal(1) / (Decimal(q) ** (D + 1))
    R = (1 + 1 / (2 * alpha)).ln()
    m = int((Decimal(k * k) * R).to_integral_value(rounding='ROUND_CEILING'))
    return alpha, R, m


def v_index(Y, alpha, R, m):
    Yd = Decimal(Y.numerator) / Decimal(Y.denominator)
    if Yd < 0:
        a = Yd + Decimal('0.5')
        l_ = int((m * (1 + a / alpha).ln() / R).to_integral_value(rounding='ROUND_FLOOR'))
        return 'L', l_
    a = Decimal('0.5') - Yd
    l_ = int((m * (1 + a / alpha).ln() / R).to_integral_value(rounding='ROUND_CEILING')) - 1
    return 'R', l_


def label(n, q, D, lam, k, alpha, R, m):
    return (tuple(math.floor(x * k * k * lam) for x in xhat(n, q, D)),
            tuple(v_index(y, alpha, R, m) for y in ytilde(n, q, D, lam)))


q, D, k, lam, ell = 2 ** 61 - 1, 3, 145, 840, 13
assert math.gcd(lam, ell) == 1 and kA <= k
alpha, Rmesh, mm = mesh(q, D, k)
E_MAX = q // (400 * k ** 3 * lam)
check(E_MAX > 10 ** 6, 'instance: E_max too small')


def in_X(n):
    """Key of n in X_13: band mod 13 in R (the rule of Theorem A, no patch)."""
    return band(n, q, D, lam) % ell in RR


def block(r, mstart, e):
    return [r + q ** (D - 1) * (mstart + j * e) for j in range(k)]


def single_label(ns):
    return len({label(n, q, D, lam, k, alpha, Rmesh, mm) for n in ns}) == 1


def good_start(r, mstart, e):
    Y = ytilde(r + q ** (D - 1) * mstart, q, D, lam)[-1]
    return Fraction(1, 8) <= Y <= Fraction(3, 8) - Fraction(k * lam * e, q)


def good_block(r, e):
    while True:
        ms = rng.randrange(q)
        if good_start(r, ms, e) and single_label(block(r, ms, e)):
            return block(r, ms, e)


counts = {'P3_met': 0, 'P3_max_keys_in_X': 0, 'P1_13_not_dividing_e_met': 0,
          'P1_13_divides_e_missed': 0, 'P1_13_divides_e_saturated': 0}
while counts['P3_met'] < 30:
    ns = good_block(rng.randrange(q ** (D - 1)), 1)
    c = sum(in_X(n) for n in ns)
    check(c >= 1, 'real P3 block missed by X')
    check(c < k, 'real P3 block saturated by X')
    counts['P3_met'] += 1
    counts['P3_max_keys_in_X'] = max(counts['P3_max_keys_in_X'], c)
while counts['P1_13_not_dividing_e_met'] < 15:
    e = rng.randint(1, E_MAX)
    if e % ell == 0:
        continue
    ns = good_block(0, e)
    c = sum(in_X(n) for n in ns)
    check(1 <= c < k, f'real P1 block with 13 not dividing e: {c} keys of {k} in X')
    counts['P1_13_not_dividing_e_met'] += 1
# Proposition B with u = 0 (that is P2): on 13 | e the rule is constant on the block,
# so it misses it or saturates it; both happen.  This is the saturation control.
for _ in range(60):
    ns = good_block(0, ell * rng.randint(1, E_MAX // ell))
    c = sum(in_X(n) for n in ns)
    check(c in (0, k), f'P1 with 13 | e: partial intersection {c}')
    counts['P1_13_divides_e_missed' if c == 0 else 'P1_13_divides_e_saturated'] += 1
    if counts['P1_13_divides_e_missed'] >= 3 and counts['P1_13_divides_e_saturated'] >= 3:
        break
check(counts['P1_13_divides_e_missed'] >= 1 and counts['P1_13_divides_e_saturated'] >= 1,
      'P1 with 13 | e: both branches of Proposition B should occur')
OUT['real_blocks'] = counts

# the killer: shifted family u = 1, e = 13; its bands x^2 + 1 are never perfect squares
u, e = 1, 13
r = (u * pow(lam, -1, q ** (D - 1))) % q ** (D - 1)
killer = None
for _ in range(20000):
    ms = rng.randrange(q)
    if not good_start(r, ms, e):
        continue
    s0 = math.floor(q * ytilde(r + q ** (D - 1) * ms, q, D, lam)[-1])
    if (s0 * s0 + 1) % ell in RR:
        continue
    ns = block(r, ms, e)
    if single_label(ns):
        killer = (ms, s0)
        break
check(killer is not None, 'killer: no single-label block found')
if killer is not None:
    ns = block(r, killer[0], e)
    bands = [band(n, q, D, lam) for n in ns]
    check(all(bands[j] == (killer[1] + j * lam * e) ** 2 + 1 for j in range(k)), 'killer: bands are not x^2 + 1')
    check(not any(math.isqrt(b) ** 2 == b for b in bands), 'killer: a band is a perfect square')
    check(not any(in_X(n) for n in ns), 'killer: the block meets X')
    OUT['killer'] = {'u': u, 'e': e, 'm_start': killer[0], 'x0': killer[1], 'x0_mod_13': killer[1] % ell,
                     'band_residue_mod_13': bands[0] % ell}
print(f'6. real construction (q = 2^61-1, D = 3, k = {k}, ell = {ell}, E_max = {E_MAX}): '
      f'{counts["P3_met"]} P3 blocks met, at most {counts["P3_max_keys_in_X"]} of {k} keys in X; '
      f'{counts["P1_13_not_dividing_e_met"]} P1 blocks with 13 not dividing e met, not saturated; '
      f'P1 with 13 | e: {counts["P1_13_divides_e_missed"]} missed, '
      f'{counts["P1_13_divides_e_saturated"]} saturated (Proposition B, u = 0); '
      f'the shifted block u = 1, e = 13 misses X and has no square band')

# ------------------------------------------ 7. rich side, typical behaviour
N = q ** D
rho = Fraction(len(RR), ell)
vals = []
for _ in range(2000):
    n0, d = rng.randrange(N), rng.randrange(1, N)
    vals.append(sum(band((n0 + j * d) % N, q, D, lam) % ell in RR for j in range(k)))
mean = Fraction(sum(vals), len(vals))
var = Fraction(sum(x * x for x in vals), len(vals)) - mean * mean
bmean, bvar = k * rho, k * rho * (1 - rho)
se_mean = math.sqrt(float(bvar) / len(vals))
check(abs(float(mean - bmean)) <= 5 * se_mean, 'rich: mean far from binomial')
se_var = float(bvar) * math.sqrt(2 / (len(vals) - 1))
check(abs(float(var - bvar)) <= 5 * se_var, 'rich: variance far from binomial')
OUT['rich_typical'] = {'samples': len(vals), 'density': str(rho), 'mean': round(float(mean), 3),
                       'binomial_mean': round(float(bmean), 3), 'variance': round(float(var), 3),
                       'binomial_variance': round(float(bvar), 3), 'max': max(vals)}
print(f'7. rich side, typical: mean {float(mean):.2f} (binomial {float(bmean):.2f}), variance '
      f'{float(var):.2f} (binomial {float(bvar):.2f}), max {max(vals)}')

# ------------------------------------------------------------------- summary
OUT['fails'] = len(FAIL)
print(json.dumps(OUT, sort_keys=True))
res = Path(__file__).with_name('RESULT.json')
if '--write' in sys.argv:
    res.write_text(json.dumps(OUT, sort_keys=True, indent=1) + '\n')
elif res.exists():
    check(json.loads(res.read_text()) == OUT, 'summary differs from RESULT.json')
if FAIL:
    print(f'Test échoué : {len(FAIL)} checks failed')
    sys.exit(1)
print('Test passé : all checks pass')
