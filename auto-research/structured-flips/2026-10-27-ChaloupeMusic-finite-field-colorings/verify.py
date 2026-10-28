"""Checks for finite-field-colorings (Berlekamp, Blankenship-Cummings-Taranchuk).

Run: python3 -B verify.py   (standard library only; exit code 0 and
last line "Test passé : all checks pass"; the JSON summary it prints must
equal RESULT.json; --write regenerates RESULT.json, refuses to if any check
fails, and skips only the
RESULT and MANIFEST comparisons, every other check still runs;
--print-sections prints the hashes of the frozen README sections).
"""
import hashlib
import itertools
import json
import math
import random
import sys
from pathlib import Path

FAIL = []
OUT = {}


def check(ok, msg):
    if not ok:
        FAIL.append(msg)
        print('FAIL:', msg)


# ------------------------------------------------------------ GF(p^M) helpers
# An element is an integer 0 <= x < p^M whose base-p digits are the
# coefficients (digit i = coefficient of x^i). f is monic of degree M, given by
# its low coefficients f_0..f_{M-1} (x^M = -sum f_i x^i).

def digits(x, p, M):
    return [(x // p ** i) % p for i in range(M)]


def undigits(v, p):
    return sum(c * p ** i for i, c in enumerate(v))


def mul_x(x, p, M, f):
    v = digits(x, p, M)
    top = v[-1]
    w = [0] + v[:-1]
    return undigits([(w[i] - top * f[i]) % p for i in range(M)], p)


def powers(p, M, f):
    """alpha = x; returns [alpha^0, ..., alpha^(P-1)] or None if x is not primitive."""
    P = p ** M - 1
    out, x = [], 1
    seen = set()
    for _ in range(P):
        if x in seen or x == 0:
            return None
        seen.add(x)
        out.append(x)
        x = mul_x(x, p, M, f)
    return out if x == 1 else None


def primitive(p, M, rng):
    cands = list(itertools.product(range(p), repeat=M))
    rng.shuffle(cands)
    for f in cands:
        if f[0] == 0:
            continue
        pw = powers(p, M, list(f))
        if pw is not None:
            return list(f), pw
    raise RuntimeError('no primitive polynomial')


class Field:
    def __init__(self, p, M, f, pw):
        self.p, self.M, self.f, self.pw = p, M, f, pw
        self.P = p ** M - 1
        self.log = {x: i for i, x in enumerate(pw)}

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.pw[(self.log[a] + self.log[b]) % self.P]

    def add(self, a, b):
        p, M = self.p, self.M
        return undigits([(u + v) % p for u, v in zip(digits(a, p, M), digits(b, p, M))], p)

    def full_degree(self, b):
        """b != 0 generates GF(p^M) over GF(p): b^(p^d) != b for every proper divisor d of M."""
        e = self.log[b]
        for d in range(1, self.M):
            if self.M % d == 0 and (e * (self.p ** d - 1)) % self.P == 0:
                return False
        return True


def functional(F, w):
    p, M = F.p, F.M
    return lambda x: sum(a * b for a, b in zip(w, digits(x, p, M))) % p


def mono_ap(colour, lo, hi, k):
    """First k-term AP inside [lo, hi] (integers) on which colour is constant, or None."""
    for d in range(1, (hi - lo) // (k - 1) + 1):
        for a in range(lo, hi - (k - 1) * d + 1):
            c = colour[a]
            if all(colour[a + j * d] == c for j in range(1, k)):
                return (a, d)
    return None


rng = random.Random(20261027)

# ------------------------------------------------------------------------ 1.
# Berlekamp's own example (Canad. Math. Bull. 11 (1968), p. 413-414) and
# Theorem 2 for t = 3, 5, 7: the 2-colouring of t*2^t consecutive integers.

def coords(F, basis):
    """Coordinates A[i][j] of alpha^j in the GF(2)-basis `basis` (solve by brute force)."""
    M = F.M
    table = {}
    for c in itertools.product(range(2), repeat=M):
        x = 0
        for ci, b in zip(c, basis):
            if ci:
                x = F.add(x, b)
        check(x not in table, 'basis not independent')
        table[x] = c
    return [[table[F.pw[j]][i] for j in range(F.P)] for i in range(M)]


def berlekamp_t(t):
    f = {3: [1, 1, 0], 5: [1, 0, 1, 0, 0], 7: [1, 1, 0, 0, 0, 0, 0]}[t]   # x^3+x+1, x^5+x^2+1, x^7+x+1
    pw = powers(2, t, f)
    check(pw is not None, f'x not primitive for t={t}')
    F = Field(2, t, f, pw)
    one = 1
    basis = [one]
    for m in range(1, (t - 1) // 2 + 1):
        basis.append(F.add(one, F.pw[m]))
    for m in range(1, (t - 1) // 2 + 1):
        basis.append(F.add(one, F.pw[(-m) % F.P]))
    A = coords(F, basis)
    W = t * (2 ** t - 1)
    h = (t - 1) // 2
    colour = {}
    for i in range(W):
        colour[i] = A[0][i % F.P]
    S1 = sorted(i for i in range(W) if colour[i] == 1)
    for i in range(1, h + 1):           # extension S0' = {-1..-h}
        colour[-i] = 0
    for i in range(h + 1):              # S0'' = {W, ..., W + h}
        colour[W + i] = 0
    check(all(colour[i] == 1 for i in range(h + 1)), f'(14) fails, t={t}')
    check(all(colour[W - i] == 1 for i in range(1, h + 1)), f'(15) fails, t={t}')
    lo, hi = -h, W + h
    check(hi - lo + 1 == t * 2 ** t, 'length')
    bad = mono_ap(colour, lo, hi, t + 1)
    return A, S1, colour, (lo, hi), bad


A3, S1_3, col3, rng3, bad3 = berlekamp_t(3)
paper_rows = ['110010111001011100101', '010111001011100101110', '001011100101110010111']
mine = [''.join(str(A3[i][j % 7]) for j in range(21)) for i in range(3)]
check(mine == paper_rows, f'Berlekamp table differs: {mine}')
check(S1_3 == [0, 1, 4, 6, 7, 8, 11, 13, 14, 15, 18, 20], f'S_1 differs: {S1_3}')
check(bad3 is None, f'mono 4-AP in Berlekamp t=3: {bad3}')
res1 = {'t=3_table_equals_paper': mine == paper_rows, 't=3_S1': S1_3}
for t in (5, 7):
    _, _, _, (lo, hi), bad = berlekamp_t(t)
    check(bad is None, f'mono {t+1}-AP in Berlekamp t={t}: {bad}')
    res1[f't={t}'] = {'interval': [lo, hi], 'length': hi - lo + 1, 'mono_(t+1)_AP': bad}
# control: the same colouring has monochromatic t-APs (runs of t ones, Theorem 1)
ctrl = mono_ap(col3, rng3[0], rng3[1], 3)
check(ctrl is not None, 'control: no mono 3-AP found in the t=3 colouring')
res1['control_t=3_has_mono_3AP'] = ctrl is not None
OUT['berlekamp_witness'] = res1
print('1. Berlekamp example and Theorem 2 (t=3,5,7):', res1)

# ------------------------------------------------------------------------ 2.
# Theorem 1: every nonzero M-tuple occurs exactly once per period in
# u_n = phi(alpha^n); hence runs of M equal nonzero values (k <= M fails),
# and the step-P progression is constant.
res2 = {}
for p, Ms in ((2, range(2, 11)), (3, range(2, 6)), (5, range(2, 4))):
    for M in Ms:
        f, pw = primitive(p, M, rng)
        F = Field(p, M, f, pw)
        for _ in range(3):
            w = [0] * M
            while not any(w):
                w = [rng.randrange(p) for _ in range(M)]
            phi = functional(F, w)
            u = [phi(x) for x in pw]
            win = [tuple(u[(n + i) % F.P] for i in range(M)) for n in range(F.P)]
            check(len(set(win)) == F.P and (0,) * M not in win, f'tuples p={p} M={M}')
            for xi in range(1, p):
                check((xi,) * M in win, f'run of {xi} missing p={p} M={M}')
        res2[f'{p}^{M}'] = 'all nonzero M-tuples once per period'
OUT['theorem1_tuples'] = sorted(res2)
print(f'2. Theorem 1 (tuples once per period) on {len(res2)} fields')


# ------------------------------------------------------------------------ 3.
# Berlekamp's coloring of Z/P as a block: for M prime, every cyclic (M+1)-AP
# of nonzero step is bichromatic (Kim's "polychromatic block"). Composite P
# included (M = 11, P = 2047 = 23 * 89). Runs are measured along each cycle
# of n -> n + b, so the test is exhaustive in O(P^2).

def longest_cyclic_run(u, P, b):
    g = math.gcd(b, P)
    best = 0
    for start in range(g):
        seq, x = [], start
        for _ in range(P // g):
            seq.append(u[x])
            x = (x + b) % P
        if len(set(seq)) == 1:
            return P // g
        cur = 0
        for i in range(2 * len(seq)):
            cur = cur + 1 if i and seq[i % len(seq)] == seq[(i - 1) % len(seq)] else 1
            best = max(best, cur)
    return best


res3 = {}
for M, f in ((3, [1, 1, 0]), (5, [1, 0, 1, 0, 0]), (7, [1, 1, 0, 0, 0, 0, 0]),
             (11, [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])):              # x^11 + x^2 + 1
    pwM = powers(2, M, f)
    check(pwM is not None, f'polynomial not primitive, M={M}')
    F = Field(2, M, f, pwM)
    u = [x & 1 for x in F.pw]
    worst = max(longest_cyclic_run(u, F.P, b) for b in range(1, F.P))
    check(worst <= M, f'cyclic run longer than M for M={M}: {worst}')
    res3[f'M={M}'] = {'P': F.P, 'P_prime': all(F.P % d for d in range(2, int(F.P ** .5) + 1)),
                      'longest_cyclic_run_nonzero_step': worst}
# control: a random 2-coloring of Z/127 has a cyclic run of length 8 at some
# nonzero step (about 125 expected). For M = 4 the subfield steps (5, 10) have
# cycles of length 3 < 5: those progressions are degenerate, not a failure.
u_r = [rng.randrange(2) for _ in range(127)]
ctrl3 = max(longest_cyclic_run(u_r, 127, b) for b in range(1, 127))
check(ctrl3 >= 8, 'control: a random coloring should have a long cyclic run')
res3['control_random_Z127_longest_run'] = ctrl3
OUT['polychromatic_blocks'] = res3
print('3. cyclic blocks:', res3)

# ------------------------------------------------------------------------ 4.
# Lemma L, with the degree d of the ratio: for beta != 1, an affine subspace
# A of dimension w with 0 not in A holds no geometric run longer than
# min(d, w + 1); a linear one of dimension w < d holds none longer than w.

def span(F, vecs):
    S = {0}
    for v in vecs:
        S = {_addmul(F, s, v, c) for s in S for c in range(F.p)}
    return S


def _addmul(F, s, v, c):
    p, M = F.p, F.M
    return undigits([(a + c * b) % p for a, b in zip(digits(s, p, M), digits(v, p, M))], p)


def degree(F, b):
    e = F.log[b]
    return next(d for d in range(1, F.M + 1) if (e * (F.p ** d - 1)) % F.P == 0)


def longest_run(F, A, gamma, beta):
    """Longest run j, j+1, ... (cyclic, capped at P) with gamma*beta^j in A."""
    lg, lb = F.log[gamma], F.log[beta]
    inside = [F.pw[(lg + j * lb) % F.P] in A for j in range(F.P)]
    if all(inside):
        return F.P
    best = cur = 0
    for x in inside + inside:
        cur = cur + 1 if x else 0
        best = max(best, cur)
    return best


res4 = {}
for p, M, trials in ((2, 4, 40), (2, 5, 40), (2, 6, 20), (3, 3, 30)):
    f, pw = primitive(p, M, rng)
    F = Field(p, M, f, pw)
    betas = [b for b in pw if b != 1]
    worst = {}
    for _ in range(trials):
        w = rng.randrange(1, M)
        while True:
            U = span(F, [rng.randrange(1, p ** M) for _ in range(w)])
            if len(U) == p ** w:
                break
        x0 = rng.randrange(p ** M)
        A = {_addmul(F, u, x0, 1) for u in U}
        linear = 0 in A
        for b in betas:
            d = degree(F, b)
            if linear and d <= w:
                continue                     # a subfield coset may sit inside
            bound = w if linear else min(d, w + 1)
            m = max(longest_run(F, A, g, b) for g in pw)
            check(m <= bound, f'Lemma L fails p={p} M={M} w={w} d={d} linear={linear}: {m}')
            key = f'{"lin" if linear else "aff"},w={w},d={d}'
            worst[key] = [max(worst.get(key, [0])[0], m), bound]
    res4[f'{p}^{M}'] = {kk: worst[kk] for kk in sorted(worst)}
# control: a subfield ratio inside a linear subspace (GF(4) in GF(16))
pw16 = powers(2, 4, [1, 1, 0, 0])
F16 = Field(2, 4, [1, 1, 0, 0], pw16)
GF4 = {0} | {pw16[5 * i] for i in range(3)}
run = longest_run(F16, GF4, 1, pw16[5])
check(run > 2, 'control: subfield ratio should give a long run')
res4['control_subfield_run'] = run
OUT['lemma_L'] = res4
print('4. Lemma L ([longest run, bound] per kind):', res4)

# ------------------------------------------------------------------------ 5.
# Corollary L1: two proper affine subspaces covering F* are, for M >= 3, a
# linear hyperplane and its complement (K = 2 only). Exhaustive; the number
# of covering pairs must be 2^M - 1 for K = 2 and 0 for K = 3.

def all_subspaces(F):
    p, M = F.p, F.M
    subs = {frozenset({0})}
    frontier = [frozenset({0})]
    while frontier:
        nxt = []
        for U in frontier:
            for v in range(1, p ** M):
                if v not in U:
                    V = frozenset(_addmul(F, u, v, c) for u in U for c in range(p))
                    if V not in subs:
                        subs.add(V)
                        nxt.append(V)
        frontier = nxt
    return [U for U in subs if len(U) < p ** M]


res5 = {}
for p, M in ((2, 3), (2, 4), (3, 2), (3, 3)):
    f, pw = primitive(p, M, rng)
    F = Field(p, M, f, pw)
    affs = set()
    for U in all_subspaces(F):
        for x0 in range(p ** M):
            affs.add(frozenset(_addmul(F, u, x0, 1) for u in U))
    affs = list(affs)
    Fstar = set(range(1, p ** M))
    pairs = [(A, B) for A, B in itertools.combinations(affs, 2) if Fstar <= (A | B)]
    shape = all(p == 2 and len(A) == len(B) == 2 ** (M - 1) and not (A & B) and (0 in A or 0 in B)
                for A, B in pairs)
    expected = 2 ** M - 1 if p == 2 else 0
    check(shape and len(pairs) == expected, f'Corollary L1 fails p={p} M={M}: {len(pairs)} pairs')
    res5[f'{p}^{M}'] = {'affine_subspaces': len(affs), 'covering_pairs': len(pairs),
                        'expected': expected, 'all_hyperplane_and_complement': shape}
# density of a certified class: {phi = 0} in F* has (2^(M-1) - 1)/(2^M - 1) < 1/2
res5['density_phi=0'] = {M: f'{2 ** (M - 1) - 1}/{2 ** M - 1}' for M in (3, 5, 7)}
OUT['double_certificate'] = res5
print('5. covering pairs of affine subspaces:', res5)

# ------------------------------------------------------------------------ 6.
# Lemma S: a slow lens b_j = floor(theta + v j) + L j^2 is affine mod P on
# k >= 3 terms only if P | 2L + eps for some eps in {-1, 0, 1}.
res6 = {'instances': 0, 'affine': 0}
for _ in range(20000):
    P = rng.choice([7, 15, 31, 63, 127, 255])
    k = rng.randrange(3, 12)
    L = rng.randrange(1, 300)
    theta = rng.random() * 50
    v = rng.choice([rng.randrange(-40, 40), rng.uniform(-40, 40)])
    b = [math.floor(theta + v * j) + L * j * j for j in range(k)]
    aff = all((b[j + 2] - 2 * b[j + 1] + b[j]) % P == 0 for j in range(k - 2))
    res6['instances'] += 1
    if aff:
        res6['affine'] += 1
        check(any((2 * L + e) % P == 0 for e in (-1, 0, 1)), f'Lemma S fails P={P} L={L}')
OUT['lemma_S'] = res6
print('6. Lemma S:', res6)

# ------------------------------------------------------------------------ 7.
# Evidence (not a theorem): on quadratic exponent windows (x0 + j mu)^2, the
# windows of the slow P1 family and, for mu = 1, of the rich squares family of
# Proposition B3, Berlekamp's colouring is monochromatic at about the chance
# rate 2^(1-k); on linear windows (its certificate) never.
res7 = {}
for M, f in ((5, [1, 0, 1, 0, 0]), (7, [1, 1, 0, 0, 0, 0, 0])):
    F = Field(2, M, f, powers(2, M, f))
    P, k = F.P, M + 1
    u = [x & 1 for x in F.pw]
    lin = quad = 0
    for x0 in range(P):
        for mu in range(1, P):
            if len({u[(x0 + j * mu) % P] for j in range(k)}) == 1:
                lin += 1
            if len({u[((x0 + j * mu) ** 2) % P] for j in range(k)}) == 1:
                quad += 1
    sq = sum(1 for a in range(P) if len({u[((a + j) ** 2) % P] for j in range(k)}) == 1)
    check(lin == 0, f'linear windows mono for M={M}')
    res7[f'M={M}'] = {'P': P, 'k': k, 'windows': P * (P - 1), 'mono_linear': lin,
                      'mono_quadratic': quad, 'chance': round(P * (P - 1) * 2 ** (1 - k), 1),
                      'mono_squares_mu1': sq}
M, f = 13, [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]          # x^13+x^4+x^3+x+1
pw13 = powers(2, M, f)
check(pw13 is not None, 'x^13+x^4+x^3+x+1 not primitive')
F = Field(2, M, f, pw13)
P, k = F.P, M + 1
u = [x & 1 for x in F.pw]
S = 300000
quad = sum(1 for _ in range(S)
           for x0, mu in [(rng.randrange(P), rng.randrange(1, P))]
           if len({u[((x0 + j * mu) ** 2) % P] for j in range(k)}) == 1)
lin = sum(1 for _ in range(S)
          for x0, mu in [(rng.randrange(P), rng.randrange(1, P))]
          if len({u[(x0 + j * mu) % P] for j in range(k)}) == 1)
check(lin == 0, 'linear windows mono for M=13')
res7['M=13_sampled'] = {'P': P, 'k': k, 'samples': S, 'mono_linear': lin, 'mono_quadratic': quad,
                        'chance': round(S * 2 ** (1 - k), 1)}
OUT['quadratic_windows_evidence'] = res7
print('7. quadratic exponent windows (evidence):', res7)

# ------------------------------------------------------------------------ 8.
# Scale: lengths p^(r-1) 2^p (BCT; r = 2 is Berlekamp's p 2^p), p <= k,
# against N = k^(c k floor(log2 r)), c = 1/8. For fixed r the ratio
# ln(length)/ln N is decreasing in k; for r >= 512 it is < 8/j + 8/j^2 < 1
# (j = floor(log2 r) >= 9). So the threshold is the largest k_r, r <= 511.
c = 1 / 8


def ratio(k, r):
    j = int(math.floor(math.log2(r)))
    return ((r - 1) * math.log(k) + k * math.log(2)) / (c * k * math.log(k) * j)


k_r = {}
for r in range(2, 512):
    k = max(r, 3)
    while ratio(k, r) >= 1:
        k += 1
    k_r[r] = k
worst_r = max(k_r, key=k_r.get)
res8 = {'threshold_r=2_berlekamp': k_r[2], 'threshold_r=3': k_r[3],
        'threshold_all_r': k_r[worst_r], 'worst_r': worst_r}
check(all(8 / j + 8 / j ** 2 < 1 for j in range(9, 200)), 'analytic tail')
OUT['scale'] = res8
print('8. scale (smallest k from which the length is below N):', res8)

# ------------------------------------------------------------------------ 9.
# Lemma R (aligned blocks) and Proposition R (the square-root rule).
# x_j = s + j mu (s >= 0 real, mu >= 1 integer), C >= 0 real, f = frac(s):
# C < (1 - f)(2 floor(s) + 1 + f)  ==>  isqrt(floor(C + x_j^2)) = floor(s) + j mu.
from fractions import Fraction as Fr                       # noqa: E402

res9 = {'aligned_blocks': 0, 'not_aligned_blocks': 0, 'not_aligned_not_arithmetic': 0}
for _ in range(20000):
    s = Fr(rng.randrange(0, 10 ** 6), 1) + Fr(rng.randrange(0, 997), 997)
    mu = rng.randrange(1, 5000)
    k = rng.randrange(3, 16)
    f = s - math.floor(s)
    bound = (1 - f) * (2 * math.floor(s) + 1 + f)
    if rng.random() < 0.8:
        C = bound * Fr(rng.randrange(0, 1000), 1000)
        word = [math.isqrt(math.floor(C + (s + j * mu) ** 2)) for j in range(k)]
        check(word == [math.floor(s) + j * mu for j in range(k)], f'Lemma R fails: s={s} mu={mu} C={C}')
        res9['aligned_blocks'] += 1
    else:
        C = bound + Fr(rng.randrange(1, 10 ** 9), 1)
        word = [math.isqrt(math.floor(C + (s + j * mu) ** 2)) for j in range(k)]
        res9['not_aligned_blocks'] += 1
        res9['not_aligned_not_arithmetic'] += any(word[j + 2] - 2 * word[j + 1] + word[j]
                                                  for j in range(k - 2))
# The negative side: Lemma R applies to |x_j|, with t = min |x_j| and frac(t).
res9['negative_side_blocks'] = 0
for _ in range(5000):
    mu = rng.randrange(1, 5000)
    k = rng.randrange(3, 16)
    t = Fr(rng.randrange(0, 10 ** 6), 1) + Fr(rng.randrange(1, 997), 997)   # smallest |x|
    xs = [-(t + (k - 1 - j) * mu) for j in range(k)]                        # all negative
    ft = t - math.floor(t)
    C = (1 - ft) * (2 * math.floor(t) + 1 + ft) * Fr(rng.randrange(0, 1000), 1000)
    word = [math.isqrt(math.floor(C + x * x)) for x in xs]
    check(word == [math.floor(t) + (k - 1 - j) * mu for j in range(k)], f'negative side fails t={t}')
    res9['negative_side_blocks'] += 1
# the contradictor's example: s = -10.9, step -60, C = 10
s0, C0 = Fr(-109, 10), Fr(10)
ex = [math.isqrt(math.floor(C0 + (s0 - 60 * j) ** 2)) for j in range(4)]
f_wrong = s0 - math.floor(s0)                                               # 1/10
t0 = -s0
f_true = t0 - math.floor(t0)                                                # 9/10
cond_wrong = C0 < (1 - f_wrong) * (2 * math.floor(t0) + 1 + f_wrong)
cond_true = C0 < (1 - f_true) * (2 * math.floor(t0) + 1 + f_true)
check(ex == [11, 70, 130, 190] and cond_wrong and not cond_true,
      f'negative-side example: {ex}, {cond_wrong}, {cond_true}')
res9['negative_side_example'] = {'word': ex, 'condition_read_with_frac_s': cond_wrong,
                                 'condition_read_with_frac_t': cond_true}
# Proposition R on the P1 family (C = 0, every s, blocks crossing 0 included):
# with M prime, M <= ceil(k/2) - 1 and P not dividing mu, the square-root
# Berlekamp rule is never constant; control: P | mu makes it constant.
for M, fM in ((5, [1, 0, 1, 0, 0]), (7, [1, 1, 0, 0, 0, 0, 0])):
    F = Field(2, M, fM, powers(2, M, fM))
    u = [x & 1 for x in F.pw]
    k = 2 * M + 2
    const = blocks = 0
    for _ in range(20000):
        mu = rng.randrange(1, 40 * F.P)
        if mu % F.P == 0:
            continue
        s = Fr(rng.randrange(-k * mu - 50, 50), 1) + Fr(rng.randrange(0, 101), 101)
        word = [u[math.isqrt(math.floor((s + j * mu) ** 2)) % F.P] for j in range(k)]
        blocks += 1
        const += len(set(word)) == 1
    check(const == 0, f'Proposition R fails M={M}: {const} constant blocks')
    ctrl = len({u[math.isqrt((1000 + j * F.P) ** 2) % F.P] for j in range(k)}) == 1
    check(ctrl, 'control: P | mu should give a constant word')
    res9[f'P1_M={M}_k={k}'] = {'blocks': blocks, 'constant': const, 'control_P_divides_mu_constant': ctrl}
OUT['square_root_rule'] = res9
print('9. Lemma R and Proposition R:', res9)

# ----------------------------------------------------------------------- 10.
# Proposition V (vertex blocks): b >= 1, a >= (2b + 1) k Lam, u = a^2 - b^2,
# x_j = 2ab + j Lam  ==>  isqrt(x_j^2 + u^2) = a^2 + b^2 for every j < k:
# every rule that reads only (box, isqrt(band)) is constant on the block.
res10 = {'instances': 0}
for _ in range(3000):
    k = rng.randrange(3, 200)
    Lam = rng.randrange(1, 10 ** 4)
    b = rng.randrange(1, 50)
    a = (2 * b + 1) * k * Lam + rng.randrange(0, 1000)
    uu = a * a - b * b
    word = {math.isqrt((2 * a * b + j * Lam) ** 2 + uu * uu) for j in range(k)}
    check(word == {a * a + b * b}, f'Proposition V fails k={k} Lam={Lam} a={a} b={b}')
    res10['instances'] += 1
# control: below the threshold the word moves
a = 3                                                      # k = 5, Lam = 1, b = 1: a < 15
moved = len({math.isqrt((2 * a + j) ** 2 + (a * a - 1) ** 2) for j in range(5)})
check(moved > 1, 'control: small a should move the word')
res10['control_small_a_distinct_values'] = moved
OUT['vertex_blocks'] = res10
print('10. Proposition V:', res10)


# ------------------------------------------------------- figures in the text
# Every figure the README quotes from this verifier is read back here, in the
# whitespace-normalised text, so that a stale number fails the check.
_flat = ' '.join((Path(__file__).resolve().parent / 'README.md').read_text().split())


def n_(x):
    return f'{x:,}'.replace(',', ' ')


r9 = OUT['square_root_rule']
p1 = r9['P1_M=5_k=12']['blocks'] + r9['P1_M=7_k=16']['blocks']
r7 = OUT['quadratic_windows_evidence']
FIGURES = [
    f"(Check 9: {n_(r9['aligned_blocks'])} aligned blocks; among {n_(r9['not_aligned_blocks'])} "
    f"unaligned ones, {n_(r9['not_aligned_not_arithmetic'])} give a word",
    f"(Check 9: {n_(p1)} `P1` blocks",
    f"Proposition R on {n_(p1)} `P1` blocks",
    f"{r9['negative_side_blocks']:,}".replace(',', ' ') + ' negative-side blocks',
    f"`P = 31`: {r7['M=5']['mono_quadratic']} of {r7['M=5']['windows']} against "
    f"{round(r7['M=5']['chance'])} expected",
    f"`P = 127`: {r7['M=7']['mono_quadratic']} of {n_(r7['M=7']['windows'])} against "
    f"{round(r7['M=7']['chance'])}",
    f"random coloring of `ℤ/127` has a run of {OUT['polychromatic_blocks']['control_random_Z127_longest_run']}",
    f"below `N` for every `k ≥ {OUT['scale']['threshold_r=2_berlekamp']}` when `r = 2`, "
    f"`k ≥ {OUT['scale']['threshold_r=3']}` when `r = 3`, and `k ≥ {OUT['scale']['threshold_all_r']}`",
]
for fig in FIGURES:
    check(fig in _flat, f'figure missing or stale in README: {fig!r}')
OUT['figures_read_back'] = len(FIGURES)

# ----------------------------------------------------------- frozen statements
# The statements are frozen by hash: header line up to the next '## ' header,
# whitespace-normalised. Changing a statement means changing this table.
FROZEN = {
    'PREAMBLE': 'bddcca22048025270eb556eb75b699b3514a5cc590d893f536f72ca5f15fa0c7',
    '## 2. Setting and translation': 'cbc850bed71364cc2d23f54679faaf550b114d87954e57d3484e1555ac65d1e5',
    '## 1. The sources': '29efc9cbe2357fcbc657fffaa9dc83692a47d80168bbaa7cce758cef348f2658',
    '## 3. The certificate': '23b77119e8c545651ab8c212e0a67789a53f5bde2c35356b6d0eed3986deb1e8',
    '## 4. Theorem 1 (the scale)': 'e08db8ad52638918403ddac45e4e05c004922791c2302351f677c4c4449b29fc',
    '## 5. Carrying it to N': '9bb991b64b52f55ca35566b89eb445792fbdd3fcb07f84a3bd021ffbe84e49ff',
    '## 6. Answers': '5ee10d796a546718fff0b40fd4462ad96c89b11dc49b6d2b396d6d6c5928ef7a',
    '## What is not claimed': '5fd9f6454ae7b859d7622c43b8bd4e0eb217db8d2abac783a375535a8f719b62',
}
_text = (Path(__file__).resolve().parent / 'README.md').read_text()


def section(head):
    if head == 'PREAMBLE':
        pre = _text.split('\n## ', 1)[0]
        return hashlib.sha256(' '.join(pre.split()).encode()).hexdigest()
    if head not in _text:
        return None
    body = _text.split(head, 1)[1]
    nxt = body.find('\n## ')
    body = body if nxt < 0 else body[:nxt]
    return hashlib.sha256(' '.join((head + body).split()).encode()).hexdigest()


for head, h in FROZEN.items():
    got = section(head)
    if '--print-sections' in sys.argv:
        print(f'   {head}: {got}')
    check(got == h, f'frozen section changed: {head}')
OUT['frozen_sections'] = sorted(FROZEN)
# ---------------------------------------------------------------- provenance
here = Path(__file__).resolve().parent
OUT['fails'] = len(FAIL)
summary = json.dumps(OUT, indent=1, sort_keys=True, ensure_ascii=False)
if '--write' in sys.argv:
    if FAIL:
        print(f'{len(FAIL)} check(s) failed: RESULT.json not written')
        sys.exit(1)
    (here / 'RESULT.json').write_text(summary + '\n')
else:
    stored = (here / 'RESULT.json').read_text().strip()
    check(stored == summary, 'summary differs from RESULT.json')
    man = json.loads((here / 'MANIFEST.json').read_text())
    for name, h in man.items():
        got = hashlib.sha256((here / name).read_bytes()).hexdigest()
        check(got == h, f'MANIFEST: {name}')
print(summary)
if FAIL:
    print(f'{len(FAIL)} check(s) failed')
    sys.exit(1)
print('Test passé : all checks pass')
