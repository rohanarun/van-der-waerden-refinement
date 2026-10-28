"""Checks for the dense-rank-split note.  Standard library only.

0. Frozen statements: title and status and every section of README.md
   except "Reproduce", by sha256 of their whitespace-normalised text.
1. Lemma A0 with gamma = gcd(J - J): on every level class of q<g,w_t> - p t
   (support <= 2, q <= 5), gamma*m1 is an integer and |<g,B> - m1| < |g|_1/n.
   Controls: the integer-slope version is refuted on the single-period
   instance, and a tenfold-smaller bound fails somewhere.
2. Lemma A1 on a non-orthogonal toy (D = 3, rank 2): exact count of the
   grid (Z/101)^3 against det(L) vol(K) = (2/n)^2 * 3.  Control: the formula
   without the sum of minors is rejected.
3. Lemma A2, det 1 => coordinate lattice: exhaustive on pairs of {-1,0,1}^4.
4. Theorem B ledger (numerical evaluation of the proved bound, not a control).
5. Measurements replayed at D = 8, k = 500, seed 1, on the named family:
   exhaustive search, greedy, d1 and mixed term of every maximal intersection,
   rank over Q (exact fractions) for the maximum, the greedy and every
   intersection with a nonzero mixed term.  Positive witness: on the
   single-period instance the greedy, given rational slopes, reaches 2D.
   Computed values are compared with RESULT.json.
6. MANIFEST hashes.
Options: --write rewrites RESULT.json (block "verify") and MANIFEST.json;
--print-sections prints the section hashes.  Any other argument is refused.
Exit code 0 and last line "Test passé" on success.
"""
import hashlib, itertools, json, math, random, sys
from fractions import Fraction as Fr
from pathlib import Path

ICI = Path(__file__).resolve().parent
OPTIONS = {"--write", "--print-sections"}
inconnus = [x for x in sys.argv[1:] if x not in OPTIONS]
if inconnus:
    sys.exit(f"unknown argument(s): {inconnus}")
ECRIRE = "--write" in sys.argv

ALEA = random.Random(20261027)
DEN = 1 << 40
P1, P2 = (1 << 61) - 1, (1 << 89) - 1
echecs, controles, calc = [], [], {}


def exige(cond, msg):
    if not cond:
        echecs.append(msg)


def controle(nom, rejete):
    """A negative control or a positive witness: counted only if it behaves."""
    exige(rejete, f"control did not behave: {nom}")
    if rejete:
        controles.append(nom)


# 0 ---------------------------------------------------------------------------
FIGES = {
    "# Dense half of (G♭)": "5b6f7b9563c2713e24d12b799b5c56fe70db381a9772e395f405b4c09cbea7c2",
    "## Question": "6f7b01e4a73e903fc866bfa4d7de124516f28948f1f4b328b1e8fda7816e47f1",
    "## A. Exact facts about relations": "ff5e06b2e6db2a0c388f5d800698aac63bcff4a5a2e298e618835c0969ed4ce7",
    "## C. Measurements (not a theorem)": "595b2a0ce078954174531e934fd324af8e582724c574f65b3342d51f43cbe046",
    "## B. In the Haar model, a height split cannot prove (ii) for small θ": "3bbafaf0d958b914fe5d74497d690d50b7b911ff5872f497b2f06200e18170ee",
    "## D. The missing statement": "50b66d28abe0fe5076b179d40bbff3fe97f7ff78043997f955e1f2414dbadda8",
    "## What is not claimed": "7234b0f485f9c222862197c7cf073c6d69d3b1598b4d32c80d08557916b42850",
}
RESULT_FIGE = "feef632935f89d04649d4f322fe370b1806c50de5fc68bfa9bdac3c45341acba"
TEXTE = (ICI / "README.md").read_text()


def section(tete):
    if tete not in TEXTE:
        return None
    corps = TEXTE.split(tete, 1)[1]
    suite = corps.find("\n## ")
    corps = corps if suite < 0 else corps[:suite]
    return hashlib.sha256(" ".join((tete + corps).split()).encode()).hexdigest()


def figes():
    for tete, h in FIGES.items():
        got = section(tete)
        if "--print-sections" in sys.argv:
            print(f"   {tete}: {got}")
        exige(got == h, f"frozen section changed: {tete}")
    print(f"0. Frozen statements: {len(FIGES)} sections checked by sha256")


# helpers ---------------------------------------------------------------------
def tirage(D, graine, periode=None):
    """Same draw as measure/: dyadic A, B of denominator 2^40."""
    R = random.Random(graine)
    A = [R.randrange(-DEN // 2, DEN // 2) for _ in range(D)]
    if periode:
        B = [DEN // periode + R.randrange(-1000, 1000) for _ in range(D)]
    else:
        B = [R.randrange(-DEN // 2, DEN // 2) for _ in range(D)]
    return A, B


def roues(A, B, k):
    """w_t = floor(A + tB + 1/2), exactly (numerators over 2^40)."""
    return [[(a + t * b + DEN // 2) >> 40 for a, b in zip(A, B)] for t in range(k)]


def rang_p(lignes, p):
    base = {}
    for L in lignes:
        v = [x % p for x in L]
        for piv, b in base.items():
            if v[piv]:
                f = v[piv]
                v = [(x - f * y) % p for x, y in zip(v, b)]
        nz = next((i for i, x in enumerate(v) if x), None)
        if nz is not None:
            inv = pow(v[nz], p - 2, p)
            base[nz] = [(x * inv) % p for x in v]
    return len(base)


def rang_Q(lignes):
    M = [[Fr(x) for x in L] for L in lignes]
    r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(r + 1, len(M)):
            if M[i][c]:
                f = M[i][c] / M[r][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


def lignes_r(W, J):
    return [[-2 * x for x in W[t]] + [-2 * t * x for x in W[t]] + [1, 2 * t, t * t] for t in J]


def lignes_v(W, J):
    return [list(W[t]) + [1, t] for t in J]


def mesure(W, J, exact=False):
    """(deficit, d1, mixed term) ; modular (larger rank over two primes: an upper bound
    for the deficit over Q) unless exact."""
    D = len(W[0])
    if exact:
        rr, rv = rang_Q(lignes_r(W, J)), rang_Q(lignes_v(W, J))
    else:
        rr = max(rang_p(lignes_r(W, J), P1), rang_p(lignes_r(W, J), P2))
        rv = max(rang_p(lignes_v(W, J), P1), rang_p(lignes_v(W, J), P2))
    deficit, d1 = 2 * D + 3 - rr, D + 2 - rv
    return deficit, d1, deficit - 2 * d1


def candidats(B, k, delta, smax):
    """The measured family: support <= smax, coefficients +-1, +-2, integer
    slope m1 = round(<g,B>), window |<g,B> - m1| <= |g|_1/(delta k)."""
    D, out = len(B), []
    for s in range(1, smax + 1):
        for S in itertools.combinations(range(D), s):
            for c in itertools.product((1, -1, 2, -2), repeat=s):
                if c[0] < 0:
                    continue
                g = [0] * D
                for i, ci in zip(S, c):
                    g[i] = ci
                x = Fr(sum(gi * b for gi, b in zip(g, B)), DEN)
                m1 = round(x)
                if abs(x - m1) <= Fr(sum(map(abs, g))) / (delta * k):
                    out.append((g, m1, 1))
    return out


def niveaux(W, g, p, q=1):
    return [q * sum(gi * wi for gi, wi in zip(g, W[t])) - p * t for t in range(len(W))]


# 1 ---------------------------------------------------------------------------
def pente():
    vus, viole = 0, False
    for graine in range(1, 5):
        D, k = 5, 300
        A, B = tirage(D, graine)
        W = roues(A, B, k)
        for s in (1, 2):
            for S in itertools.combinations(range(D), s):
                for c in itertools.product((1, -1), repeat=s):
                    if c[0] < 0:
                        continue
                    g = [0] * D
                    for i, ci in zip(S, c):
                        g[i] = ci
                    x = Fr(sum(gi * b for gi, b in zip(g, B)), DEN)
                    l1 = sum(map(abs, g))
                    for q in range(1, 6):
                        for p in range(math.floor(x * q) - 1, math.floor(x * q) + 3):
                            if math.gcd(p, q) != 1:
                                continue
                            classes = {}
                            for t, v in enumerate(niveaux(W, g, p, q)):
                                classes.setdefault(v, []).append(t)
                            for J in classes.values():
                                if len(J) < 2:
                                    continue
                                vus += 1
                                n = J[-1] - J[0]
                                gam = 0
                                for t in J:
                                    gam = math.gcd(gam, t - J[0])
                                exige((gam * p) % q == 0, f"gamma*m1 not an integer, g={g}")
                                exige(abs(x - Fr(p, q)) < Fr(l1, n), f"slope lemma fails g={g}")
                                if abs(x - Fr(p, q)) >= Fr(l1, 10 * n):
                                    viole = True
    exige(vus > 1000, "too few level classes")
    controle("tenfold-smaller slope bound fails somewhere", viole)
    # the integer-slope version (A0 of the first draft) is false on the single-period instance
    D, k = 8, 1000
    A, B = tirage(D, 1, periode=5)
    W = roues(A, B, k)
    J = [t for t in range(k) if t % 5 == 0]
    x = Fr(B[0], DEN)
    affine = len({5 * W[t][0] - t for t in J}) == 1            # slope 1/5 on J
    entier = abs(x - round(x)) < Fr(1, J[-1] - J[0])
    controle("integer-slope A0 refuted on the single-period instance", affine and not entier)
    print(f"1. Lemma A0: {vus} level classes with slopes p/q (q <= 5): gamma*m1 integer and "
          f"|<g,B> - m1| < |g|_1/n on each; integer-slope version refuted on the period-5 instance "
          f"(slope 1/5, dist(B_1, Z) = {float(abs(x - round(x))):.3f})")


# 2 ---------------------------------------------------------------------------
def haar():
    """L = span((1,1,0), (0,1,1)), primitive (minor 1).  y in L* + K iff the
    coordinates (a, b) = (<B,g1>, <B,g2>) mod 1, centred, satisfy |a|, |b|,
    |a - b| < 2/n (x2 is then free in an interval).  Exact count on the grid."""
    Q, n = 101, 5
    r = Fr(2, n)
    dans = 0
    for i, j, l in itertools.product(range(Q), repeat=3):
        a = Fr((i + j) % Q, Q)
        b = Fr((j + l) % Q, Q)
        a = a - 1 if a >= Fr(1, 2) else a
        b = b - 1 if b >= Fr(1, 2) else b
        if abs(a) < r and abs(b) < r and abs(a - b) < r:
            dans += 1
    freq = Fr(dans, Q ** 3)
    formule = Fr(2, n) ** 2 * 3                 # det(L) vol(K) = (2/n)^m sum |det M_S|
    sans = Fr(2, n) ** 2                        # without the sum of minors
    marge = Fr(6, Q)                            # boundary layer of the hexagon
    exige(abs(freq - formule) < marge, f"Lemma A1 toy: {float(freq)} vs {float(formule)}")
    controle("formula without the sum of minors rejected", abs(freq - sans) >= marge)
    calc["A1_toy"] = {"grid": Q, "n": n, "frequency": str(freq), "formula": str(formule)}
    print(f"2. Lemma A1 toy (D = 3, rank 2, grid 101^3, n = 5): frequency {float(freq):.4f}, "
          f"det(L) vol(K) = {float(formule):.4f}; without the minors {float(sans):.4f} rejected")


# 3 ---------------------------------------------------------------------------
def coordonnees():
    vecs = [v for v in itertools.product((-1, 0, 1), repeat=4) if any(v)]
    unimod = 0
    for u, v in itertools.combinations(vecs, 2):
        gram = sum(x * x for x in u) * sum(x * x for x in v) - sum(x * y for x, y in zip(u, v)) ** 2
        if gram == 1:
            unimod += 1
            G = [i for i in range(4) if u[i] or v[i]]
            ok = len(G) == 2 and abs(u[G[0]] * v[G[1]] - u[G[1]] * v[G[0]]) == 1
            exige(ok, f"det 1 but not a coordinate plane: {u}, {v}")
    calc["A2_det1_pairs"] = unimod
    print(f"3. Lemma A2: {unimod} pairs of {{-1,0,1}}^4 with Gram determinant 1, all bases of coordinate planes")


# 4 ---------------------------------------------------------------------------
def ledger():
    a, delta = 0.45, 0.1
    lg = math.log2
    s = int(1 / a) + 2
    lignes = []
    for e in (1024, 4096, 16384):
        lgD = a * e
        for nom, lgm in (("m = 1", 0.0), ("m = D/(2s)", lgD - lg(2 * s)), ("m = D/200", lgD - lg(200))):
            f = s * lgD + (1 - s) * lg(s) - lgm - lg(delta) - e
            exige(f > 0, f"Theorem B factor should exceed 1 at e={e}, {nom}")
            lignes.append(f"2^{e}/{nom}: 2^{f:.0f}")
    print(f"4. Theorem B ledger (evaluation, a = 0.45, s = {s}, delta = 1/10), per-generator factor: "
          + "; ".join(lignes))


# 5 ---------------------------------------------------------------------------
def glouton(W, cands, k, delta):
    J = list(range(k))
    while True:
        best = None
        for g, p, q in cands:
            u = niveaux(W, g, p, q)
            cnt = {}
            for t in J:
                cnt[u[t]] = cnt.get(u[t], 0) + 1
            v, c = max(cnt.items(), key=lambda kv: (kv[1], -kv[0]))
            if c < len(J) and c >= delta * k and (best is None or c > best[0]):
                best = (c, u, v)
        if best is None:
            return J
        _, u, v = best
        J = [t for t in J if u[t] == v]


def mesures():
    delta = Fr(1, 10)
    # positive witness: the greedy on the measured family (support <= 2 here,
    # integer slopes) finds the period through the relations e_i - e_j
    D, k = 8, 1000
    A, B = tirage(D, 1, periode=5)
    W = roues(A, B, k)
    Jw = glouton(W, candidats(B, k, delta, 2), k, delta)
    dw = mesure(W, Jw, exact=True)
    controle("greedy on the measured family finds the single-period witness (deficit 2D over Q)",
             dw[0] == 2 * D)
    calc["witness"] = {"D": D, "k": k, "J": len(Jw), "deficit_Q": dw[0], "d1_Q": dw[1]}
    print(f"5a. Witness: B_i ~ 1/5, the greedy on the measured family (support <= 2) returns "
          f"|J| = {len(Jw)}, deficit over Q = {dw[0]} (2D = {2 * D})")

    D, k = 8, 500
    A, B = tirage(D, 1)
    W = roues(A, B, k)
    cands = candidats(B, k, delta, 3)
    seuil = math.ceil(delta * k)
    E, vus = [], set()
    for g, p, q in cands:
        classes = {}
        for t, v in enumerate(niveaux(W, g, p, q)):
            classes.setdefault(v, []).append(t)
        for Jv in classes.values():
            if seuil <= len(Jv) < k:
                m = sum(1 << t for t in Jv)
                if m not in vus:
                    vus.add(m)
                    E.append(m)
    feuilles, noeuds = {}, [0]

    def coupable(J):
        return any(J & e != J and bin(J & e).count("1") >= seuil for e in E)

    # every intersection of a family is a node (classes taken in increasing
    # index); a node is maximal when no class at all cuts it keeping >= delta k
    def dfs(J, debut):
        noeuds[0] += 1
        for i in range(debut, len(E)):
            J2 = J & E[i]
            if J2 != J and bin(J2).count("1") >= seuil:
                dfs(J2, i + 1)
        if J not in feuilles and not coupable(J):
            feuilles[J] = mesure(W, [t for t in range(k) if J >> t & 1])

    dfs((1 << k) - 1, 0)
    pire = max(f[0] for f in feuilles.values())
    mixtes = {J: f for J, f in feuilles.items() if f[2] != 0}
    a_certifier = {J for J, f in feuilles.items() if f[0] == pire} | set(mixtes)
    certif = {J: mesure(W, [t for t in range(k) if J >> t & 1], exact=True) for J in a_certifier}
    exige(all(certif[J] == feuilles[J] for J in a_certifier), "rank mod p differs from rank over Q")
    Jg = glouton(W, cands, k, delta)
    dg = mesure(W, Jg, exact=True)
    histo = {}
    for f in feuilles.values():
        histo[f"{f[0]}/{f[1]}/{f[2]}"] = histo.get(f"{f[0]}/{f[1]}/{f[2]}", 0) + 1
    calc["replay_D8_k500_seed1"] = {
        "relations": len(cands), "level_classes": len(E), "nodes": noeuds[0],
        "maximal_intersections": len(feuilles), "max_deficit": pire,
        "max_deficit_certified_over_Q": all(certif[J][0] == pire for J in certif if feuilles[J][0] == pire),
        "nonzero_mixed_term": len(mixtes),
        "histogram deficit/d1/mixed": dict(sorted(histo.items())),
        "greedy": {"J": len(Jg), "deficit_Q": dg[0], "d1_Q": dg[1], "mixed_Q": dg[2]},
    }
    print(f"5b. D = 8, k = 500, seed 1 (support <= 3, coefficients +-1, +-2, integer slopes, window "
          f"|g|_1/(delta k)): {len(cands)} relations, {len(E)} level classes, {len(feuilles)} maximal "
          f"intersections (exhaustive): max deficit {pire}, certified over Q; mixed term nonzero on "
          f"{len(mixtes)} of them (certified over Q; deficit/d1/mixed: "
          f"{sorted(certif[J] for J in mixtes)}); greedy {dg[0]} with d1 = {dg[1]}")


# 6 ---------------------------------------------------------------------------
def resultat_et_manifeste():
    chemin = ICI / "RESULT.json"
    res = json.loads(chemin.read_text())
    reste = {c: v for c, v in res.items() if c != "verify"}
    h_reste = hashlib.sha256(json.dumps(reste, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    if "--print-sections" in sys.argv:
        print(f"   RESULT.json outside verify: {h_reste}")
    exige(h_reste == RESULT_FIGE, "RESULT.json changed outside the block verify")
    noms = ["README.md", "NOTICE.md", "RESULT.json", "verify.py",
            "measure/attaque.py", "measure/exact.py", "measure/serie2.py"]
    if ECRIRE and echecs:
        print("   --write refused: failures above, nothing written")
    elif ECRIRE:
        res["verify"] = calc
        chemin.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
        (ICI / "MANIFEST.json").write_text(json.dumps(
            {n: hashlib.sha256((ICI / n).read_bytes()).hexdigest() for n in noms}, indent=2) + "\n")
    exige(res.get("verify") == json.loads(json.dumps(calc)), "RESULT.json (block verify) differs from the computation")
    m = json.loads((ICI / "MANIFEST.json").read_text())
    exige(sorted(m) == sorted(noms), "MANIFEST lists other files")
    for nom, h in sorted(m.items()):
        exige(hashlib.sha256((ICI / nom).read_bytes()).hexdigest() == h, f"hash {nom}")
    print(f"6. RESULT.json compared with the computation; MANIFEST: {len(m)} files checked")


def main():
    figes()
    pente()
    haar()
    coordonnees()
    ledger()
    mesures()
    resultat_et_manifeste()
    if echecs:
        print("FAIL")
        for e in sorted(set(echecs)):
            print("  -", e)
        return 1
    print(f"Test passé : all checks pass ({len(controles)} controls and witnesses behaved: "
          + "; ".join(controles) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
