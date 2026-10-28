"""Recherche exacte (séparation-évaluation) du J de déficit maximal parmi les
intersections de classes de niveau des relations candidates (support <= smax).

Chaque relation candidate g (presque entière sur B) et chacune de ses classes
de niveau v de taille >= delta k donne un ensemble E(g,v). On parcourt toutes
les familles dont l'intersection garde >= delta k positions (exhaustif sauf
budget de noeuds, dit dans la sortie), et l'on calcule le déficit exact de
chaque intersection maximale. Le glouton d'attaque.py est rejoué pour comparer.
"""
import json, random, sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from attaque import candidats, deficit, glouton

def ensembles(W, cands, k, delta):
    t = np.arange(k)
    vus, out = set(), []
    for g, m1 in cands:
        u = W @ g - m1 * t
        vals, cnt = np.unique(u, return_counts=True)
        for v, c in zip(vals, cnt):
            if c >= delta * k and c < k:
                m = 0
                for x in np.nonzero(u == v)[0]:
                    m |= 1 << int(x)
                if m not in vus:
                    vus.add(m); out.append(m)
    return out

def main():
    D, k, delta, smax, graine, budget = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    R = random.Random(graine)
    den = 1 << 40
    A = np.array([R.randrange(-den // 2, den // 2) / den for _ in range(D)])
    B = np.array([R.randrange(-den // 2, den // 2) / den for _ in range(D)])
    t = np.arange(k)[:, None]
    W = np.floor(A[None, :] + t * B[None, :] + 0.5).astype(np.int64)
    cands = candidats(B, k, delta, smax)
    E = ensembles(W, cands, k, delta)
    seuil = int(np.ceil(delta * k))
    noeuds, memo = 0, {}
    pire = [0, None]
    complet = True

    def dfs(J, debut, prof):
        nonlocal noeuds, complet
        noeuds += 1
        if noeuds > budget:
            complet = False
            return
        for i in range(debut, len(E)):
            J2 = J & E[i]
            if J2 != J and bin(J2).count("1") >= seuil:
                dfs(J2, i + 1, prof + 1)
        # maximal: no class at all cuts J while keeping >= delta k
        maximal = not any(J & e != J and bin(J & e).count("1") >= seuil for e in E)
        if maximal and J not in memo:
            Jl = [x for x in range(k) if J >> x & 1]
            d, ok = deficit(W, Jl)
            memo[J] = d
            if d > pire[0]:
                pire[0], pire[1] = d, (len(Jl), prof, ok)

    dfs((1 << k) - 1, 0, 0)
    Jg, pris, _ = glouton(W, B, k, delta, smax)
    dg, _ = deficit(W, list(Jg))
    print(json.dumps({"D": D, "k": k, "delta": delta, "smax": smax, "graine": graine,
                      "ensembles": len(E), "noeuds": noeuds, "exhaustif": complet,
                      "feuilles": len(memo), "exact_deficit": pire[0], "exact_J_prof_accord": pire[1],
                      "glouton_deficit": dg, "glouton_J": int(len(Jg))}), flush=True)

main()
