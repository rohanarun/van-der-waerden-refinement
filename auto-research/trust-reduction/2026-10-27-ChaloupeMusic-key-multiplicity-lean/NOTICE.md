# Notice

Pinned sources: this repository at `84ed864` (PR #19). The package
formalizes Lemma 3 of `2026-10-26-ChaloupeMusic-source-only-1-16` with the
key of the OpenAI preprint `Quantitative-Superexponential-Bounds-for-van-der-
Waerden-Numbers-September-23-2026` (pinned in `source-manifest.json`), and
modifies no upstream file.

Toolchain: Lean 4.21.0 (`leanprover/lean4:v4.21.0`) and Mathlib v4.21.0
(`308445d7985027f538e281e18df29ca16ede2ba3`, as in `lean/lake-manifest.json`),
the versions of PR #10. The layout (`Axioms.lean`, `evidence/`,
`record-evidence.sh`) follows `key-measurable-lean` (PR #23).

Credits:
* The three-point identity in the last step of the proof is that of PR #10
  by rohanarun: `formal/Vdw/Geometry.lean`, `no_three_in_unit_band`, added
  in `815a4c0`, unchanged at the PR head `a46ef51`. Its Lean code is not
  copied: `three_point_left` and `three_point_right` restate the identity
  for vectors, one coordinate at a time.
* The separation and affinity arguments are the source's (§06, §05).
* The bound two is Lemma 3 of `source-only-1-16`. The source proves four.
* radar-89 validated the statement before the proof was written. It asked
  that the source line fixing `α`, `R` and `m` be cited, that PR #10 be
  credited, and that `lam_coprime` be stated on its own. The referee's cold
  objections (sprint 6, U4) asked for the source's own key rather than an
  abstraction, for mutants, and for the degenerate progressions to be
  excluded explicitly.

Review history: radar-89's contradicteur rebuilt the first draft from scratch
(same 57 constants, same axioms) and found nothing blocking. Applied:
* the bound is now exercised. The earlier toys never showed a key twice: on
  the exhaustive ones every term is alone in its box. Random short steps
  with `q > k²` now show a key twice, three terms in one box, and the bound
  `⌈k/2⌉` reached. The false explanation for `D = 2` is gone;
* the mesh (`α`, `m`) of each toy is in `RESULT.json`, so a mesh `k` times
  coarser no longer passes unnoticed. Coarser meshes are measured, and none
  breaks the conclusion; the README says that `k w < 1` is not shown to be
  necessary;
* the direct search of the mesh intervals is certified by a margin, with
  `a_m = 1/2` set exactly; before, the contact at `s = 0` rested on rounding
  noise;
* the bridge to `hm` of PR #23 is proved (`key_range_finite`, `hm_bridge`);
* nits: the converse `meshV_of_mem`; the limits of the audit's prefix
  filter are stated; `set_option` is linted; dead code and a wrong comment
  removed; the mesh line numbers corrected.

Departures from the validated statement, all weakenings of hypotheses:
* `mult_le_two` and `distinct_keys` no longer assume `e > 0`. `lemma3`
  keeps it, because it needs `α ≤ 1/2`.
* `meshV_width` no longer assumes `H > 0`.

AI assistance: the formalization, verifier and text were prepared with Claude
Opus 5.5 (Anthropic), in cooperating sessions. Not independently reviewed by
a human. `verify.py` uses only the Python standard library.
