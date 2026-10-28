# Conditional logarithmic endpoint bound

This contribution gives a variable-parameter proof of

```math
W_r(k)>\left(\frac{k^{1/8}}{e^{20}\log k}\right)^{k\lfloor\log_2 r\rfloor}
\qquad(k\ge2^{1024},\ r\ge2).
```

It also gives

```math
W_r(k)>k^{(k/9)\lfloor\log_2r\rfloor}
\qquad(k\ge2^{4096},\ r\ge2).
```

Both statements are conditional on the finite geometric and digit-rank interfaces stated in `PROOF.md`, Section 2.
Independent mathematical review is pending.

## What changes

The main repository admits each fixed `c < 1/8` with an unspecified threshold.
This contribution controls the error from 1/8 by `k log log k + 20k` in the two-color logarithmic bound.
A fixed-coefficient theorem alone does not supply this rate.

The new outer family balances light positions with an additive tolerance of `k/log k`.
An elementary prime-counting bound replaces `log(lambda) <= h_0 log(2M)` with `log(lambda) <= 60h_0` at the chosen scales.
Variable dimension and cutoffs make both estimates uniform in `k`.
The short-period family keeps a fixed tolerance, independent of the near-half tolerance for long blocks.

PR #9 gives `K=2^33554432` for its literal `c=1/9` tuple.
The new tuple varies with `k` and gives `K=2^4096` for the same coefficient.
The sufficient value of `log_2 K` decreases by a factor of 8192.
This comparison does not change the guarantee for PR #9's unchanged tuple.

For `Delta=1/8-c`, the generic threshold satisfies

```math
\log K(c)=O(\Delta^{-1}\log(1/\Delta)).
```

The leading coefficient does not exceed 1/8.
The logarithmic denominator does not disappear.
No practical coloring or runtime improvement is claimed.

## Proof and verification

Read `PROOF.md` for the complete new argument and its dependency boundary.
Read `SOURCES.json` for immutable source references.

From the repository root, run:

```sh
python3 -B auto-research/quantitative-endpoint/2026-10-15-1337isnot1337-logarithmic-loss/verify.py
```

The verifier uses only the Python standard library.
It verifies 14 exact monomial certificates for every real `t >= 512`, not only sampled values.
The analytic justification uses monotonicity and rational endpoint bounds for exponentials.
Additional finite checks cover 768 coefficients, 61,560 scalar denominators, weighted events, and rank-split accounting.
Nine negative controls reject invalid coefficients, missing monotonicity, and underpaid proof budgets.

`RESULT.json` contains the deterministic output.
`MANIFEST.json` authenticates the package files relative to the supplied manifest.
It excludes itself and includes the track index.
The manifest is not a signed provenance certificate.

These checks do not formally verify the imported geometric or digit-rank encodings.
The source programs are unchanged and were not rerun for this additive contribution.
The sources do not have an end-to-end human or formal verification claim.

## Base and publication status

Base: `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.
All changes are new files under `auto-research/quantitative-endpoint/`.
No existing top-level file or contributor source is changed.
The contribution is prepared as a reviewable patch. No PR is open for this package.
