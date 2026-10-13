# Partial formal verification of the van der Waerden PRs

Lean 4.21.0 checks **84 named theorems** in this package. They cover selected
universal lemmas, exact parameter regions, and all 42 recorded dyadic threshold
comparisons. **This is not a formal proof of the complete van der Waerden
construction or of any PR's headline lower bound.**

The local build, transitive axiom audit, and four rejection controls passed.
The portable results are in [evidence/verification.json](evidence/verification.json)
and [evidence/axioms.txt](evidence/axioms.txt). The GitHub workflow produces fresh
receipts separately; the checked-in local receipt is not evidence of remote CI.

For a source-review verdict conditional on the pinned OpenAI construction, see
[CONDITIONAL-REVIEW.md](CONDITIONAL-REVIEW.md). Its acceptance boundary differs
from the full-formal-proof boundary below.

## Exact scope by PR

Every source below is pinned in [SOURCES.json](SOURCES.json), with its full commit,
Git blob identity, SHA-256, and retained text. A later PR revision is not covered
until this manifest, translation, and proofs are reviewed and rerun.

| PR and pinned head | Kernel-checked obligations | Remaining outside the formal proof |
|---|---|---|
| [#1](https://github.com/rohanarun/van-der-waerden-refinement/pull/1), `22fa19e` | All four saved parameter tuples satisfy the original rational region. | Original construction, asymptotics, outer coloring, probability/counting bounds. |
| [#2](https://github.com/rohanarun/van-der-waerden-refinement/pull/2), `9a1de8d` | The `1/25` tuple; three samples separated by at least one cannot lie in a half-open unit band of a quadratic with leading coefficient at least one. | Reduction of geometric keys to that quadratic, sharpened dilation/outer argument and counting. |
| [#3](https://github.com/rohanarun/van-der-waerden-refinement/pull/3), `6caa55c` | `b<a` and `2a+b≤1` imply `b<1/3`; the conditional `1/24` ceiling; the floor-factor and finite weighted-sum bounds underlying the corrected dilation estimate. | Deriving the exponent hypotheses from asymptotics; identifying the prime product with the logarithmic sum; architectural obstruction commentary. |
| [#4](https://github.com/rohanarun/van-der-waerden-refinement/pull/4), `4b4e80e` | The literal `1/19` tuple and tau; repeated-position split; inconsistent-event rejection; the union assigned one certificate is covered by its all-flips event; quadratic pair identity and half-open convexity. | Common-return geometry, nested matching, literal certificate cardinality, product probability and imported outer dichotomy. |
| [#6](https://github.com/rohanarun/van-der-waerden-refinement/pull/6), `fc5738b` | The `1/16` tuple; carry-rank cost bound for every normalized rank, not just sampled breakpoints; the balanced cover-margin formula. | Geometric realization, rank-dependent encoding counts and probability estimates. |
| [#7](https://github.com/rohanarun/van-der-waerden-refinement/pull/7), `987c96c` | The `2/25` and `1/9` tuples; two-digit identity and balanced-coordinate bound for every dimension; return-digit bound; equality of linear forms extends to their span; matched cost identity and conditional `1/8` ceiling. | Association with actual modular carry data, full rank/cardinality estimates, single-run geometry, outer families and asymptotic bounds. |
| [#9](https://github.com/rohanarun/van-der-waerden-refinement/pull/9), `8966035` | Both literal tuples; all 21 recorded threshold comparisons for each route; the parameter family for every `0<c<1/8`; full digit-product obstruction for every nonzero interval step below `N^s`, assuming a valid cyclic coloring; existence outside a bad set with mass below one. | Analytic sufficiency and all-larger-input monotonicity of the threshold checklist, termination, full LLL proof, exact event enumeration/decision procedures, and existence of the cyclic coloring. |

PR #5 is closed and superseded by #6; its distinct historical head is not separately
certified. PR #8 adds research-process documentation and has no new mathematical
theorem to formalize. These are separate source revisions, not a test of a combined
merge of all branches.

## Proof files

- [Bounds.lean](Vdw/Bounds.lean): exponent/ceiling implications, floor bound,
  rich-cover split, rank costs, and PR9's entire parameter family.
- [Geometry.lean](Vdw/Geometry.lean): quadratic band obstruction, pair identity,
  and half-open interval convexity.
- [Covers.lean](Vdw/Covers.lean): literal event containment, general cover margins,
  and the finite weighted floor-sum bound.
- [Digits.lean](Vdw/Digits.lean): arbitrary-length digit recurrence, the exact
  two-leading-digit identity, balanced tails, return-digit bounds, and span recovery.
- [Runs.lean](Vdw/Runs.lean): separation of integer interval lifts, uniqueness
  of a lift along a small path, and consecutiveness within an affine interval.
- [Transfer.lean](Vdw/Transfer.lean): existence of a nonzero digit place, progression
  digit identity, cyclic-to-product non-monochromatic witness, and positive-mass existence.
- [Parameters.lean](Vdw/Parameters.lean), [Thresholds.lean](Vdw/Thresholds.lean):
  explicit source-derived rational propositions. The threshold proofs compare to
  small powers of two and use power monotonicity, so they do not allocate enormous integers.

The generic algebraic statements hold in every linearly ordered field, including
the reals. Exact recorded tuples and threshold comparisons use the rationals.
The digit recurrence is defined explicitly; equivalence with each source's modular
coordinate convention remains a translation obligation, not a silently assumed theorem.

## Reproduce

With the pinned Lean toolchain available:

```sh
cd formal
lake update
lake exe cache get
python3 -B verify.py
```

`verify.py` verifies retained source hashes, rejects stale generated propositions,
builds the library, prints and checks transitive dependencies of every listed
theorem, and runs four rejection controls. An optional `--git-sources` also compares
every snapshot with its exact Git object; the recorded commits must first be fetched.
The checked-in Lake manifest pins dependency commits; `lake update` installs them
for an initial setup, and any resulting manifest change should be reviewed.

`generate.py` reads JSON values and the displayed PR4 tuple from retained source
text. It emits explicit propositions, never a precomputed success boolean. Python
source association and the correspondence between mathematical prose and formal
definitions are outside Lean's kernel and remain reviewable trust boundaries.

No theorem uses a placeholder, custom axiom, or native decision shortcut. The audit
allows only the standard `propext`, `Classical.choice`, and `Quot.sound` axioms. It
rejects both former PR3 mistakes as false propositions, the strict endpoint claim,
and a changed source snapshot. This is proof checking by Lean, not an independently
implemented second kernel.

The CI setup uses the official [Lean action](https://github.com/leanprover/lean-action).
Disposable build products and current-run logs are ignored under `.lake/` and
`receipts/`. This package changes no contributor branch or original proof text.

## Attribution

The underlying construction belongs to the authors of the pinned OpenAI manuscript.
Rohan Arun's PRs provide the earlier refinements and barrier note; Artus
Krohn-Grimberghe (`artuskg`) contributed the repeated-key and effective-completion
proposals; `DaysSky` contributed the carry-rank, digit-rank and run proposals.
The snapshots preserve their more detailed attribution, including disclosed AI
assistance. This package adds an AI-assisted formalization and verification layer;
it does not claim mathematical discovery or priority.
