# The seven-eighths loss is the limit of the union-bound template

**Status:** proof draft with exact checks, about the proofs of PR #12, N1b and the composed endpoint.
Independent review is pending. Nothing here changes those bounds or their conditional status.

PR #12, N1b and the composed endpoint prove

```math
W_r(k)>\left(\frac{k^{1/8}}{e^{C}(\log k)^{\theta}}\right)^{k\lfloor\log_2 r\rfloor}
```

with `θ = 7/8` and, at best, `C = 71/20`. This note asks how far the same chain of argument can go. The
chain is an outer colouring from three local-lemma families, a dichotomy, and union bounds over rich and
non-rich progressions. Six inequalities, read off those proofs, constrain its parameters
`D, M, h_0, ε_1, ε_2, γ, p, q` ([PROOF.md](PROOF.md), Section 2). Under those six alone:

- **Theorem A.** No parameter choice gives `θ < 7/8`.
- **Theorem B.** No parameter choice gives `C < C^*` for all large `k`, where
  `C^* = (1/2)(log 10 + ℓ_cls) + 1/2 + (1/4) log(18√2)`.

| tier (class product of PR #9, Section 8.3) | `C^*` | delivered `C` |
|---|---:|---:|
| D″, `45^{k/2}` | `3.41219` | `71/20` |
| D′, `19^k` | `3.93275` | `403/100` |
| N1a's D, `37^k` | `4.26599` | `35/8` |

So at most `0.138` of the constant is left to win under D″ by retuning. The exponent `7/8` cannot move
without changing the argument itself.

## Where the 7/8 comes from

| source | share |
|---|---:|
| non-rich union over affine key words: the flip rate is at least `12 log q/k`, and `log q` is of order `kt/D` | `1/4` |
| second-family entropy of order `Dt` against a tail `h ε_2^2` | `1/8` |
| first-family tolerance: Hoeffding pays `ε_1^2` in `D^2`, and the dichotomy pays `ε_1` in `γ` | `1/4` |
| second-family tolerance: the same with `ε_2` | `1/4` |

The two tolerances are best at `(1 + o(1))/t`, the value all three proofs use. Going below `7/8` needs a
new ingredient in one of four places (PROOF.md, Section 4):

- a non-rich bound over `q^{o(1)}` words;
- a second-family count of `o(Dt)`;
- a first-family union over fewer than `λ^{Θ(D)}` words;
- a concentration step whose tolerance is not paid in `γ`.

## Reproduce

From the repository root:

```sh
python3 -B auto-research/quantitative-endpoint/2026-10-26-ChaloupeMusic-template-limit/verify.py
```

Expected: exit code 0, and standard output byte-identical to `RESULT.json` (about 7 seconds, standard
library only). The verifier checks:

- `C^*` in each tier, enclosed by certified rational bounds for the logarithms, and its gap to the
  delivered constants;
- the exact identities of the proof;
- as evidence only, a numerical optimisation of the six inequalities at finite `t`. The best constant the
  template allows increases from `3.238` at `t = 256` and `3.321` at `t = 512` to `3.41211` at `t = 10^6`.
  The optimal tolerances are `1.0/t` to `1.2/t`;
- negative controls: a wrong constant in `C^*`, tolerances held at `2/t`, or a smaller entropy each miss
  the limit;
- file integrity against `MANIFEST.json`.
