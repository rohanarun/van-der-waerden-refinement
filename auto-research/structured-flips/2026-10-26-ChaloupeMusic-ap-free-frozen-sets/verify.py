"""Checks for "AP-free frozen key sets cannot carry door 1".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json).

Notation is that of the source (OpenAI, pinned commit fd4aeeb, Sections 2, 5
and 6): q a prime power, N = q^D, the dilation lam, x_i(n) = n/q^i mod 1,
y_i(n) = lam x_i(n), y~ the centred representative in [-1/2, 1/2)^D,
band(n) = floor(||q y~(n)||^2), key = (V-box of y~(n), band).  A fibre is
{r + q^(D-1) m : m in Z/q} with r fixed.

What is checked:

  1. Embedding lemma (Lemma E) on the real-mesh toy of the lens note
     (q = 2^61 - 1, D = 3, lam = 840, k = 145): for random single-label
     fibre progressions m + i delta (i < k, one full label, so a case (ii)
     block) and a prime h not dividing lam*delta with (l-1)h <= k-1, the
     progression n_j = n_0 + j q^(D-1) e, e = delta h^{-1} mod q, has
     n_{ih} = r + q^(D-1)(m + i delta) for i < l (l = 3, 4, 5), its D-th
     step w (centred lam e mod q) has |w|(k-1) >= q, and it is NOT affine
     (the increments of y~(n_j) are not constant): by the dichotomy it is a
     rich progression.  The lower bound |w| >= (q - lam delta)/h of the proof
     is checked.  Control: with h = 5 (which divides lam) the same recipe
     gives a slow, affine progression.
  2. The band triple (Corollary Q): on the three points m, m + delta,
     m + 2 delta, band = floor(theta + v i) + lam^2 delta^2 i^2 (Lemma 1 of
     the lens note), exactly (Fractions).
  3. The reduction (Theorem 3) on small cases, exhaustive: the largest Y for
     which [Y] splits into a 3-AP-free S and a k-AP-free complement is
     W(3, k) - 1, with W(3, k) = 9, 18, 22, 32 for k = 3..6 (known values).
     So "S hits every k-AP of [Y] and S has no 3-AP" is exactly Y < W(3,k).
  4. Digit sets (the bound on useful l): for p prime and L digits, the set
     A_t = {j : the L low base-p digits of j + t are all nonzero} meets no
     p-AP inside [p^L] (exhaustive for p = 3, 5, 7 and small L); the average
     of |A_t cap [K]| over t equals K (1 - 1/p)^L exactly.
  5. Exact numerics (Decimal, 60 digits): for the template (D = k^a,
     h0 = D ceil(ln k)^2, ln q = c k ln k / D) and for the source
     (c = 1e-5, D = ceil(k^(1/10)), h0 = D^2), at k = 2^739, 2^1024, 2^4096:
     ln Y0 (Lemma R scale), the prime condition of Lemma E
     (theta((k-1)/(l-1)) - theta(h0) > ln q, via Rosser-Schoenfeld, at
     l = 3 and at the worst useful l = p0(k) - 1), the
     Behrend density against 1/(2k), the Kelley-Meka / Bloom-Sisask
     critical constant ln(2k)/(ln Y0)^(1/9), the bound p0(k) on useful l,
     and the Rankin/O'Bryant density at every l < p0(k).
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


# mesh and label: transcribed from the lens note's verifier (itself adapted
# from radar-99's single-label obstructions verifier).
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


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


rng = random.Random(20261026)

# ------------------------------------------------- 1-2. embedding on the toy
q, D, k, lam = 2 ** 61 - 1, 3, 145, 840
N = q ** D
alpha, Rmesh, mm = mesh(q, D, k)


def lab(n):
    return label(n, q, D, lam, k, alpha, Rmesh, mm)


def affine(ns):
    ys = [ytilde(n, q, D, lam) for n in ns]
    inc = [tuple(b - a for a, b in zip(ys[j], ys[j + 1])) for j in range(len(ys) - 1)]
    return len(set(inc)) == 1


def single_label_block():
    """A case (ii) block: r + q^(D-1)(m + i delta), i < k, in one full label,
    in the P1 region 1/8 <= y~_D <= 3/8 (bands increasing along the block)."""
    while True:
        r = rng.randrange(q ** (D - 1))
        delta = rng.randint(1, 4000)
        m = rng.randrange(q)
        Y = ytilde(r + q ** (D - 1) * m, q, D, lam)[-1]
        if not (Fraction(1, 8) <= Y <= Fraction(3, 8) - Fraction(k * lam * delta, q)):
            continue
        ns = [r + q ** (D - 1) * (m + i * delta) for i in range(k)]
        if len({lab(n) for n in (ns[0], ns[k // 2], ns[-1])}) == 1 and len({lab(n) for n in ns}) == 1:
            return r, m, delta, ns


primes_h = [p for p in range(11, 73) if is_prime(p)]      # 840 = 2^3 3 5 7: h > 7 never divides lam
emb = {'blocks': 0, 'by_l': {3: 0, 4: 0, 5: 0}, 'min_w_times_k_over_q': None,
       'max_labels_on_P': 0, 'min_labels_on_P': None, 'band_triples': 0}
for trial in range(24):
    r, m, delta, ns = single_label_block()
    check(affine(ns), 'case (ii) block is not affine')
    emb['blocks'] += 1
    for ell in (3, 4, 5):
        hs = [h for h in primes_h if delta % h and (ell - 1) * h <= k - 1]
        h = rng.choice(hs)
        e = delta * pow(h, -1, q) % q
        d = q ** (D - 1) * e
        n0 = ns[0]
        P = [(n0 + j * d) % N for j in range(k)]
        for i in range(ell):
            check(P[i * h] == ns[i], f'embedding: P[{i}h] is not the block point {i}')
        w = lam * e % q
        w = w - q if w > q // 2 else w
        check(abs(w) * h >= q - lam * delta, 'embedding: |w| below (q - lam delta)/h')
        check(abs(w) * (k - 1) >= q, 'embedding: |w|(k-1) < q')
        check(not affine(P), 'embedding: P is affine')
        nl = len({lab(n) for n in P})
        emb['max_labels_on_P'] = max(emb['max_labels_on_P'], nl)
        emb['min_labels_on_P'] = nl if emb['min_labels_on_P'] is None else min(emb['min_labels_on_P'], nl)
        ratio = abs(w) * (k - 1) / q
        if emb['min_w_times_k_over_q'] is None or ratio < emb['min_w_times_k_over_q']:
            emb['min_w_times_k_over_q'] = ratio
        emb['by_l'][ell] += 1
    # Corollary Q: the three bands, Lemma 1 of the lens note with step delta
    s = q * ytilde(ns[0], q, D, lam)[-1]
    C = sum((q * v) ** 2 for v in ytilde(r, q, D, lam)[:-1])
    theta, v = C + s * s, 2 * s * lam * delta
    for i in range(3):
        check(band(ns[i], q, D, lam) == math.floor(theta + v * i) + lam ** 2 * delta ** 2 * i * i,
              'band triple identity')
    emb['band_triples'] += 1
    # control: h = 5 divides lam, the recipe gives a slow affine progression
    if delta % 5:
        e5 = delta * pow(5, -1, q) % q
        P5 = [(ns[0] + j * q ** (D - 1) * e5) % N for j in range(k)]
        check(affine(P5), 'control h = 5: progression should be affine')
emb['min_w_times_k_over_q'] = round(emb['min_w_times_k_over_q'], 4)
emb['by_l'] = {str(a): b for a, b in emb['by_l'].items()}
OUT['embedding_toy'] = emb
print(f'1-2. embedding on the toy (q = 2^61-1, D = 3, lam = 840, k = 145): {emb["blocks"]} case (ii) '
      f'blocks; l = 3, 4, 5 patterns embedded at indices 0, h, 2h, ... of non-affine progressions '
      f'(min |w|(k-1)/q = {emb["min_w_times_k_over_q"]}, {emb["min_labels_on_P"]} to '
      f'{emb["max_labels_on_P"]} labels on P); band triples exact; control h = 5 affine')

# ------------------------------------------------- 3. W(3, k), exhaustive


def max_split(kk, ymax):
    """Largest Y <= ymax such that [Y] = S u A, S without 3-AP, A without kk-AP."""
    best = 0
    col = [0] * (ymax + 1)

    def ok(y, c):
        L = 3 if c == 1 else kk
        for dd in range(1, (y - 1) // (L - 1) + 1):
            if all(col[y - t * dd] == c for t in range(1, L)):
                return False
        return True

    def dfs(y):
        nonlocal best
        if y - 1 > best:
            best = y - 1
        if y > ymax:
            return
        for c in (0, 1):            # 0: complement A, 1: S
            if ok(y, c):
                col[y] = c
                dfs(y + 1)
                col[y] = -1
    col = [-1] * (ymax + 2)
    dfs(1)
    return best


known = {3: 9, 4: 18, 5: 22, 6: 32}
w3 = {}
for kk, W in known.items():
    b = max_split(kk, W + 2)
    w3[str(kk)] = b + 1
    check(b + 1 == W, f'W(3,{kk}) = {b + 1}, expected {W}')
OUT['W3_small'] = w3
print(f'3. W(3,k) from the split formulation: {w3} (known values 9, 18, 22, 32)')

# ------------------------------------------------- 4. digit sets


def has_ap(A, L, lo, hi):
    S = set(A)
    for a in A:
        for dd in range(1, (hi - a) // (L - 1) + 1):
            if all(a + t * dd in S for t in range(L)):
                return True
    return False


digit = {}
for p, L in ((3, 3), (3, 4), (5, 2), (5, 3), (7, 2)):
    M = p ** L
    tot = 0
    for t in range(M):
        A = [j for j in range(M) if all(((j + t) // p ** i) % p for i in range(L))]
        check(not has_ap(A, p, 0, M - 1), f'digit set p={p}, L={L}, t={t} has a p-AP')
        tot += len(A)
    check(Fraction(tot, M) == M * Fraction(p - 1, p) ** L, 'digit set average')
    K = M - 3
    tot = sum(sum(1 for j in range(K) if all(((j + t) // p ** i) % p for i in range(L))) for t in range(M))
    check(Fraction(tot, M) == K * Fraction(p - 1, p) ** L, 'digit set average on [K]')
    digit[f'{p}^{L}'] = 'p-AP-free, average exact'
OUT['digit_sets'] = digit
print(f'4. digit sets: {len(digit)} cases p-AP-free for every shift, averages exact')

# ------------------------------------------------- 5. exact numerics
getcontext().prec = 60
LN2 = Decimal(2).ln()


def D_(x):
    return Decimal(x)


def p0(lnk):
    """Least prime p with (1 - 1/p)^ceil(ln k / ln p) >= 1/4."""
    p = 2
    while True:
        if is_prime(p):
            Ld = (lnk / D_(p).ln()).to_integral_value(rounding='ROUND_CEILING')
            if Ld * (1 - D_(1) / p).ln() >= -D_(4).ln():
                return p
        p += 1


def numerics(log2k, a=None, c=None, source=False):
    k_ = D_(2) ** log2k
    lnk = log2k * LN2
    if source:
        c = D_('1e-5')
        Dd = (k_ ** (D_(1) / 10)).to_integral_value(rounding='ROUND_CEILING')
        h0 = Dd * Dd
        M = (k_.sqrt()).to_integral_value(rounding='ROUND_CEILING')
        lnlam = h0 * (2 * M).ln()
    else:
        Dd = (k_ ** D_(a)).to_integral_value(rounding='ROUND_CEILING')
        h0 = Dd * lnk.to_integral_value(rounding='ROUND_CEILING') ** 2
        lnlam = D_('1.25506') * h0 / h0.ln() * lnk         # pi(h0) < 1.25506 h0/ln h0 factors, each <= 2M <= k
    lnq = D_(c) * k_ * lnk / Dd
    lnY = lnq - lnlam - 2 * lnk - D_(2048).ln()           # Y0 = q / (2048 k^2 lam), Lemma R
    if lnY <= 4 * lnk:
        return None                                       # lam too close to q: outside the regime
    x = (k_ - 1) / 2
    prime_gap = x * (1 - 1 / x.ln()) - D_('1.01624') * h0  # Rosser-Schoenfeld lower bound
    ln2k = lnk + LN2
    behrend = 2 * (2 * LN2 * lnY).sqrt()                   # -ln(Behrend density) at scale Y0
    km_crit = ln2k / lnY ** (D_(1) / 9)                    # KM applies if c_KM exceeds this
    pp = p0(lnk)
    xw = (k_ - 1) / (pp - 2)                              # worst useful l = p0 - 1: x = (k-1)/(l-1)
    prime_gap_worst = xw * (1 - 1 / xw.ln()) - D_('1.01624') * h0
    # Rankin/O'Bryant: -ln density >= n 2^((n-1)/2) (ln Y)^(1/n) - ln(ln Y)/(2n) - C_l, n = ceil(log2 l)
    nmax = max(2, math.ceil(math.log2(pp)))
    rankin = min(n * D_(2) ** (D_(n - 1) / 2) * lnY ** (D_(1) / n) - lnY.ln() / (2 * n)
                 for n in range(2, nmax + 1))
    lrand = 2 * lnY / (k_ / (2 * lnY)).ln()                # random split needs l >= this
    return {'ln_q_log2': float(lnq.ln() / LN2), 'ln_Y0_log2': float(lnY.ln() / LN2),
            'h0_log2': float(h0.ln() / LN2),
            'prime_condition_margin_log2': float((prime_gap / lnq).ln() / LN2),
            'prime_condition_margin_worst_l_log2': float((prime_gap_worst / lnq).ln() / LN2),
            'behrend_minus_ln_density_log2': float(behrend.ln() / LN2),
            'ln_2k_log2': float(ln2k.ln() / LN2),
            'km_critical_constant_log2': float(km_crit.ln() / LN2),
            'p0': pp,
            'rankin_min_exponent_log2': float(rankin.ln() / LN2),
            'random_split_l_log2': float(lrand.ln() / LN2)}


table = {}
for log2k in (739, 1024, 4096):
    for a in ('0.3', '0.45', '0.49'):
        for c in ('1/9', '1/4'):
            cc = D_(Fraction(c).numerator) / D_(Fraction(c).denominator)
            row = numerics(log2k, a, cc)
            if row is None:
                table[f'k=2^{log2k},a={a},c={c}'] = 'outside regime (lam >= q k^-6)'
                continue
            table[f'k=2^{log2k},a={a},c={c}'] = {kk: (round(v, 2) if isinstance(v, float) else v)
                                                 for kk, v in row.items()}
    row = numerics(log2k, source=True)
    table[f'k=2^{log2k},source'] = {kk: (round(v, 2) if isinstance(v, float) else v) for kk, v in row.items()}
for name, row in table.items():
    if isinstance(row, str):
        continue
    check(row['prime_condition_margin_log2'] > 0, f'{name}: prime condition of Lemma E fails')
    check(row['prime_condition_margin_worst_l_log2'] > 0, f'{name}: (S3) fails at l = p0 - 1')
    check(row['ln_Y0_log2'] > row['ln_2k_log2'], f'{name}: Y0 not long')
    check(row['behrend_minus_ln_density_log2'] > row['ln_2k_log2'] + 5,
          f'{name}: Behrend density not far below 1/(2k)')
    check(row['rankin_min_exponent_log2'] > row['ln_2k_log2'],
          f'{name}: a Rankin-type set could reach 1/(2k)')
    check(row['random_split_l_log2'] > math.log2(row['p0']), f'{name}: random split below p0')
OUT['numerics'] = table
for name, row in table.items():
    if isinstance(row, str):
        print(f'5. {name}: {row}')
        continue
    print(f'5. {name}: log2 ln Y0 = {row["ln_Y0_log2"]}, log2(-ln Behrend) = '
          f'{row["behrend_minus_ln_density_log2"]} vs log2 ln 2k = {row["ln_2k_log2"]}; '
          f'KM critical constant 2^{row["km_critical_constant_log2"]}; p0 = {row["p0"]}; '
          f'log2 Rankin exponent = {row["rankin_min_exponent_log2"]}; log2 l_random = '
          f'{row["random_split_l_log2"]}; prime margin 2^{row["prime_condition_margin_log2"]} (l = 3), '
          f'2^{row["prime_condition_margin_worst_l_log2"]} (l = p0 - 1)')

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
