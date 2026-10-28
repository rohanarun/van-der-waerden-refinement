"""Exact checks for the local-lemma hub obstruction (b < a for the canonical
local lemma over iid flips).

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary it prints must equal RESULT.json; --write regenerates it).

Definitions are those of 2026-10-20-ChaloupeMusic-single-label-obstructions
(the source's Section 2 meshes and Section 6 keys), copied verbatim below.

  1. Hub lemma.  On q = 2^61 - 1, D = 3, k = 12, lam = 840, the procedure of
     the proof finds n0 = q^(D-1) m whose E = floor(q/(64 k^3 lam)) star
     progressions P_e = {n0 + q^(D-1) j e : j < k}, 1 <= e <= E, all keep the
     full label of n0.  Certified for every e by the two endpoints (U and V
     cells are intervals, x_D and y_D move monotonically without wrap), and
     re-checked position by position on 200 random e plus e = 1 and e = E.
  2. Keys.  On the same sample, every P_e has k distinct keys, all contain
     kappa0 = kappa(n0), and the key sets are pairwise distinct.
  3. Independence polynomial.  Z_{K_{s,t}}(-p) = prod(1-x) + prod(1-y) - 1,
     checked against brute-force enumeration on random small instances.
  4. Toy star (k = 3), exact over all 2^(1 + 2L) flip assignments for L = 4:
     P(no mono) = (1-p)(1-(1-p)^2)^L + p(1-p^2)^L > 0, the variable
     counter-model covers [0, 1) when L(1-p)^3 >= 1, and the canonical
     events are pairwise disjoint across D/I (forced lopsided edges).
  5. Toy star, L = 12, p = 1/4: the canonical family fails the graph test
     (Z_{K_{L,L}} <= 0, exact Fractions); the cover family {hub unflipped}
     plus the I-events passes even the complete-graph test (sum < 1); the
     disjointified refinement passes it too (sum = P(some mono) < 1).
  6. Exponents.  ln E - ln(k ln(1/p) + ln 2) - k(p + p^2) is positive (no
     graph-only or variable-only criterion can certify) at b = a and b > a,
     negative inside b < a once k is large, at k = 10^400, 10^1000, 10^3000
     (lam <= q/(400 k^3) is checked at each).
  7. LP.  With the local lemma the constraints are F (a < 1/2) and B (b < a):
     sup c = 1/8, the same with or without R; relaxing F as well gives 1/4.
"""
import json
import math
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

getcontext().prec = 200
FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL', msg)


# ------------------------------------- definitions (single-label-obstructions)
def centered(fr):
    r = fr - math.floor(fr)
    if r >= Fraction(1, 2):
        r -= 1
    return r


def ytilde(n, q, D, lam):
    return [centered(Fraction(lam * n, q ** i)) for i in range(1, D + 1)]


def xhat(n, q, D):
    return [Fraction(n % q ** i, q ** i) for i in range(1, D + 1)]


def mesh(q, D, k):
    alpha = Decimal(1) / (Decimal(q) ** (D + 1))
    R = (1 + 1 / (2 * alpha)).ln()
    m = int((Decimal(k * k) * R).to_integral_value(rounding='ROUND_CEILING'))
    return alpha, R, m


def v_index(Y, alpha, R, m):
    Yd = Decimal(Y.numerator) / Decimal(Y.denominator)
    if Yd < 0:
        a = Yd + Decimal('0.5')
        side = 'L'
        l = int((m * (1 + a / alpha).ln() / R).to_integral_value(rounding='ROUND_FLOOR'))
    else:
        a = Decimal('0.5') - Yd
        side = 'R'
        l = int((m * (1 + a / alpha).ln() / R).to_integral_value(rounding='ROUND_CEILING')) - 1
    return side, l


def interval_bounds(side, l, alpha, R, m):
    a_l = alpha * ((Decimal(l) * R / m).exp() - 1)
    a_l1 = alpha * ((Decimal(l + 1) * R / m).exp() - 1)
    if side == 'L':
        return Decimal('-0.5') + a_l, Decimal('-0.5') + a_l1
    return Decimal('0.5') - a_l1, Decimal('0.5') - a_l


def u_index(X, k, lam):
    return math.floor(X * k * k * lam)


def label(n, q, D, lam, k, alpha, R, m):
    return (tuple(u_index(x, k, lam) for x in xhat(n, q, D)),
            tuple(v_index(y, alpha, R, m) for y in ytilde(n, q, D, lam)))


def key(n, q, D, lam, k, alpha, R, m):
    return (label(n, q, D, lam, k, alpha, R, m)[1],
            math.floor(sum((q * v) ** 2 for v in ytilde(n, q, D, lam))))


# ---------------------------------------------------------------- 1. hub lemma
q = 2 ** 61 - 1
D, k = 3, 12
lam = 840
alpha, R, mm = mesh(q, D, k)
H = Fraction(1, k * k)
check(q >= 400 * k ** 3 * lam, 'instance: lam above q/(400 k^3)')
E = q // (64 * k ** 3 * lam)
span = (k - 1) * E                    # m-range swept by the largest star progression

# Proof procedure: a U cell t whose y-range [t/k^2, t/k^2 + 1/(2k^2)) lies in
# [1/8 + H, 3/8 - H]; inside its left half, a V cell with room lam*span/q.
hub = None
for t in range(k * k // 8 + 2, k * k // 8 + 40):
    m_lo = -(-t * q // (k * k * lam))                 # first m of U cell t
    m_hi = (2 * t + 1) * q // (2 * k * k * lam)       # end of its left half
    m = m_lo
    while m < m_hi:
        Y = centered(Fraction(lam * m, q))
        if not (Fraction(1, 8) + H <= Y <= Fraction(3, 8) - H):
            break
        side, l = v_index(Y, alpha, R, mm)
        lo_, hi_ = interval_bounds(side, l, alpha, R, mm)
        room = hi_ - Decimal(Y.numerator) / Decimal(Y.denominator)
        if room > Decimal(lam * span) / q * Decimal('1.01'):
            hub = m
            break
        # jump to the first m whose y lies past this V cell
        m += int((room * q / lam).to_integral_value(rounding='ROUND_CEILING')) + 1
    if hub is not None:
        break
check(hub is not None, 'hub: procedure found no n0')
m = hub
n0 = q ** (D - 1) * m
lab0 = label(n0, q, D, lam, k, alpha, R, mm)
n_end = q ** (D - 1) * (m + span)
check(label(n_end, q, D, lam, k, alpha, R, mm) == lab0, 'hub: far endpoint leaves the label')
Y0 = centered(Fraction(lam * m, q))
check(Fraction(1, 8) <= Y0 and Y0 + Fraction(lam * span, q) < Fraction(1, 2),
      'hub: y_D wraps or starts below 1/8')
check((m + span) < q, 'hub: x_D wraps')
s = lam * m % q
check(s == q * Y0 and s >= q / 8, 'hub: s is not the integer q y_D(n0) >= q/8')

rng = random.Random(20261026)
sample = sorted({1, E} | {rng.randint(1, E) for _ in range(200)})
kappa0 = key(n0, q, D, lam, k, alpha, R, mm)
keysets = {}
for e in sample:
    ns = [n0 + q ** (D - 1) * j * e for j in range(k)]
    check(all(label(n, q, D, lam, k, alpha, R, mm) == lab0 for n in ns),
          f'hub: P_e leaves the label, e = {e}')
    ks = [key(n, q, D, lam, k, alpha, R, mm) for n in ns]
    check(ks[0] == kappa0, f'keys: P_e misses kappa0, e = {e}')
    check(len(set(ks)) == k, f'keys: repeated key in P_e, e = {e}')
    check([b for _, b in ks] == [(s + j * lam * e) ** 2 for j in range(k)],
          f'keys: bands differ from (s + j lam e)^2, e = {e}')
    keysets[e] = frozenset(ks)
check(len(set(keysets.values())) == len(keysets), 'keys: two star progressions share a key set')
# negative control: a step 1000 times above E leaves the label
ns = [n0 + q ** (D - 1) * j * 1000 * E for j in range(k)]
check(len({label(n, q, D, lam, k, alpha, R, mm) for n in ns}) > 1,
      'control: step 1000 E should leave the label')
print(f'1. hub: n0 = q^2 * {m}, E = {E} star progressions keep the full label '
      f'(endpoints certify all e; {len(sample)} sampled e checked position by position)')
print(f'2. keys: every sampled P_e has {k} distinct keys, contains kappa0, key sets distinct')


# ------------------------------------------------- 3. independence polynomial
def indep_poly(n, edges, w):
    """Z_G(-w) by brute force over subsets."""
    adj = {frozenset(e) for e in edges}
    tot = Fraction(0)
    for r in range(n + 1):
        for S in combinations(range(n), r):
            if any(frozenset((u, v)) in adj for u, v in combinations(S, 2)):
                continue
            term = Fraction(1)
            for v in S:
                term *= -w[v]
            tot += term
    return tot


for trial in range(40):
    s_, t_ = rng.randint(1, 4), rng.randint(1, 4)
    w = [Fraction(rng.randint(1, 30), 100) for _ in range(s_ + t_)]
    edges = [(i, s_ + j) for i in range(s_) for j in range(t_)]
    px = math.prod((1 - w[i] for i in range(s_)), start=Fraction(1))
    py = math.prod((1 - w[s_ + j] for j in range(t_)), start=Fraction(1))
    check(indep_poly(s_ + t_, edges, w) == px + py - 1, f'Z(K_s,t) formula, trial {trial}')
print('3. Z_{K_{s,t}}(-p) = prod(1-x) + prod(1-y) - 1 on 40 random small instances')


# ------------------------------------------------------------ 4-5. toy stars
def toy_events(L):
    """Hub key 0; progression i has keys 0, 2i+1, 2i+2 (k = 3), outer color 0.
    D_i = all unflipped (mono in 0), I_i = all flipped (mono in 1)."""
    return [(0, 2 * i + 1, 2 * i + 2) for i in range(L)]


def toy_no_mono_exact(L, p):
    return (1 - p) * (1 - (1 - p) ** 2) ** L + p * (1 - p * p) ** L


L, p = 4, Fraction(1, 4)
progs = toy_events(L)
nkeys = 1 + 2 * L
tot = Fraction(0)
disjoint_ok = True
for flips in product((0, 1), repeat=nkeys):
    w = math.prod((p if f else 1 - p for f in flips), start=Fraction(1))
    d = [all(flips[x] == 0 for x in P) for P in progs]
    i_ = [all(flips[x] == 1 for x in P) for P in progs]
    if any(d) and any(i_):
        disjoint_ok = False
    if not any(d) and not any(i_):
        tot += w
check(tot == toy_no_mono_exact(L, p) and tot > 0, 'toy: exact P(no mono) mismatch')
check(disjoint_ok, 'toy: some D_i meets some I_j')
x = (1 - p) ** 3
check(L * x >= 1, 'toy: variable counter-model needs L(1-p)^3 >= 1')
# variable counter-model: every D_i is an interval of the hub variable U ~ [0, 1)
cuts = [min(Fraction(1), i * x) for i in range(L + 1)]
check(cuts[-1] == 1 and all(cuts[i + 1] - cuts[i] <= x for i in range(L)),
      'toy: intervals of length (1-p)^3 do not cover [0, 1)')
print(f'4. toy L={L}: P(no mono) = {tot} > 0 exactly, D/I disjoint, '
      f'yet hub-only intervals of mass {x} cover [0,1): every variable-only criterion fails')

L, p = 12, Fraction(1, 4)
x, y = (1 - p) ** 3, p ** 3
Z = (1 - x) ** L + (1 - y) ** L - 1
check(Z <= 0, 'toy: canonical K_{L,L} should leave the Shearer region')
# negative control: with 4 progressions instead of 12 the same test passes
check((1 - x) ** 4 + (1 - y) ** 4 - 1 > 0, 'control: K_{4,4} at p = 1/4 should stay in the region')
check(L * x >= 3 * math.log(1 / float(p)) + math.log(2), 'toy: graph test threshold')
cover_sum = (1 - p) + L * y
check(cover_sum < 1, 'toy: cover family should pass the complete-graph test')
some_mono = 1 - toy_no_mono_exact(L, p)
check(some_mono < 1, 'toy: disjointified refinement should pass')
print(f'5. toy L={L}, p=1/4: canonical Z_K(L,L) = {float(Z):.4f} <= 0 (fails); '
      f'cover family sum {cover_sum} < 1 and disjointified sum {float(some_mono):.4f} < 1 (pass)')


# ---------------------------------------------------------------- 6. exponents
def lll_margin(kexp10, a, b, c, m_=Decimal('0.99')):
    """ln E - ln(k ln(1/p) + ln 2) - k(p + p^2), with
    ln E >= ln q - ln lam - 3 ln k - ln 67, ln q = c k^(1-a) ln k, p = k^(-b),
    and ln lam bounded as in single-label-obstructions (Rosser-Schoenfeld,
    h_0 = (k^a + 1)(ln k + 1)^2, M = k^m + 1).  Positive: no graph-only or
    variable-only criterion certifies.  Also checks lam <= q/(400 k^3)."""
    a, b = Decimal(str(a)), Decimal(str(b))
    lk = Decimal(kexp10) * Decimal(10).ln()
    k_ = Decimal(10) ** kexp10
    logq = Decimal(c.numerator) / Decimal(c.denominator) * k_ ** (1 - a) * lk
    h0 = (k_ ** a + 1) * (lk + 1) ** 2
    loglam = Decimal('1.25506') * h0 / h0.ln() * (2 * (k_ ** m_ + 1) + 2).ln()
    check(loglam <= logq - Decimal(400).ln() - 3 * lk, f'exponent: lam > q/(400k^3) at k=1e{kexp10}')
    p_ = k_ ** (-b)
    lnE = logq - loglam - 3 * lk - Decimal(67).ln()
    return lnE - (k_ * b * lk + Decimal(2).ln()).ln() - k_ * (p_ + p_ * p_)


rows = []
for a, b, lab in ((0.49, 0.49, 'b = a'), (0.49, 0.495, 'b > a'), (0.49, 0.485, 'b < a')):
    for kx in (400, 1000, 3000):
        mg = lll_margin(kx, a, b, Fraction(1, 9))
        rows.append((lab, kx, mg))
        if lab == 'b < a':
            if kx >= 1000:
                check(mg < 0, f'exponent: b < a should escape the hub at k = 1e{kx}')
        else:
            check(mg > 0, f'exponent: {lab} should be obstructed at k = 1e{kx}')
print('6. exponents (ln E(1-p)^k - ln(k ln(1/p) + ln 2); + means no criterion certifies):')
for lab, kx, mg in rows:
    print(f'     {lab:<6} k=1e{kx:<5} {"+" if mg > 0 else "-"} {abs(mg):.3e}')


# ---------------------------------------------------------------- 7. LP
def sup_b(cons):
    cons = cons + [(Fraction(-1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(-1), Fraction(0)),
                   (Fraction(1), Fraction(0), Fraction(1)), (Fraction(0), Fraction(1), Fraction(1))]
    best = None
    for (a1, b1, r1), (a2, b2, r2) in combinations(cons, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        a_ = (r1 * b2 - r2 * b1) / det
        b_ = (a1 * r2 - a2 * r1) / det
        if all(al * a_ + be * b_ <= rh for al, be, rh in cons):
            best = b_ if best is None or b_ > best else best
    return best


F = (Fraction(1), Fraction(0), Fraction(1, 2))
F_weak = (Fraction(1), Fraction(0), Fraction(1))
B = (Fraction(-1), Fraction(1), Fraction(0))
Rr = (Fraction(1), Fraction(1), Fraction(1))
lp = {
    'union bound: F, B, R': sup_b([F, B, Rr]) / 4,
    'local lemma: F, B': sup_b([F, B]) / 4,
    'local lemma, F relaxed: B': sup_b([F_weak, B]) / 4,
}
check(lp['union bound: F, B, R'] == Fraction(1, 8), 'LP: union bound')
check(lp['local lemma: F, B'] == Fraction(1, 8), 'LP: dropping R should gain nothing')
check(lp['local lemma, F relaxed: B'] == Fraction(1, 4), 'LP: F relaxed')
print('7. LP sup c: ' + ', '.join(f'{n_} -> {v}' for n_, v in lp.items()))

summary = {
    'base_commit': '63bef9ca996786a41169de4a0c3d6b3b47b0fe96',
    'hub_lemma': {
        'hypotheses': ['lambda <= q/(400 k^3)', 'D >= 2'],
        'star': 'P_e = {n0 + q^(D-1) j e : j < k}, 1 <= e <= E = floor(q/(64 k^3 lambda)), one full label, '
                'k distinct keys each, all through kappa0 = kappa(n0)',
    },
    'theorem': {
        'variable_only_criteria_fail_if': 'E (1-p)^k >= 1',
        'graph_only_criteria_fail_if': 'E (1-p)^k >= k ln(1/p) + ln 2',
        'necessary_for_either': 'k (p + p^2) > ln E - ln(k ln(1/p) + ln 2)',
        'exponent_scale': 'b < a',
        'family': 'canonical: one event per progression and color, on its own keys',
    },
    'not_closed': [
        'refined families: a family passing the complete-graph test exists iff P_p(no mono) > 0',
        'cover families: contain door 1 (any X_s with its union bound gives a local-lemma proof)',
        'criteria reading both the variables and the conflict structure beyond Shearer',
    ],
    'R': 'implied by F and B; sup c = 1/8 with or without it',
    'finite_checks': {
        'instance': 'q = 2^61 - 1, D = 3, k = 12, lambda = 840',
        'E': E,
        'hub_m': m,
        'sampled_steps': len(sample),
        'Z_bipartite_instances': 40,
        'toy_exact_P_no_mono_L4_p1_4': str(toy_no_mono_exact(4, Fraction(1, 4))),
        'toy_L12_canonical_Z': str((1 - (1 - Fraction(1, 4)) ** 3) ** 12
                                   + (1 - Fraction(1, 64)) ** 12 - 1),
    },
    'lp_sup_c': {n_: str(v) for n_, v in lp.items()},
}
out = json.dumps(summary, indent=2, sort_keys=True) + '\n'
result = Path(__file__).with_name('RESULT.json')
if '--write' in sys.argv:
    result.write_text(out)
elif not result.exists() or result.read_text() != out:
    check(False, 'RESULT.json differs from the computed summary')

if FAIL:
    print(f'{len(FAIL)} check(s) failed')
    raise SystemExit(1)
print('Test passé : all checks pass')
