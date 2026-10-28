"""Attaque de (G♭)(ii) : chercher un J de >= delta*k positions de grand déficit.

Pour (A,B) tiré au hasard (dyadiques 2^-40), w_t = round(A + tB), t < k.
Déficit sur J = 2D + 3 - rang(r_t : t in J), r_t = (-2w_t, -2t w_t, 1, 2t, t^2),
rang exact modulo deux premiers de 61 bits (le minimum des deux, borne inf.
du rang rationnel ; on annonce le déficit seulement si les deux s'accordent).
Recherche gloutonne : on intersecte J avec la plus grande classe de niveau
d'une relation g de la famille mesurée (support <= smax, coefficients +-1,
+-2, pente entière m1 = round(<g,B>), fenêtre |<g,B> - m1| <= |g|_1/(delta k)),
tant que |J| >= delta*k. Instance à une période (B_i ~ 1/r) : déficit sur
J = {t mod r < 2 delta r}, cas dégénéré, sert de témoin. Rangs modulo deux
premiers : bornes supérieures du déficit, non certifiées sur Q.
Une ligne JSON par cas.
"""
import itertools, json, random, sys
import numpy as np

P1, P2 = (1 << 61) - 1, (1 << 89) - 1  # deux premiers de Mersenne

def rang(lignes, p):
    base = {}  # pivot -> ligne réduite
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

def deficit(W, J):
    D = W.shape[1]
    J = [int(t) for t in J]
    lignes = [[-2 * int(x) for x in W[t]] + [-2 * t * int(x) for x in W[t]] + [1, 2 * t, t * t] for t in J]
    r1, r2 = rang(lignes, P1), rang(lignes, P2)
    return 2 * D + 3 - max(r1, r2), r1 == r2

def candidats(B, k, delta, smax):
    D = len(B)
    out = []
    coefs = (1, -1, 2, -2)
    for s in range(1, smax + 1):
        for S in itertools.combinations(range(D), s):
            for c in itertools.product(coefs, repeat=s):
                if c[0] < 0:
                    continue
                g = np.zeros(D, dtype=np.int64); g[list(S)] = c
                x = float(np.dot(g, B))
                if abs(x - round(x)) <= np.abs(g).sum() / (delta * k):
                    out.append((g, round(x)))
    return out

def glouton(W, B, k, delta, smax):
    cands = candidats(B, k, delta, smax)
    J = np.arange(k)
    pris = []
    t = np.arange(k)
    while True:
        meilleur = None
        for g, m1 in cands:
            u = W @ g - m1 * t
            vals, cnt = np.unique(u[J], return_counts=True)
            i = cnt.argmax()
            if cnt[i] == len(J):
                continue  # déjà vraie sur J, ne coupe rien
            if cnt[i] >= delta * k and (meilleur is None or cnt[i] > meilleur[0]):
                meilleur = (cnt[i], g, u, vals[i])
        if meilleur is None:
            return J, pris, len(cands)
        _, g, u, v = meilleur
        J = J[u[J] == v]
        pris.append([int(x) for x in np.nonzero(g)[0]])

def cas(D, k, delta, graine, mode, smax):
    R = random.Random(graine)
    den = 1 << 40
    A = np.array([R.randrange(-den // 2, den // 2) / den for _ in range(D)])
    if mode == "periode":
        r = max(3, int(round(1 / (2 * delta))))
        B = np.array([1 / r + R.randrange(-1000, 1000) / den for _ in range(D)])
    else:
        B = np.array([R.randrange(-den // 2, den // 2) / den for _ in range(D)])
    t = np.arange(k)[:, None]
    W = np.floor(A[None, :] + t * B[None, :] + 0.5).astype(np.int64)
    if mode == "periode":
        J = [x for x in range(k) if (x % r) < max(1, int(delta * r * 2))]
        d, ok = deficit(W, J)
        return {"D": D, "k": k, "delta": delta, "graine": graine, "mode": mode, "J": len(J), "deficit": d, "accord": ok}
    J, pris, nc = glouton(W, B, k, delta, smax)
    d, ok = deficit(W, list(J))
    d0, _ = deficit(W, list(range(k)))
    return {"D": D, "k": k, "delta": delta, "graine": graine, "mode": mode, "smax": smax,
            "candidats": nc, "relations_prises": len(pris), "J": int(len(J)),
            "deficit": d, "deficit_tout": d0, "accord": ok, "supports": pris}

if __name__ == "__main__":
    delta = float(sys.argv[1]); smax = int(sys.argv[2])
    for Dk in sys.argv[3].split(","):
        D, k = map(int, Dk.split(":"))
        print(json.dumps(cas(D, k, delta, 1, "periode", smax)), flush=True)
        for graine in range(1, 4):
            print(json.dumps(cas(D, k, delta, graine, "hasard", smax)), flush=True)


def boites(W, A, B, k, delta, essais, graine):
    """Attaque 2 : J = {t : phi_t,i dans une boîte pour i dans S}, S et boîte
    au hasard, côté réglé pour |J| ~ delta k. Rend le pire déficit vu."""
    R = random.Random(graine)
    D = len(A)
    t = np.arange(k)[:, None]
    phi = A[None, :] + t * B[None, :] - W
    pire = (0, 0, None)
    for _ in range(essais):
        s = R.randint(1, max(1, int(np.log(1 / delta) / np.log(2)) + 1))
        S = R.sample(range(D), s)
        cote = delta ** (1 / s)
        c = [R.uniform(-0.5, 0.5) for _ in S]
        ok = np.ones(k, dtype=bool)
        for i, ci in zip(S, c):
            d = np.abs((phi[:, i] - ci + 0.5) % 1 - 0.5)
            ok &= d <= cote / 2
        J = np.nonzero(ok)[0]
        if len(J) < delta * k:
            continue
        d, _ = deficit(W, list(J))
        if d > pire[0]:
            pire = (d, len(J), sorted(S))
    return pire


def cas2(D, k, delta, graine, smax, essais):
    R = random.Random(graine)
    den = 1 << 40
    A = np.array([R.randrange(-den // 2, den // 2) / den for _ in range(D)])
    B = np.array([R.randrange(-den // 2, den // 2) / den for _ in range(D)])
    t = np.arange(k)[:, None]
    W = np.floor(A[None, :] + t * B[None, :] + 0.5).astype(np.int64)
    J, pris, nc = glouton(W, B, k, delta, smax)
    d, ok = deficit(W, list(J))
    pb = boites(W, A, B, k, delta, essais, graine)
    return {"D": D, "k": k, "delta": delta, "graine": graine, "smax": smax, "candidats": nc,
            "glouton": {"J": int(len(J)), "deficit": d, "accord": ok, "relations": len(pris)},
            "boites": {"deficit": pb[0], "J": pb[1], "S": pb[2]}}
