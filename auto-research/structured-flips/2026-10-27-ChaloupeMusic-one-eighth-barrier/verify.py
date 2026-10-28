"""Checks for 'The 1/8 barrier of the frozen-key method, in one statement'.

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary must equal RESULT.json; --write regenerates it; --git also
checks the notes of PRs #14, #19 and #21 at their pinned commits).

  0. The statement: the key sentences of the theorem and of Propositions 1
     and 2 occur verbatim in README.md, against a list frozen here.
  1. Every reference: each statement the synthesis names occurs verbatim in
     the README of the note it cites (in-tree notes always; out-of-tree
     notes with --git, against pinned commits and README hashes; with --git
     an unreachable commit is a failure).
  2. Propositions 1 and 2 at the 18 template points of ap-free-frozen-sets:
     lambda <= q/(400k^3), ln E >= 0.59 ln q, the forced rate p and marginal
     rho > ln E/(k + ln E), whose exponent (b for Proposition 1, b_X for
     Proposition 2) stays within 0.02 of a; the ceilings b/4 and
     (1/2 - theta) b_X/2 follow, and their margin below 1/8 is recorded.
  3. The hub inequality on toy stars, exactly: E(1-rho)^k < 1 iff
     rho > 1 - E^(-1/k), and ln E/(k + ln E) lies below that threshold.
  4. The ledger is closed: every row of section 4 has a checked anchor.
  5. Provenance: MANIFEST hashes (also under --write, except RESULT.json);
     summary equal to RESULT.json. --manifest rewrites RESULT.json and
     MANIFEST.json together, on purpose only.
"""
import hashlib
import json
import subprocess
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 60
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL', msg)


SF = 'auto-research/structured-flips/'
SPS = 'auto-research/short-period-sensitivity/'
TR = 'auto-research/trust-reduction/'

# Notes in this tree (PRs #16, #20, #22): path -> anchors.
IN_TREE = {
    SF + '2026-10-27-ChaloupeMusic-key-measurable-colorings': [
        '## Theorem 1 (exact reformulation)', '**Corollary.**',
        '## Proposition 2 (each half alone is satisfiable)',
        '## Proposition 3 (the interaction, exactly)', '* **(D) density.**',
        '* **(S) supersaturation.**', '### (D): what is proved, and what is possible',
        '## Answer to S6'],
    SF + '2026-10-26-ChaloupeMusic-exact-door-one-condition': [
        '**Proposition 1.**', '**(II′_θ)**', '**(I′_η)**', '**(I′_w)**', '**Theorem 2.**',
        '**Proposition 4 (no ceiling on `b`', '**Proposition 5 (first moment of a random-like `X`).**',
        '| P1b B1 (dense rules fail (II)) | yes | **falls.**', '## 4. The closures, re-read under (II′)'],
    SF + '2026-10-26-ChaloupeMusic-keyed-local-lemma-and-large-moduli': [
        '**Theorem A (clique bound).**', '**Corollary A1 (a local lemma is a first moment).**',
        '**Corollary A2 (uniform laws stay at 1/8 when b ≤ 1).**',
        '**Corollary A3 (what a certificate beyond 1/8 must contain).**',
        'The same proof applied to the flips themselves', '**Lemma B1 (density).**',
        '**Corollary B1′ (residue and character rules; literal (II)).**',
        '**Lemma B2 (every rule has the random second moment).**',
        '**Proposition B3 (the squares family).**', '**Where (b) stands.**',
        'Lemma H at `e = 1`'],
    SF + '2026-10-20-ChaloupeMusic-single-label-lenses': [
        '### Theorem A (a residue rule meets, without saturating, every block with `ℓ ∤ e`)',
        '### Corollary A (the `e = 1` family at `b_X → 1/2`)',
        '### Proposition B (the shifted family defeats every such rule)',
        '### Lemma R (the exact reduction behind (I))'],
    SF + '2026-10-20-ChaloupeMusic-algebraic-band-rules': [
        '**Theorem 1.**', '**Corollary 2 (door 1).**', '**Corollary 3 (sizes).**',
        '**Pseudo-random residue sets.**'],
    SF + '2026-10-26-ChaloupeMusic-ap-free-frozen-sets': [
        '### Lemma E (embedding a fibre pattern into a rich progression)',
        '### Theorem 2 (index-side 3-AP-free mechanisms are closed)',
        '### Theorem 3 (longer forbidden lengths: a reduction, and where it stops)',
        '### Proposition 4 (band-side AP-free sets: the count the referee asked for)',
        'S_J = {m ∈ J : κ(r + q^{D−1} m) ∈ X}   meets every k-AP contained in J.     (H)'],
    SF + '2026-10-26-ChaloupeMusic-off-diagonal-window': [
        '## Proposition 1 (density reduction)', '## Proposition 2 (first moment)',
        '(Cl)   r_{p₀(k)−1}(N₀) < ⌊N₀/k⌋', '(Op)   W(ℓ, k) > N₀'],
    SF + '2026-10-27-ChaloupeMusic-non-polynomial-bands': [
        '## Theorem 3', '**Corollary 4 (rich progressions).**',
        '## What this closes, and in which range of `ℓ`'],
    SF + '2026-10-27-ChaloupeMusic-more-keys': [
        '**Theorem A.**', '**Theorem B.**', '**Lemma F (a fibre is already separated).**',
        '**Corollary F (fibre invariance).**',
        '**Theorem C (a random X fails (I′) with N^{β} bits).**',
        '**Proposition D ((II′) at second order).**'],
    SF + '2026-10-27-ChaloupeMusic-moment-certificates': [
        '**Theorem 1 (independence is invisible to moments).**',
        '**Theorem 2 (the exact second-moment certificate).**',
        '**Theorem 3 (what a second-moment certificate looks like).**',
        '**Corollary 4 (hashing).**', '**Proposition 6 (Janson).**'],
    SF + '2026-10-27-ChaloupeMusic-supersaturation-is-global': [
        '**Proposition 1 (small families never witness (S)).**',
        '**Corollary 1′ (adaptive arguments).**',
        '**Proposition 2 (a line carries too few progressions).**',
        '**Proposition 3 (where (S) can hold at all).**', '## What this says about (S)'],
    SF + '2026-10-27-ChaloupeMusic-colour-correlated-rules': [
        '**Proposition A.**', '**Theorem B.**', '**Corollary B′ (dense form).**',
        '**Proposition E (a count is also necessary for the clique-bound class',
        '**Theorem C.**', '**Lemma D1 (Warren).**', '**(Q-S1b)**'],
    SF + '2026-10-27-ChaloupeMusic-dangerous-traces-scope': [
        '**Proposition 1.**', '**Corollary.**', '## 2. The dense case: where the count must come from'],
    SF + '2026-10-27-ChaloupeMusic-slow-word-transversal-density': [
        '**Theorem 1.**', '**Corollary 4.**', '**Proposition 6.**',
        '**Proposition 7 (random key sets are proper at `k^{−a+o(1)}`).**',
        '**Theorem 9 (the fractional barrier holds in `𝒞`).**', '## 5. What (D) needs now, exactly',
        '## 6. Inside the key-measurable class, with proper colorings'],
    SF + '2026-10-27-ChaloupeMusic-digit-transversals-saturate': [
        '## Theorem 1 (every digit rule saturates or misses a block)',
        '**Corollary 1 (the S6-63 candidate).**',
        '## Theorem 2 (rules linear in the digits need a modulus of size N)',
        '## Lemma W (where (II′) can fail at all)'],
    SF + '2026-10-27-ChaloupeMusic-line-witnesses': [
        '**Theorem A (no line witnesses).**', '**Corollary A2 (scope of arguments).**',
        'The P1a route with witnesses off the lines stays open.',
        'Such an argument is excluded, unconditionally for an upper bound on `𝒞`, and under'],
    SF + '2026-10-27-ChaloupeMusic-first-family-caps-dilation': [
        '**Corollary 3.**', '**Theorem 4.**',
        'So the method has **no fixed `c > 1/8`** through K1 or K3, indexed by'],
    'auto-research/template-ceilings/2026-10-20-ChaloupeMusic-outside-template-ceilings': [
        '## The one exception, stated exactly', '**No-go for one named class.**',
        '## The torus uncertainty principle'],
}

# Notes of PRs #14, #19, #21 (not in this tree): pinned commit, README sha256, anchors.
OUT_OF_TREE = {
    SPS + '2026-10-20-ChaloupeMusic-single-label-obstructions': (
        'cd1de3807cd1813cf640cda037869f2c30ff5541', '#14',
        ['1. **Theorem 1.**', '## Lemma C (many good blocks for each word)', '## Proposition P2',
         '## Lemma D (scope)']),
    SPS + '2026-10-20-ChaloupeMusic-first-family-circularity': (
        'cd1de3807cd1813cf640cda037869f2c30ff5541', '#14',
        ['**Lemma 1 (injective x-labels).**', '**Lemma 2 (when Lemma 1 applies).**',
         '**Proposition 3 (the first family becomes the whole problem).**',
         '**Remark (the intermediate window).**',
         'For fixed `a < 1/2` and the sharpened `h_0`, we have `q ≥ 400k³λ` for',
         '`log λ = O(k^a log² k) = o(k^{1−a} log k)`']),
    SPS + '2026-10-20-erwan-binding-lever': (
        'cd1de3807cd1813cf640cda037869f2c30ff5541', '#14',
        ['| drop B | 1 | 1/4 |', '**B is the only one whose relaxation alone raises the supremum.**']),
    SPS + '2026-10-26-ChaloupeMusic-local-lemma-hub': (
        'cd1de3807cd1813cf640cda037869f2c30ff5541', '#14',
        ['## Lemma H (a hub)', '## Theorem 1', '## Proposition 2 (refined families are complete)',
         '## Proposition 3 (cover families contain door 1)', '## Section R',
         'ln E ≥ ln q − ln λ − 3 ln k − ln 67']),
    SPS + '2026-10-20-ChaloupeMusic-rich-cover-barrier': (
        '98e6d36fb2de2d646dbc0ce17f818412b58f32e8', '#21',
        ['2. **Small sets (rigorous).**', '> **Proposition 5′.**',
         '4. **Lemma (rank ≥ 4, rigorous).**', '3. **Larger `S₀` (rigorous).**']),
    TR + '2026-10-26-ChaloupeMusic-source-only-1-8': (
        '84ed864cc8c25113a80e33644992878c740fc332', '#19',
        ['**Theorem 9.**', '## 8. Region, supremum, explicit choice']),
    TR + '2026-10-26-ChaloupeMusic-source-only-1-16': (
        '84ed864cc8c25113a80e33644992878c740fc332', '#19',
        ['**Lemma 3.**', '**Proposition 5.**', '**Theorem 6.**', '**Theorem 8.**',
         '## 2. Parameters, and the source lemmas reused']),
}
README_SHA = {
    SPS + '2026-10-20-ChaloupeMusic-single-label-obstructions':
        '173b414d6a458ca38f2e7611d37478bae2451039571546b152886f67ea20808b',
    SPS + '2026-10-20-ChaloupeMusic-first-family-circularity':
        'bf6bfda5be21db2e1fff29658e280224f0dcb8d64c7ecd2043eceb66696479a8',
    SPS + '2026-10-20-erwan-binding-lever':
        'bb7b9da942e40bedb73bf276566a97066e8e4590e2f7bb07a17f14adb151d028',
    SPS + '2026-10-26-ChaloupeMusic-local-lemma-hub':
        '6149aca0a8c6acf2af65fe0073189cde5ba221e42edb5546351a60d858edfd35',
    SPS + '2026-10-20-ChaloupeMusic-rich-cover-barrier':
        '1cff7437399e80c60471c3ec4711b3bdcddf3fd8feeb6197f0593e0ed81c8752',
    TR + '2026-10-26-ChaloupeMusic-source-only-1-8':
        'fb34b82a8d65a3847aa88a102408e7dbe2fffb743492b1d5036f28c6efdc2a53',
    TR + '2026-10-26-ChaloupeMusic-source-only-1-16':
        '4d049caaeb9640fddaed46cfe2d28a03de76d847fe94ea1ec74b0036ef9281f5',
}

# ------------------------------------------------------------ 0. the statement
STATEMENT = [
    'Theorem 2 of Fox–Hunter (`r ≥ (ln k)^{3/ε}`) is outside its scope (§ 1).',
    'The template\'s asymmetric local-lemma criterion for `c₀` fails, whatever its weights, '
    'whenever `λ > q/(400k³)`: for every fixed `a > 1/2`, and in the window of the Remark of '
    '`first-family-circularity`.',
    'Sequences `a_k → 1/2⁻` with `ln E = o(ln q)` are **not covered by the proofs of this note**.',
    '**For K1 and K3, indexed by `(P, β)`, this regime is empty.**',
    'That note does not cover the merged forms of K1 and K3, nor K2.',
    'Fix `a < 1/2`. Suppose a certificate of one of the following kinds concludes at `(a, c)` '
    'for all large `k`. Then `c ≤ a/4`, so `c < 1/8`.',
    'the canonical events indexed by `(P, β)`: *unconditional*. With coinciding events merged: '
    '*conditional* on (G♭)(ii) (Proposition 1, Remark 3).',
    'The bound `b < a` is unconditional. The rich half `c ≤ b/4` is *conditional* on (G♭) of '
    '`rich-cover-barrier` (#21), for every `θ, δ > 0`: on part (ii), and on part (i) beyond `σ₄`, '
    'where (i) is not proved.',
    'Then `c ≤ (1/2 − θ)a/2`. Indexed by `(P, β)`: *unconditional*. With coinciding events merged: '
    '*conditional* on (G♭)(ii) (Proposition 2, Remark 3).',
    'So the method passes `1/8` if and only if `(Ω_c)` holds for some `c > 1/8`.',
    'Then `b ≤ a + o(1)` and `2c ≤ b/2 + o(1)`, so `c ≤ a/4`.',
    'Hence `c ≤ (1/2 − θ)a/2 < a/4`, whatever `b`.',
    'Only the rich step uses `ρ ≤ 1/2`.',
]
flat = ' '.join(line[2:] if line.startswith('> ') else (line[1:] if line == '>' else line)
                for line in (HERE / 'README.md').read_text().splitlines())
flat = ' '.join(flat.split())
found = 0
for st in STATEMENT:
    ok = ' '.join(st.split()) in flat
    check(ok, f'statement changed or missing: {st[:70]!r}')
    found += ok
OUT['statement_sentences'] = len(STATEMENT)

# frozen sections: header line up to the next '## ' header, whitespace-normalised
FROZEN = {
    '## 2. The statement': '3ffd40e92238eb0a66be15cecfd13e95ef0b1139513dcd05aab6adb88906d805',
    '## 4. The ledger of closed routes': 'a3bc2225927bc857e144cd4fa56b50f1cac0fed9f18f5e127b379b09bbd2129f',
    '## What is not claimed': '65cf1f0c7a883b05bf90832db3359ddd7ff747873387c1817770b1e61f20d1f7',
}
_text = (HERE / 'README.md').read_text()


def section(head):
    if head not in _text:
        return None
    body = _text.split(head, 1)[1]
    nxt = body.find('\n## ')
    body = body if nxt < 0 else body[:nxt]
    return hashlib.sha256(' '.join((head + body).split()).encode()).hexdigest()


for head, h in FROZEN.items():
    got = section(head)
    if '--print-sections' in sys.argv:
        print(f'   {head}: {got}')
    check(got == h, f'frozen section changed: {head}')
OUT['frozen_sections'] = sorted(FROZEN)
print(f'0. statement: {found} of {len(STATEMENT)} frozen sentences found verbatim in README.md')

# ------------------------------------------------------------ 1. references
n_in = 0
for note, anchors in IN_TREE.items():
    path = ROOT / note / 'README.md'
    check(path.exists(), f'missing note {note}')
    text = path.read_text() if path.exists() else ''
    for a in anchors:
        check(a in text, f'anchor not found in {note}: {a!r}')
        n_in += 1
n_pin = sum(len(a) for _, _, a in OUT_OF_TREE.values())
OUT['notes_cited'] = len(IN_TREE) + len(OUT_OF_TREE)
OUT['anchors_in_tree'] = n_in
OUT['anchors_pinned_checked_only_with_git'] = n_pin
OUT['out_of_tree_pins'] = {n: {'pr': pr, 'commit': c} for n, (c, pr, _) in OUT_OF_TREE.items()}
OUT['out_of_tree_readme_sha256'] = README_SHA

git_checked = 0
if '--git' in sys.argv:
    for note, (commit, _, anchors) in OUT_OF_TREE.items():
        r = subprocess.run(['git', '-C', str(ROOT), 'show', f'{commit}:{note}/README.md'],
                           capture_output=True)
        if r.returncode != 0:
            check(False, f'--git: commit {commit[:7]} not reachable for {note}')
            continue
        text = r.stdout.decode()
        sha = hashlib.sha256(r.stdout).hexdigest()
        check(sha == README_SHA[note], f'README hash changed: {note}')
        for a in anchors:
            check(a in text, f'anchor not found in {note}@{commit[:7]}: {a!r}')
        git_checked += 1
pin_done = sum(len(OUT_OF_TREE[n][2]) for n in OUT_OF_TREE) if git_checked == len(OUT_OF_TREE) else 0
print(f'1. references: {n_in} anchors in {len(IN_TREE)} in-tree notes checked; '
      f'{pin_done} of {n_pin} anchors in {len(OUT_OF_TREE)} pinned notes checked '
      f'({"with --git" if "--git" in sys.argv else "rerun with --git to check them"})')

# ------------------------------------------------------------ 2. propositions at template points
LN2 = Decimal(2).ln()


def ceil(x):
    return x.to_integral_value(rounding='ROUND_CEILING')


def point(log2k, a, c):
    """P1a's template model: D = ceil(k^a), h0 = D ceil(ln k)^2, ln q = c k ln k / D,
    ln lambda <= 1.25506 (h0/ln h0) ln k (each prime power <= 2M <= k)."""
    k = Decimal(2) ** log2k
    lnk = log2k * LN2
    D = ceil(k ** Decimal(a))
    h0 = D * ceil(lnk) ** 2
    lnlam = Decimal('1.25506') * h0 / h0.ln() * lnk
    lnq = Decimal(c) * k * lnk / D
    scope = lnq - lnlam - 3 * lnk - Decimal(400).ln()       # ln(q/(400 k^3 lambda)) >= 0
    lnE = lnq - lnlam - 3 * lnk - Decimal(67).ln()            # Lemma H / Theorem 1 of local-lemma-hub
    # rho > ln E/(k + ln E): b_X = -log_k rho <= log_k((k + ln E)/ln E)
    bX = ((k + lnE) / lnE).ln() / lnk
    # Proposition 1: E(1-p)^k < 1 gives p > ln E/(k + ln E) by the same step, so b <= bX too.
    return {'scope_log2': float(scope.ln() / LN2) if scope > 0 else None,
            'lnE_over_lnq': float(lnE / lnq), 'bX_max': float(bX), 'b_max_prop1': float(bX),
            'ceiling_prop1_b_over_4': float(bX / 4),
            'ceiling_prop2_theta_0.01': float((Decimal('0.49') * bX) / 2),
            'margin_below_1_8': float(Decimal(1) / 8 - bX / 4)}


pts = {}
for log2k in (739, 1024, 4096):
    for a in ('0.3', '0.45', '0.49'):
        for c, cn in ((Fraction(1, 9), '1/9'), (Fraction(1, 4), '1/4')):
            r = point(log2k, a, Decimal(c.numerator) / Decimal(c.denominator))
            name = f'k=2^{log2k},a={a},c={cn}'
            check(r['scope_log2'] is not None, f'{name}: lambda > q/(400k^3)')
            check(r['lnE_over_lnq'] > 0.59, f'{name}: ln E below 0.59 ln q')
            check(r['bX_max'] < float(a) + 0.02, f'{name}: b_X bound {r["bX_max"]} far above a')
            check(r['bX_max'] > float(a) - 0.05, f'{name}: b_X bound below a (model error?)')
            check(r['margin_below_1_8'] > 0, f'{name}: ceiling not below 1/8')
            check(abs(r['ceiling_prop2_theta_0.01'] - 0.49 * r['bX_max'] / 2) < 1e-12, 'prop 2 ceiling')
            pts[name] = {kk: round(v, 4) for kk, v in r.items()}
OUT['propositions_at_template_points'] = pts
worst = max(v['ceiling_prop1_b_over_4'] for v in pts.values())
print(f'2. Propositions 1, 2 at {len(pts)} template points: lambda <= q/(400k^3) everywhere, '
      f'ln E/ln q >= {min(v["lnE_over_lnq"] for v in pts.values())}, '
      f'b and b_X within 0.02 of a; largest ceiling b/4 = {worst}, '
      f'smallest margin below 1/8 = {min(v["margin_below_1_8"] for v in pts.values())} '
      f'(a consequence of b_X <= a + 0.02 with a <= 0.49)')

# ------------------------------------------------------------ 3. hub inequality, exactly
hub = 0
for k in range(2, 13):
    for E in (2, 3, 5, 17, 100, 10 ** 4):
        thr = 1 - Decimal(E) ** (-Decimal(1) / k)                 # E(1-rho)^k < 1 iff rho > thr
        lnE = Decimal(E).ln()
        lower = lnE / (k + lnE)
        check(lower <= thr, f'hub: ln E/(k+ln E) above threshold at k={k}, E={E}')
        for num in range(1, 400):
            rho = Fraction(num, 400)
            holds = E * (1 - rho) ** k < 1
            check(holds == (Decimal(rho.numerator) / rho.denominator > thr), f'hub iff at {k},{E},{rho}')
            if holds:
                check(Decimal(rho.numerator) / rho.denominator > lower, 'hub: implied bound fails')
            hub += 1
# control: the 2k-1 block of A2(1) (E = k) gives only rho > ln k/(k + ln k), exponent -> 1
ctrl = float((Decimal(2) ** 739 + Decimal(739) * LN2).ln() / (Decimal(739) * LN2)
             - (Decimal(739) * LN2).ln() / (Decimal(739) * LN2))
check(ctrl > 0.98, 'control: the A2(1) block should only give b_X close to 1')
OUT['hub_cases'] = hub
OUT['control_A2_block_exponent'] = round(ctrl, 4)
print(f'3. hub inequality: {hub} exact cases; control, the block of A2(1) gives b_X <= {round(ctrl, 4)}')

# ------------------------------------------------------------ 4. ledger closed
readme = (HERE / 'README.md').read_text()
cited = set(n.split('/')[-1].split('ChaloupeMusic-')[-1].split('erwan-')[-1]
            for n in list(IN_TREE) + list(OUT_OF_TREE))
ledger = readme.split('## 4. The ledger of closed routes')[1].split('## 5.')[0]
named = set()
for line in ledger.splitlines():
    if line.startswith('|') and not line.startswith('|---') and not line.startswith('| route') \
            and not line.startswith('| step'):
        cells = [x.strip() for x in line.strip('|').split('|')]
        src = cells[-1]
        hits = [n for n in cited if f'`{n}`' in src or (n == 'keyed-local-lemma-and-large-moduli'
                                                       and '`keyed-local-lemma…`' in src)]
        here = 'here' in src
        check(hits or here, f'ledger row without a checked note: {cells[0]}')
        named.update(hits)
OUT['ledger_notes'] = sorted(named)
print(f'4. ledger: every row cites a checked note ({len(named)} distinct notes)')

# ------------------------------------------------------------ 5. provenance
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
    if '--manifest' in sys.argv and not FAIL:
        man.write_text(json.dumps({n: hashlib.sha256((HERE / n).read_bytes()).hexdigest()
                                   for n in FILES}, indent=2) + '\n')
elif not res.exists() or res.read_text() != out:
    check(False, 'RESULT.json differs from the computed summary')
if FAIL:
    print(f'{len(FAIL)} check(s) failed')
    raise SystemExit(1)
print('Test passé : all checks pass')
