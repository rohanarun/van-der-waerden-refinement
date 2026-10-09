# Conditional refinements of OpenAI's October 2026 math release

This research draft proposes a stronger coefficient in the released van der Waerden lower bound, together with an elementary geometric lemma and a parameter-transfer argument. It also gives an abstract obstruction for a selected set of matrix-multiplication profile inequalities.

**Status:** AI-generated mathematical research prepared with Codex. The main refinement is conditional on the upstream geometric and counting arguments; it has not received independent mathematical review or formal verification. This repository does not claim a verified world record or a new matrix-multiplication algorithm. It is an independent follow-up, not an official OpenAI publication.

Read the full argument in **[research-note.tex](research-note.tex)**. Exact checks, parameter choices, and experimental records are included below.

## Main proposed refinement

The original manuscript establishes a bound of the form

```math
W_r(k)>k^{c k\lfloor\log_2 r\rfloor}
```

with $c=1/100000$, for sufficiently large $k$ and every integer $r\ge2$. Our conditional parameter-transfer argument admits **$c=1/200$**, with the threshold independent of $r$.

That is a **500-fold increase in the coefficient inside the exponent**. It is not a 500-fold increase in a finite van der Waerden number, an explicit finite coloring record, or a runtime improvement. The threshold may be very large and is not made explicit here.

### Why the argument changes

The source bounds the multiplicity of a geometric key by four. Its affinity and separation properties place points of one key on an affine real line, at mutual distances at least one, with squared norms in a half-open interval $[m,m+1)$.

In fact there are at most **two** such points. Parameterize the line by signed arclength $t$ from its nearest point to the origin, so squared norm is $t^2+C$. Among three parameters, two lie on the same half-line. Their absolute values satisfy $v-u\ge1$, hence

```math
v^2-u^2=(v-u)(v+u)\ge1,
```

contradicting membership in a common half-open interval of width one. This elementary lemma is proved directly; applying it to the original construction still requires the source's hypotheses.

Using this multiplicity bound, write $D=\lceil k^a\rceil$, $M=\lceil k^m\rceil$, and $p=k^{-b}$. The note derives the sufficient region

```math
a,b,c>0,\quad 3a<m<1,\quad b<a,\quad 3a<1-b,
```

```math
0<\delta<1,\quad 0<\gamma\le\delta/4,\quad \gamma<(1-\delta)/8,\quad 2c<\gamma b/2.
```

| Choice | $a$ | $m$ | $b$ | $\delta$ | $\gamma$ | $c$ | Coefficient ratio |
|---|---|---|---|---|---|---|---|
| Original dimension scales | 1/10 | 1/2 | 1/20 | 1/10 | 1/40 | 1/4000 | 25 |
| Retuned parameters | 1/5 | 3/4 | 1/6 | 1/10 | 1/40 | 1/1000 | 100 |
| Main proposed choice | 1/4 | 4/5 | 247/1000 | 1/3 | 41/500 | 1/200 | 500 |

For the last row, $\gamma b/2-2c=127/1000000$ and both affine entropy power gaps equal $3/1000$. These strict margins are checked with exact rational arithmetic in [parameters.json](parameters.json) and [audit_math.py](audit_math.py).

The same sufficient region admits every fixed positive $c<1/192$. The endpoint is not asserted, and this is only a supremum within the retained estimates. The full transfer proof and its dependencies are in the note; passing the scripts does not establish that transfer as a theorem.

## Original work and attribution

All comparisons refer to **OpenAI's manuscripts at commit [`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb)**, not to a claim about the latest literature.

- OpenAI, [*Quantitative Superexponential Bounds for van der Waerden Numbers*](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026), September 23, 2026. This is the original construction on which the main refinement depends.
- OpenAI, [*An Upper Bound of 9/4 for the Matrix Multiplication Exponent*](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026), October 2, 2026. Source of the profile constraints considered here.
- OpenAI, [*A counterexample to Sidorenko's conjecture*](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026), September 23, 2026. Source of the finite certificate reproduced for exploratory searches.
- OpenAI, [*A power saving for planar unit distances*](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-power-saving-for-planar-unit-distances-September-23-2026), September 23, 2026. Inspected for possible quantitative improvements; none is claimed.

The original authors retain credit for their constructions, lemmas, and results. The finite Sidorenko baseline is derived from the original manuscript. [source-manifest.json](source-manifest.json) records the pinned revision and SHA-256 hashes of the inspected source files. Upstream source trees are not bundled; the fetch command below retrieves and verifies them from the original repository. Citation entries supplied by the authors are available in the linked original directories.

## Companion result and unsuccessful searches

For the selected scalar matrix-profile constraints, let $u=\min(a,b)$ and $v=\max(a,b)$. The explicit profile

```math
P_*(a,b)=\left(\frac{3u-1}{2}\right)^{1/3}\left(v+\frac{u-1}{2}\right)
```

is symmetric, positive, nondecreasing, and separately concave, with $P_*(1,b)=b$. It satisfies shifted tripling and the rank envelope at $t=3/4$, while its diagonal grows as $\Theta(a^{4/3})$. Thus those listed constraints alone cannot exclude $t=3/4$. **This is not an actual tensor character or a lower bound on the matrix-multiplication exponent.** The note gives an analytic proof; finite LP experiments are exploratory.

The Sidorenko search found **no smaller certificate**: 56,984 labeled candidates in the contraction/flip run, and 28,281 in the weighted-cut run, of which 2,518 passed the discrete and degree screen. These nonexhaustive searches may overlap and include isomorphic duplicates. Floating-point LP failures are not infeasibility certificates. The original 35-vertex, 66-edge finite certificate passes the independent combinatorial checker; this does not verify the full analytic counterexample proof.

No improved unit-distance exponent was obtained.

## Reproduce the checks

Use Python 3.11 or 3.12 in a local checkout:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -B audit_math.py
python -B check_complex.py experiments/complex-contractions/baseline.json --output experiments/baseline-independent-check.json
```

Do not run with `-O` or `PYTHONOPTIMIZE`: the verification scripts use assertions. GitHub Actions runs these same checks on pushes and pull requests.

| Check | Evidence | Limitation |
|---|---|---|
| Three parameter proposals | Exact rational margins; three invalid boundary controls rejected | Validates inequalities, not the imported lemmas |
| Norm-band lemma | Displayed proof plus 26,180 finite rational cases | Finite cases supplement the proof |
| Abstract matrix profile | Symbolic identities plus 10,000 exact cube comparisons | No tensor realizability claim |
| Released Sidorenko baseline | Independent reconstruction; duplicate-face and incomplete-exposure controls rejected | Finite combinatorial hypotheses only |

Saved outputs are [exact-audit.json](experiments/exact-audit.json) and [baseline-independent-check.json](experiments/baseline-independent-check.json). The LaTeX source was successfully compiled in the Codex document editor; no compiled PDF is included.

To retrieve the exact upstream source files (optional for the checks above):

```sh
python -B fetch_sources.py --output upstream
```

Exploratory scripts provide `--help`: [search_complex.py](search_complex.py), [weighted_cuts.py](weighted_cuts.py), and [profile_lp.py](profile_lp.py). Searches require explicit seeds, time budgets, and output paths. Their wall-clock-limited candidate counts are machine-dependent; historical summaries are retained under [experiments](experiments/). Use a new output directory when rerunning a search to preserve those records.

## What still needs review

The main outstanding work is independent verification of the complete van der Waerden parameter transfer, including uniform constants and all imported hypotheses. Literature priority has not been established. For matrix multiplication, progress requires additional valid tensor constraints or a different construction. Any smaller Sidorenko finite object would still need the full analytic transfer before it could be called a new counterexample.
