"""Checks for: a local lemma on keyed frozen sets is a first moment, and what
algebraic rules of large modulus can and cannot do for (II).

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the last line is "Test passé : all checks pass" and the JSON summary printed
before it must equal RESULT.json; --write regenerates RESULT.json).

What is checked (the proofs are in README.md; these checks illustrate them):

  A. Clique bound (Theorem A).
     1. For random x in (0,1)^m (exact Fractions):
        sum_i x_i prod_{j != i}(1 - x_j) <= 1 - prod_j (1 - x_j) < 1,
        so asymmetric-LLL weights on a clique force sum_i P(E_i) < 1.
     2. Shearer: on random small graphs containing a clique K, random
        probability vectors in Shearer's region (independence polynomial
        Z_S(-p) > 0 on every induced S) all have sum_K p < 1; vectors with
        sum_K p >= 1 are all outside the region.
     3. The covering instance of the proof: events sharing one variable U,
        uniform on a grid, laid as consecutive arcs of lengths mu(E) with
        sum >= 1, cover every value of U.
     4. Double counting on the toy group: sum_P mu(B_P) r(P) equals
        sum_kappa sum_{P contains kappa} mu(B_P) for a product law.
     5. Exponent table: log|K| / log N -> 0 in the template regime.

  B. Large-modulus rules (Part B), on the toy group q = 31, D = 2, k = 6,
     lam = 12 (exhaustive over all (n0, d), d != 0), with the source's U mesh
     and adaptive V mesh (floats; the toy has no boundary ties):
     1. multiplicity of a key on a progression <= 4;
     2. pairs (n0, d) with a repeated full label <= N^2 (1/lam + k^2/(2N));
     3. E[Y] = k delta_X and E[Y(Y-1)] = k(k-1) P(pair) exactly, for every
        rule tested (Y = number of positions of P whose key lies in X);
     4. density lemma: some all-light P has >= k(delta_X - eta)/4 distinct
        X-keys, for non-residue rules chi_l(t - c) = -1 with l prime > q;
     5. shift average: (1/l) sum_c delta(X_c) = (l - 1)/(2l) exactly;
     6. squares family (toy q = 101, D = 2, k = 6, lam = 12 and lam = 40 > k^2):
        for every a with
        -q/2 <= a and a + k - 1 < q/2, the progression n_j = lam^{-1}(a + j)
        has k distinct U labels in coordinate D alone (hence k distinct full
        labels, all light) and bands exactly (a + j)^2.
"""
import bisect
import json
import math
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)


# ---------------------------------------------------------------- Part A ---

def part_a1(rng):
    n = 0
    for _ in range(300):
        m = rng.randint(1, 9)
        xs = [Fraction(rng.randint(1, 999), 1000) for _ in range(m)]
        prod_all = Fraction(1)
        for x in xs:
            prod_all *= 1 - x
        s = Fraction(0)
        for i, x in enumerate(xs):
            t = x
            for j, y in enumerate(xs):
                if j != i:
                    t *= 1 - y
            s += t
        check(s <= 1 - prod_all, 'A1 identity')
        check(s < 1, 'A1 strict')
        n += 1
    return n


def independent_sets(n, adj):
    out = []
    for mask in range(1 << n):
        ok = True
        for i in range(n):
            if mask >> i & 1 and adj[i] & mask:
                ok = False
                break
        if ok:
            out.append(mask)
    return out


def in_shearer(n, adj, p, indep):
    # Z_S(-p) > 0 for every vertex subset S
    for S in range(1 << n):
        z = Fraction(0)
        for I in indep:
            if I & ~S:
                continue
            t = Fraction(1)
            sign = 1
            for i in range(n):
                if I >> i & 1:
                    t *= p[i]
                    sign = -sign
            z += sign * t
        if z <= 0:
            return False
    return True


def part_a2(rng):
    inside = outside_big = 0
    for _ in range(40):
        n = rng.randint(3, 6)
        ksz = rng.randint(2, n)
        K = list(range(ksz))
        adj = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if (i in K and j in K) or rng.random() < 0.4:
                    adj[i] |= 1 << j
                    adj[j] |= 1 << i
        indep = independent_sets(n, adj)
        for _ in range(15):
            p = [Fraction(rng.randint(1, 60), 100) for _ in range(n)]
            sk = sum(p[i] for i in K)
            ok = in_shearer(n, adj, p, indep)
            if ok:
                inside += 1
                check(sk < 1, 'A2 Shearer point with clique sum >= 1')
            if sk >= 1:
                outside_big += 1
                check(not ok, 'A2 clique sum >= 1 inside Shearer')
    return inside, outside_big


def part_a3(rng):
    cases = 0
    for _ in range(200):
        g = rng.randint(50, 400)               # U uniform on {0, ..., g-1}
        m = rng.randint(2, 12)
        mus = [Fraction(rng.randint(1, g), g) for _ in range(m)]
        if sum(mus) < 1:
            mus[-1] += 1 - sum(mus)
        covered = [False] * g
        start = Fraction(0)
        for mu in mus:                        # arc [start, start + mu) mod 1
            for u in range(g):
                v = Fraction(u, g)
                off = (v - start) % 1
                if off < mu:
                    covered[u] = True
            start = (start + mu) % 1
        check(all(covered), 'A3 cover')
        # marginals are exact: each arc has measure mu (arc length on grid)
        cases += 1
    return cases


def exponent_table():
    rows = []
    for a in (0.2, 0.3, 0.45):
        for c in (0.111, 0.125, 0.2):
            for lk in (2 ** 6, 2 ** 10, 2 ** 14):   # log2 k
                # D = k^a, ln q = c k^(1-a) ln k, |V| = 2m with
                # m <= 2 k^2 (D+1) ln q, |K| <= |V|^D (D q^2/4 + 1).
                # log|K| / log N = ln(2|V|)/ln q + 2/D + (ln D + 1)/(D ln q),
                # every term computed in logarithms (the numbers overflow).
                lnk = lk * math.log(2)
                lnD = a * lnk
                lnlnq = math.log(c) + (1 - a) * lnk + math.log(lnk)
                lnm = math.log(2) + 2 * lnk + lnD + math.log(2) + lnlnq
                t1 = math.exp(math.log(math.log(4) + lnm) - lnlnq)
                t2 = 2 * math.exp(-lnD)
                t3 = (lnD + 1) * math.exp(-lnD - lnlnq)
                rows.append({'a': a, 'c': c, 'log2_k': lk,
                             'ratio_logK_logN': float('%.3g' % (t1 + t2 + t3))})
    for a, c in {(r['a'], r['c']) for r in rows}:
        seq = [r['ratio_logK_logN'] for r in rows
               if r['a'] == a and r['c'] == c]
        check(seq == sorted(seq, reverse=True), 'A5 ratio not decreasing')
    check(max(r['ratio_logK_logN'] for r in rows if r['log2_k'] == 2 ** 14)
          < 0.01, 'A5 ratio at k = 2^(2^14)')
    return rows


# ---------------------------------------------------------- toy geometry ---

class Toy:
    def __init__(self, q, D, k, lam):
        assert math.gcd(lam, q) == 1 and lam % 2 == 0
        self.q, self.D, self.k, self.lam = q, D, k, lam
        self.N = q ** D
        H = Fraction(1, k * k)
        self.UK = k * k * lam                    # U intervals per circle
        alpha = 1.0 / q ** (D + 1)
        R = math.log(1 + 1 / (2 * alpha))
        m = math.ceil(k * k * R)
        self.a = [alpha * (math.exp(l * R / m) - 1) for l in range(m + 1)]
        self.a[m] = 0.5
        self.m = m
        self.H = H

    def vlabel(self, num, den):
        # Y = num/den in [-1/2, 1/2)
        Y = num / den
        if Y < 0:
            u = Y + 0.5
            l = bisect.bisect_right(self.a, u) - 1
            return ('L', l)
        u = 0.5 - Y
        l = bisect.bisect_left(self.a, u) - 1
        return ('R', max(l, 0))

    def position(self, n):
        q, D, lam = self.q, self.D, self.lam
        U, V, cen = [], [], []
        for i in range(1, D + 1):
            Q = q ** i
            xu = n % Q
            U.append(xu * self.UK // Q)
            v = lam * n % Q
            if 2 * v >= Q:
                v -= Q
            cen.append((v, Q))
            V.append(self.vlabel(v, Q))
        # band = floor(sum (q v_i / q^i)^2) = floor(sum v_i^2 q^(2(D-i)) / q^(2(D-1)))
        num = sum(v * v * q ** (2 * (D - i)) for i, (v, _) in
                  enumerate(cen, start=1))
        band = num // q ** (2 * (D - 1))
        return tuple(U), tuple(V), band


def legendre(a, l):
    a %= l
    if a == 0:
        return 0
    return 1 if pow(a, (l - 1) // 2, l) == 1 else -1


def part_b():
    T = Toy(q=31, D=2, k=6, lam=12)
    N, k = T.N, T.k
    U = [None] * N
    V = [None] * N
    band = [0] * N
    for n in range(N):
        U[n], V[n], band[n] = T.position(n)
    keys = {}
    key_id = [0] * N
    lab_id = [0] * N
    labs = {}
    for n in range(N):
        key_id[n] = keys.setdefault((V[n], band[n]), len(keys))
        lab_id[n] = labs.setdefault((U[n], V[n]), len(labs))
    nkeys = len(keys)

    rules = {}
    for l in (37, 101, 211):
        for c in (0, 5, 17):
            rules['chi_%d(t-%d)=-1' % (l, c)] = (l, c)
    inX = {}
    for name, (l, c) in rules.items():
        kx = set()
        for (vw, t), kid in keys.items():
            if legendre(t - c, l) == -1:
                kx.add(kid)
        inX[name] = [key_id[n] in kx for n in range(N)]

    eta = Fraction(2, T.lam) + Fraction(k * k, N)
    bad = 0
    maxmult = 0
    total = 0
    sumY = {r: 0 for r in rules}
    sumYY = {r: 0 for r in rules}
    best_light = {r: 0 for r in rules}
    # double counting (A4): product law rho = 1/10 on all keys, B_P = {>= 2 keys in X}
    rho = Fraction(1, 10)
    s_thr = 2
    lhs = Fraction(0)
    binom_cache = {}

    def mu_B(r):
        if r not in binom_cache:
            binom_cache[r] = sum(Fraction(math.comb(r, i)) * rho ** i *
                                 (1 - rho) ** (r - i) for i in range(s_thr, r + 1))
        return binom_cache[r]

    load = [Fraction(0)] * nkeys
    for d in range(1, N):
        for n0 in range(N):
            pos = [(n0 + j * d) % N for j in range(k)]
            total += 1
            ks = [key_id[p] for p in pos]
            cnt = {}
            for x in ks:
                cnt[x] = cnt.get(x, 0) + 1
            mm = max(cnt.values())
            if mm > maxmult:
                maxmult = mm
            light = len({lab_id[p] for p in pos}) == k
            if not light:
                bad += 1
            ds = set(ks)
            mu = mu_B(len(ds))
            lhs += mu * len(ds)
            for x in ds:
                load[x] += mu
            for r in rules:
                X = inX[r]
                y = sum(1 for p in pos if X[p])
                sumY[r] += y
                sumYY[r] += y * (y - 1)
                if light:
                    dk = len({key_id[p] for p in pos if X[p]})
                    if dk > best_light[r]:
                        best_light[r] = dk
    check(maxmult <= 4, 'B1 key multiplicity > 4')
    bound_bad = Fraction(N * N) * (Fraction(1, T.lam) + Fraction(k * k, 2 * N))
    check(bad <= bound_bad, 'B2 repeated-label count above bound')
    check(lhs == sum(load), 'A4 double counting')

    dens = {}
    for r in rules:
        npos = sum(inX[r])
        delta = Fraction(npos, N)
        dens[r] = delta
        check(Fraction(sumY[r], total) == k * delta, 'B3 first moment ' + r)
        pair = Fraction(npos * (npos - 1), N * (N - 1))
        check(Fraction(sumYY[r], total) == k * (k - 1) * pair,
              'B3 second moment ' + r)
        need = k * (delta - eta) / 4
        check(best_light[r] >= need, 'B4 density lemma ' + r)

    # B5 shift average, exact
    shift = {}
    for l in (37, 101):
        tot = Fraction(0)
        for c in range(l):
            tot += Fraction(sum(1 for n in range(N)
                                if legendre(band[n] - c, l) == -1), N)
        avg = tot / l
        check(avg == Fraction(l - 1, 2 * l), 'B5 shift average l=%d' % l)
        shift[str(l)] = str(avg)

    return {
        'toy': {'q': T.q, 'D': T.D, 'k': k, 'lam': T.lam, 'N': N,
                'V_intervals': 2 * T.m, 'keys': nkeys,
                'progressions': total},
        'max_key_multiplicity': maxmult,
        'repeated_label_pairs': bad,
        'repeated_label_bound': str(bound_bad),
        'eta': str(eta),
        'rules': {r: {'delta_X': '%.4f' % float(dens[r]),
                      'max_distinct_X_keys_on_all_light_P': best_light[r],
                      'lemma_lower_bound': '%.3f' % float(k * (dens[r] - eta) / 4)}
                  for r in sorted(rules)},
        'shift_average': shift,
        'A4_max_key_load': '%.4f' % float(max(load)),
    }


def part_b6(lam):
    T = Toy(q=101, D=2, k=6, lam=lam)
    N, k, q = T.N, T.k, T.q
    inv = pow(T.lam, -1, N)
    tested = 0
    for a in range(-(q // 2), q // 2 - k + 1):
        pos = [inv * (a + j) % N for j in range(k)]
        labs = set()
        u_last = set()
        for j, n in enumerate(pos):
            Uv, Vv, t = T.position(n)
            labs.add((Uv, Vv))
            u_last.add(Uv[-1])
            check(t == (a + j) ** 2, 'B6 band a=%d j=%d' % (a, j))
        check(len(labs) == k, 'B6 labels a=%d' % a)
        # the proof separates the terms in the U label of coordinate D alone
        check(len(u_last) == k, 'B6 U_D labels a=%d lam=%d' % (a, lam))
        tested += 1
    return tested


def main():
    rng = random.Random(20261026)
    res = {'base_commit': '63bef9ca996786a41169de4a0c3d6b3b47b0fe96'}
    res['A1_instances'] = part_a1(rng)
    ins, out = part_a2(rng)
    res['A2_shearer_points_inside'] = ins
    res['A2_points_with_clique_sum_ge_1'] = out
    res['A3_cover_instances'] = part_a3(rng)
    res['A5_exponent_table'] = exponent_table()
    res['B'] = part_b()
    res['B6_squares_family_progressions'] = part_b6(12)
    # lam = 40 > k^2 = 36: the gap 1/lam between two terms is below the
    # U width a mesh coarser by the factor lam would have, so B6 then tests it
    res['B6_squares_family_progressions_lam40'] = part_b6(40)
    res['claims'] = {
        'theorem_A': 'any criterion sound for every variable-generated system '
                     'with the same event-variable incidence and marginals '
                     '(asymmetric LLL, Shearer, cluster expansion, Moser-Tardos, '
                     'variable-version LLL) certifies only if, for every random '
                     'key, the bad events through it have total probability < 1',
        'corollary_A1': 'sum over rich P of mu(B_P) < 4|K|/k when every key is '
                        'random; log|K| = o(log N): LLL = first moment on the '
                        'exponent scale',
        'lemma_B1': '(II) forces position density delta_X <= 4 eps + 2/lam + k^2/N',
        'lemma_B2': 'every rule has exactly the random first and second moments '
                    'of Y along uniform progressions',
        'proposition_B3': 'n_j = lam^-1 (a + j): all labels distinct, bands '
                          'exactly (a + j)^2',
        'new_bound': None,
    }
    out = json.dumps(res, indent=2, sort_keys=True)
    print(out)
    path = os.path.join(HERE, 'RESULT.json')
    if '--write' in sys.argv:
        with open(path, 'w') as f:
            f.write(out + '\n')
    else:
        with open(path) as f:
            check(json.load(f) == json.loads(out), 'RESULT.json differs')
    if FAILS:
        for f in FAILS[:20]:
            print('FAIL:', f)
        print('%d failed checks' % len(FAILS))
        sys.exit(1)
    print('Test passé : all checks pass')


if __name__ == '__main__':
    main()
