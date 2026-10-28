# The 1/9 threshold: 2^940 proved, nothing in this chain between e^256 and 2^934

**Status:** conditional bound and a floor for this chain, with exact checks. Independent review is pending.

The retuned endpoint gives `W_r(k) > k^{(k/9)⌊log_2 r⌋}` from `k >= 2^950`. This note asks what fixes that
threshold, and answers with two bounds ([PROOF.md](PROOF.md)).

- **Theorem T.** Under the same interfaces (PR #12, Section 2, and PR #9's factors), the same chain gives
  `W_r(k) > k^{(k/9)⌊log_2 r⌋}` for every `k >= 2^940` under Lemma D″.
- **Theorem F.** Under the template (T1)-(T6) of `2026-10-26-ChaloupeMusic-template-limit/` alone, no
  parameter choice gives it for any `k` with `e^256 <= k <= 2^934`. This is a floor for this chain, not
  for every proof.

| class product | retuned endpoint | Theorem T | Theorem F (no template proof up to) |
|---|---:|---:|---:|
| D″, `45^{k/2}` | `2^950` | `2^940` | `2^934` |
| D′, `19^k` | `2^1009` | `2^1000` | `2^994` |
| D, `37^k` | `2^1048` | `2^1038` | `2^1032` |

## What fixes the threshold

Not `C` alone. The threshold is where the rich inequality first holds with `F = kt/9`. Its left side is
`t/72 − (7/8) log t` against four constants: `2.103` from `2^k`, `5^{k/2}` and the class product, `0.502`
from the two tolerances, `log A_p / 4 = 0.811` from the flip rate, and `+0.040` of positive terms that the
retuned endpoint drops to keep a constant uniform in `t`. Each `0.01` of constant is worth about `1.15` in
the exponent of `2^n`.

Three changes give `2^940`:

- prove `F = kt/9` directly, instead of the form `k^{k/8}/(e^C (log k)^{7/8})` with a constant `C`;
- keep the two positive terms of the exact identity for `γL/2`;
- retune for `t >= 651`: `B_h = 4.51`, `A_D = 18.05`, `A_p = 25.68` (case (ii) reads `6A_D/9` once
  `F = kt/9`, where the retuned endpoint had `6A_D/8`).

The gap of six to the floor is mostly two constraints that (T1)-(T6) do not contain (approximate
attributions, not claims): `h_0 <= sqrt(kt)/4`,
which forces `A_D > 4B_h` (about `2.7` in the exponent), and `δ_s = 1/16` in case (ii) (about `1.9`).

## Reproduce

From the repository root:

```sh
python3 -B auto-research/quantitative-endpoint/2026-10-27-ChaloupeMusic-one-ninth-threshold/verify.py
```

Expected: exit code 0; standard output is `RESULT.json` followed by `Test passé` (standard library only,
about six minutes). The verifier checks:

- every monomial certificate of the retuned endpoint, re-certified at `T_0 = 651`;
- every budget in exact rationals, and the rich inequality on a cover of `[N_0 log 2, ∞)`, for each tier;
- that `N_0 − 1` fails, so the certificate goes no lower;
- the floor of Theorem F in exact arithmetic (`plancher.py`, certified logarithms in `logs.py`), and that
  its bound turns positive at the next power of two;
- negative controls, among them `A_D = 18.03`, `B_h = 4.505`, `A_p = 25.66`, case (ii) with `6A_D/8`, the
  kept terms dropped, `G = 2.1`, and the floor pushed to `2^935`;
- a 90-digit decimal replay of the sixteen inequalities with `F = kt/9` (a control, not a proof);
- file integrity against `MANIFEST.json`.
