# Notice

Pinned sources:

- this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`
  (`rank-certificate-proof.md`, `digit-rank-proof.md`,
  `short-period-runs-proof.md`);
- PR #4 at `4b4e80ea5e0ffec956577004905f22659af0bff5`
  (`repeated-key-certificate-proof.md`), as restated in
  `rank-certificate-proof.md`, Section 1;
- the companion note `../2026-10-26-ChaloupeMusic-source-only-1-16/`
  (commit `f5a6858` on this branch), for the parameters, outer coloring,
  dichotomy and non-rich estimate;
- OpenAI, *Quantitative Superexponential Bounds for van der Waerden Numbers*,
  `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, Sections 02 to 07,
  with the SHA-256 listed in the companion note's NOTICE.

Credits: the construction and every lemma quoted from it are OpenAI's. The
repeated-key facts (common return, affine collision classes, vertex
constraint) and the certificate idea are Artus Krohn-Grimberghe's (`artuskg`,
PR #4, initial argument attributed there to GPT-6 Pro). The carry and digit
ranks, Lemmas A\* and C\* and the rank split are `DaysSky`'s (PRs #6, #7).
What is new here is the complete re-derivation at the source's level, two
repairs (K1, K2), and the combination with the companion note into one proof
from the source alone.

AI assistance: the proof write-up, the verifier and this text were prepared
with Claude (Anthropic), one session among several Claude sessions working on
this repository. Not reviewed by a human.
