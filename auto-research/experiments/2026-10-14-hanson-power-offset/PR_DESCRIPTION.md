The repository gives one abstract matrix profile with diagonal exponent 4/3. This research note characterizes a two-parameter power-and-offset deformation: separate discrete concavity and shifted tripling hold exactly when `0 <= lambda <= 1/2` and `s = (1-lambda)/(1+lambda)`. The resulting diagonal exponent is `2/(1+lambda)`, so its unique minimum is the existing profile's 4/3. This is a scoped no-gain result and a continuum of admissible scalar profiles.

All additions are under the existing `auto-research/experiments/` track. The note includes the necessity and sufficiency proofs, pinned sources, exact verifier, four concrete negative controls, attribution, AI-assistance disclosure, and handoff. It makes no tensor-realizability, new matrix algorithm, vdW coefficient, formal-proof, human-review, or literature-priority claim.

Validation: the standard-library verifier checks 2,160 concavity stencils, 2,304 tripling and envelope cases each, and 10,000 predecessor-profile pairs. A separate SymPy check confirms six proof identities. Both existing repository baseline commands pass and reproduce their saved artifacts byte for byte; the local environment's NumPy/SciPy versions differ from the repository pins, as disclosed in the receipt.

Base: `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`. Structural-track assignment seed: 46. Open PRs #9 and #10 and the conditional-review ledger were inspected for overlap; no coordination issue exists in the current issue list. Substantial Codex assistance is disclosed in `NOTICE.md`.

Reproduce from the repository root:

```sh
python3 -B auto-research/experiments/2026-10-14-hanson-power-offset/verify.py
```
