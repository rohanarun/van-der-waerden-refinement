# Composed endpoint bound: seven-eighths loss with retuned constants

**Status:** conditional bound with exact checks. It combines two contributions built on open PR #12 and
depends on them. Independent review is pending.

```math
W_r(k)>\left(\frac{k^{1/8}}{e^{C}(\log k)^{7/8}}\right)^{k\lfloor\log_2 r\rfloor}
\qquad(k\ge2^{739},\ r\ge2).
```

The bound is conditional on PR #12's Section 2 interfaces and on PR #9's displayed finite factors. The
constant `C` comes in three tiers, according to the bound used for one product of PR #9 (Section 8.3,
step 4). Each tier is proved and certified separately:

| tier | assumption | `C` | `c = 1/9` from | coefficient at `2^1024` |
|---|---|---:|---|---:|
| D″ | Lemma D″: collision classes have at least two positions, so the product is `<= 45^{k/2}` | `71/20` | `2^960` | `> 0.1119` |
| D′ | Lemma D′ alone: `<= 19^k` | `403/100` | `2^1015` | `> 0.1112` |
| D | N1a's Lemma D alone: `<= 37^k` | `35/8` | `2^1054` | `> 0.1107` |

Comparison with the earlier bounds on `W_2(k)^{1/k}`:

| | bound | from | `c = 1/9` from |
|---|---|---|---|
| PR #12 | `k^{1/8} / (e^{20} log k)` | `2^1024` | `2^4096` |
| `2026-10-20-ChaloupeMusic-endpoint-constants` (N1a) | `k^{1/8} / (e^{9/2} log k)` | `2^1024` | `2^1163` |
| `2026-10-20-ChaloupeMusic-seven-eighths` (N1b) | `k^{1/8} / (e^{35/2} (log k)^{7/8})` | `2^739` | `2^2504` |
| this note, tier D″ | `k^{1/8} / (e^{71/20} (log k)^{7/8})` | `2^739` | `2^960` |

Every tier beats every earlier bound on that bound's own range, even before the `(log k)^{1/8}` factor.
No coefficient above `1/8` is claimed.

## What is combined

- **N1b's architecture.** A remainder-free canonical partition of long-period progressions into blocks of
  lengths in `[h/2, h]`. With it, `M = ⌊k/32⌋`, `D ∝ sqrt(k)/t^{5/2}` and `p ∝ t^{7/2}/sqrt(k)`.
- **N1a's five scale-free lemmas**, restated in [PROOF.md](PROOF.md), Section 2: the dilation bound (A),
  local-lemma weights `Pbar·e^{1/8}` (B), the asymmetric rich split (C), PR #9's products in `5^{k/2}` and
  `37^k` (D), and the s-light threshold `k/16` (E).
- **Two new arithmetic lemmas on PR #9's class product.**
  - D′ uses each class's own length `K_a`, with `K_h <= K_a + 1`, and gives `19^k`.
  - D″ adds that the classes counted in Section 8.3 are collision classes, which hold a repeated key and so
    have `K_a >= 2`, and gives `45^{k/2}`. The reading of PR #9 behind it is written out line by line in
    PROOF.md, Section 2.
- **Eligibility threshold.** The anchored patterns of N1b's (I2) are asked to have at least
  `(1 − ε_reg)ℓ` regular positions instead of `ℓ/2`. Canonical blocks satisfy this by N1b's Lemma 5.2.
  It doubles the second-family tail exponent, from `h/(2t^2)` to `(1 − ε_reg)h/t^2`, so `h_0 = ⌈5Dt^3⌉`
  suffices.

## Reproduce

From the repository root:

```sh
python3 -B auto-research/quantitative-endpoint/2026-10-20-ChaloupeMusic-composed-endpoint/verify.py
```

Expected: exit code 0, and standard output byte-identical to `RESULT.json` (about a second, standard
library only). The verifier checks:

- 26 monomial certificates, valid for every real `t >= 512`;
- every budget of PROOF.md in exact rationals, with certified logarithm bounds, separately for each tier;
- the three class-product bounds, for every `k <= 300` and `h < k`. A control shows that D″ needs
  `K_a >= 2`.
- the canonical partition and the counting core of the short-block lemma;
- a 90-digit replay of 15 inequalities at 44 values of `t` for the three tiers;
- the hashes of the package files.

`budgets()` takes the constants as parameters, and the negative controls feed each change back into it.
`verify.py` requires each of these to fail:

- `AD = 21`, `BH = 4`, `AS = 1024`, `AP = 35`, and `AP = 37` under D′;
- `C = 7/2` under D″, `C = 4.02` under D′, and `C = 4.35` under D;
- `19^k` at `C = 71/20`, and `37^k` at `C = 403/100` (each lemma is load-bearing for its tier);
- N1b's `ℓ/2` eligibility threshold;
- `G = 2`, and `ε_reg = 1/(2t)`;
- a monomial claimed from `t_0 = 30`.

It also requires the delivered constants to pass in all three tiers.

## Track index

The track README is not edited, because PR #12's `MANIFEST.json` pins it. The proposed line is:

```
2026-10-20, `ChaloupeMusic`: [Composed endpoint bound](2026-10-20-ChaloupeMusic-composed-endpoint/README.md).
Status: conditional bound with exact checks, combining the two 2026-10-20 contributions. Independent review is pending.
```

## Scope

- Imported, as stated by their authors: N1b's Lemmas 5.1–5.3 and its interface extensions (I1)–(I2),
  N1a's Lemmas A–E, PR #12's Section 2 interfaces and Family 3, and PR #9's displayed factors.
- Lemmas D′ and D″, like N1a's Lemma D, re-bound a displayed product of PR #9. They do not re-derive the
  encoding that produces it. D″ also depends on the reading that this product runs over collision classes.
- The local lemma, Hoeffding's inequality and PR #9's encodings are not formalized.
- Finite checks corroborate the proof and are not its premises.
- N1a and N1b are separate packages on separate branches. This one cites them and does not contain them.
