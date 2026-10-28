"""Exact checks for the source-only proof of every c < 1/8 (explicit 1/9).

Checks, in exact rational arithmetic:
  1. the explicit tuple lies strictly inside the region, with the margins of
     README.md section 8; the supremum is 1/8 and the endpoint is rejected;
  2. for every digit rank R <= D, kappa_R + nu_R = 2, 0 < theta_R < gamma,
     and both rich margins equal mu (Theorem 9);
  3. the identities of Lemma R4, Lemma A* and (4), on random rational
     instances, with a mutated identity rejected;
  4. the digit expansions (2) and (3) on exact modular instances, and the
     recovery of e in Lemma C*, with rho <= R <= min(2 rho, D);
  5. the files match MANIFEST.json.
The asymptotic counts are proved in README.md, not checked here.
"""

import hashlib
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

ICI = Path(__file__).resolve().parent
ALEA = random.Random(20261026)

TUPLE = dict(a=F(49, 100), m=F(99, 100), b=F(97, 200), eps=F(1, 200),
             eps_r=F(1, 200), delta=F(1, 200), delta_s=F(1, 2),
             gamma=F(97, 200), c=F(1, 9))
TUPLE_1_17 = dict(a=F(497, 1000), m=F(999, 1000), b=F(99, 200), eps=F(1, 1000),
                  eps_r=F(1, 1000), delta=F(1, 1000), delta_s=F(1, 2),
                  gamma=F(497, 1000), c=F(1, 17))

echecs = []


def exige(cond, message):
    if not cond:
        echecs.append(message)


def marges(t):
    cap = (F(1, 2) - t["eps"]) * (1 - t["eps_r"]) * (1 - t["delta"])
    return [
        ("b > 0", t["b"]),
        ("b < a", t["a"] - t["b"]),
        ("a + b < 1", 1 - t["a"] - t["b"]),
        ("2a < m", t["m"] - 2 * t["a"]),
        ("m < 1", 1 - t["m"]),
        ("0 < eps < 1/2", min(t["eps"], F(1, 2) - t["eps"])),
        ("0 < eps_r", t["eps_r"]),
        ("0 < delta < 1", min(t["delta"], 1 - t["delta"])),
        ("0 < delta_s < 1", min(t["delta_s"], 1 - t["delta_s"])),
        ("0 < gamma < cap", min(t["gamma"], cap - t["gamma"])),
        ("0 < c < gamma*b/2", min(t["c"], t["gamma"] * t["b"] / 2 - t["c"])),
    ]


def admis(t):
    return all(v > 0 for _, v in marges(t)) and t["eps_r"] <= F(1, 2)


def region():
    print("1. Region, explicit c = 1/9")
    attendu = {"b < a": F(1, 200), "a + b < 1": F(1, 40), "2a < m": F(1, 100),
               "m < 1": F(1, 100), "0 < gamma < cap": F(40499, 8000000),
               "0 < c < gamma*b/2": F(4681, 720000)}
    for nom, v in marges(TUPLE):
        print(f"   {nom:22s} margin {v}")
        exige(v > 0, f"tuple: {nom}")
        if nom in attendu:
            exige(v == attendu[nom], f"margin {nom}: {v} != README {attendu[nom]}")
    exige(admis(TUPLE_1_17), "the 1/17 tuple of the companion note must stay admissible")
    for n in (10, 100, 1000, 10000):
        e = F(1, n)
        t = dict(a=F(1, 2) - e, m=1 - e, b=F(1, 2) - 2 * e, eps=e * e, eps_r=e * e,
                 delta=e * e, delta_s=F(1, 2), gamma=F(1, 2) - e)
        t["c"] = t["gamma"] * t["b"] / 2 - e ** 3
        exige(admis(t) and t["c"] < F(1, 8), f"sup sequence n={n}")
        print(f"   n={n:5d}  c = {float(t['c']):.10f}  gap to 1/8 = {float(F(1, 8) - t['c']):.2e}")
    controles = {
        "c = 1/8": dict(TUPLE, c=F(1, 8)),
        "b = a": dict(TUPLE, b=TUPLE["a"]),
        "m = 2a": dict(TUPLE, m=2 * TUPLE["a"]),
        "gamma at the balance cap": dict(
            TUPLE, gamma=(F(1, 2) - TUPLE["eps"]) * (1 - TUPLE["eps_r"]) * (1 - TUPLE["delta"])),
        "c = gamma*b/2": dict(TUPLE, c=TUPLE["gamma"] * TUPLE["b"] / 2),
        "eps = 1/2": dict(TUPLE, eps=F(1, 2)),
    }
    rejetes = 0
    for nom, t in controles.items():
        ok = admis(t)
        print(f"   control {nom:28s} {'ACCEPTED (bad)' if ok else 'rejected'}")
        exige(not ok, f"control accepted: {nom}")
        rejetes += not ok
    return rejetes


def rangs():
    print("2. Rank split of Theorem 9")
    t = TUPLE
    b, c, g = t["b"], t["c"], t["gamma"]
    mu = (g * b - 2 * c) / 2
    for D in (1, 2, 3, 7, 50, 333):
        for R in range(D + 1):
            kap, nu = F(R, D), F(2 * D - R, D)
            theta = (kap * c + g * b - nu * c) / (2 * b)
            exige(kap + nu == 2, f"kappa+nu D={D} R={R}")
            exige(0 < theta < g, f"theta range D={D} R={R}")
            exige(b * theta - kap * c == mu, f"certificate margin D={D} R={R}")
            exige(b * (g - theta) - nu * c == mu, f"count margin D={D} R={R}")
    print(f"   mu = {mu}, both margins equal mu for every R <= D, D in (1,2,3,7,50,333)")


def ps(u, v):
    return sum(x * y for x, y in zip(u, v))


def identites():
    print("3. Identities of R4, Lemma A* and (4)")
    rejetes = 0
    mutations = mutations_rejetees = 0
    for _ in range(300):
        D = ALEA.randint(1, 6)
        h = ALEA.randint(1, 9)
        q = ALEA.choice([3, 5, 7, 11, 101])
        rq = lambda: F(ALEA.randint(-999, 999), ALEA.randint(1, 999))
        Y0 = [rq() for _ in range(D)]
        beta = [rq() for _ in range(D)]
        tt = [ALEA.randint(0, h - 1) for _ in range(D)]
        dm = [ALEA.randint(-h, h) for _ in range(D)]
        ca = F(ALEA.randint(0, h - 1), h)
        sig_a, sig_0 = ALEA.randint(1, 30), ALEA.randint(1, 30)
        w = ps(beta, beta)
        W = q * q * w
        Ya = [y0 + ca * (ti + bi) - mi for y0, ti, bi, mi in zip(Y0, tt, beta, dm)]
        zeta_a = q * q * (2 * ps(Ya, beta) + sig_a * w)
        zeta_0 = q * q * (2 * ps(Y0, beta) + sig_0 * w)
        # R4: f_{a+sh} = q^2|Y_a|^2 + s(s - sigma_a)W + s zeta_a
        for s in range(5):
            Ys = [y + s * bi for y, bi in zip(Ya, beta)]
            exige(q * q * ps(Ys, Ys) == q * q * ps(Ya, Ya) + s * (s - sig_a) * W + s * zeta_a,
                  "R4 identity")
        # Lemma A*
        droite = (q * q * ps(Y0, Y0) + 2 * ca * q * q * ps(Y0, tt) - (ca * ca + ca * sig_a) * W
                  - 2 * q * q * ps(Y0, dm)
                  + q * q * (ca * ca * ps(tt, tt) + ps(dm, dm) - 2 * ca * ps(tt, dm)) + ca * zeta_a)
        exige(q * q * ps(Ya, Ya) == droite, "Lemma A* identity")
        if ca * zeta_a != 0:
            mutations += 1
            mutations_rejetees += droite - ca * zeta_a != q * q * ps(Ya, Ya)
        # (4)
        T = ps(tt, beta)
        exige(ps(dm, beta) == ca * (T + w) + F(sig_a - sig_0, 2) * w + (zeta_0 - zeta_a) / (2 * q * q),
              "identity (4)")
    exige(mutations > 0 and mutations_rejetees == mutations, "mutated Lemma A* identity accepted")
    rejetes += mutations > 0 and mutations_rejetees == mutations
    print(f"   300 random instances: R4, Lemma A*, (4) exact; "
          f"{mutations_rejetees}/{mutations} mutations without c_a*zeta_a rejected")
    return rejetes


def centre(x):
    """Centered representative in [-1/2, 1/2) of a rational x mod 1."""
    y = x - (x.numerator // x.denominator)
    return y - 1 if y >= F(1, 2) else y


def chiffres_equilibres(n, q, D):
    n %= q ** D
    out = []
    for _ in range(D):
        r = n % q
        if r > (q - 1) // 2:
            r -= q
        out.append(r)
        n = (n - r) // q
    return out


def rang(lignes):
    """Rank over Q by exact Gaussian elimination."""
    m = [list(map(F, l)) for l in lignes if any(l)]
    r = 0
    ncol = len(m[0]) if m else 0
    for col in range(ncol):
        piv = next((i for i in range(r, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][col] != 0:
                f = m[i][col] / m[r][col]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def S1(v):
    """(S_1 v)_l = v_{l+1}, digit positions l = 0..D-1, v indexed from 1."""
    return list(v)


def S2(v):
    """(S_2 v)_l = v_{l+2}, with v_{D+1} = 0."""
    return list(v[1:]) + [0]


def chiffres():
    print("4. Digit expansions (2), (3) and the recovery of Lemma C*")
    rejetes = 0
    decalees = decalees_rejetees = 0
    for _ in range(200):
        q = ALEA.choice([3, 5, 7, 11, 13, 101])
        D = ALEA.randint(2, 6)
        N = q ** D
        lam = ALEA.choice([l for l in range(2, 50) if l % q])
        z = ALEA.randrange(1, N)
        y = chiffres_equilibres(lam * z, q, D)
        Y = [centre(F(lam * z, q ** i)) for i in range(1, D + 1)]
        for i in range(1, D + 1):
            exige(Y[i - 1] == sum(F(y[l]) * F(q) ** (l - i) for l in range(i)), "Y_i digit sum")
        Fv = [sum(F(y[l]) * F(q) ** (l - i + 2) for l in range(i - 2)) for i in range(1, D + 1)]
        exige(all(abs(f) <= F(1, 2) for f in Fv), "|F_i| <= 1/2")
        v = [ALEA.randint(-9, 9) for _ in range(D)]
        exige(q * q * ps(Y, v) == q * ps(S1(v), y) + ps(S2(v), y) + ps(v, Fv), "identity (2)")
        # (3): digits of a step return beta = Y(z)
        bvec = [q ** i * Y[i - 1] for i in range(1, D + 1)]
        exige(all(x.denominator == 1 for x in bvec), "b_i integral")
        for i in range(1, D):
            exige((bvec[i] - bvec[i - 1]) % q ** i == 0, "b_{i+1} = b_i mod q^i")
        e = [bvec[0]] + [(bvec[i] - bvec[i - 1]) / q ** i for i in range(1, D)]
        for i in range(1, D + 1):
            exige(Y[i - 1] == sum(e[l] * F(q) ** (l - i) for l in range(i)), "beta_i digit sum")
        Rv = q * q * ps(v, Y) - q * ps(S1(v), e) - ps(S2(v), e)
        emax = max(abs(x) for x in e)
        exige(abs(Rv) <= emax * sum(map(abs, v)) / (q - 1), "|R_v| bound")
        # Lemma C*: rank and recovery of e_L
        nb = ALEA.randint(1, 4)
        dms = [[ALEA.choice([0, 0, ALEA.randint(-3, 3)]) for _ in range(D)] for _ in range(nb)]
        rho = rang(dms)
        cands = [S1(dm) for dm in dms] + [S2(dm) for dm in dms]
        R = rang(cands)
        exige(rho <= R <= min(2 * rho, D), "rho <= R <= min(2 rho, D)")
        base = []
        for u in cands:
            if rang(base + [u]) > len(base):
                base.append(u)
        if not base:
            continue
        cols = []
        for col in range(D):
            essai = [[u[c] for c in cols + [col]] for u in base]
            if rang(essai) > len(cols):
                cols.append(col)
        exige(len(cols) == len(base), "nonsingular minor")
        ee = [ALEA.randint(-50, 50) for _ in range(D)]
        valeurs = [ps(u, ee) for u in base]
        # solve for e_L from e off L and the R values
        M = [[F(u[c]) for c in cols] + [F(val - sum(u[c] * ee[c] for c in range(D) if c not in cols))]
             for u, val in zip(base, valeurs)]
        n = len(cols)
        for col in range(n):
            piv = next(i for i in range(col, n) if M[i][col] != 0)
            M[col], M[piv] = M[piv], M[col]
            for i in range(n):
                if i != col and M[i][col] != 0:
                    f = M[i][col] / M[col][col]
                    M[i] = [x - f * yv for x, yv in zip(M[i], M[col])]
        sol = [M[i][n] / M[i][i] for i in range(n)]
        exige(sol == [ee[c] for c in cols], "recovery of e_L")
        decale = list(ee)
        decale[cols[0]] += 1
        decalees += 1
        decalees_rejetees += [ps(u, decale) for u in base] != valeurs
    exige(decalees > 0 and decalees_rejetees == decalees, "shifted e_L consistent with the code")
    rejetes += decalees > 0 and decalees_rejetees == decalees
    print(f"   200 modular instances: (2), (3), digit sums, rank bounds and recovery exact; "
          f"{decalees_rejetees}/{decalees} shifted e_L rejected")
    return rejetes


def manifeste():
    print("5. Manifest")
    m = json.loads((ICI / "MANIFEST.json").read_text())
    for nom, h in sorted(m.items()):
        reel = hashlib.sha256((ICI / nom).read_bytes()).hexdigest()
        print(f"   {nom:12s} {'ok' if reel == h else 'MISMATCH'}")
        exige(reel == h, f"hash {nom}")


def main():
    rejetes = region()
    rangs()
    rejetes += identites()
    rejetes += chiffres()
    manifeste()
    print()
    if echecs:
        print("FAIL")
        for e in sorted(set(echecs)):
            print("  -", e)
        return 1
    print(f"PASS ({rejetes} negative controls rejected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
