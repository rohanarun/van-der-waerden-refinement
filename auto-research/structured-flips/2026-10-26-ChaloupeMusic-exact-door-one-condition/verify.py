"""Exact checks for "The exact form of Door 1: one condition, two thresholds".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json).

A toy progression is a list of k positions, each with a key (a key occupies at
most two positions, as in Lemma 3 of source-only-1-16) and an outer colour c0.
X is a set of keys, frozen: c1 = c0 xor [key in X], and keys outside X get iid
Bernoulli(p) flips.  Everything is exact (Fractions).

What is checked:

  1. Proposition 1: the probability that the progression ends monochromatic in
     beta, by enumerating every flip of the free keys, equals
     1[(a) and (b)] * p^#keys(D) * (1-p)^#(other free keys),
     D = {c1 != beta}, (a) no key with both c1-colours, (b) no frozen key in D.
  2. The majority case: X equal to the majority class makes the progression
     monochromatic in the minority colour with probability (1-p)^(...) > 0; a
     "minority-only" criterion misses it, the exact criterion does not.
  3. Splitting: X meeting both c0-classes gives probability 0 for both targets.
  4. Corollary 3.1: at most eps*k keys of X and a gamma-balanced c0 give
     |C_notbeta minus X_P| >= (gamma - 2 eps) k whenever X_P lies in C_notbeta.
     Control: gamma - eps (keys read as positions) has a counterexample.
  5. Proposition 5: for small k, the exact probability over a random X (each
     key with probability rho) that (II'_theta) fails at the majority target is
     at least rho^((1/2-theta)k+1) (1-rho)^k.
  6. Exponents: theta*b/2 at b = 1; the optimum b*bX/(4(b+bX)) and its supremum
     bX/4; at bX = a = 49/100 it stays below 1/8.
  7. Negative controls, each required to fail.
"""
import json
import random
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL:', msg)


def random_progression(rng, k, n_keys_hint):
    """Keys of multiplicity <= 2 on k positions, random c0."""
    keys, pos_of = [], {}
    nxt = 0
    for j in range(k):
        reuse = [κ for κ, ps in pos_of.items() if len(ps) == 1]
        if reuse and rng.random() < 0.3:
            κ = rng.choice(reuse)
        else:
            κ, nxt = nxt, nxt + 1
        keys.append(κ)
        pos_of.setdefault(κ, []).append(j)
    c0 = [rng.randrange(2) for _ in range(k)]
    return keys, c0


def enumerate_mono(keys, c0, X, p, beta):
    free = sorted(set(keys) - X)
    total = Fraction(0)
    for bits in product((0, 1), repeat=len(free)):
        f = dict(zip(free, bits))
        final = [c0[j] ^ (1 if keys[j] in X else f[keys[j]]) for j in range(len(keys))]
        if all(v == beta for v in final):
            w = Fraction(1)
            for b_ in bits:
                w *= p if b_ else 1 - p
            total += w
        # (iid weights multiply to the probability of this flip pattern)
    return total


def formula(keys, c0, X, p, beta):
    k = len(keys)
    c1 = [c0[j] ^ (keys[j] in X) for j in range(k)]
    colours = {}
    for j in range(k):
        colours.setdefault(keys[j], set()).add(c1[j])
    if any(len(s) == 2 for s in colours.values()):          # (a)
        return Fraction(0)
    D = {j for j in range(k) if c1[j] != beta}
    if any(keys[j] in X for j in D):                        # (b)
        return Fraction(0)
    kd = {keys[j] for j in D}
    other_free = set(keys) - X - kd
    return p ** len(kd) * (1 - p) ** len(other_free)


rng = random.Random(20261026)
p = Fraction(1, 5)

# ---------------------------------------------------------------- 1. and 3.
n_inst, n_split, n_nonzero = 0, 0, 0
for _ in range(400):
    k = rng.randrange(3, 10)
    keys, c0 = random_progression(rng, k, k)
    allk = sorted(set(keys))
    X = {κ for κ in allk if rng.random() < rng.choice((0.1, 0.3, 0.6))}
    split = any(keys[j] in X and c0[j] == 0 for j in range(k)) and \
        any(keys[j] in X and c0[j] == 1 for j in range(k))
    for beta in (0, 1):
        e, f = enumerate_mono(keys, c0, X, p, beta), formula(keys, c0, X, p, beta)
        check(e == f, f'Proposition 1 on {keys}, {c0}, {sorted(X)}, beta={beta}')
        n_nonzero += e > 0
        if split:
            check(e == 0, 'a split progression is monochromatic')
    n_split += split
    n_inst += 1
OUT['prop1'] = {'instances': n_inst, 'split_instances': n_split,
                'nonzero_events': n_nonzero, 'p': str(p)}
print(f'1. Proposition 1 exact on {n_inst} instances ({n_nonzero} non-empty events); '
      f'3. {n_split} split instances, all with probability 0')

# ------------------------------------------------------------------------ 2.
k = 8
keys = list(range(k))
c0 = [0, 0, 0, 0, 0, 1, 1, 1]                 # majority 0 (5), minority 1 (3)
X = {0, 1, 2, 3, 4}                           # X_P = the majority class
prob_min = enumerate_mono(keys, c0, X, p, 1)  # monochromatic in the minority colour


def minority_only_harmful(keys, c0, X):
    ones = [j for j in range(len(keys)) if c0[j] == 1]
    zeros = [j for j in range(len(keys)) if c0[j] == 0]
    minority = ones if len(ones) <= len(zeros) else zeros
    return {keys[j] for j in minority} <= X and not any(
        keys[j] in X for j in range(len(keys)) if j not in minority)


check(prob_min == (1 - p) ** 3, 'majority case: probability is not (1-p)^3')
check(not minority_only_harmful(keys, c0, X), 'majority case: minority-only criterion caught it')
check(formula(keys, c0, X, p, 1) == prob_min, 'majority case: exact criterion missed it')
OUT['majority_case'] = {'probability_mono_in_minority': str(prob_min),
                        'minority_only_flags_it': minority_only_harmful(keys, c0, X)}
print(f'2. X_P = majority class: monochromatic in the minority colour with probability '
      f'{prob_min} = (1-p)^3; the minority-only criterion misses it')

# ------------------------------------------------------------------------ 4.


def worst_remaining(keys, c0, X):
    """min over beta with X_P inside C_notbeta of |C_notbeta minus X_P| (positions)."""
    k, best = len(keys), None
    for beta in (0, 1):
        if any(keys[j] in X and c0[j] == beta for j in range(k)):
            continue
        rem = sum(1 for j in range(k) if c0[j] != beta and keys[j] not in X)
        best = rem if best is None else min(best, rem)
    return best


n4 = 0
for _ in range(3000):
    k = rng.randrange(6, 16)
    keys, c0 = random_progression(rng, k, k)
    gamma_pos = min(c0.count(0), c0.count(1))          # balance of c0, in positions
    allk = sorted(set(keys))
    budget = rng.randrange(0, k // 3 + 1)              # eps*k keys
    X = set(rng.sample(allk, min(budget, len(allk))))
    w = worst_remaining(keys, c0, X)
    if w is not None:
        check(w >= gamma_pos - 2 * len(X), 'Corollary 3.1 fails')
        n4 += 1
# control: one key on two positions of the minority class, gamma - eps fails
keys_c = [0, 0, 1, 2, 3, 4]
c0_c = [1, 1, 0, 0, 0, 0]
w_c = worst_remaining(keys_c, c0_c, {0})
check(w_c == 2 - 2 * 1, 'control instance')
control4 = w_c < 2 - 1                                  # gamma - eps reading would be violated
check(control4, 'control 4: keys-as-positions reading not violated')
OUT['cor31'] = {'instances': n4, 'control_remaining': w_c}
print(f'4. Corollary 3.1 (theta = gamma - 2 eps, positions) on {n4} instances; '
      f'control: one key on two minority positions leaves {w_c} < gamma - eps')

# ------------------------------------------------------------------------ 5.


def exact_fail_prob(keys, c0, rho, theta_k):
    """Pr over X (iid rho per key) that (II'_theta) fails at the majority target."""
    allk = sorted(set(keys))
    k = len(keys)
    maj = 0 if c0.count(0) >= c0.count(1) else 1
    tot = Fraction(0)
    for bits in product((0, 1), repeat=len(allk)):
        X = {κ for κ, b_ in zip(allk, bits) if b_}
        w = Fraction(1)
        for b_ in bits:
            w *= rho if b_ else 1 - rho
        if any(keys[j] in X and c0[j] == maj for j in range(k)):
            continue                                       # split side: blocked
        rem = sum(1 for j in range(k) if c0[j] != maj and keys[j] not in X)
        if rem < theta_k:
            tot += w
    return tot


n5 = 0
for k in (6, 8, 10):
    for _ in range(25):
        keys = list(range(k))                             # distinct keys (family F)
        c0 = [rng.randrange(2) for _ in range(k)]
        for rho in (Fraction(1, 3), Fraction(1, 8)):
            for theta_k in (1, 2):
                theta = Fraction(theta_k, k)
                lower = rho ** (int((Fraction(1, 2) - theta) * k) + 1) * (1 - rho) ** k
                check(exact_fail_prob(keys, c0, rho, theta_k) >= lower, 'Proposition 5 bound')
                n5 += 1
OUT['prop5'] = {'cases': n5}
print(f'5. Proposition 5 lower bound holds exactly in {n5} cases')

# ------------------------------------------------------------------------ 6.
theta, b = Fraction(1, 2) - Fraction(1, 100), Fraction(1)
c_rich = theta * b / 2
check(c_rich < Fraction(1, 4), 'theta b / 2 not below 1/4')


def opt(b_, bx):
    return b_ * bx / (4 * (b_ + bx))


a = Fraction(49, 100)
grid = [Fraction(n, 10) for n in range(1, 101)] + [Fraction(10 ** e) for e in range(2, 7)]
check(all(opt(bb, a) < Fraction(1, 8) for bb in grid), 'random-like at bX = a reaches 1/8')
check(all(opt(bb, Fraction(1)) < Fraction(1, 4) for bb in grid), 'bX = 1 reaches 1/4')
check(opt(Fraction(10 ** 6), a) > a / 4 - Fraction(1, 10 ** 6), 'sup bX/4 not approached')
# optimum over theta of min(theta b, (1/2 - theta) bX)/2 is at theta = bX/(2(b+bX))
for bb in (Fraction(1, 2), Fraction(1), Fraction(3)):
    th = a / (2 * (bb + a))
    check(th * bb / 2 == opt(bb, a) and (Fraction(1, 2) - th) * a / 2 == opt(bb, a),
          'optimum of theta')
OUT['exponents'] = {'theta_b_over_2_at_b1': str(c_rich), 'random_like_at_bX_a_b1': str(opt(1, a)),
                    'sup_over_b': str(a / 4)}
print(f'6. theta b/2 = {c_rich} < 1/4 at b = 1; random-like with bX = a = {a}: '
      f'c < {opt(1, a)} at b = 1, sup over b = {a / 4} < 1/8')

# ------------------------------------------------------------------------ 7.
# (a) the formula without condition (b) disagrees with enumeration somewhere
def formula_no_b(keys, c0, X, p, beta):
    k = len(keys)
    c1 = [c0[j] ^ (keys[j] in X) for j in range(k)]
    D = {j for j in range(k) if c1[j] != beta}
    kd = {keys[j] for j in D} - X
    return p ** len(kd) * (1 - p) ** len(set(keys) - X - kd)


keys, c0, X = [0, 1, 2, 3], [0, 0, 1, 1], {0}
ctrl_a = formula_no_b(keys, c0, X, p, 0) != enumerate_mono(keys, c0, X, p, 0)
# (b) the cost read with |X ∩ P| in positions instead of keys: key 0 on two positions
keys, c0, X = [0, 0, 1, 2], [1, 1, 1, 0], {0}
wrong = p ** (len({0, 1}) - 2)                          # #keys(C_notbeta) - positions in X
ctrl_b = wrong != enumerate_mono(keys, c0, X, p, 0)
# (c) the minority-only harmful event (check 2)
ctrl_c = not minority_only_harmful([0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 1, 1, 1],
                                   {0, 1, 2, 3, 4})
for name, ok in (('formula without (b)', ctrl_a), ('positions read as keys', ctrl_b),
                 ('minority-only event', ctrl_c), ('Corollary 3.1 with gamma - eps', control4)):
    check(ok, 'negative control did not fail: ' + name)
OUT['negative_controls'] = {'formula_without_b': ctrl_a, 'positions_as_keys': ctrl_b,
                            'minority_only': ctrl_c, 'gamma_minus_eps': control4}
print('7. negative controls fail as required: formula without (b), positions read as keys, '
      'minority-only event, gamma - eps')

# ------------------------------------------------------------------- summary
OUT['fails'] = len(FAIL)
print(json.dumps(OUT, sort_keys=True))
res = Path(__file__).with_name('RESULT.json')
if '--write' in sys.argv:
    res.write_text(json.dumps(OUT, sort_keys=True, indent=1) + '\n')
elif res.exists():
    check(json.loads(res.read_text()) == OUT, 'summary differs from RESULT.json')
man = Path(__file__).with_name('MANIFEST.json')
if man.exists() and '--write' not in sys.argv:
    import hashlib
    m = json.loads(man.read_text())
    pkg = Path(__file__).parent
    listed = sorted(f.name for f in pkg.iterdir() if f.is_file() and f.name != 'MANIFEST.json')
    check(sorted(m) == listed, 'MANIFEST does not list exactly the package files')
    for name, h in m.items():
        check(hashlib.sha256((pkg / name).read_bytes()).hexdigest() == h, 'MANIFEST hash ' + name)
if FAIL:
    print(f'Test échoué : {len(FAIL)} checks failed')
    sys.exit(1)
print('Test passé : all checks pass')
