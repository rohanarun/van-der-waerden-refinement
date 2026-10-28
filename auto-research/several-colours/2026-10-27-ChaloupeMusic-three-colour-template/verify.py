"""Exact checks for "The template with r colours: W_3(k) > k^{k/7}".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json and refuses to when a check fails).

  1. The r = 2 instance of the region reproduces the published margins of
     source-only-1-8 (balance cap 40499/8000000, gamma b/2 - c = 4681/720000).
  2. The r = 3 explicit tuple satisfies every inequality of the region, with
     exact margins; c = 1/7 > 1/8 > 1/9.  The cap formula is recomputed from
     its proof (sum over the r - 1 other colours) for r = 2..8.  Every margin
     row of the README table, the headline statements and the tuple row are
     read in README.md and must equal what is recomputed here.
  3. Suprema (1 - 1/r)/4 and the best mixed-base combination of the explicit
     coefficients c_2 = 1/9, c_3 = 1/7, against floor(log2 r)/9, r = 2..48.
  4. Case (ii) per-key bound: max(1 - p, p/(r - 1)) = 1 - p for p <= 1/2,
     r >= 2, on an exact grid.
  5. Mixed-base digit product, exhaustively, at k = 4 (outside the theorem's
     regime: this tests the composition step only).  Cyclic colourings C_i of
     Z/N_i (N_i prime > k) with no monochromatic cyclic k-AP, found by
     exhaustive search, give a colouring of {0, ..., N_0 N_1 - 1} with
     r_0 r_1 colours and no monochromatic k-AP of Z.  Control: a constant
     factor makes the product fail.
  6. Mutants of the formulas and of the data: each must be caught.
"""
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('ÉCHEC :', msg)


def cap_formula(r, eps, eps_r, delta, loss=lambda r, eps: (r - 1) * eps):
    """Theorem 6_r: gamma must stay below (1 - 1/r - (r-1) eps)(1 - eps_r)(1 - delta)."""
    return (1 - F(1, r) - loss(r, eps)) * (1 - eps_r) * (1 - delta)


def cap_by_sum(r, eps, eps_r, delta):
    """The same cap recomputed from its proof: every colour v != beta occurs more than
    (1/r - eps)|S| times, and #{c0 != beta} is the sum over the r - 1 other colours."""
    return sum(F(1, r) - eps for _ in range(r - 1)) * (1 - eps_r) * (1 - delta)


def region(r, a, m, b, eps, eps_r, delta, delta_s, gamma, c, cap=cap_formula):
    """The inequalities of § 3: name -> (margin, strict).  Names are the rows of
    the README table at r = 3."""
    return {
        '`b < a`': (a - b, True),
        '`a + b < 1`': (1 - a - b, True),
        '`2a < m`': (m - 2 * a, True),
        '`m < 1`': (1 - m, True),
        '`0 < ε`, `2ε < 2/3`': (min(eps, 1 - F(1, r) - (r - 1) * eps), True),
        '`0 < ε_r ≤ 1/2`': (min(eps_r, F(1, 2) - eps_r), False),
        '`0 < δ, δ_s < 1`': (min(delta, 1 - delta, delta_s, 1 - delta_s), True),
        '`γ < (2/3 − 2ε)(1 − ε_r)(1 − δ)`': (cap(r, eps, eps_r, delta) - gamma, True),
        '`c < γb/2`': (gamma * b / 2 - c, True),
    }


def holds(reg):
    return all(v > 0 if strict else v >= 0 for v, strict in reg.values())


CAP = '`γ < (2/3 − 2ε)(1 − ε_r)(1 − δ)`'
GB = '`c < γb/2`'
README = (Path(__file__).parent / 'README.md').read_text()

# ------------------------------------------------------------------ 1. r = 2
TUPLE = dict(a=F(49, 100), m=F(99, 100), b=F(97, 200), eps=F(1, 200), eps_r=F(1, 200),
             delta=F(1, 200), delta_s=F(1, 2))
r2 = region(2, gamma=F(97, 200), c=F(1, 9), **TUPLE)
check(r2[CAP][0] == F(40499, 8000000), 'r = 2 balance-cap margin differs from source-only-1-8')
check(r2[GB][0] == F(4681, 720000), 'r = 2 margin gamma b/2 - c differs from source-only-1-8')
check(holds(r2), 'r = 2 published tuple fails the region')
check('cap `40499/8000000`' in README and '`γb/2 − c = 4681/720000`' in README,
      'README does not state the r = 2 margins that check 1 recomputes')
OUT['r2_margins'] = {k: str(v[0]) for k, v in r2.items()}
print(f'1. r = 2 reproduces source-only-1-8: cap margin {r2[CAP][0]}, gamma b/2 - c = {r2[GB][0]}')

# ------------------------------------------------------------------ 2. r = 3
G3, C3 = F(13, 20), F(1, 7)
r3 = region(3, gamma=G3, c=C3, **TUPLE)
check(holds(r3), 'r = 3 explicit tuple fails the region')
check(C3 > F(1, 8) > F(1, 9), 'c_3 does not beat 1/8')
for r in range(2, 9):
    check(cap_formula(r, **{k: TUPLE[k] for k in ('eps', 'eps_r', 'delta')})
          == cap_by_sum(r, **{k: TUPLE[k] for k in ('eps', 'eps_r', 'delta')}),
          f'cap formula differs from its proof at r = {r}')
# every margin of the README table at r = 3 is the one recomputed here
for name, (v, _) in r3.items():
    check(f'| {name} | {v} |' in README, f'README margin row differs or is missing: {name} = {v}')
for phrase in ('`W_3(k) > k^{k/7}`', '`c < (1 − 1/r)/4`', '`1/7 − 1/9 = 2/63`',
               '| 49/100 | 99/100 | 97/200 | 1/200 | 1/2 | 13/20 | 1/7 |'):
    check(phrase in README, f'README does not state {phrase}')
OUT['r3_margins'] = {k: str(v[0]) for k, v in r3.items()}
print(f'2. r = 3, gamma = 13/20, c = 1/7: margins {OUT["r3_margins"]}')

# ------------------------------------------------------------------ 3. suprema and combinations
best = {1: F(0)}
explicit = {2: F(1, 9), 3: F(1, 7)}
for r in range(2, 49):
    cand = [best[r // f] + explicit[f] for f in explicit if r // f >= 1 and r >= f]
    best[r] = max(cand + [best[r - 1]])
table = {}
gain = []
for r in range(2, 49):
    s = r.bit_length() - 1
    table[r] = {'floor_log2_r_over_9': str(F(s, 9)), 'best_mixed': str(best[r]),
                'sup_direct': str((1 - F(1, r)) / 4)}
    if best[r] > F(s, 9):
        gain.append(r)
check(gain[:4] == [3, 6, 7, 12], f'unexpected list of r with a gain: {gain[:6]}')
check(all(r >= 3 * 2 ** (r.bit_length() - 2) for r in gain), 'a gain outside r >= 3 2^(s-1)')
check(all(best[r] - F(r.bit_length() - 1, 9) == F(1, 7) - F(1, 9) for r in gain),
      'the gain is not exactly 1/7 - 1/9')
runs, i = [], 0
while i < len(gain):
    j = i
    while j + 1 < len(gain) and gain[j + 1] == gain[j] + 1:
        j += 1
    runs.append(str(gain[i]) if j == i else
                f'{gain[i]}, {gain[j]}' if j == i + 1 else f'{gain[i]}, …, {gain[j]}')
    i = j + 1
gain_text = '`r = ' + ', '.join(runs) + '`'
check(gain_text in README, f'README does not list the gains as {gain_text}')
OUT['table_r_upto_16'] = {str(r): table[r] for r in range(2, 17)}
OUT['gain_r_upto_48'] = gain
OUT['gain_value'] = str(F(1, 7) - F(1, 9))
print(f'3. r with best_mixed > floor(log2 r)/9 (r <= 48): {gain}; gain = {F(1, 7) - F(1, 9)}')

# ------------------------------------------------------------------ 4. case (ii) per-key bound
ok4 = all(max(1 - p, p / (r - 1)) == 1 - p
          for r in range(2, 20) for p in (F(i, 200) for i in range(0, 101)))
check(ok4, 'case (ii): max(1-p, p/(r-1)) != 1-p somewhere')
OUT['case_ii_per_key_bound'] = ok4
print(f'4. max(1-p, p/(r-1)) = 1-p for p <= 1/2, 2 <= r < 20: {ok4}')


# ------------------------------------------------------------------ 5. mixed-base product
def cyclic_ok(col, N, k):
    """No monochromatic cyclic k-AP (d != 0) in Z/N; N prime > k: none degenerate."""
    return not any(len({col[(a + j * d) % N] for j in range(k)}) == 1
                   for a in range(N) for d in range(1, N))


def find_cyclic(N, r, k):
    for col in itertools.product(range(r), repeat=N):
        if col[0] == 0 and cyclic_ok(col, N, k):
            return col
    return None


def product_ok(cols, Ns, k):
    tot = 1
    for n in Ns:
        tot *= n

    def colour(x):
        out = []
        for col, n in zip(cols, Ns):
            out.append(col[x % n])
            x //= n
        return tuple(out)
    cs = [colour(x) for x in range(tot)]
    return not any(len({cs[a + j * d] for j in range(k)}) == 1
                   for d in range(1, tot) for a in range(tot - (k - 1) * d))


res5 = {}
# These toys are far outside the regime of the theorem (k = 4): they test the
# composition step only, not the template.
K5 = 4
for (N0, r0), (N1, r1) in (((11, 2), (5, 3)), ((5, 3), (11, 2)), ((11, 2), (7, 3)), ((7, 3), (5, 3))):
    c0, c1 = find_cyclic(N0, r0, K5), find_cyclic(N1, r1, K5)
    check(c0 is not None and c1 is not None, f'no cyclic colouring for {(N0, r0)} or {(N1, r1)}')
    if c0 is None or c1 is None:
        continue
    ok = product_ok([c0, c1], [N0, N1], K5)
    check(ok, f'mixed product fails for {(N0, r0)} x {(N1, r1)}')
    res5[f'Z/{N0} ({r0} col) x Z/{N1} ({r1} col), k = 4'] = {
        'colours': r0 * r1, 'interval': N0 * N1, 'no_mono_AP': ok}
# control: a factor that is not AP-free in Z/N breaks the product
bad = (0,) * 11
c1 = find_cyclic(5, 3, K5)
ctrl = product_ok([bad, c1], [11, 5], K5)
check(not ctrl, 'control 5: a factor with a monochromatic cyclic AP did not break the product')
res5['control_bad_factor_breaks'] = not ctrl
OUT['mixed_product'] = res5
print(f'5. mixed-base product: {res5}')

# ------------------------------------------------------------------ 6. mutants
# Each mutant changes a formula or a datum; each must be caught by a check above
# (a margin row of the README, the cap's proof, or the region itself).
def caught(reg):
    rows_ok = all(f'| {n} | {v} |' in README for n, (v, _) in reg.items())
    return not (holds(reg) and rows_ok)


def wrong_loss(r, eps):
    return eps                                       # (r-1) eps replaced by eps

mutants = {
    'cap with eps instead of (r-1) eps (formula)': caught(region(3, gamma=G3, c=C3, cap=lambda r, e, er, d:
                                                               cap_formula(r, e, er, d, loss=wrong_loss),
                                                               **TUPLE)),
    'cap formula against its proof, mutated': cap_formula(3, F(1, 200), F(1, 200), F(1, 200), loss=wrong_loss)
                                              != cap_by_sum(3, F(1, 200), F(1, 200), F(1, 200)),
    'c = 1/6 at the explicit tuple': caught(region(3, gamma=G3, c=F(1, 6), **TUPLE)),
    'the r = 3 coefficient at r = 2': caught(region(2, gamma=G3, c=C3, **TUPLE)),
    'b = a': caught(region(3, gamma=G3, c=C3, **{**TUPLE, 'b': TUPLE['a']})),
}
check(all(mutants.values()), f'a mutant is not caught: {mutants}')
OUT['mutants_caught'] = mutants
print(f'6. mutants caught: {mutants}')

# ------------------------------------------------------------------ summary
OUT['fails'] = len(FAIL)
print(json.dumps(OUT, sort_keys=True))
here = Path(__file__).parent
res = here / 'RESULT.json'
if '--write' in sys.argv and FAIL:
    print(f'Test échoué : {len(FAIL)} checks failed, RESULT.json not written')
    sys.exit(1)
if '--write' in sys.argv:
    res.write_text(json.dumps(OUT, sort_keys=True, indent=1) + '\n')
elif res.exists():
    check(json.loads(res.read_text()) == OUT, 'summary differs from RESULT.json')
man = here / 'MANIFEST.json'
if man.exists() and '--write' not in sys.argv:
    import hashlib
    m = json.loads(man.read_text())
    listed = sorted(f.name for f in here.iterdir() if f.is_file() and f.name != 'MANIFEST.json')
    check(sorted(m) == listed, 'MANIFEST does not list exactly the package files')
    for name, h in m.items():
        check(hashlib.sha256((here / name).read_bytes()).hexdigest() == h, 'MANIFEST hash ' + name)
if FAIL:
    print(f'Test échoué : {len(FAIL)} checks failed')
    sys.exit(1)
print('Test passé : all checks pass')
