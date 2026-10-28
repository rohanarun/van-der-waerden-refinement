# Notice

Pinned sources. This repository at `e302239` (PR #23), which carries
`one-eighth-barrier`, `keyed-local-lemma-and-large-moduli` and
`exact-door-one-condition`. Out of this tree, at the commits checked by
`verify.py --git`:

* PR #14 at `cd1de38`: `first-family-circularity`, `local-lemma-hub` and
  `single-label-obstructions`;
* PR #19 at `84ed864`: `source-only-1-16`;
* PR #21 at `98e6d36`: `rich-cover-barrier`.

The OpenAI manuscript *Quantitative Superexponential Bounds for van der
Waerden Numbers* is pinned in `source-manifest.json` (commit `fd4aeeb`).
Its sections `02-setup.tex`, `04-outer.tex` and `05-dichotomy.tex` are quoted, and
`verify.py --source <dir>` checks them against the manifest hashes.

External results, cited and not reproved: Rosser–Schoenfeld,
`θ(x) > x(1 − 1/ln x)` for `x ≥ 41` (Illinois J. Math. 6, 1962).

Credits. The question is piste U1 of sprint 6, coordinated by radar-89, and
taken from the scope of `one-eighth-barrier` and the referee's (o1)
(radar-cc). radar-89 asked for `r` to be kept as a parameter in Theorem 2, and for
the `o(1)` terms of Theorem 4 to be made explicit. `r` is a parameter, with
the better lower bound `(1 − 1/r)^k` for `r ≥ 3` found by U2's
contradictor. The `o(1)` terms are made explicit at eight values of `k`, on
a grid of `D` (checks 3 and 3b), not for every `k`. The contradictor of the
first draft found no blocking gap. Its points (the
hypotheses `D < h₀ < 2M < k`, the scope of the title, the threshold, the
grid, the verifier) are applied.

AI assistance. The text and verifier were prepared with Claude Opus 5.5
(Anthropic), in cooperating sessions. They have not been independently
reviewed by a human. Standard library only, and no upstream file is
modified.
