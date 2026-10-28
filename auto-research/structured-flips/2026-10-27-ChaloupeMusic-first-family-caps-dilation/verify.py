"""Checks for 'The first family caps the dilation: the 1/8 barrier holds uniformly in a'.

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary must equal RESULT.json; --write regenerates it only when every
check passes).

  1. Lemma 1 (the count) exhaustively on toys: Z/q^D with the source's U mesh
     (H_x = 1/(k^2 lambda)); for a fixed n0, the progressions through n0 whose k
     x-labels are distinct, and the number of distinct x-label SETS they carry,
     against the bound (N - 1 - (k-1)|Delta|)/(k F) with F, Delta computed
     exactly, and F <= (floor(q H_x)+1)^D; the two steps of the proof, at most
     k(k-1)|Delta| pairs with a repeated label and at most k^2 F pairs per label
     set.  Mutants: an injective map to label sets, and (k-1)(|Delta|-1) repeated
     pairs (no factor k for the position of n0), must each fail on some toy.
  2. Corollary 3 at k = 2^739, 2^1024, 2^4096, r = 2: the largest D allowed by
     condition (U) with ln lambda >= theta(D); there, ln lambda / ln q, the scope
     lambda <= q/(400 k^3), and ln E / ln q.
  3. Theorem 4, the o(1) terms: for each D allowed by (U) (all D up to D_max,
     geometric grid plus the endpoints), the least c for which the necessary
     inequality of K1 fails, by bisection in exact Decimal arithmetic; its
     supremum over D, against 1/8.  Mutant: with ln lambda >= 0 instead of
     theta(D), the supremum climbs towards 1/4.  The same supremum on a grid of
     smaller k (2^20 ... 2^200), for the explicit threshold.  The scope of
     Lemma H, lambda <= q/(400 k^3), is checked at every (c, D) used; where it
     fails, no failure of K1 is inferred.
  4. Provenance: MANIFEST hashes; summary equal to RESULT.json.  --write and
     --manifest write nothing when a check fails; --manifest rewrites
     MANIFEST.json (it is the only option that does), --write only RESULT.json.
  5. Frozen statement: the key sentences and numbers of README.md, verbatim.
  0. (first) References: the cited statements occur verbatim in the notes of
     this tree; with --git, in the pinned notes of PRs #14, #19, #21; with
     --source <dir>, in the source sections, whose sha256 must equal
     source-manifest.json.
"""
import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 80
HERE = Path(__file__).resolve().parent
FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL', msg)


# ------------------------------------------------------------ 0. references
import subprocess  # noqa: E402

ROOT = HERE.parents[2]
SF = 'auto-research/structured-flips/'
IN_TREE = {
    SF + '2026-10-26-ChaloupeMusic-keyed-local-lemma-and-large-moduli': [
        '**Theorem A (clique bound).**', 'then for every `v ∈ 𝒱`, `Σ_{E : v ∈ vbl(E)} μ(E) < 1`.',
        'log|𝒦| ≤ D ln(2|V|) + ln(Dq²/4 + 1)', '**Lemma B1 (density).**',
        'Let `δ_X = |κ^{−1}(X)|/N` be the density of `X` among positions, and `η = 2/λ + k²/N`.'],
    SF + '2026-10-27-ChaloupeMusic-one-eighth-barrier': [
        '> **Fixed `a`.**', 'with `ln E = o(ln q)` are **not covered by the proofs of this', '**Proposition 1 (K1).**', '**Proposition 2 (K3).**'],
    SF + '2026-10-26-ChaloupeMusic-exact-door-one-condition': [
        '**Proposition 5 (first moment of a random-like `X`).**'],
}
PINNED = {
    ('cd1de3807cd1813cf640cda037869f2c30ff5541',
     'auto-research/short-period-sensitivity/2026-10-20-ChaloupeMusic-first-family-circularity'): [
        'More generally, a fibre of the x-label has at most `(⌊qH_x⌋ + 1)^D`',
        'Every admissible `h_0` here is at least `D`.'],
    ('cd1de3807cd1813cf640cda037869f2c30ff5541',
     'auto-research/short-period-sensitivity/2026-10-26-ChaloupeMusic-local-lemma-hub'): [
        '## Lemma H (a hub)', 'Assume `λ ≤ q/(400k³)` and `D ≥ 2`, and set `E = ⌊q/(64k³λ)⌋`.',
        'ln E ≥ ln q − ln λ − 3 ln k − ln 67'],
    ('cd1de3807cd1813cf640cda037869f2c30ff5541',
     'auto-research/short-period-sensitivity/2026-10-20-ChaloupeMusic-single-label-obstructions'): [
        '1. **Theorem 1.**'],
    ('98e6d36fb2de2d646dbc0ce17f818412b58f32e8',
     'auto-research/short-period-sensitivity/2026-10-20-ChaloupeMusic-rich-cover-barrier'): [
        '2. **Small sets (rigorous).**',
        'so at most `kN²(4/k² + 1/q)^D = o(N²)` progressions.'],
    ('84ed864cc8c25113a80e33644992878c740fc332',
     'auto-research/trust-reduction/2026-10-26-ChaloupeMusic-source-only-1-16'): [
        '**Proposition 5.**', '**Family 1.**', '**Lemma 3.**',
        'order `S` by grouping equal labels and deal it cyclically into `w_max ≤ k/M` rows'],
}
SRC = 'preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/'
SOURCE = {
    SRC + '02-setup.tex': ['We take $k$ large enough that $h_0<2M<k$.', 'H_x=\\frac H\\lambda', '[aH_x,(a+1)H_x),\\qquad 0\\le a<k^2\\lambda.',
                           '\\lambda=\\prod_{\\substack{\\ell\\le h_0\\\\ \\ell\\text{ prime}}}',
                           'ck\\log k\\le D\\log q\\le ck\\log k+D\\log(2k^2).'],
    SRC + '05-dichotomy.tex': ['D\\left(4\\eta+\\frac1{h_0}\\right)'],
    SRC + '04-outer.tex': ['call a full label \\emph{light} if its multiplicity',
                           'For the first family, take each distinct full-label word of a cyclic',
                           'Distribute the resulting list cyclically among',
                           'Assign to every $\\beta\\in\\cL$ an independent uniform random bit'],
}
n_in = 0
def norm(t):
    return ' '.join(t.split())


for note, anchors in IN_TREE.items():
    path = ROOT / note / 'README.md'
    text = norm(path.read_text()) if path.exists() else ''
    check(bool(text), f'missing note {note}')
    for an in anchors:
        check(norm(an) in text, f'anchor not found in {note}: {an!r}')
        n_in += 1
SM_SHA = 'e6dd98f5338eb7c981ed68afaca2b998c66f5c68397acccdb682c8d70a75e98c'
check(hashlib.sha256((ROOT / 'source-manifest.json').read_bytes()).hexdigest() == SM_SHA,
      'source-manifest.json differs from the pinned one')
n_pin = sum(len(v) for v in PINNED.values())
done_pin = 0
if '--git' in sys.argv:
    for (commit, note), anchors in PINNED.items():
        r = subprocess.run(['git', '-C', str(ROOT), 'show', f'{commit}:{note}/README.md'], capture_output=True)
        check(r.returncode == 0, f'--git: {commit[:7]} not reachable for {note}')
        text = norm(r.stdout.decode()) if r.returncode == 0 else ''
        for an in anchors:
            check(norm(an) in text, f'anchor not found in {note}@{commit[:7]}: {an!r}')
            done_pin += norm(an) in text
n_src = sum(len(v) for v in SOURCE.values())
done_src = 0
if '--source' in sys.argv:
    i = sys.argv.index('--source')
    check(i + 1 < len(sys.argv), '--source needs a directory')
    sdir = Path(sys.argv[i + 1]) if i + 1 < len(sys.argv) else Path('/nonexistent')
    man = json.loads((ROOT / 'source-manifest.json').read_text())
    pinned = {f['path']: f['sha256'] for f in man.get('files', []) if isinstance(f, dict) and 'path' in f}
    for rel, anchors in SOURCE.items():
        f = sdir / rel
        check(f.exists(), f'--source: missing {rel}')
        data = f.read_bytes() if f.exists() else b''
        check(pinned.get(rel) == hashlib.sha256(data).hexdigest(), f'--source: {rel} differs from source-manifest.json')
        for an in anchors:
            ok = an in data.decode(errors='replace')
            check(ok, f'anchor not found in {rel}: {an!r}')
            done_src += ok
OUT['anchors'] = {'in_tree': n_in, 'pinned_with_git': n_pin, 'source_with_source': n_src}
print(f'0. references: {n_in} in-tree anchors checked; {done_pin} of {n_pin} pinned anchors '
      f'({"--git" if "--git" in sys.argv else "rerun with --git"}); {done_src} of {n_src} source anchors '
      f'({"--source" if "--source" in sys.argv else "rerun with --source <dir>"})')

# ------------------------------------------------------------ 1. Lemma 1 on toys
def xlabel(n, q, D, kl):
    """U-labels of x_i(n) = (n mod q^i)/q^i, U cells of width 1/kl (kl = k^2 lambda)."""
    return tuple(((n % q ** i) * kl) // q ** i for i in range(1, D + 1))


def lemma1(q, D, k, lam):
    N = q ** D
    kl = k * k * lam
    lab = [xlabel(n, q, D, kl) for n in range(N)]
    fib = {}
    for n, L in enumerate(lab):
        fib.setdefault(L, []).append(n)
    F = max(len(v) for v in fib.values())
    Delta = set()
    for v in fib.values():
        for x in v:
            for y in v:
                Delta.add((x - y) % N)
    n0 = 0
    sets = {}
    good = 0
    for d in range(1, N):
        for j0 in range(k):
            P = [(n0 + (j - j0) * d) % N for j in range(k)]
            if len(set(P)) < k:
                continue
            Ls = [lab[n] for n in P]
            if len(set(Ls)) == k:
                good += 1
                key = frozenset(Ls)
                sets[key] = sets.get(key, 0) + 1
    qHx = Decimal(q) / kl
    Fbound = (int(qHx) + 1) ** D
    bound = Decimal(N - 1 - (k - 1) * len(Delta)) / (k * F)
    return {'N': N, 'F': F, 'F_bound': Fbound, 'Delta': len(Delta), 'good_pairs': good,
            'repeated_pairs': k * (N - 1) - good, 'repeated_bound': k * (k - 1) * len(Delta),
            'mut_repeated_bound': (k - 1) * (len(Delta) - 1),
            'sets': len(sets), 'max_preimage': max(sets.values()), 'preimage_bound': k * k * F,
            'bound': float(bound)}


toys = {}
mut1 = mut2 = False
for q, D, k, lam in ((7, 2, 3, 1), (11, 2, 3, 1), (13, 2, 3, 1), (11, 2, 4, 1), (13, 2, 4, 1),
                     (17, 2, 4, 1), (7, 3, 3, 1), (5, 3, 3, 1), (11, 2, 3, 2), (13, 2, 3, 3),
                     (29, 2, 4, 1), (31, 2, 3, 1), (7, 2, 6, 1), (11, 2, 6, 1), (13, 2, 6, 1)):
    r = lemma1(q, D, k, lam)
    name = f'q={q},D={D},k={k},lam={lam}'
    check(r['F'] <= r['F_bound'], f'{name}: fibre above (floor(qHx)+1)^D')
    check(r['sets'] >= r['bound'], f'{name}: Lemma 1 bound fails ({r["sets"]} < {r["bound"]})')
    check(r['repeated_pairs'] <= r['repeated_bound'], f'{name}: repeated-label pairs above k(k-1)|Delta|')
    check(r['max_preimage'] <= r['preimage_bound'], f'{name}: a label set has more than k^2 F preimages')
    mut1 |= r['max_preimage'] > 1                    # mutant: (j0, d) -> label set injective
    mut2 |= r['repeated_pairs'] > r['mut_repeated_bound']   # mutant: no factor k for the position
    toys[name] = {kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in r.items()}
check(mut1, 'mutant "the map to label sets is injective" never fails')
check(mut2, 'mutant "(k-1)(|Delta|-1) repeated pairs" never fails')
OUT['lemma1_toys'] = toys
print(f'1. Lemma 1 on {len(toys)} toys: distinct label sets >= (N-1-(k-1)|Delta|)/(kF) everywhere; '
      f'preimages <= k^2 F, repeated pairs <= k(k-1)|Delta|; both mutants fail on some toy')

# ------------------------------------------------------------ 2, 3. template scale
LN2 = Decimal(2).ln()


def theta_low(D):
    """Rosser-Schoenfeld: theta(x) > x(1 - 1/ln x) for x >= 41; 0 below (trivially valid)."""
    D = Decimal(D)
    return D * (1 - 1 / D.ln()) if D >= 41 else Decimal(0)


def U_holds(D, lnk, k, r=2, lnlam=None):
    """Condition (U): D ln(min(k^2 lam, q)/2) < (k-1) ln r + ln(4k), at the smallest
    admissible ln lam (theta(D)); returns the largest ln lam allowed, or None."""
    lnr = Decimal(r).ln()
    rhs = (k - 1) * lnr + (4 * k).ln()
    lam_min = theta_low(D) if lnlam is None else lnlam
    if D * (2 * lnk + lam_min - LN2) >= rhs:
        return None
    return rhs / D - 2 * lnk + LN2                       # ln lam < this


def Dmax(lnk, k, lnlam_floor=None):
    lo, hi = 2, int(k.sqrt() * 3) + 50
    if lnlam_floor is not None:
        hi = int(k / lnk) + 50
    while hi - lo > 1:
        mid = (lo + hi) // 2
        ok = U_holds(mid, lnk, k, lnlam=(None if lnlam_floor is None else lnlam_floor)) is not None
        lo, hi = (mid, hi) if ok else (lo, mid)
    return lo


def necessary_fails(c, D, k, lnk, lnlam_up):
    """K1 at (c, D): True if the necessary inequality of Theorem 3 fails.
    ln N >= c k ln k; ln q in [c k ln k/D, (c k ln k + D ln 2k^2)/D];
    ln E >= ln q_low - ln lam_up - 3 ln k - ln 67; p > ln E/(k + ln E), p <= 1/2;
    ln|K| <= D ln(4(k^2 (D+1) ln q_up + 1)) + ln D + 2 ln q_up;
    need 2 ln N - ln 4 + ln k - (k/2) ln(1/p) - k ln 2 < ln|K|."""
    lnN = c * k * lnk
    lnq_low = lnN / D
    lnq_up = (lnN + D * (2 * k * k).ln()) / D
    if lnq_low - lnlam_up - 3 * lnk - Decimal(400).ln() < 0:   # Lemma H out of scope
        return False
    lnE = lnq_low - lnlam_up - 3 * lnk - Decimal(67).ln()
    if lnE <= 0:
        return False
    p = min(lnE / (k + lnE), Decimal(1) / 2)
    lnK = D * (4 * (k * k * (D + 1) * lnq_up + 1)).ln() + Decimal(D).ln() + 2 * lnq_up
    lhs = 2 * lnN - Decimal(4).ln() + lnk - (k / 2) * (1 / p).ln() - k * LN2
    return lhs >= lnK


def cstar(D, k, lnk, lnlam_up):
    lo, hi = Decimal(0), Decimal(1)
    if not necessary_fails(hi, D, k, lnk, lnlam_up):
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if necessary_fails(mid, D, k, lnk, lnlam_up) else (mid, hi)
    return hi


scale = {}
for log2k in (739, 1024, 4096):
    k = Decimal(2) ** log2k
    lnk = log2k * LN2
    dm = Dmax(lnk, k)
    check(Decimal(dm) < (k * LN2).sqrt() * Decimal('1.01'), f'2^{log2k}: D_max above sqrt(k ln 2)')
    # Corollary 2 at D_max and c = 1/9: ln lam / ln q, scope, ln E
    lnlam_up = U_holds(dm, lnk, k)
    c = Decimal(1) / 9
    lnq = c * k * lnk / dm
    ratio = lnlam_up / lnq
    check(ratio < 2 * LN2 / (c * lnk), f'2^{log2k}: ln lam/ln q not O(1/ln k)')
    check(lnq - lnlam_up - 3 * lnk - Decimal(400).ln() > 0, f'2^{log2k}: lambda > q/(400k^3)')
    lnE_ratio = (lnq - lnlam_up - 3 * lnk - Decimal(67).ln()) / lnq
    # Theorem 3: sup over D of the least failing c
    Ds = sorted({2, 3, 5, 10, dm, max(2, dm - 1)} |
                {int(Decimal(dm) ** (Decimal(t) / 20)) for t in range(1, 21)})
    worst = Decimal(0)
    argD = None
    for D in Ds:
        lu = U_holds(D, lnk, k)
        if lu is None:
            continue
        cs = cstar(D, k, lnk, lu)
        check(cs is not None, f'2^{log2k}, D={D}: no failing c found')
        if cs is not None and cs > worst:
            worst, argD = cs, D
    check(worst < Decimal(1) / 8, f'2^{log2k}: sup c* = {worst} not below 1/8')
    # mutant: without the dilation floor theta(D), D can reach k/ln k and c* climbs
    dm0 = Dmax(lnk, k, lnlam_floor=Decimal(0))
    lu0 = U_holds(dm0, lnk, k, lnlam=Decimal(0))
    cs0 = cstar(dm0, k, lnk, lu0)
    check(cs0 is not None and cs0 > Decimal(1) / 8, f'2^{log2k}: mutant (no theta(D)) stays below 1/8')
    scale[f'k=2^{log2k}'] = {
        'D_max': dm, 'log_k_D_max': round(float(Decimal(dm).ln() / lnk), 5),
        'lnlam_over_lnq_at_Dmax_c=1/9': round(float(ratio), 6),
        'lnE_over_lnq_at_Dmax_c=1/9': round(float(lnE_ratio), 6),
        'sup_c_star': round(float(worst), 6), 'argmax_D': argD,
        'gap_below_1/8': round(float(Decimal(1) / 8 - worst), 6),
        'mutant_no_theta_c_star': round(float(cs0), 6)}
OUT['template_scale'] = scale


def sup_cstar(log2k):
    k = Decimal(2) ** log2k
    lnk = log2k * LN2
    dm = Dmax(lnk, k)
    Ds = sorted({2, 3, 5, 10, dm, max(2, dm - 1)} |
                {max(2, int(Decimal(dm) ** (Decimal(t) / 20))) for t in range(1, 21)})
    best = Decimal(0)
    for D in Ds:
        lu = U_holds(D, lnk, k)
        if lu is None:
            continue
        cs = cstar(D, k, lnk, lu)
        best = max(best, cs if cs is not None else Decimal(1))
    return best


small = {f'k=2^{e}': round(float(sup_cstar(e)), 5) for e in (20, 40, 60, 100, 200)}
vals = list(small.values()) + [v['sup_c_star'] for v in scale.values()]
check(all(x < 0.125 for x in vals[2:]), 'sup c* not below 1/8 at some k >= 2^60')
check(small['k=2^40'] > 0.125 and small['k=2^60'] < 0.125, 'threshold not between 2^40 and 2^60')
OUT['threshold_sweep'] = small
print('3b. sup c* at smaller k: ' + ', '.join(f'{n}: {v}' for n, v in small.items()))
for n, v in scale.items():
    print(f'2-3. {n}: D_max = {v["D_max"]} (log_k {v["log_k_D_max"]}), ln lam/ln q <= '
          f'{v["lnlam_over_lnq_at_Dmax_c=1/9"]}, ln E/ln q >= {v["lnE_over_lnq_at_Dmax_c=1/9"]}; '
          f'K1 fails for every c >= {v["sup_c_star"]} (1/8 - {v["gap_below_1/8"]}); '
          f'mutant without theta(D): {v["mutant_no_theta_c_star"]}')

# ------------------------------------------------------------ 5. frozen statement
STATEMENT = [
    'D · ln( min(k²λ, q) / 2 )  <  k ln(r/(r−1)) + ln(4k)',
    '`h₀ < 2M < k`',
    'there is `k₀(c)`, depending only on `c`',
    'So the method has **no fixed `c > 1/8`** through K1 or K3, indexed by `(P, β)`, whatever `a_k`.',
    '`0.12357`, `0.12385` and `0.12459`',
    'No claim is made at `c = 1/8` itself.',
    'K2\'s rich half, and the merged forms, are unchanged and conditional.',
]
flat = ' '.join((HERE / 'README.md').read_text().split())
found = 0
for st in STATEMENT:
    ok = ' '.join(st.split()) in flat
    check(ok, f'statement changed or missing: {st[:60]!r}')
    found += ok
print(f'5. statement: {found} of {len(STATEMENT)} frozen sentences found verbatim in README.md')

# ------------------------------------------------------------ 4. provenance
FILES = ('NOTICE.md', 'README.md', 'RESULT.json', 'verify.py')
man = HERE / 'MANIFEST.json'
writing = '--write' in sys.argv or '--manifest' in sys.argv
if '--manifest' not in sys.argv:
    check(man.exists(), 'MANIFEST.json missing')
    m = json.loads(man.read_text()) if man.exists() else {}
    check(sorted(m) == sorted(FILES), 'MANIFEST: wrong file list')
    for name, h in m.items():
        if writing and name == 'RESULT.json':
            continue
        f = HERE / name
        check(f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() == h, f'MANIFEST: {name}')
out = json.dumps(OUT, indent=2, sort_keys=True, ensure_ascii=False) + '\n'
res = HERE / 'RESULT.json'
if writing:
    if not FAIL:
        res.write_text(out)
        if '--manifest' in sys.argv:
            man.write_text(json.dumps({n: hashlib.sha256((HERE / n).read_bytes()).hexdigest()
                                       for n in FILES}, indent=2) + '\n')
elif not res.exists() or res.read_text() != out:
    check(False, 'RESULT.json differs from the computed summary')
if FAIL:
    print(f'{len(FAIL)} check(s) failed')
    raise SystemExit(1)
print('Test passé : all checks pass')
