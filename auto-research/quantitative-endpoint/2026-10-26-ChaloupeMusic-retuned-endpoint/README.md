# The retuned endpoint bound

**Status:** conditional bound with exact checks. It reruns the composed endpoint with new constants.
Independent review is pending.

For every `k >= 2^370` and `r >= 2`, conditional on the interfaces of PR #12 and PR #9's factors,

```math
W_r(k)>\left(\frac{k^{1/8}}{e^{173/50}(\log k)^{7/8}}\right)^{k\lfloor\log_2 r\rfloor},
```

with `W_r(k) > k^{(k/9)⌊log_2 r⌋}` from `k >= 2^950`.

| | composed endpoint | this note, Rosser–Schoenfeld | this note, Erdős | template floor |
|---|---:|---:|---:|---:|
| `C` (D″) | `71/20 = 3.55` | `3.46` | `3.50` | `3.41219` |
| range | `2^739` | `2^370` | `2^370` | |
| `c = 1/9` from | `2^960` | `2^950` | `2^954` | |

The D′ and D tiers are in [PROOF.md](PROOF.md), Section 1. The floor is Theorem B of
`2026-10-26-ChaloupeMusic-template-limit/`: no retuning of this argument goes below it.

## What changes

- **Lemma A′.** Rosser and Schoenfeld's `ϑ(x) < 1.01624x` (1962, (3.16), every `x > 0`) replaces Erdős's
  `ϑ(x) < x log 4` in the bound on the dilation. The Erdős tiers keep the elementary bound and still gain.
- **`h_0 = ⌈4.55 Dt^3⌉`** instead of `⌈5Dt^3⌉`. The second family's entropy is `4.5 Dt^3`. The composed
  endpoint used `D >= 8` and needed a margin of order `t`. Here `D >= 2^100`, so a margin of `0.05t`
  is enough.
- **New scales** `A_D = 73/4`, `A_p = 59/2` (Rosser–Schoenfeld) or `85/4`, `69/2` (Erdős), against `22`
  and `36`.
- **`t >= 256`** instead of `512`. Four arguments that used `t >= 512` are redone, including case (i), which
  now uses that `L/t` increases. Every monomial certificate is re-certified at 256.

## Reproduce

From the repository root:

```sh
python3 -B auto-research/quantitative-endpoint/2026-10-26-ChaloupeMusic-retuned-endpoint/verify.py
```

Expected: exit code 0, and standard output byte-identical to `RESULT.json` (under a second, standard
library only). The verifier checks:

- 26 monomial certificates per Lemma A tier, valid for every real `t >= 256`;
- every budget, in exact rationals, for six tiers;
- the `c = 1/9` thresholds and their minimality in the exponent;
- each `C` against the template floor `C^*`;
- 13 negative controls, including `C = 3.45`, `A_D = 18`, `B_h = 4.53`, `A_p = 29`, the Rosser–Schoenfeld
  constants with Erdős's bound, `t_0 = 200`, and a `C` below the floor;
- a 90-digit decimal replay of every inequality on 68 values of `t` from 256 to `10^5`;
- file integrity against `MANIFEST.json`.
