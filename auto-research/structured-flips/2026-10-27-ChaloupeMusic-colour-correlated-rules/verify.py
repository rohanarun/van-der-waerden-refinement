"""Checks for the colour-correlated-rules note.

1. The combinatorial core of Theorem C, on random small integer lines, with
   two-sided windows; 1b. the referee's control (x1) on the window, exactly.
2. The local-lemma inequality used for families 4a and 4b (Theorem B).
3. Lemma D1's Warren bound on random quadratic toys.
4. The exponent ledger of section 4 at k = 2^4096, and the size of lambda/q
   at k = 2^1024 and 2^4096 (Theorem C needs q > k^3 lambda m).
5. MANIFEST hashes.
Standard library only.  Exit code 0 and last line "Test passé" on success.
"""

import hashlib
import json
import math
import random
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
ALEA = random.Random(20261027)
echecs = []


def exige(cond, message):
    if not cond:
        echecs.append(message)


def runs(mask):
    """Maximal runs of a 0/1 list, as (start, end_exclusive, value)."""
    out, i = [], 0
    while i < len(mask):
        j = i
        while j < len(mask) and mask[j] == mask[i]:
            j += 1
        out.append((i, j, mask[i]))
        i = j
    return out


def coeur_C():
    """Two-sided windows [s - W, s + W] around starts placed with gaps <= g on
    [0, J].  With fewer than J/((m+2)(3W)) - 1 runs on [0, J], some window is
    saturated or m pairwise disjoint windows are untouched (spacing 3W > 2W + g).
    Control: fine alternation leaves none."""
    essais = temoins = 0
    for _ in range(400):
        W, m = ALEA.randint(3, 8), ALEA.randint(1, 3)
        g = ALEA.randint(1, W - 1)
        J = ALEA.randint((m + 3) * 3 * W * 2, (m + 3) * 3 * W * 6)
        starts, t = [], 0
        while t <= J:
            starts.append(t)
            t += ALEA.randint(1, g)
        seuil = J / ((m + 2) * 3 * W) - 1
        nb = max(1, int(seuil) - 1) if seuil >= 2 else 1
        cuts = sorted(ALEA.sample(range(1, J), nb - 1)) if nb > 1 else []
        mask, v, c = [], ALEA.randint(0, 1), 0
        for x in range(-W, J + W + 1):
            if c < len(cuts) and x == cuts[c]:
                v, c = 1 - v, c + 1
            mask.append(v)
        val = lambda x: mask[x + W]
        if len(runs(mask[W:J + W + 1])) >= seuil:
            continue
        essais += 1
        fen = lambda s: [val(x) for x in range(s - W, s + W + 1)]
        sature = any(all(fen(s)) for s in starts)
        libres, fin = 0, -10 ** 9
        for s in starts:
            if s - W > fin and not any(fen(s)):
                libres, fin = libres + 1, s + W
        exige(sature or libres >= m, f"Theorem C core fails W={W} g={g} m={m} J={J}")
    exige(essais >= 100, "too few core instances")
    for W in range(4, 9):
        mask = [x % 2 for x in range(200)]
        ok = all(any(mask[s - W:s + W + 1]) and not all(mask[s - W:s + W + 1]) for s in range(W, 150))
        exige(ok, "control: fine alternation should leave no saturated/untouched window")
        temoins += ok
    print(f"1. Theorem C core (two-sided windows): {essais} instances, saturated or m untouched "
          f"windows each time; {temoins}/5 fine-alternation controls hit and miss every window")
    return temoins == 5


def fenetre_bilaterale():
    """(x1) of the referee: bands of P_s go below t_0 when A_1 < 0.  Exact replay
    with q = 10007, D = 3, lambda = 5, k = 8: the one-sided window fails on some
    start, the two-sided window always holds."""
    from fractions import Fraction as Fr
    q, D, lam, k = 10007, 3, 5, 8
    N = q ** D
    def centre(x):
        y = x - (x.numerator // x.denominator)
        return y - 1 if y >= Fr(1, 2) else y
    pire, unilat_rejete, ok = 0, False, True
    for _ in range(300):
        n = ALEA.randrange(N)
        Y = [centre(Fr(lam * n, q ** i)) for i in range(1, D + 1)]
        w = [Fr(lam, q ** i) for i in range(1, D + 1)]
        t0 = int(q * q * sum(y * y for y in Y))
        for j in range(k):
            P = [y + j * wi for y, wi in zip(Y, w)]
            if any(not (Fr(-1, 2) <= x < Fr(1, 2)) for x in P):
                break
            tj = int(q * q * sum(x * x for x in P))
            bas = t0 - k * q * lam * (1 + Fr(2, q)) - 1
            haut = t0 + k * q * lam * (1 + Fr(2, q)) + 2 * k * k * lam * lam
            ok &= bas <= tj <= haut
            if tj < t0:
                unilat_rejete = True
            pire = min(pire, tj - t0)
    exige(ok, "two-sided window violated")
    exige(unilat_rejete, "one-sided window should fail somewhere (referee's control)")
    print(f"1b. Two-sided window: holds on 300 exact starts; one-sided window rejected "
          f"(min t_j - t_0 = {pire}, k q lambda = {k * q * lam})")
    return unilat_rejete


def lll_4():
    ok = all((1 - l) * math.log(2) <= -l / 4 - 2 * l * i / 100 + 1e-12
             for l in range(4, 400) for i in range(0, 11))
    exige(ok, "2^(1-l) <= exp(-l/4 - 2 l iota) on l >= 4, iota <= 1/10")
    c1 = (1 - 2) * math.log(2) <= -2 / 4 - 2 * 2 * 0.1
    c2 = (1 - 4) * math.log(2) <= -4 / 4 - 2 * 4 * 0.25
    exige(not c1 and not c2, "controls l = 2 and iota = 1/4 must fail")
    print(f"2. Local-lemma inequality of families 4a/4b: grid {'ok' if ok else 'FAIL'}; "
          f"controls l=2, iota=1/4 rejected: {not c1 and not c2}")
    return (not c1) + (not c2)


def warren():
    pires = 0.0
    for _ in range(60):
        n, s = 2, ALEA.randint(2, 6)
        polys = [[ALEA.uniform(-1, 1) for _ in range(6)] for _ in range(s)]
        vus = set()
        for _ in range(4000):
            x, y = ALEA.uniform(-3, 3), ALEA.uniform(-3, 3)
            mon = (1, x, y, x * x, x * y, y * y)
            vus.add(tuple(sum(c * v for c, v in zip(p, mon)) > 0 for p in polys))
        borne = (4 * math.e * 2 * s / n) ** n
        exige(len(vus) <= borne, "Warren bound exceeded on a toy")
        pires = max(pires, len(vus) / borne)
    print(f"3. Warren toys: realised sign vectors at most {pires:.3f} of (4eds/n)^n")


def ledger():
    """All quantities as log2 of their natural-log size, to avoid overflow."""
    a, m, c, b = 0.49, 0.99, 1 / 9, 1.0
    lg = math.log2
    print("4. Ledger, a = 0.49, m = 0.99, c = 1/9, b = 1 (sizes as log2 of natural logs):")
    for e in (1024, 4096):
        lnk = e * math.log(2)
        lgL = lg(math.ceil(lnk))
        lg_lnq = lg(c) + (1 - a) * e + lg(lnk)
        for sigma in ((0.0,) if e == 1024 else (0.0, 0.004, 0.0099)):
            assert 2 * a + sigma < m
            lg_h0 = a * e + (2 * lgL if sigma == 0 else sigma * e)
            lg_lnlam = lg_h0 + lg((m * e + 1) * math.log(2))
            rapport = 2 ** (lg_lnlam - lg_lnq)
            portee_B = 2 * lgL if sigma == 0 else sigma * e
            print(f"   k = 2^{e}, sigma = {sigma}: log lambda / log q = {rapport:.3g}", end="")
            if rapport >= 1:
                print("  (Theorem C not yet in force: lambda >= q)")
                continue
            # log rho_* = log q - log lambda - O(k^(1-b) + log k); the O-term is ~ 3e, negligible
            lg_C = lg_lnq + lg(1 - rapport)
            print(f"; Theorem B reaches log R ~ 2^{portee_B:.1f}, Theorem C demands 2^{lg_C:.1f}")
            exige(lg_C - portee_B > 20, f"gap too small at k=2^{e}, sigma={sigma}")
            if e == 4096:
                exige(rapport < 0.01, "lambda not negligible against q at k = 2^4096")
    lg_A = (2 * a - 1) * 4096 + 2 * lg(4096 * math.log(2))
    exige(lg_A < -10, "refined keys cost not o(k log k)")
    print(f"   (A) at k = 2^4096: k^(2a) log^3 k / (k log k) = 2^{lg_A:.1f}")


def manifeste():
    m = json.loads((ICI / "MANIFEST.json").read_text())
    for nom, h in sorted(m.items()):
        exige(hashlib.sha256((ICI / nom).read_bytes()).hexdigest() == h, f"hash {nom}")
    print(f"5. MANIFEST: {len(m)} files checked")


def main():
    controles = int(coeur_C()) + int(fenetre_bilaterale()) + lll_4()
    warren()
    ledger()
    manifeste()
    if echecs:
        print("FAIL")
        for e in sorted(set(echecs)):
            print("  -", e)
        return 1
    print(f"Test passé : all checks pass ({controles} negative controls rejected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
