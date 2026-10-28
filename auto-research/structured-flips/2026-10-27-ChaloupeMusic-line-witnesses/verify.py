#!/usr/bin/env python3
"""Checks for `line-witnesses`. Standard library only, exact rationals where it matters.

1. Lemma A1, exactly, on toys of the literal template (U, adaptive mesh V, bands, keys, labels)
   chosen so that many values of psi share a vertical cell (q up to 15625, lambda close to q):
   coordinates i < D constant along a line, number of vertical boundaries, constancy on each
   vertical cell, at most two pieces A_j, the band law, the type a function of the face.
   Three mutants must be rejected. Multiplicity <= 2 on every line progression of two toys.
2. Scale: ln T_line <= (k/2) ln 2 / 1.01 at template points (m = (1+2a)/2), hence
   2 T_line 2^{-k/2} <= 2 exp(-(1/101)(k/2) ln 2); negative control at a = 1/2.
3. Moments: Lemma B2 (Lagrange), exactly; Proposition B3; the m = 2 identity; Corollary B4.
4. Provenance: MANIFEST hashes; JSON summary equal to RESULT.json.
"""
import hashlib
import json
import math
import random
import sys
from bisect import bisect_left
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUNT = []


def require(cond, name, detail=""):
    if not cond:
        print("FAIL", name, detail)
        sys.exit(1)
    COUNT.append(name)
    print("ok", name, detail, file=sys.stderr)


# ---------------------------------------------------------------- template
class Template:
    def __init__(self, k, P, e, D, lam):
        self.k, self.q, self.D, self.lam = k, P ** e, D, lam
        assert P > k and math.gcd(lam, P) == 1
        self.N = self.q ** D
        alpha = float(self.q) ** -(D + 1)
        R = math.log(1 + 1 / (2 * alpha))
        m = math.ceil(k * k * R)
        a = [alpha * (math.exp(l * R / m) - 1) for l in range(m + 1)]
        a[0], a[m] = 0.0, 0.5
        # left ends of the 2m intervals of V on [-1/2, 1/2)
        self.Vg = sorted([-0.5 + x for x in a[:-1]] + [0.5 - x for x in a[1:]])
        self.J = len(self.Vg)
        self.nU = k * k * lam            # H_x = 1/(k^2 lambda)

    def Vlab(self, Yc):
        y = float(Yc)
        i = bisect_left(self.Vg, y)
        if i < len(self.Vg) and self.Vg[i] == y:
            return i
        for b in self.Vg[max(0, i - 1):i + 1]:
            assert abs(b - y) > 1e-13      # no ambiguous floating-point tie
        return i - 1

    def point(self, n):
        q, D, lam = self.q, self.D, self.lam
        U, V, Y2 = [], [], F(0)
        for i in range(1, D + 1):
            x = F(n % q ** i, q ** i)
            Yc = centre(F((lam * n) % q ** i, q ** i))
            U.append(math.floor(x * self.nU))
            V.append(self.Vlab(Yc))
            Y2 += Yc * Yc
        return (tuple(V), math.floor(q * q * Y2)), (tuple(U), tuple(V))   # key, label

    def table(self):
        return [self.point(n) for n in range(self.N)]


def centre(y):
    return y if y < F(1, 2) else y - 1


def lemma_A1(k, P, e, D, lam, npairs, seed, mutant=None):
    """Exact check of Lemma A1 on lines: (u, e') drawn at random, every v < q^{D-1}.

    mutant: 'noV' (V boundaries omitted), 'noh' (lam^2 psi^2 dropped), 'noJ' (J dropped from
    the vertical bound). Returns (ok, number of psi sharing a vertical cell with another).
    """
    G = Template(k, P, e, D, lam)
    q, N, J = G.q, G.N, G.J
    Q = q ** (D - 1)
    rnd = random.Random(seed)
    vbound = k * ((k * k * lam) // q + 1) + (k * J if mutant != "noJ" else 0)
    shared = 0
    for _ in range(npairs):
        u, ep = rnd.randrange(q), rnd.randrange(1, q)
        s = [(u + j * ep) % q for j in range(k)]
        cuts = set()
        for sj in s:
            # U boundaries: (psi + sj)/q = a/(k^2 lam), exact
            a = math.ceil(F(sj * k * k * lam, q))
            while F(a * q, k * k * lam) - sj < 1:
                cuts.add(float(F(a * q, k * k * lam) - sj))
                a += 1
            if mutant != "noV":
                # V boundaries: lam (psi + sj)/q = b + t, b a left end of V
                for b in G.Vg:
                    t = math.floor(lam * sj / q - b) - 1
                    while q * (b + t) / lam - sj < 1:
                        p_ = q * (b + t) / lam - sj
                        if p_ >= 0:
                            cuts.add(p_)
                        t += 1
        if len(cuts) > vbound:
            return False, f"vertical boundaries {len(cuts)} > {vbound}"
        cuts = sorted(cuts)
        cell, func, Avals = {}, {}, {}
        for v in range(Q):
            psi = F(v, Q)
            i0 = bisect_left(cuts, float(psi))
            if i0 < len(cuts) and abs(cuts[i0] - float(psi)) < 1e-12:
                continue                                  # psi on a boundary: a separate face
            S0, sig = F(0), []
            for i in range(1, D):
                x = F(v % q ** i, q ** i)
                Yc = centre(F(lam * v % q ** i, q ** i))
                S0 += Yc * Yc
                sig.append((math.floor(x * G.nU), G.Vlab(Yc)))
            B0 = math.floor(q * q * S0)
            f = q * q * S0 - B0
            h = f + (lam * psi) ** 2 if mutant != "noh" else f
            part, As, typ = [], [], []
            for j in range(k):
                key, lab = G.point((v + Q * s[j]) % N)
                if lab[0][:-1] != tuple(c for c, _ in sig) or lab[1][:-1] != tuple(c for _, c in sig):
                    return False, "a coordinate i < D moves along the line"
                A = q * centre((lam * (psi + s[j]) / q) % 1) - lam * psi
                if A.denominator != 1:
                    return False, "A_j not an integer"
                Avals.setdefault(j, set()).add(A)
                if key[1] - B0 != math.floor(h + 2 * lam * A * psi + A * A):
                    return False, f"band law fails (v={v}, j={j})"
                part.append((lab[0][-1], lab[1][-1]))
                As.append(A)
                typ.append((key, lab))
            c = (tuple(part), tuple(As))
            if cell.setdefault(i0, c) != c:
                return False, f"vertical cell {i0} not constant"
            floors = tuple(math.floor(h + 2 * lam * A * psi + A * A) for A in As)
            if func.setdefault((tuple(sig), B0, i0, floors), tuple(typ)) != tuple(typ):
                return False, "type not a function of the face"
        if max(len(x) for x in Avals.values()) > 2:
            return False, "more than two pieces A_j"
        shared += Q - len(cell)
    return True, shared


def check_lines():
    out = {}
    for (k, P, e, D, lam, npa) in [(3, 5, 6, 2, 5 ** 6 - 1, 3), (3, 5, 6, 2, 7, 3),
                                   (3, 5, 3, 3, 124, 2), (4, 7, 4, 2, 7 ** 4 - 2, 3)]:
        ok, info = lemma_A1(k, P, e, D, lam, npa, 1)
        require(ok and info > 0, f"Lemma A1 exact, k={k} q={P ** e} D={D} lambda={lam}",
                f"({info} values of psi share a vertical cell)")
        out[f"k={k},q={P ** e},D={D},lambda={lam}"] = info
    rejected = {}
    for mut in ("noV", "noh", "noJ"):
        ok, info = lemma_A1(3, 5, 6, 2, 5 ** 6 - 1, 3, 1, mutant=mut)
        require(not ok, f"mutant {mut} rejected", f"({info})")
        rejected[mut] = info
    mult = {}
    for (k, P, e, D, lam) in [(4, 5, 1, 3, 2), (4, 5, 2, 2, 24)]:
        G = Template(k, P, e, D, lam)
        tab = G.table()
        mu = 0
        for ep in range(1, G.q):
            d = G.q ** (D - 1) * ep
            for n0 in range(G.N):
                c = {}
                for j in range(k):
                    kk = tab[(n0 + j * d) % G.N][0]
                    c[kk] = c.get(kk, 0) + 1
                mu = max(mu, *c.values())
        require(mu <= 2, f"multiplicity <= 2 on every line progression, k={k} q={G.q} D={D}", f"(max {mu})")
        mult[f"k={k},q={G.q},D={D}"] = mu
    return {"psi_sharing_a_cell": out, "mutants_rejected": rejected, "max_multiplicity": mult}


# ---------------------------------------------------------------- scale
def lse(*v):
    m = max(v)
    return m + math.log(sum(math.exp(x - m) for x in v))


def ln_lnT(lk, a, c):
    """ln of an upper bound for ln T_line (Lemma A1), in log space.

    ln T_line <= (D-1)(ln(k^2 lambda) + ln J) + ln(q^2 (D-1)/4 + 1) + 2 ln q + ln 2 + 2 ln(L+1),
    with D <= 2k^a, ln lambda <= h0 ln(2M), h0 = D ceil(ln k)^2, M <= 2k^m, m = (1+2a)/2,
    ln q <= c k ln k / D + ln(2k^2) (D >= k^a), J <= 4k^2 (R + 1), R + 1 <= 2D ln q + 1,
    and L + 1 <= 8 k q^2 once lambda < q and J <= q (`hyp`, upper bounds of ln lambda and ln J
    against a lower bound of ln q).
    """
    llk = math.log(lk)
    lnD = a * lk + math.log(2)
    m = (1 + 2 * a) / 2
    ln_lnlam = lnD + 2 * math.log(lk + 1) + math.log(math.log(4) + m * lk)
    ln_lnq = lse(math.log(c) + (1 - a) * lk + llk, math.log(math.log(2) + 2 * lk))
    ln_R = lse(lnD + math.log(2) + ln_lnq, 0.0)
    lnJ = math.log(4) + 2 * lk + ln_R
    A1 = lnD + lse(math.log(2 * lk), ln_lnlam)
    A2 = lnD + math.log(lnJ)
    A3 = lse(math.log(2) + ln_lnq, math.log(lnD + 1))
    A4 = math.log(2) + ln_lnq
    A5 = math.log(2) + lse(math.log(math.log(8)), llk, math.log(2) + ln_lnq)
    lnT = lse(A1, A2, A3, A4, A5, math.log(math.log(2)))
    # lower bound: ln q >= c k ln k / D >= c k^{1-a} ln k / 2 (D <= 2k^a)
    ln_lnq_low = math.log(c) + (1 - a) * lk + llk - math.log(2)
    hyp = ln_lnlam < ln_lnq_low and math.log(lnJ) < ln_lnq_low
    return lnT, hyp


def check_scale():
    out = {}
    for a in (F(3, 10), F(2, 5), F(9, 20), F(49, 100)):
        for c in (F(1, 9), F(1, 2), F(1)):
            first = None
            for t in range(10, 400):
                lk = 1.1 ** t
                lnT, hyp = ln_lnT(lk, float(a), float(c))
                good = hyp and (lk + math.log(math.log(2) / 2)) - lnT > math.log(1.01)
                if first is None and good:
                    first = lk
                if first is not None and not good:
                    require(False, f"scale a={a} c={c}: fails again at ln k = {lk:.4g}")
            require(first is not None, f"scale a={a} c={c}, m=(1+2a)/2: ln T_line <= (k/2) ln 2 / 1.01",
                    f"(from ln k = {first:.4g})")
            out[f"a={a},c={c}"] = round(first, 3)
    per_a = {}
    for key, v in out.items():
        per_a.setdefault(key.split(",")[0], set()).add(round(v))
    require(all(len(x) == 1 for x in per_a.values()), "scale: thresholds do not depend on c here")
    stated = "`ln k ≈ " + ", ".join(str(min(per_a[f"a={a}"])) for a in ("3/10", "2/5", "9/20", "49/100")) + "`"
    require(stated in " ".join(README.split()), "scale: thresholds stated in README.md equal the computed ones",
            f"({stated})")
    lnT, _ = ln_lnT(1e6, 0.5, 1 / 9)
    require(lnT > 1e6 + math.log(math.log(2) / 2), "negative control: the bound fails at a = 1/2")
    return out


# ---------------------------------------------------------------- moments
def lagrange0(z):
    out = []
    for i, zi in enumerate(z):
        p = F(1)
        for j, zj in enumerate(z):
            if j != i:
                p *= F(zj, zj - zi)
        out.append(p)
    return out


def interp(nodes, vals):
    def u(x):
        s = F(0)
        for i, (xi, vi) in enumerate(zip(nodes, vals)):
            p = F(vi)
            for j, xj in enumerate(nodes):
                if j != i:
                    p *= F(x - xj, xi - xj)
            s += p
        return s
    return u


def binom_moments(law, m):
    return [sum(w * math.comb(z, j) for z, w in law.items()) for j in range(m + 1)]


def check_moments():
    rnd = random.Random(7)
    n_ok, signed_below = 0, False
    for _ in range(3000):
        m = rnd.choice([2, 3, 4])
        ns = rnd.randint(m + 1, 12)
        nodes = [0] + rnd.sample(range(1, ns + 1), m)
        vals = [F(-1)] + [F(rnd.randint(0, 20), rnd.randint(1, 5)) for _ in range(m)]
        u = interp(nodes, vals)
        if any(u(z) < 0 for z in range(1, ns + 1)):
            continue
        for _ in range(3):
            z = sorted(rnd.sample(range(1, ns + 1), m + 1))
            l0 = lagrange0(z)
            signed = sum(l * u(zi) for l, zi in zip(l0, z))
            assert signed == -1                       # exact interpolation at 0
            if sum(abs(l) * u(zi) for l, zi in zip(l0, z)) < 1:
                require(False, "Lemma B2", f"{nodes} {vals} {z}")
            signed_below = signed_below or signed < 1  # the bound needs the absolute values
            n_ok += 1
    require(n_ok > 1000, "Lemma B2 (Lagrange): sum u(z_i)|l_i(0)| >= 1", f"({n_ok} exact cases)")
    require(signed_below, "negative control: without absolute values the sum is -1 < 1")

    ns, t = 1000, 500
    law = {0: F(1, 2), t: F(1, 2)}
    S = binom_moments(law, 3)
    second = S[1] - 2 * S[2] / ns
    require(not (S[1] < 1 or second < 1), "law {0, n*/2}: two moments do not certify (#22, Theorem 2)",
            f"(S1 - 2S2/n* = {float(second):.2f})")

    def u_t(z):
        return F((z - 1) * (z - t) ** 2, t * t)
    assert u_t(0) == -1 and all(u_t(z) >= 0 for z in range(1, ns + 1))
    vals = [u_t(z) for z in range(4)]
    y = [sum((-1) ** (j - i) * math.comb(j, i) * vals[i] for i in range(j + 1)) for j in range(4)]
    assert all(sum(y[j] * math.comb(z, j) for j in range(4)) == u_t(z) for z in range(50))
    Eu = sum(y[j] * S[j] for j in range(4))
    require(Eu < 0, "law {0, n*/2}: certified at order 3 by u_t", f"(E u_t = {Eu})")

    for nst in (5, 17, 100):
        require(all(F((z - 1) * (nst - z), nst) == F(z * (nst + 1 - z), nst) - 1 for z in range(nst + 1)),
                f"identity, n* = {nst}: (z-1)(n*-z)/n* = f - 1 with f of #22, Theorem 2")

    rnd = random.Random(11)
    seen = 0
    for _ in range(4000):
        ns = rnd.randint(8, 40)
        tt = rnd.randint(2, ns)
        pts = rnd.sample(range(1, ns + 1), 4)
        w = [F(rnd.randint(1, 50)) for _ in range(5)]
        tot = sum(w)
        law = {0: w[0] / tot}
        for p_, wi in zip(pts, w[1:]):
            law[p_] = wi / tot
        if sum(wi * F((z - 1) * (z - tt) ** 2, tt * tt) for z, wi in law.items()) >= 0:
            continue
        z = sorted(pts)
        g = min(b - a for a, b in zip(z, z[1:]))
        mu = min(law[x] for x in z)
        if not law[0] > mu * F(g, ns) ** 3:
            require(False, "Corollary B4", f"{law} {ns} {tt}")
        seen += 1
    require(seen > 20, "Corollary B4 (m = 3, singletons W_i): P(Z=0) > mu (g/n*)^3", f"({seen} certified laws)")
    return {"lagrange_cases": n_ok, "B4_laws": seen, "second_moment_value": str(second), "E_u_t": str(Eu)}


README = (HERE / "README.md").read_text()

# frozen sentences (whitespace-normalised, verbatim in README.md)
STATEMENT = [
    "`1 − e^{−(ln 2/2 − o(1))k}`, for every fixed `a < 1/2` and every fixed `c`",
    "T_line = (k²λJ)^{D−1} · (⌊q²(D−1)/4⌋ + 1) · q(q−1) · 2(L+1)²,",
    "L = k(⌊k²λ/q⌋ + J + 1) + 2k(⌊q²/4⌋ + 1)",
    "Pr[ some line progression is monochromatic under c₀∘L ⊕ 1_Y∘κ ] ≤ 2 T_line 2^{−⌈k/2⌉}",
    "= e^{−(ln 2/2 − o(1)) k}.",
    "1. *Unconditional.* An argument that proves a van der Waerden upper bound for `𝒞(c₀)` by producing,",
    "2. *For (S), which concerns proper `Y` only,* one needs a proper `Y` without a line witness.",
    "3. *The case of the P1a route where the final witness comes from Lemma E*",
    "* Theorem A needs `a < 1/2` and `c` **fixed**.",
]

# frozen sections: header line up to the next '## ' header, whitespace-normalised
FROZEN = {
    "## The family of methods, and the scope": None,
    "## A. Line progressions": None,
    "## What this says about Door 1": None,
    "## What is not claimed": None,
}
FROZEN_HASHES = {
    "## The family of methods, and the scope":
        "606d58bddd7fa1c5e7bf0191b79bb78edfcb3109c441034f97f29f7b15cfdc6b",
    "## A. Line progressions":
        "33b585e225d6663e881fae5d21c0a6e659cec628f5475d7a28b428ec4e0d318f",
    "## What this says about Door 1":
        "9d79e304072adeea3a722b30a95a8c06e20ec67fb67953e85fb48c18c0869875",
    "## What is not claimed":
        "13ac966ece42c4f96b3c3167cc9771b00139d9186912ca6e7bb624470784d7fc",
}


def section(head):
    if head not in README:
        return None
    body = README.split(head, 1)[1]
    nxt = body.find("\n## ")
    body = body if nxt < 0 else body[:nxt]
    return hashlib.sha256(" ".join((head + body).split()).encode()).hexdigest()


def check_frozen():
    flat = " ".join(README.split())
    for st in STATEMENT:
        require(" ".join(st.split()) in flat, f"frozen sentence present: {st[:60]!r}")
    for head in FROZEN:
        got = section(head)
        if "--print-sections" in sys.argv:
            print(f"   {head}: {got}", file=sys.stderr)
        require(got == FROZEN_HASHES.get(head), f"frozen section unchanged: {head}")
    return {"sentences": len(STATEMENT), "sections": sorted(FROZEN)}


FILES = ("NOTICE.md", "README.md", "RESULT.json", "verify.py")
WRITING = "--write" in sys.argv or "--manifest" in sys.argv


def integrity():
    if "--manifest" in sys.argv:
        return list(FILES)
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    require(sorted(manifest) == sorted(FILES), "MANIFEST lists the four files")
    for name, digest in sorted(manifest.items()):
        if WRITING and name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash of {name}")
    return list(FILES)


def main():
    # every require() exits on failure, so nothing below runs after a failed check
    report = {"frozen": check_frozen(), "lines": check_lines(), "scale_first_ln_k": check_scale(),
              "moments": check_moments(), "integrity_files": integrity()}
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(text)
    stored = HERE / "RESULT.json"
    if WRITING:
        stored.write_text(text)
        if "--manifest" in sys.argv:
            (HERE / "MANIFEST.json").write_text(json.dumps(
                {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest() for n in FILES}, indent=2) + "\n")
    else:
        require(stored.read_text() == text, "output equal to RESULT.json")
    print(f"Test passé : all checks pass ({len(COUNT)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
