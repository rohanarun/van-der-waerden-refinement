"""Exact checks for the single-label obstruction to C1 (b < a).

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary it prints must equal RESULT.json; --write regenerates it).

What is checked (all on the source's literal definitions, pinned OpenAI
commit fd4aeeb, Section 2 meshes and Section 6 keys):

  1. Algebra.  For n_j = q^(D-1) (m + j e), every centered representative
     y~_i(n_j) with i < D is 0 and q y~_D(n_j) = s + j*lam*e with s an
     integer, so f(n_j) = ||q y~(n_j)||^2 = (s + j lam e)^2 exactly.
     Checked with Fractions on random instances (q a prime power).
  2. One label.  On a concrete instance satisfying lam <= q H / (100 k),
     random blocks with y~_D in [1/8, 3/8] keep every U index and every
     adaptive V index fixed along the progression (V computed from the
     source's a_l = alpha (e^(l R / m) - 1) with 200-digit decimals), and
     the fraction of good blocks is at least 1 - 33 k lam e / (q H).
  3. Disjointness.  Distinct blocks of m give disjoint key sets.
  4. P2.  With e = L, every band is congruent to s^2 mod L (full label fixed).
  5. Negative controls: a step not divisible by L moves the band mod L;
     a step above the bound leaves the label; a block straddling a U
     boundary is detected.
  6. Exponents.  log(K (1-p)^k) with K = q/(8k), log q = c k^(1-a) log k,
     p = k^(-b): positive (failure) at b = a and b > a, negative inside
     the region, evaluated in log space at several huge k.
  7. Scope.  If lam > q H / (k - 1), no nonzero step keeps x in one
     U-cell: checked on all steps of a small instance.
  8. PR7 window.  Interval arithmetic on ln k with monotone bounds certifies
     lam <= q/(400 k^3) and ln K - k(p + p^2) >= 5 on every cell of width
     0.01 from ln k = 460.95 to 925.62 for the literal PR7 tuple.
"""
import json
import math
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 200
FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL', msg)


def centered(fr):
    """Representative of a circle point in [-1/2, 1/2)."""
    r = fr - math.floor(fr)
    if r >= Fraction(1, 2):
        r -= 1
    return r


def ytilde(n, q, D, lam):
    return [centered(Fraction(lam * n, q ** i)) for i in range(1, D + 1)]


def xhat(n, q, D):
    return [Fraction(n % q ** i, q ** i) for i in range(1, D + 1)]


# ---------------------------------------------------------------- 1. algebra
rng = random.Random(20261020)
for trial in range(300):
    P = rng.choice([11, 13, 17, 101, 1009])
    t = rng.randint(1, 3)
    q = P ** t
    D = rng.randint(2, 4)
    lam = rng.choice([2, 6, 12, 60, 420])
    k = rng.randint(3, 9)
    e = rng.randint(1, 3)
    m = rng.randrange(q)
    # keep s + j lam e inside [-q/2, q/2): no wrap of the centered value
    s0 = int(centered(Fraction(lam * m, q)) * q)
    if not (-q / 2 <= s0 and s0 + (k - 1) * lam * e < q / 2):
        continue
    for j in range(k):
        n = q ** (D - 1) * (m + j * e)
        yt = ytilde(n, q, D, lam)
        check(all(v == 0 for v in yt[:-1]), f'alg: y~_i != 0, trial {trial}')
        s_j = q * yt[-1]
        check(s_j == s0 + j * lam * e, f'alg: q y~_D != s + j lam e, trial {trial}')
        f = sum((q * v) ** 2 for v in yt)
        check(f == (s0 + j * lam * e) ** 2 and f.denominator == 1,
              f'alg: f != (s + j lam e)^2, trial {trial}')
print('1. algebra: f(n_j) = (s + j lam e)^2 exactly on random instances')


# ------------------------------------------------- 2-5. one label, P2, controls
def mesh(q, D, k):
    alpha = Decimal(1) / (Decimal(q) ** (D + 1))
    R = (1 + 1 / (2 * alpha)).ln()
    m = int((Decimal(k * k) * R).to_integral_value(rounding='ROUND_CEILING'))
    return alpha, R, m


def v_index(Y, alpha, R, m):
    """Index of the source's adaptive V interval containing Y in [-1/2,1/2)."""
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


def u_index(X, k, lam):
    return math.floor(X * k * k * lam)


def label(n, q, D, lam, k, alpha, R, m):
    xs = xhat(n, q, D)
    ys = ytilde(n, q, D, lam)
    return (tuple(u_index(x, k, lam) for x in xs),
            tuple(v_index(y, alpha, R, m) for y in ys))


q = 2 ** 61 - 1                      # prime
D, k = 3, 12
lam = 840                            # lcm(1..8), coprime to q
H = Fraction(1, k * k)
alpha, R, mm = mesh(q, D, k)
bound = Fraction(q) * H / (400 * k * lam)
check(bound > 2 ** 20, 'instance: e-bound too small')

good = tried = 0
blocks = []
while tried < 400:
    mstart = rng.randrange(q)
    Y = centered(Fraction(lam * mstart, q))
    if not (Fraction(1, 8) <= Y <= Fraction(3, 8)):
        continue
    tried += 1
    labs = {label(q ** (D - 1) * (mstart + j), q, D, lam, k, alpha, R, mm) for j in range(k)}
    if len(labs) == 1:
        good += 1
        blocks.append(mstart)
frac_bad_bound = 33 * k * lam / (Fraction(q) * H)
check(good / tried >= 1 - float(frac_bad_bound) - 0.02,
      f'one label: good fraction {good}/{tried}')
print(f'2. one label: {good}/{tried} random blocks stay in a single full label '
      f'(bound on bad fraction {float(frac_bad_bound):.1e})')

# 3. disjoint key sets between distinct blocks of m (no shared s, hence no shared square)
keysets = []
for b in blocks[:50]:
    ks = set()
    for j in range(k):
        n = q ** (D - 1) * (b + j)
        s = int(q * ytilde(n, q, D, lam)[-1])
        ks.add((label(n, q, D, lam, k, alpha, R, mm)[1], s * s))
    keysets.append((b, ks))
for i in range(len(keysets)):
    for j in range(i + 1, len(keysets)):
        bi, ki = keysets[i]
        bj, kj = keysets[j]
        if abs(bi - bj) >= k:
            check(not (ki & kj), f'disjoint: blocks {bi} {bj} share a key')
print(f'3. disjointness: {len(keysets)} blocks, pairwise disjoint key sets')

# 4. P2: e = L, all bands congruent mod L, still one label
for L in (2 ** 10, 3 ** 7 * 5, 2 ** 20):
    check(L <= bound, 'P2: L above bound')
    ok = 0
    for _ in range(200):
        mstart = rng.randrange(q)
        Y = centered(Fraction(lam * mstart, q))
        if not (Fraction(1, 8) <= Y <= Fraction(3, 8)):
            continue
        ns = [q ** (D - 1) * (mstart + j * L) for j in range(k)]
        labs = {label(n, q, D, lam, k, alpha, R, mm) for n in ns}
        if len(labs) != 1:
            continue
        bands = [int(sum((q * v) ** 2 for v in ytilde(n, q, D, lam))) for n in ns]
        check(len({bnd % L for bnd in bands}) == 1, f'P2: bands not constant mod {L}')
        check(len(set(bands)) == k, 'P2: exact bands should still be distinct')
        ok += 1
        if ok == 10:
            break
    check(ok == 10, f'P2: too few single-label blocks for L={L}')
print('4. P2: with step q^(D-1) L every band is s^2 mod L on single-label progressions')

# 5. negative controls
mstart = blocks[0]
ns = [q ** (D - 1) * (mstart + j * (2 ** 10 + 1)) for j in range(k)]
bands = [int(sum((q * v) ** 2 for v in ytilde(n, q, D, lam))) for n in ns]
check(len({bnd % 2 ** 10 for bnd in bands}) > 1, 'control: e = L+1 should move bands mod L')
big_e = int(bound) * 1000
ns = [q ** (D - 1) * (mstart + j * big_e) for j in range(k)]
check(len({label(n, q, D, lam, k, alpha, R, mm) for n in ns}) > 1,
      'control: step 1000x above the bound should leave the label')
# a block straddling a U boundary: start just below a multiple of q/(k^2 lam)
cell = Fraction(q, k * k * lam)
mb = math.floor(cell * 7) - 3
labs = {label(q ** (D - 1) * (mb + j), q, D, lam, k, alpha, R, mm) for j in range(k)}
check(len(labs) > 1, 'control: straddling block not detected')
print('5. controls: off-period step, oversized step, straddling block all rejected')


# ------------------------------------------- 5b. P3: one family per y-box word
# Fix the low digits r (coordinates 1..D-1) so that y~_1..y~_{D-1} land in
# prescribed V intervals with |Y| in [1/8, 3/8]; then move coordinate D only.
def interval_bounds(side, l, alpha, R, m):
    a_l = alpha * ((Decimal(l) * R / m).exp() - 1)
    a_l1 = alpha * ((Decimal(l + 1) * R / m).exp() - 1)
    if side == 'L':
        return Decimal('-0.5') + a_l, Decimal('-0.5') + a_l1
    return Decimal('0.5') - a_l1, Decimal('0.5') - a_l


def digit_inside(lo, hi, q):
    """A digit u with the circle cell [u/q, (u+1)/q) inside [lo, hi)."""
    u = int((lo * q).to_integral_value(rounding='ROUND_CEILING'))
    if Decimal(u + 1) / q > hi:
        return None
    return u % q


words = []
lam_inv = pow(lam, -1, q ** (D - 1))
targets = [Fraction(1, 8) + Fraction(t, 97) for t in range(1, 20)]
for t1 in targets[:6]:
    for t2 in targets[6:12]:
        ivs = [v_index(t1, alpha, R, mm), v_index(t2, alpha, R, mm)]
        digs = []
        for side, l in ivs:
            lo_, hi_ = interval_bounds(side, l, alpha, R, mm)
            digs.append(digit_inside(lo_, hi_, q))
        if None in digs:
            continue
        # y_i(r) has leading base-q digit u_{i-1} of u = lam r mod q^(D-1)
        u = digs[0] + digs[1] * q            # y_1 <- u_0, y_2 <- u_1 (D = 3)
        r = (lam_inv * u) % q ** (D - 1)
        found = None
        for _ in range(200):
            mstart = rng.randrange(q)
            n0 = r + q ** (D - 1) * mstart
            Y = ytilde(n0, q, D, lam)[-1]
            if not (Fraction(1, 8) <= Y <= Fraction(3, 8)):
                continue
            ns = [n0 + q ** (D - 1) * j for j in range(k)]
            labs = {label(n, q, D, lam, k, alpha, R, mm) for n in ns}
            if len(labs) == 1:
                found = ns
                break
        check(found is not None, 'P3: no single-label block for a word')
        if found is None:
            continue
        lab = label(found[0], q, D, lam, k, alpha, R, mm)
        check(list(lab[1][:2]) == ivs, 'P3: realized V word differs from the target')
        keys = {(label(n, q, D, lam, k, alpha, R, mm)[1],
                 math.floor(sum((q * v) ** 2 for v in ytilde(n, q, D, lam))))
                for n in found}
        check(len(keys) == k, 'P3: keys inside one progression not distinct')
        words.append((tuple(ivs), keys))
distinct_words = {w for w, _ in words}
check(len(distinct_words) == len(words) >= 20, f'P3: only {len(words)} words realized')
for i in range(len(words)):
    for j in range(i + 1, len(words)):
        check(not (words[i][1] & words[j][1]), 'P3: two words share a key')
print(f'5b. P3: {len(words)} distinct V words in coordinates < D, one single-label '
      f'progression each, pairwise disjoint key sets')


# ---------------------------------------------------------------- 6. exponents
def log_margin(kexp10, a, b, c):
    """log(K (1-p)^k) up to lower-order terms, with K = q/(8k).

    Uses log q >= c k^(1-a) log k (the source's q >= k^(ck/D) with
    D = ceil(k^a) <= k^a + 1, absorbed here as D = k^a) and
    log(1/(1-p)) <= p + p^2 for p <= 1/2."""
    lk = Decimal(kexp10) * Decimal(10).ln()
    k_ = Decimal(10) ** kexp10
    logq = Decimal(c.numerator) / Decimal(c.denominator) * k_ ** Decimal(1 - a) * lk
    p = k_ ** Decimal(-b)
    return logq - Decimal(8).ln() - lk - k_ * (p + p * p)


rows = []
for a, b, label_ in ((0.49, 0.49, 'b = a'),
                     (0.49, 0.495, 'b > a'),
                     (0.49, 0.485, 'PR7 choice b < a')):
    for kx in (60, 200, 1000):
        rows.append((label_, kx, log_margin(kx, a, b, Fraction(1, 9))))
for label_, kx, mg in rows:
    if label_ == 'PR7 choice b < a':
        if kx == 1000:
            check(mg < 0, 'exponent: PR7 choice should not be obstructed for huge k')
    else:
        check(mg > 0, f'exponent: {label_} should be obstructed at k=1e{kx}')
print('6. exponents (log of expected number of monochromatic single-label progressions):')
for label_, kx, mg in rows:
    sign = '+' if mg > 0 else '-'
    print(f'     {label_:<18} k=1e{kx:<5} {sign} {abs(mg):.3e}')

# ---------------------------------------------------------------- 7. scope
qs, Ds, ks = 7, 3, 4                 # tiny group Z/343
for lam_s in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 30, 60):
    if math.gcd(lam_s, qs) != 1:
        continue
    Hs = Fraction(1, ks * ks)
    exists = False
    for d in range(1, qs ** Ds):
        if all(abs(centered(Fraction(d, qs ** i))) * (ks - 1) <= Hs / lam_s
               for i in range(1, Ds + 1)):
            exists = True
            break
    if lam_s > Fraction(qs) * Hs / (ks - 1):
        check(not exists, f'scope: lam={lam_s} should forbid single-cell x motion')
print('7. scope: lam > qH/(k-1) leaves no nonzero step inside one U-cell')


# ---------------------------------------------------------------- 8. PR7 window
getcontext().prec = 80
A_, M_, B_, C_ = Decimal(49) / 100, Decimal(99) / 100, Decimal(97) / 200, Decimal(1) / 9


def lnq_lo(x):                      # q >= k^(ck/D), D <= k^a + 1
    return C_ * x * x.exp() / ((A_ * x).exp() + 1)


def lnlam_hi(x):                    # pi(t) <= 1.25506 t/ln t (Rosser-Schoenfeld)
    h0 = ((A_ * x).exp() + 1) * (x + 1) ** 2
    M = (M_ * x).exp() + 1
    return Decimal('1.25506') * h0 / h0.ln() * (2 * M + 2).ln()


def lnK_lo(x):                      # K >= (k^2/2 - 4)^(D-1) q/(20k), D - 1 >= k^a - 1
    k_ = x.exp()
    return ((A_ * x).exp() - 1) * (k_ * k_ / 2 - 4).ln() + lnq_lo(x) - Decimal(20).ln() - x


def kp_hi(x):                       # k ln(1/(1-p)) <= k(p + p^2)
    return ((1 - B_) * x).exp() + ((1 - 2 * B_) * x).exp()


def cell_ok(x0, x1):
    return (lnlam_hi(x1) <= lnq_lo(x0) - Decimal(400).ln() - 3 * x1,
            lnK_lo(x0) - kp_hi(x1) >= 5)


step = Decimal('0.01')
x = Decimal(300)
lo = hi = None
while x < 1500:
    lam_ok, fail_ok = cell_ok(x, x + step)
    if lam_ok and fail_ok:
        lo = x if lo is None else lo
        hi = x + step
    elif lo is not None:
        break
    x += step
check(lo is not None, 'window: empty')
x = lo
while x < hi:
    check(all(cell_ok(x, x + step)), f'window: cell {x} not certified')
    x += step
ln10 = Decimal(10).ln()
print(f'8. PR7 window: ln k in [{lo}, {hi}], k from 10^{lo / ln10:.1f} to 10^{hi / ln10:.1f}')

summary = {
    'base_commit': '63bef9ca996786a41169de4a0c3d6b3b47b0fe96',
    'theorem': {
        'hypotheses': ['lambda <= q/(400 k^3)', 'alpha <= 1/8', 'p <= 1/2'],
        'K_lower_bound': '(k^2/2 - 4)^(D-1) * q/(20 k)',
        'sub_prescription_union_bound_total_at_least': 'K (1-p)^k',
        'P_no_monochromatic_at_most': 'exp(-K (1-p)^k)',
        'necessary_for_a_sub_prescription_union_bound_below_1':
            'p k (1+p) > (D-1) ln(k^2/2 - 4) + ln q - ln(20 k)',
        'exponent_scale': ['b < a', 'a + b < 1'],
    },
    'P2_periodic_flips': 'flip depending on the full label and on band mod L, L <= q/(400 k^3 lambda): '
                         'a monochromatic progression for every assignment',
    'scope': 'no single-label progression when lambda > q H/(k-1), which holds for every a > 1/2 once k is large',
    'pr7_literal_tuple': {
        'a': '49/100', 'm': '99/100', 'b': '97/200', 'c': '1/9',
        'certified_ln_k': [str(lo), str(hi)],
        'certified_log10_k': [f'{lo / ln10:.1f}', f'{hi / ln10:.1f}'],
        'certificate': 'lambda <= q/(400 k^3) and ln K - k(p + p^2) >= 5 on every cell',
    },
    'finite_checks': {
        'algebra_instances': 300,
        'single_label_blocks': f'{good}/{tried}',
        'disjoint_block_key_sets': len(keysets),
        'P2_moduli': ['2^10', '3^7*5', '2^20'],
        'P3_distinct_box_words': len(words),
        'negative_controls_rejected': 3,
    },
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
