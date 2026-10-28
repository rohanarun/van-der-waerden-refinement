#!/usr/bin/env python3
"""Checks for the moment-certificate note (PROOF.md). Not a formal proof.

Standard library only, exact rationals, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0, last line "Test passé : all checks pass", and a JSON summary equal to RESULT.json.

1. Proposition 7: polynomial hashing over F_Q is exactly d-wise independent (exhaustive, Q = 5, 7).
2. Theorem 1 on toy event systems: under the d-wise hash law, S_1 equals the iid value when d >= k and S_2
   when d >= 2k (exhaustive over seeds); control: some system has S_2 different at d = 2k - 1.
3. Theorem 2: inequality (1) for every n* <= 40, and the converse by an explicit W on {1..n*} with the
   given (S_1, S_2) on a rational grid.
4. Theorem 3 on random laws of W satisfying the certificate: E[W | W <= (1-delta) n*] < 1 for
   delta > 1 - pi; control at delta < 1 - pi.
5. Proposition 5 (blocks) on toy instances: without straddling blocks, the exact block-law probability
   of a failure is at least rho^{j_B} (1-rho)^{n_B}, which is at least the key bound rho^{j_K} (1-rho)^{n_K};
   straddling blocks carrying theta k positions make (II') hold for every draw.
6. Corollary 4's exponents.
7. Negative controls and provenance.
"""
import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
RNG = random.Random(20261027)


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def comb2(w):
    return w * (w - 1) // 2


# ---------------------------------------------------------------- 1. hashing
def poly_values(a, xs, Q):
    return tuple(sum(c * pow(x, i, Q) for i, c in enumerate(a)) % Q for x in xs)


def check_hash_independence():
    cases = 0
    for Q in (5, 7):
        for d in range(1, 4):
            seeds = list(itertools.product(range(Q), repeat=d))
            for xs in itertools.combinations(range(Q), d):
                counts = {}
                for a in seeds:
                    v = poly_values(a, xs, Q)
                    counts[v] = counts.get(v, 0) + 1
                require(len(counts) == Q ** d and set(counts.values()) == {1}, "d-wise uniformity")
                cases += 1
            if d < Q:   # control: d + 1 points are not independent under degree < d
                xs = tuple(range(d + 1))
                counts = {}
                for a in seeds:
                    counts[poly_values(a, xs, Q)] = 1
                require(len(counts) < Q ** (d + 1), "control: (d+1)-wise independence")
    return cases


# ---------------------------------------------------------------- toy event systems
def toy_system(Q, k, nprog, theta_k, rng):
    """Progressions: k positions, each with a key in F_Q (a key at most twice) and a colour.
    Event (P, beta): X misses keys(C_beta) and |C_notbeta \\ X_P| < theta_k (positions)."""
    events = []
    for _ in range(nprog):
        keys = []
        while len(keys) < k:
            x = rng.randrange(Q)
            if keys.count(x) < 2:
                keys.append(x)
        cols = [rng.randrange(2) for _ in range(k)]
        for beta in (0, 1):
            cb = {keys[i] for i in range(k) if cols[i] == beta}
            cnb = [keys[i] for i in range(k) if cols[i] != beta]
            events.append((frozenset(cb), tuple(cnb)))
    return events


def occurs(ev, X):
    cb, cnb = ev
    return not (cb & X) and sum(1 for x in cnb if x not in X) < THETA_K


THETA_K = 1


def moments_hash(events, Q, d, r):
    s1 = s2 = Fr(0)
    seeds = list(itertools.product(range(Q), repeat=d))
    dist = {}
    for a in seeds:
        X = frozenset(x for x in range(Q) if poly_values(a, (x,), Q)[0] < r)
        z = sum(1 for ev in events if occurs(ev, X))
        dist[z] = dist.get(z, 0) + 1
    tot = len(seeds)
    for z, c in dist.items():
        s1 += Fr(z * c, tot)
        s2 += Fr(comb2(z) * c, tot)
    return s1, s2, {z: Fr(c, tot) for z, c in dist.items()}


def moments_iid(events, Q, rho):
    s1 = s2 = Fr(0)
    dist = {}
    for bits in itertools.product((0, 1), repeat=Q):
        X = frozenset(x for x in range(Q) if bits[x])
        pr = Fr(1)
        for b in bits:
            pr *= rho if b else 1 - rho
        z = sum(1 for ev in events if occurs(ev, X))
        dist[z] = dist.get(z, 0) + pr
        s1 += z * pr
        s2 += comb2(z) * pr
    return s1, s2, dist


def check_theorem1():
    Q, k, r = 5, 2, 2
    rho = Fr(r, Q)
    systems, s2_differs = 0, False
    for _ in range(25):
        ev = toy_system(Q, k, 4, THETA_K, RNG)
        i1, i2, _ = moments_iid(ev, Q, rho)
        for d in range(1, 5):
            h1, h2, _ = moments_hash(ev, Q, d, r)
            if d >= k:
                require(h1 == i1, "S_1 equals iid for d >= k")
            if d >= 2 * k:
                require(h2 == i2, "S_2 equals iid for d >= 2k")
            if d == 2 * k - 1 and h2 != i2:
                s2_differs = True
        systems += 1
    require(s2_differs, "control: S_2 never differs at d = 2k - 1")
    return systems


# ---------------------------------------------------------------- 3. Theorem 2
def check_theorem2():
    for n in range(1, 41):
        for w in range(0, n + 1):
            require((1 if w >= 1 else 0) * n <= w * (n + 1 - w), "inequality (1)")
    built = 0
    for n in range(2, 13):
        for s1 in [Fr(x, 4) for x in range(4, 4 * n + 1)]:
            lo_w = int(s1)                                  # lower envelope g(s1) between floor and ceil
            hi_w = min(lo_w + 1, n)
            t = s1 - lo_w
            g = comb2(lo_w) * (1 - t) + comb2(hi_w) * t
            chord = (s1 - 1) * n / 2
            if g > chord:
                continue
            for s2 in sorted({g, chord, (g + chord) / 2}):
                # W = mixture: envelope point (lo_w, hi_w) with weight u, chord point (1, n) with 1 - u
                if chord == g:
                    u = Fr(1)
                else:
                    u = (chord - s2) / (chord - g)
                law = {}
                for w, p in ((lo_w, u * (1 - t)), (hi_w, u * t)):
                    law[w] = law.get(w, 0) + p
                if n > 1:
                    v = (s1 - 1) / (n - 1)                   # chord point: mean s1 on {1, n}
                    law[1] = law.get(1, 0) + (1 - u) * (1 - v)
                    law[n] = law.get(n, 0) + (1 - u) * v
                require(all(p >= 0 for p in law.values()) and sum(law.values()) == 1, "W is a law")
                require(min(w for w, p in law.items() if p > 0) >= 1, "W avoids 0")
                require(sum(w * p for w, p in law.items()) == s1, "W has mean S_1")
                require(sum(comb2(w) * p for w, p in law.items()) == s2, "W has S_2")
                built += 1
    return built


# ---------------------------------------------------------------- 4. Theorem 3
def check_theorem3():
    tested, control = 0, False
    for _ in range(3000):
        n = RNG.randrange(2, 30)
        # a law of W on {0..n}: most mass at 0, some catastrophes near n, some mid values
        p0 = Fr(RNG.randrange(30, 95), 100)
        rest = 1 - p0
        cat = rest * Fr(RNG.randrange(0, 101), 100)
        mid = rest - cat
        law = {0: p0}
        law[n] = law.get(n, 0) + cat
        wm = RNG.randrange(1, n + 1)
        law[wm] = law.get(wm, 0) + mid
        s1 = sum(w * p for w, p in law.items())
        s2 = sum(comb2(w) * p for w, p in law.items())
        pi = 1 - s1 + Fr(2) * s2 / n
        if pi <= 0:
            continue
        for delta in (1 - pi + Fr(1, 1000), (1 - pi + 1) / 2, Fr(1)):
            if delta <= 1 - pi or delta > 1:
                continue
            A = {w: p for w, p in law.items() if w <= (1 - delta) * n}
            pa = sum(A.values())
            require(pa >= pi, "P(A) >= pi")
            require(sum(w * p for w, p in A.items()) / pa < 1, "Theorem 3")
            tested += 1
        dl = (1 - pi) / 2
        if dl > 0:
            A = {w: p for w, p in law.items() if w <= (1 - dl) * n}
            if sum(w * p for w, p in A.items()) / sum(A.values()) >= 1:
                control = True
    require(tested > 500, "too few certified laws")
    require(control, "control: delta < 1 - pi never fails")
    return tested


# ---------------------------------------------------------------- 5. blocks
def check_blocks():
    cases = 0
    for _ in range(400):
        Q, k = 6, 4
        keys = [RNG.randrange(Q) for _ in range(k)]
        cols = [RNG.randrange(2) for _ in range(k)]
        nb = RNG.randrange(1, 4)
        block = [RNG.randrange(nb) for _ in range(Q)]
        theta_k = RNG.randrange(0, 3)
        for beta in (0, 1):
            cb = [keys[i] for i in range(k) if cols[i] == beta]
            cnb = [keys[i] for i in range(k) if cols[i] != beta]
            bb = {block[x] for x in cb}
            bnb = {block[x] for x in cnb}
            straddle = bb & bnb
            free_pos = sum(1 for x in cnb if block[x] in straddle)
            fails_any = False
            for chosen in itertools.product((0, 1), repeat=nb):
                X = {x for x in range(Q) if chosen[block[x]]}
                if not (set(cb) & X) and sum(1 for x in cnb if x not in X) < theta_k:
                    fails_any = True
            if straddle and free_pos >= theta_k:
                require(not fails_any, "straddling blocks with theta k free positions: no failure")
            if not straddle:
                rho = Fr(1, 3)
                need = len(cnb) - theta_k + 1                     # positions of C_notbeta to cover
                if need <= 0:
                    jB = jK = 0
                else:                                             # None: the event is empty
                    jB = min((len(S) for m in range(len(bnb) + 1) for S in itertools.combinations(sorted(bnb), m)
                              if sum(1 for x in cnb if block[x] in S) >= need), default=None)
                    jK = min((len(S) for m in range(len(set(cnb)) + 1) for S in itertools.combinations(sorted(set(cnb)), m)
                              if sum(1 for x in cnb if x in S) >= need), default=None)
                require((jB is None) == (jK is None), "blocks and keys agree on emptiness")
                if jB is not None:
                    exact = Fr(0)
                    for chosen in itertools.product((0, 1), repeat=nb):
                        X = {x for x in range(Q) if chosen[block[x]]}
                        if not (set(cb) & X) and sum(1 for x in cnb if x not in X) < theta_k:
                            pr = Fr(1)
                            for c in chosen:
                                pr *= rho if c else 1 - rho
                            exact += pr
                    lb_block = rho ** jB * (1 - rho) ** len(bb)
                    lb_key = rho ** jK * (1 - rho) ** len(set(cb))
                    require(exact >= lb_block, "block lower bound")
                    require(lb_block >= lb_key, "block bound dominates the key bound")
            cases += 1
    return cases


# ---------------------------------------------------------------- 6. exponents
def check_exponents():
    out = {}
    for a, gamma in ((Fr(49, 100), Fr(49, 100)), (Fr(1, 3), Fr(2, 5))):
        bX = a                                              # supremum: b_X -> a
        sup = bX * gamma / 4
        require(sup < Fr(1, 16), "sup below 1/16")
        require(2 * sup < Fr(1, 8), "remark: twice the sup below 1/8")
        # region min(bX (gamma - theta)/4, theta b/2) approaches sup as theta -> 0, theta b -> infinity
        th = Fr(1, 10 ** 6)
        b = 10 ** 9
        val = min(bX * (gamma - th) / 4, th * b / 2)
        require(sup - val < Fr(1, 10 ** 5), "approach of the supremum")
        out[f"a={a},gamma={gamma}"] = str(sup)
    # 2^k rho^j beats N^2 iff 4c < b_X (gamma - theta): coefficient of k log k
    for c, bX, g, th in ((Fr(1, 20), Fr(49, 100), Fr(49, 100), Fr(1, 100)), (Fr(1, 8), Fr(49, 100), Fr(49, 100), Fr(0))):
        coeff = 2 * c - bX * (g - th) / 2
        require((coeff < 0) == (4 * c < bX * (g - th)), "exponent equivalence")
    return out


# ---------------------------------------------------------------- 7. controls, provenance
def negative_controls():
    rej = {}
    # Theorem 2 with the wrong sign (S_1 + 2 S_2/n* < 1) misses a certified law
    law = {0: Fr(1, 2), 10: Fr(1, 2)}
    s1 = sum(w * p for w, p in law.items()); s2 = sum(comb2(w) * p for w, p in law.items())
    rej["thm2_wrong_sign"] = (s1 - 2 * s2 / 10 < 1) and not (s1 + 2 * s2 / 10 < 1)
    # inequality (1) with denominator n* - 1 (an a.s. bound that is too small) fails at w = n*
    n = 7
    rej["ineq1_too_small_bound"] = (n - 1) > n * ((n - 1) + 1 - n)
    require(all(rej.values()), f"negative control not rejected: {rej}")
    return rej


def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(name for name in manifest if name != "RESULT.json")


def main():
    report = {
        "hash_independence_cases": check_hash_independence(),
        "theorem1_toy_systems": check_theorem1(),
        "theorem2_laws_built": check_theorem2(),
        "theorem3_laws_tested": check_theorem3(),
        "blocks_cases": check_blocks(),
        "corollary4_suprema": check_exponents(),
        "negative_controls_rejected": negative_controls(),
        "integrity_files": integrity(),
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(text)
    stored = HERE / "RESULT.json"
    if "--write" in sys.argv:
        stored.write_text(text)
    else:
        require(stored.read_text() == text, "output differs from RESULT.json")
    print("Test passé : all checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
