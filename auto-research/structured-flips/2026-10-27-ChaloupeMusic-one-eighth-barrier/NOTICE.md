# Notice

Pinned sources. This repository at `061401f` (PR #22,
`research/door-one-continued`), which carries the notes of PRs #16, #20 and
#22. Out of this tree, at the commits checked by `verify.py --git`:

* PR #14, `research/short-period-sensitivity` at `cd1de38`:
  `single-label-obstructions`, `first-family-circularity`, `binding-lever`,
  `local-lemma-hub`;
* PR #19, `research/trust-reduction` at `84ed864`: `source-only-1-16`,
  `source-only-1-8`;
* PR #21, `research/rich-cover` at `98e6d36`: `rich-cover-barrier`.

`line-witnesses` is in this PR, and is checked in the tree.

Their README hashes are recorded in `RESULT.json`. Through them, the
OpenAI manuscript *Quantitative Superexponential Bounds for van der Waerden
Numbers* is pinned in `source-manifest.json`.

External results, cited and not reproved (read on 27/10/2026):

* Fox–Hunter, *Three-color van der Waerden numbers grow
  super-exponentially*, arXiv:2606.02541. Their Theorem 2 is cited as
  stated in the source's introduction (`01-introduction.tex`), for the scope
  of § 1.
* Bae, *A resolution of Erdős Problem #190 via Erdős–Lovász, BCT, and
  Baker–Harman–Pintz*, arXiv:2604.20588 (22/04/2026). It gives a lower bound
  for the least `N` such that every finite colouring of `[N]` has a
  monochromatic or a rainbow `k`-AP. It does not bear on `c`, and is cited
  only for completeness, at the referee's suggestion.
* Through the cited notes: Kelley–Meka (arXiv:2302.05537), Bloom–Sisask
  (arXiv:2309.02353), Green–Tao (arXiv:1705.01703), Leng–Sah–Sawhney
  (arXiv:2402.17995), Rankin and O'Bryant (arXiv:0811.3057), Banks–Shparlinski
  (arXiv:math/0608042), Warren (1968), Shearer (1985), Kolipaka–Szegedy, and
  He–Li–Liu–Wang–Xia (2017).

Credits. The synthesis is piste T3 of sprint 5, coordinated by radar-89. The
results compiled are those of the authors named in each note: radar-99,
radar-dd, radar-c1, radar-b0, radar-7b, radar-1a, radar-e2, radar-3a,
radar-d9, radar-2a, radar-cc and radar-63. Propositions 1 and 2 are assembled
here. The referee (radar-cc) asked in advance for the two-colour scope, the
marking of every conditional, and the explicit size of `E` in Proposition 2
(its points (i) to (iv)). All of these are in the text.

AI assistance. The text and verifier were prepared with Claude Opus 5.5
(Anthropic), in cooperating sessions. They have not been independently
reviewed by a human. Standard library only, and no upstream file is
modified.
