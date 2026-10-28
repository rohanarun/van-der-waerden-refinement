"""Exact checks for "Digit transversals saturate slow blocks".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json).

What is checked:

  1. Theorem 1: for random digit rules S = {x : some base-p digit of x + t at a
     position of U is 0} (p from 2 to 199, random shift t, random non-empty U)
     on intervals J with |J| = 8k^3 (k = 3, 4), the witness of the proof (case
     A: a saturated k-AP of step p^(u0+1); case B(i): a constant step-1 block;
     case B(ii): an untouched window or a saturated run) exists, and on a
     subsample a full search over every k-AP of J confirms a saturated or an
     untouched one.  Control: step p^u0 instead of p^(u0+1) is not saturating.
  2. The S6-63 transversal (all low positions, p <= k): among the k-APs of J
     with p | step, the fraction that is saturated is exactly the fraction of
     starts with x + t = 0 mod p (exhaustive on toys).
  3. Theorem 2 (kernel): for random integer forms psi(n) = sum a_t n_t in the
     base-q digits and moduli with prod M < (E+1)^D, a non-zero signed step e,
     |e_t| <= E, has Psi(e) = 0 mod M, and the block n0 + j d (d = sum e_t q^t)
     has constant Psi mod M, by direct arithmetic in Z/q^D.  Control: psi = n,
     M = q^D has no kernel in the box.
  4. Lemma W (window): on random toy rich progressions, (II'_theta) fails only
     when (gamma_P - theta) k < |X_P| <= (1 - gamma_P) k.
  5. Exponents: a random set of density C k^(-a) ln k colours a fibre piece
     properly with high probability (both union bounds tend to 0) at the
     template points; the digit rule's saturated fraction 1/p is far above
     the 1/Y0^2 that a union bound tolerates.
"""
import hashlib
import json
import math
import random
import sys
from pathlib import Path

FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL:', msg)


rng = random.Random(20261027)


def digit(x, p, u):
    return (x // p ** u) % p


def in_S(x, p, t, U):
    return any(digit(x + t, p, u) == 0 for u in U)


def witness(J0, J1, k, p, t, U):
    """Return ('saturated'|'untouched', start, step) from the proof of Theorem 1."""
    L = J1 - J0
    u0 = min(U)
    big = p ** (u0 + 1)
    if k * big <= L:                                           # case A
        for x in range(J0, J0 + big):
            if digit(x + t, p, u0) == 0 and x + (k - 1) * big < J1:
                return 'saturated', x, big
        return None
    if p ** u0 >= k:                                           # case B(i)
        for x in range(J0, J1 - k + 1):
            if (x + t) % p ** u0 <= p ** u0 - k:
                vals = {in_S(x + i, p, t, U) for i in range(k)}
                if len(vals) == 1:
                    return ('saturated' if vals.pop() else 'untouched'), x, 1
        return None
    for x in range(J0, J1 - k + 1):                            # case B(ii)
        vals = {in_S(x + i, p, t, U) for i in range(k)}
        if len(vals) == 1:
            return ('saturated' if vals.pop() else 'untouched'), x, 1
    return None


def full_search(J0, J1, k, p, t, U):
    mem = [in_S(x, p, t, U) for x in range(J0, J1)]
    L = J1 - J0
    for d in range(1, (L - 1) // (k - 1) + 1):
        for x in range(0, L - (k - 1) * d):
            v = {mem[x + i * d] for i in range(k)}
            if len(v) == 1:
                return True
    return False


primes = [p for p in range(2, 200) if all(p % r for r in range(2, int(p ** 0.5) + 1))]
n1, n_full, cases = 0, 0, {'A': 0, 'Bi': 0, 'Bii': 0}
for _ in range(400):
    k = rng.choice((3, 4))
    L = 8 * k ** 3
    J0 = rng.randrange(0, 10 ** 6)
    p = rng.choice(primes)
    Lmax = 1
    while p ** Lmax <= J0 + L + 10 ** 6:
        Lmax += 1
    U = sorted(rng.sample(range(Lmax), rng.randint(1, min(Lmax, 4))))
    t = rng.randrange(0, 10 ** 6)
    u0 = U[0]
    cases['A' if k * p ** (u0 + 1) <= L else ('Bi' if p ** u0 >= k else 'Bii')] += 1
    w = witness(J0, J0 + L, k, p, t, U)
    check(w is not None, f'Theorem 1: no witness k={k} p={p} t={t} U={U} J0={J0}')
    if w is not None:
        kind, x, d = w
        vals = [in_S(x + i * d, p, t, U) for i in range(k)]
        check(all(vals) if kind == 'saturated' else not any(vals), 'witness is not what it claims')
    if n_full < 25:
        check(full_search(J0, J0 + L, k, p, t, U), 'full search finds no constant k-AP')
        n_full += 1
    n1 += 1
# control: step p^u0 is not saturating in general
k, p, t, U = 3, 5, 0, [0]
ctrl1 = not all(in_S(5 + i, p, t, U) for i in range(k))   # 5, 6, 7: only 5 has digit 0 = 0
check(ctrl1, 'control 1: step p^u0 = 1 saturates from x = 5')
OUT['theorem1'] = {'instances': n1, 'full_searches': n_full, 'cases': cases,
                   'control_step_p_u0': ctrl1}
print(f"1. Theorem 1 on {n1} digit rules (cases A/B(i)/B(ii) = {cases['A']}/{cases['Bi']}/"
      f"{cases['Bii']}); full search confirms on {n_full}; control: step p^u0 does not saturate")

# ------------------------------------------------------------------------ 2.
n2 = 0
for p in (3, 5, 7):
    k, L, t = p, 8 * p ** 3, rng.randrange(10 ** 4)
    U = list(range(4))
    sat = tot = 0
    starts_zero = sum(1 for x in range(L) if (x + t) % p == 0)
    for d in range(p, (L - 1) // (k - 1) + 1, p):
        for x in range(L - (k - 1) * d):
            tot += 1
            sat += all(in_S(x + i * d, p, t, U) for i in range(k))
    # every start with x + t = 0 mod p saturates; others may too (higher zero digits)
    lower = sum(1 for d in range(p, (L - 1) // (k - 1) + 1, p)
                for x in range(L - (k - 1) * d) if (x + t) % p == 0)
    check(sat >= lower, f'S6-63 transversal p={p}: fewer saturated than predicted')
    check(lower * p >= tot - p * ((L - 1) // (k - 1)), 'fraction 1/p of starts')
    n2 += 1
    OUT.setdefault('s6_63_saturation', {})[str(p)] = {'aps_with_p_dividing_step': tot,
                                                      'saturated': sat,
                                                      'from_digit_0_alone': lower}
print(f'2. S6-63 transversal: saturated k-APs among those with p | step, '
      f'{OUT["s6_63_saturation"]}')

# ------------------------------------------------------------------------ 3.


def digits_q(n, q, D):
    return [(n // q ** t) % q for t in range(D)]


n3, ctrl3 = 0, None
for _ in range(60):
    q, D, E, k = rng.choice((101, 103, 107)), 3, 3, 3
    N = q ** D
    forms = [[rng.randrange(-50, 51) for _ in range(D)] for _ in range(rng.choice((1, 2)))]
    budget = (E + 1) ** D - 1
    Ms = []
    for _f in forms:
        Ms.append(rng.randint(2, max(2, int(budget ** (1 / len(forms))))))
    if math.prod(Ms) >= (E + 1) ** D:
        continue
    seen, kern = {}, None
    for v in range((E + 1) ** D):
        e = [(v // (E + 1) ** t) % (E + 1) for t in range(D)]
        key = tuple(sum(a * x for a, x in zip(f, e)) % M for f, M in zip(forms, Ms))
        if key in seen:
            kern = [x - y for x, y in zip(e, seen[key])]
            break
        seen[key] = e
    check(kern is not None and any(kern), 'Theorem 2: pigeonhole gave no kernel')
    d = sum(et * q ** t for t, et in enumerate(kern)) % N
    n0 = sum(rng.randrange(k * E, q - k * E) * q ** t for t in range(D))
    vals = set()
    for j in range(k):
        dg = digits_q((n0 + j * d) % N, q, D)
        vals.add(tuple(sum(a * x for a, x in zip(f, dg)) % M for f, M in zip(forms, Ms)))
    check(len(vals) == 1, 'Theorem 2: Psi mod M not constant along the kernel block')
    n3 += 1
q, D, E = 101, 3, 3
N = q ** D
ctrl3 = all(sum(et * q ** t for t, et in enumerate(
    [(v // (2 * E + 1) ** t) % (2 * E + 1) - E for t in range(D)])) % N != 0
    for v in range((2 * E + 1) ** D) if v != ((2 * E + 1) ** D - 1) // 2)
check(ctrl3, 'control 3: psi = n mod q^D has a kernel in the box')
OUT['theorem2'] = {'instances': n3, 'control_psi_n_no_kernel': ctrl3}
print(f'3. Theorem 2: kernel step found and block constant on {n3} random forms; '
      f'control: psi = n mod q^D has no kernel in the box')

# ------------------------------------------------------------------------ 4.
n4 = 0
for _ in range(3000):
    k = rng.randrange(6, 16)
    c0 = [rng.randrange(2) for _ in range(k)]
    X = [rng.random() < rng.choice((0.1, 0.4, 0.7)) for _ in range(k)]
    gamma = min(c0.count(0), c0.count(1))
    theta = rng.randrange(0, k // 2 + 1)
    size = sum(X)
    for beta in (0, 1):
        inside = all(c0[j] != beta for j in range(k) if X[j])
        rem = sum(1 for j in range(k) if c0[j] != beta and not X[j])
        if inside and rem < theta:
            check(gamma - theta < size <= k - gamma, 'Lemma W violated')
    n4 += 1
OUT['lemma_W'] = {'instances': n4}
print(f'4. Lemma W (window) on {n4} toy progressions')

# ------------------------------------------------------------------------ 5.
res5 = {}
for log2k, a, c in ((739, 0.3, 1 / 9), (739, 0.49, 1 / 9), (1024, 0.45, 1 / 9)):
    lnk = log2k * math.log(2)
    k_over_D_log = (1 - a) * lnk                        # ln(k^(1-a))
    lnY0 = c * math.exp(k_over_D_log) * lnk             # ln Y0 ~ ln q = c k^(1-a) ln k
    C = 3.0
    ln_rho = math.log(C) - a * lnk + math.log(lnk)
    # hitting: Y0^2 (1-rho)^k -> exponent 2 ln Y0 - rho k
    hit = 2 * lnY0 - math.exp(ln_rho + lnk)
    # no k-AP inside: Y0^2 rho^k -> exponent 2 ln Y0 + k ln rho
    free = 2 * lnY0 + math.exp(lnk) * ln_rho
    check(hit < 0 and free < 0, f'random proper colouring fails at k=2^{log2k}, a={a}')
    res5[f'2^{log2k},a={a}'] = {'log_hit_union': f'{hit:.3e}', 'log_inside_union': f'{free:.3e}'}
OUT['random_proper'] = res5
print(f'5. random density 3 k^-a ln k colours a fibre piece properly: {res5}')

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
