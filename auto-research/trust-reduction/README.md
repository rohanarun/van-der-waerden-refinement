# Trust reduction

Goal: shrink what each coefficient depends on. Every refinement in this
repository is conditional on correctness, not on a conjecture: it assumes the
OpenAI source's lemmas and adds arguments reviewed only by AI-assisted source
reviews. A contribution here proves an added link in full, or shows that a
coefficient does not need it.

Open questions:

- A Lean statement of the parameter transfer (the side-condition table).

Related tracks, in open PRs #13–#18: `independent-audit`, `short-period-sensitivity`.

## Index

| Date | Handle | Result | Status | PR |
|---|---|---|---|---|
| 2026-10-26 | ChaloupeMusic | every c < 1/16 (explicit 1/17) from the source's proofs alone, replayed; (O), (R), (P2) proved, (K) not used | research note | — |
| 2026-10-26 | ChaloupeMusic | every c < 1/8 (explicit 1/9) from the source's proofs alone, replayed; rich chain (K) of PRs #4, #6, #7 proved, repairs K1, K2 | research note | — |
| 2026-10-27 | ChaloupeMusic | [Lean: a key occurs at most twice on a progression](2026-10-27-ChaloupeMusic-key-multiplicity-lean/README.md) (Lean 4.21, Mathlib v4.21): Lemma 3 of `source-only-1-16` for the source's own key (adaptive mesh `V`, band `⌊‖qỹ‖²⌋`, dilation `λ`), no `sorry`, standard axioms only. On every progression `n₀ + jd`, `d ≠ 0`, `j < k`, of `ℤ/q^D` (`q = P^e`, `P > k` prime, `h₀ < P`), each key occurs at most twice, so there are at least `⌈k/2⌉` distinct keys; for every family of such progressions, the hypothesis `hm` of `key-measurable-lean` (PR #23) holds with `m = ⌈k/2⌉`, the key valued in its finite range (`hm_bridge`). The last step uses the three-point identity of PR #10. The existence of `P` is not formalized | formalization | — |
