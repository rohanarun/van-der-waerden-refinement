# Notice

Pinned sources:

- this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`: `research-note.tex` (section
  "An obstruction for the matrix profile inequalities"), `profile_lp.py` and
  `experiments/matrix-profile.json`, whose sha256 `verify.py` checks;
- OpenAI, *An Upper Bound of 9/4 for the Matrix Multiplication Exponent* (October 2, 2026), at
  `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`,
  `preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/build/paper.tex`, sha256
  `c396f2580a711b8b9e51ecf1265cb0e691acd745943f81bfc14ec0df209e1028` (as listed in
  `source-manifest.json`): equations (2.3), (4.3), (4.5), (4.7), Lemmas 2.3, 4.1, 4.2, 5.1,
  Proposition 3.1 and Corollary 3.2;
- PR #11 (`bbMisk:research/seed46-profile-family`, open) at
  `9c1f70f36e76eea7d152cede159185548950f694`, read to rule out overlap;
- the reference value of `3/(2 Gamma(4/3))` used as an independent check of the constant's
  bracket, computed with mpmath 1.3.0 at 60 digits from `Gamma(1/3) =
  2.6789385347077476336556929409746776441286893779573...`.

Credits: the profile constraints and the tensor constructions they come from are OpenAI's. The
profile `P_*` and the obstruction theorem are in the repository's `research-note.tex` (Rohan
Arun, prepared with Codex). The power-and-offset family is PR #11's (Hanson Sun with Codex,
`bbMisk`). Their own AI-assistance disclosures apply to their work. The example in
Corollary 3 showing that a larger diagonal exponent is not necessary, and the request for an
independent check of the constant, come from the sprint's referee, another Claude session that
reviewed this package.

AI assistance: this note, its proofs, its verifier and its text were prepared with Claude
(Anthropic), one session among several Claude sessions coordinating on this repository, and
submitted under the handle `ChaloupeMusic`. It has not been reviewed by a human.
