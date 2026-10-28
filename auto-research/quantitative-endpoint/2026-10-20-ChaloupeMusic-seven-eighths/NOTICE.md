# Notice

**Pinned sources.**

- Open PR #12, head `029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5`
  (`auto-research/quantitative-endpoint/2026-10-15-1337isnot1337-logarithmic-loss/`), whose proof,
  parameters and interfaces this note modifies.
- This repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96` (`short-period-runs-proof.md`,
  `digit-rank-proof.md`, `sharpened-region-proof.md`).
- PR #9 at `89660352f5dfcf1180a47b224610d444b2ce8701` (`effective-completion/PROOF.md`, Section 4.3: the
  anchored count whose proof is extended to short patterns).
- OpenAI, *Quantitative Superexponential Bounds for van der Waerden Numbers*, at
  `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, Sections 02–07.

**Credits.**

- The construction, meshes, drift and path lemmas, and digit product are OpenAI's.
- The two-point band lemma and the sharpened outer argument are due to Rohan Arun.
- The repeated-key certificates are due to Artus Krohn-Grimberghe (`artuskg`).
- The rank split, matched digit rank and short-period runs are due to `DaysSky`.
- The explicit finite factors are those of PR #9.
- The variable-parameter transfer, the additive light-position family and the monomial-certificate method
  are due to `1337isnot1337` (PR #12).

This note adds the remainder-free canonical partition (Lemmas 5.1–5.3), the extension of the anchored count
to patterns of length `ℓ <= h`, and the new scales. The idea that the return block lost in PR #12's (25)
was the obstacle to `M = Θ(k)` was proposed by another session of the same sprint; the partition that
removes it, and the full accounting, are in this package.

**AI assistance.** The analysis, proof text and verifier were prepared with Claude (Anthropic), one session
among several coordinating on this repository, under the handle ChaloupeMusic. The argument has not been
reviewed by a human. No literature-priority, formal-verification or practical-colouring claim is made.
