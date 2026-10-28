# Seven-eighths logarithmic loss at the conditional 1/8 endpoint

**Status:** conditional bound with exact checks. It builds on open PR #12 and depends on it.
Independent review is pending.

This contribution modifies the variable-parameter proof of PR #12
(`2026-10-15-1337isnot1337-logarithmic-loss/`, head `029431bb`) and proves

```math
W_r(k)>\left(\frac{k^{1/8}}{e^{35/2}(\log k)^{7/8}}\right)^{k\lfloor\log_2 r\rfloor}
\qquad(k\ge2^{739},\ r\ge2),
```

and `W_r(k) > k^{(k/9)⌊log_2 r⌋}` for `k >= 2^2504`. Both are conditional on the finite source interfaces
that PR #12 states in its Section 2.

| | PR #12 | this note |
|---|---|---|
| second-order loss in `log W_2(k)` | `k log log k + 20k` | `(7/8) k log log k + (35/2) k` |
| range | `k >= 2^1024` | `k >= 2^739` |
| threshold for `c = 1/9` | `2^4096` | `2^2504` |

For every `k >= 2^1024` the new base is larger than PR #12's by the factor `e^{5/2}(log k)^{1/8}`. No
coefficient above `1/8` is claimed.

## What changes

PR #12 partitions a long-period progression into full blocks of the closest-return length `h` plus a
remainder of fewer than `h` positions. The heavy positions of the remainder are lost, which costs `h <= 2M`
positions in the dichotomy (its equation (25)). This forces `M <= k/t`, and through the first local-lemma
family it forces `D ∝ sqrt(k)/t^3` and `p ∝ t^4/sqrt(k)`.

Here the progression is cut **without remainder** into `⌈k/h⌉` consecutive blocks with lengths in
`[h/2, h]` (Lemma 5.1). The partition depends only on `h` and `k`, so it is a function of the label word.

- Blocks of length at most `h` still have pairwise distinct labels.
- The source's eligibility argument goes through sentence by sentence (Lemma 5.3).
- The nonregular fraction rises from `4η + 1/s_i` to at most `12η + 3/h_0` (Lemma 5.2).
- The second family is extended to patterns of every length `ℓ ∈ [h/2, h]`, at a factor `h` in its count.

The dichotomy then loses nothing to the return block, so `M = ⌊k/32⌋`. As a result `D ∝ sqrt(k)/t^{5/2}`,
`p = 16384 t^{7/2}/sqrt(k)`, and the coefficient of `k log log k` drops from `4/4` to `3.5/4`. The new
parameters, and every inequality of PR #12's Sections 4 to 10 at those scales, are in
[PROOF.md](PROOF.md).

The constants are deliberately those of PR #12 where possible: `log λ <= 60 h_0`,
`E = 10k + 100Dt + 6 log q`, weights `e^{-w}`. Sharper constants for the same families (a concurrent
track) compose with this architecture and are not used here.

## Reproduce

From the repository root:

```sh
python3 -B auto-research/quantitative-endpoint/2026-10-20-ChaloupeMusic-seven-eighths/verify.py
```

Expected: exit code 0, and standard output byte-identical to `RESULT.json` (under a second, standard
library only). The verifier checks:

- 17 monomial certificates `A t^j e^{-dt} <= B`, valid for every real `t >= 512`;
- every constant budget, in exact rationals, with certified rational bounds for `log 2` and `log 1735`;
- Lemma 5.1, exhaustively for `k <= 400`, and the counting core of Lemma 5.2, exhaustively for periods
  up to 16;
- a 90-digit replay of the main inequalities on a grid of `t`;
- the hashes of the package files.

Negative controls rejected by `verify.py`:

- full blocks plus a remainder with `M = ⌊k/32⌋` (the dichotomy fails);
- `M = ⌊k/t⌋` with the new `D` (the first family fails);
- `4096 → 2048` in `u`;
- `16384 → 8192` in `p`;
- `C = 14`;
- `θ = 3/4`;
- a block shorter than `h/2` whose grid values all lie within `2η` of the cut (the quantity Lemma 5.2
  bounds);
- a monomial claimed from `t_0 = 30`.

Mutation tests, run by hand on a copy whose `MANIFEST.json` was regenerated. With the delivered
manifest, any edit of `verify.py` fails first on its own hash. Each constant enters `verify.py` only
through the inequalities it serves, and γ through the single constant `G` (`γ = 1/2 − G/t`).

| Mutation | Inequality that fails |
|---|---|
| `AD = 2048` | `h_0 <= sqrt(kt)/7` |
| `AD = 4000` | first-family budget |
| `AH = 64` | second-family budget |
| `AS = 1024` | third-family budget |
| `AP = 8192` | few-s-light budget |
| `G = 2` | dichotomy `A_0 − 1/t > γ` |
| `C = 17` | rich budget `Γ >= 14k` |
| `T0 = 256` | `F >= kt/32` |
| `T0 = 500` | crude many-s-light bound `t/64 − 2 >= 6` |

`C = 69/4` still passes, as it should: the rich budget only needs
`C >= 14 + 3/100 + (log AP)/4 + G/4 ≈ 17.21`.

## Track index

The track README (`auto-research/quantitative-endpoint/README.md`) is not edited. PR #12's `MANIFEST.json`
pins its hash, so appending a line would make PR #12's `verify.py` fail. Once PR #12 is merged and its
manifest no longer covers the index, the proposed line is:

```
2026-10-20, `ChaloupeMusic`: [Seven-eighths logarithmic loss](2026-10-20-ChaloupeMusic-seven-eighths/README.md).
Status: conditional bound with exact checks, built on the 2026-10-15 contribution. Independent review is pending.
```

## Scope

- The interfaces imported by PR #12 (finite geometry, word counts, digit-rank encodings of PR #9, affine
  key words) are imported here unchanged. Two of them are re-derived in an extended form, in Section 2 of
  PROOF.md: the truncation constant `B_0` for `η = 1/(24Dt)`, and the anchored count for patterns of
  length `ℓ <= h`.
- The local lemma, Hoeffding's inequality and PR #9's encodings are not formalized.
- Finite checks corroborate the proof and are not its premises.
- No practical colouring, finite record or runtime improvement is claimed.
