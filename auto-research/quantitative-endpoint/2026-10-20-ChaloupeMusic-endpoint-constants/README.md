# Retuned endpoint constants

This contribution keeps the construction of
[the logarithmic endpoint contribution](../2026-10-15-1337isnot1337-logarithmic-loss/README.md)
(PR #12, head `029431bb`) and changes its constants and four estimates. It proposes

```math
W_r(k)>\left(\frac{k^{1/8}}{e^{9/2}\log k}\right)^{k\lfloor\log_2 r\rfloor}
\qquad(k\ge2^{1024},\ r\ge2),
```

in place of `e^{20}`. It also gives the coefficient `1/9` for every
`k >= 2^1163`, in place of `2^4096`, and the coefficient `1093/10000` for
every `k >= 2^1024`, in place of about `0.0876`.

The statements are conditional on the same finite interfaces as PR #12. One
more imported input is used: the displayed form of two finite products in
PR #9. Independent mathematical review is pending.

## What changes

The second-order term `k log log k` and all functional forms are unchanged.
The gain comes from five lemmas, each independent of the scales `M`, `D`
and `p`:

- **A.** The dilation is bounded through `theta(x) < x log 4`, which gives
  `log lambda <= (1.39 + o(1)) h0` in place of `60 h0`.
- **B.** Local-lemma weights equal to the probability bound times `e^{1/8}`,
  so that each family keeps its full Hoeffding exponent.
- **C.** An asymmetric rich split that needs `Gamma >= (E_c + E_p)/2`
  instead of `Gamma >= max(E_c, E_p)`.
- **D.** Sharper arithmetic on PR #9's displayed products: `5^{k/2}` in
  place of `4^k`, and `37^k` in place of `256^k`.
- **E.** An s-light threshold `k/16` instead of `k/2`, so that the heavy-run
  case prescribes `15k/32` distinct keys instead of `k/4`.

Then `u = e^{t/2}/(4t^3)`, `h0 = ceil(5Dt^3)`, `p = 8t^4/sqrt(k)`,
`eps_reg = 1/(4t)` and `gamma = 1/2 - 25/(8t)`.

The binding rich inequality reads, in units of `k`,
`C > (1/2) log 370 + (1/4) log 8 + 25/32 = 4.258`. PR #12 paid `13.77` plus
slack at this point. Without Lemma D, using only PR #12's own Appendix A
table with exact coefficients, the rich inequalities hold with `C = 6`. The
verifier checks this as well, under `without_lemma_D`.

## Proof and verification

`PROOF.md` gives the five lemmas and the changed sections, which correspond
to Sections 3 to 10 of PR #12. From the repository root, run:

```sh
python3 -B auto-research/quantitative-endpoint/2026-10-20-ChaloupeMusic-endpoint-constants/verify.py
```

The verifier uses only the Python standard library and runs in under a
second.

- **Certificates.** It certifies 17 inequalities for every real
  `t >= 709`, not only sampled values. Fifteen are sums of terms
  `a t^j e^{-dt}`, nonincreasing on `[709, oo)`, bounded exactly at 709.
  The other two are `third_family`, a linear inequality whose margin grows
  with `t`, checked at 709, and `dichotomy`, an exact cubic identity in
  `1/t` with nonnegative leading coefficients. Logarithms are enclosed by
  atanh series.
- **Exact checks.** It checks the dichotomy identity, Lemma D's integer
  inequalities, Erdős's bound up to 20000 and the dilation identity.
- **Thresholds.** It checks the three thresholds and 768 generic
  coefficients.
- **Replay.** It replays the main inequalities from their definitions at
  eight values of `t`.
- **Negative controls.** Thirteen controls in all. Eight each change one
  constant (`C = 4.2`, `A_D = 3`, `A_p = 6`, `B_H = 9/2`, `g = 3`,
  `delta_s = 1/64`, `B_S = 1024`, `t0 = 300`) and require the corresponding
  certificate to fail. The other five check that PR #12's own class
  arithmetic cannot carry `C = 9/2`, that a term increasing on `[709, oo)` is
  refused, and that the coefficients `0`, `1/8` and `1/7` are refused.

`RESULT.json` is the output of `verify.py --json`. `MANIFEST.json`
authenticates the package files. It excludes itself.

These checks do not formally verify the local lemma or the imported
geometric and digit-rank encodings.

## Base and publication status

Base: `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, with PR #12 at
`029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5`. All changes are new files under
`auto-research/quantitative-endpoint/2026-10-20-ChaloupeMusic-endpoint-constants/`.
No PR is open for this package.

The track index `auto-research/quantitative-endpoint/README.md` is left
unchanged on purpose: PR #12's `MANIFEST.json` authenticates it, so editing it
would break PR #12's verifier. The proposed index entry, to add once the two
packages are merged in order, is:

```
2026-10-20, `ChaloupeMusic`: [Retuned endpoint constants](2026-10-20-ChaloupeMusic-endpoint-constants/README.md).
Status: conditional proof draft with exact all-larger-`t` checks, building on the 2026-10-15 contribution. Constant `e^{9/2}` in place of `e^{20}`, coefficient 1/9 from `k >= 2^1163`. Independent review is pending.
```
