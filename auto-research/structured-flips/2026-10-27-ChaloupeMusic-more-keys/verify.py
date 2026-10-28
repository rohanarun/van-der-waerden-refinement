"""Exact checks for "More keys for X: what a refinement of the key map buys and costs".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json).

What is checked:

  1. Proposition 1' (two layers): coarse keys carry the iid flips, fine keys
     (a refinement) carry the frozen set X.  The probability that a toy
     progression ends monochromatic in beta, by enumerating every coarse flip,
     equals the formula of Proposition 1 read with "coarse keys of free
     positions".  Control: counting fine keys instead fails.
  2. Lemma F (a fibre is already separated): on the fibre r + q^(D-1) m',
     s = centred(s0 + lambda m' mod q) has a fixed fractional part, and the band
     floor(C + s^2) takes each value at most twice on {|s| >= q/8}.  Exhaustive
     on several (q, lambda, s0, C).  Control: points spaced 1/q^2 (not separated) break it.
  3. Lemma G (greedy): a family of position-disjoint blocks of k positions,
     under a key map of maximal fibre F, has a key-disjoint subfamily of size
     >= |B| / (k(F-1)+1).  Greedy on random toy key maps.
  4. Theorem A and Observation A': per block, (1-p)^k + p^k >= 2^(1-k); random
     X (density rho) plus iid flips on the SAME keys is iid flips at rate
     pi = rho + (1-rho) p (exhaustive on a toy instance); with flips on the
     coarse keys it is not (control).
  5. Exponents: the case (ii) threshold w (keys) at the witness point; the
     ceilings (1 - kappa)/4 for iid flips and for random X; the rigorous
     (II') failure threshold beta c > (1/2 - theta) bX; the trivial rich
     barrier beta > b/(4c).  Exact rationals where it matters.
  6. Negative controls, each required to fail.
"""
import hashlib
import json
import math
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


rng = random.Random(20261027)

# ------------------------------------------------------------------------ 1.


def random_two_layer(rng, k):
    """Coarse keys of multiplicity <= 2 on k positions; each coarse pair may be
    split into two fine keys.  Returns coarse, fine, c0."""
    coarse, open_ = [], []
    nxt = 0
    for _ in range(k):
        if open_ and rng.random() < 0.35:
            κ = open_.pop(rng.randrange(len(open_)))
        else:
            κ, nxt = nxt, nxt + 1
            open_.append(κ)
        coarse.append(κ)
    fine, seen = [], {}
    for κ in coarse:
        if κ in seen and rng.random() < 0.5:
            fine.append((κ, 1))                  # the refinement splits this pair
        else:
            fine.append((κ, 0))
        seen[κ] = True
    c0 = [rng.randrange(2) for _ in range(k)]
    return coarse, fine, c0


def enumerate_two_layer(coarse, fine, c0, X, p, beta):
    flip_keys = sorted(set(coarse[j] for j in range(len(coarse)) if fine[j] not in X))
    total = Fraction(0)
    for bits in product((0, 1), repeat=len(flip_keys)):
        E = dict(zip(flip_keys, bits))
        final = [c0[j] ^ (1 if fine[j] in X else E[coarse[j]]) for j in range(len(c0))]
        if all(v == beta for v in final):
            w = Fraction(1)
            for b_ in bits:
                w *= p if b_ else 1 - p
            total += w
    return total


def formula_two_layer(coarse, fine, c0, X, p, beta, count='coarse'):
    k = len(c0)
    frozen = [fine[j] in X for j in range(k)]
    c1 = [c0[j] ^ frozen[j] for j in range(k)]
    D = [j for j in range(k) if c1[j] != beta]
    if any(frozen[j] for j in D):                                   # (b)
        return Fraction(0)
    key = coarse if count == 'coarse' else fine
    need = {key[j] for j in D}
    keep = {key[j] for j in range(k) if not frozen[j] and j not in D}
    if need & keep:                                                 # (a)
        return Fraction(0)
    return p ** len(need) * (1 - p) ** len(keep)


p = Fraction(1, 5)
n1, nz, ctrl1 = 0, 0, False
for _ in range(500):
    k = rng.randrange(3, 10)
    coarse, fine, c0 = random_two_layer(rng, k)
    X = {f for f in set(fine) if rng.random() < rng.choice((0.1, 0.3, 0.6))}
    for beta in (0, 1):
        e = enumerate_two_layer(coarse, fine, c0, X, p, beta)
        check(e == formula_two_layer(coarse, fine, c0, X, p, beta),
              f"Proposition 1' on {coarse} {fine} {c0} {sorted(X)} beta={beta}")
        nz += e > 0
        if e != formula_two_layer(coarse, fine, c0, X, p, beta, count='fine'):
            ctrl1 = True
    n1 += 1
check(ctrl1, 'control 1: counting fine keys never differs')
OUT['prop1_two_layer'] = {'instances': n1, 'nonzero_events': nz, 'p': str(p),
                          'control_fine_count_fails': ctrl1}
print(f"1. Proposition 1' (flips on coarse keys, X on fine keys) exact on {n1} instances "
      f"({nz} non-empty events); counting fine keys fails (control)")

# ------------------------------------------------------------------------ 2.


def fibre_multiplicity(q, lam, s0, C, spacing=Fraction(1)):
    """Max number of m' in Z/q with |s| >= q/8 sharing a band floor(C + s^2)."""
    bands = {}
    for m in range(q):
        u = (s0 + spacing * lam * m) % q
        s = u - q if u >= Fraction(q, 2) else u            # centred, in [-q/2, q/2)
        if abs(s) * 8 < q:
            continue
        b = math.floor(C + s * s)
        bands[b] = bands.get(b, 0) + 1
    return max(bands.values())


n2, worst2 = 0, 0
for q in (101, 127, 211, 401, 1009):
    for _ in range(12):
        lam = rng.randrange(2, q)
        while math.gcd(lam, q) != 1:
            lam = rng.randrange(2, q)
        s0 = Fraction(rng.randrange(q * 997), 997)
        C = Fraction(rng.randrange(10 ** 6), 1000)
        mult = fibre_multiplicity(q, lam, s0, C)
        check(mult <= 2, f'Lemma F: multiplicity {mult} at q={q}')
        worst2 = max(worst2, mult)
        n2 += 1
# control: points closer than 4/q (not separated by 1) share bands massively
mult_ctrl = fibre_multiplicity(401, 1, Fraction(401, 4), Fraction(0),
                               spacing=Fraction(1, 401 ** 2))
check(mult_ctrl > 2, 'control 2: unseparated points keep multiplicity <= 2')
OUT['lemma_F'] = {'instances': n2, 'max_multiplicity': worst2,
                  'control_unseparated': mult_ctrl}
print(f'2. Lemma F on {n2} fibres (q up to 1009): each band holds at most {worst2} points '
      f'of {{|s| >= q/8}}; control, spacing 1/q^2: {mult_ctrl}')

# ------------------------------------------------------------------------ 3.
n3 = 0
for _ in range(200):
    k = rng.randrange(2, 6)
    nb = rng.randrange(5, 60)
    F = rng.randrange(1, 5)
    npos = nb * k
    # random key map of maximal fibre F on npos positions
    order = list(range(npos))
    rng.shuffle(order)
    key = [None] * npos
    nxt, i = 0, 0
    while i < npos:
        sz = rng.randrange(1, F + 1)
        for j in order[i:i + sz]:
            key[j] = nxt
        nxt, i = nxt + 1, i + sz
    blocks = [set(key[j] for j in range(b * k, (b + 1) * k)) for b in range(nb)]
    used, chosen = set(), 0
    for B in blocks:
        if not (B & used):
            used |= B
            chosen += 1
    check(chosen * (k * (F - 1) + 1) >= nb, 'Lemma G: greedy below |B|/(k(F-1)+1)')
    n3 += 1
OUT['lemma_G'] = {'instances': n3}
print(f'3. Lemma G (greedy key-disjoint subfamily) on {n3} random key maps')

# ------------------------------------------------------------------------ 4.
for kk in range(1, 13):
    for num in range(0, 21):
        pp = Fraction(num, 20)
        check((1 - pp) ** kk + pp ** kk >= Fraction(1, 2 ** (kk - 1)),
              f'Theorem A: per-block bound at k={kk}, p={pp}')


def final_law(keys, rho, pf, flip_on):
    """Exact law of the flip vector (final xor c0) over random X (iid rho on
    the fine keys) and iid flips pf on `flip_on` keys."""
    fine = sorted(set(keys['fine']))
    flipk = sorted(set(keys[flip_on]))
    law = {}
    for xb in product((0, 1), repeat=len(fine)):
        X = {f for f, b_ in zip(fine, xb) if b_}
        wx = Fraction(1)
        for b_ in xb:
            wx *= rho if b_ else 1 - rho
        for eb in product((0, 1), repeat=len(flipk)):
            E = dict(zip(flipk, eb))
            we = Fraction(1)
            for b_ in eb:
                we *= pf if b_ else 1 - pf
            vec = tuple(1 if keys['fine'][j] in X else E[keys[flip_on][j]]
                        for j in range(len(keys['fine'])))
            law[vec] = law.get(vec, 0) + wx * we
    return law


toy = {'fine': [0, 1, 2, 3], 'coarse': [0, 0, 1, 1]}
rho, pf = Fraction(1, 3), Fraction(1, 7)
pi = rho + (1 - rho) * pf
same = final_law(toy, rho, pf, 'fine')
iid = {}
for vec in product((0, 1), repeat=4):
    w = Fraction(1)
    for v in vec:
        w *= pi if v else 1 - pi
    iid[vec] = w
check(same == iid, "Observation A': random X + flips on the same keys is not iid(pi)")
two = final_law(toy, rho, pf, 'coarse')
ctrl4 = two != iid
check(ctrl4, "control 4: two layers coincide with iid(pi)")
OUT['theorem_A'] = {'per_block_grid': '12 x 21', 'pi': str(pi),
                    'random_X_same_keys_is_iid': same == iid,
                    'two_layers_differ': ctrl4}
print(f"4. (1-p)^k + p^k >= 2^(1-k) on a grid; random X + flips on the same keys = "
      f"iid({pi}); with coarse flips it is not (control)")

# ------------------------------------------------------------------------ 5.
# Witness point of the short-period region (PR #7) and a Door-1 point b = 1.
a, c = Fraction(49, 100), Fraction(1, 9)
LN10 = math.log(10)
lnk = 400 * LN10                                   # k = 10^400, D = k^(49/100)
# H/k = 6 ln q / k + D ln^3 k / k, with D ln q = c k ln k (constants 1)
H_over_k = 6 * float(c) * lnk / 10 ** 196 + 10.0 ** (196 - 400) * lnk ** 3
res5 = {}
for b in (Fraction(97, 200), Fraction(1)):
    w_coarse = 1.01 * H_over_k / (float(b) * lnk)
    w_fine = 1.01 * (H_over_k + math.log(2)) / (float(b) * lnk)
    check(w_fine < 1 / 2, f'threshold w beyond k/2 at b={b}')
    res5[str(b)] = {'w_coarse_over_k': f'{w_coarse:.3e}',
                    'w_two_layer_over_k': f'{w_fine:.3e}'}
OUT['case_ii_threshold'] = res5

# kappa = log_k ln K.  Coarse keys: ln K_c ~ c k^(1-a) ln k + 2 k^a ln k, so
# kappa_c = max(1-a, a) = 1 - a for a < 1/2.
grid = [Fraction(i, 200) for i in range(1, 100)]          # a in (0, 1/2)
sup_flip = max(min(aa, 1 - aa) / 4 for aa in grid)        # (1 - kappa_c)/4, b < 1 - kappa
check(sup_flip < Fraction(1, 8), 'iid ceiling reaches 1/8')
for kap_extra in (Fraction(1, 2), Fraction(2, 3), Fraction(9, 10), Fraction(1)):
    s = max((1 - max(1 - aa, aa, kap_extra)) / 4 for aa in grid)
    check(s <= (1 - kap_extra) / 4 and s < Fraction(1, 8), 'refined ceiling')
# random X: (I') forces bX <= 1 - kappa; Prop. 5 then leaves c < b bX/(4(b+bX)) < bX/4
sup_rand = max(Fraction(b_, 1) * (1 - aa_k) / (4 * (b_ + 1 - aa_k))
               for aa_k in [1 - g for g in grid] for b_ in (1, 10, 1000))
check(sup_rand < Fraction(1, 8), 'random-X ceiling reaches 1/8')
# rigorous (II') failure with N^beta keys: beta c > (1/2 - theta) bX
theta, bX = Fraction(1, 4), Fraction(1, 5)
beta_star = (Fraction(1, 2) - theta) * bX / c
# trivial rich barrier for flips on fine keys: beta > b/(4c), below 1 iff c > b/4
b_bar = Fraction(1, 3)
beta_bar = b_bar / (4 * c)
check(beta_bar < 1, 'trivial barrier threshold not below 1')
OUT['exponents'] = {'sup_iid_flips': str(sup_flip), 'sup_random_X_first_moment': str(sup_rand),
                    'beta_star_II_fails_whp': str(beta_star),
                    'beta_trivial_barrier_at_b_1_3': str(beta_bar)}
print(f"5. case (ii) threshold w/k at b = 1: {res5['1']['w_two_layer_over_k']} (two layers), "
      f"{res5['1']['w_coarse_over_k']} (coarse); ceilings: iid {sup_flip}, random X {sup_rand}, "
      f"both < 1/8; (II') fails w.h.p. for beta > {beta_star} (theta = 1/4, bX = 1/5, c = 1/9)")

# ------------------------------------------------------------------------ 6.
# (a) the per-block bound fails if the two monochromatic colours are not both counted
ctrl6a = (1 - Fraction(1, 2)) ** 6 < Fraction(1, 2 ** 5)
check(ctrl6a, 'control 6a: (1-p)^k alone meets 2^(1-k) at p = 1/2')
# (b) Lemma G is false without the factor k: a block of k = 3 keys, each key
# shared (F = 2) with one of three otherwise disjoint blocks; greedy keeps 1
blocks = [{0, 1, 2}, {0, 3, 4}, {1, 5, 6}, {2, 7, 8}]
used, ch = set(), 0
for B in blocks:
    if not (B & used):
        used |= B
        ch += 1
ctrl6b = ch * (3 * 1 + 1) >= len(blocks) and ch * (1 + 1) < len(blocks)
check(ctrl6b, 'control 6b: Lemma G without k not violated')
OUT['negative_controls'] = {'one_colour_only': ctrl6a, 'greedy_without_k': ctrl6b,
                            'fine_count_in_prop1': ctrl1, 'unseparated_points': mult_ctrl > 2,
                            'two_layers_not_iid': ctrl4}
print('6. negative controls fail as required')

# ---------------------------------------------------------------- provenance
here = Path(__file__).resolve().parent
OUT['fails'] = len(FAIL)
summary = json.dumps(OUT, indent=1, sort_keys=True, ensure_ascii=False)
if '--write' in sys.argv:
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
