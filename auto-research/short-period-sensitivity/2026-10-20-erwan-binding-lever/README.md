# Which constraint caps the short-period region at 1/8?

**Status:** research note, exact sensitivity analysis. Not a new bound, and not
a proof about van der Waerden numbers. What is proved is an elementary fact
about the stated system of sufficient inequalities.
**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.

## What was checked

In the short-period region the flip exponent `b` is bounded only by three
inequalities (constraint list as encoded in `audit_math.py::sp_margins`):

| Label | Inequality | Origin in `short-period-runs-proof.md` |
|---|---|---|
| F | `2a < m < 1` | first local-lemma family, `ι_1 ≤ k T_glob e^{-ε²δM}` with `log T_glob = O(k^{2a} log³k)` |
| B | `b < a` | case (ii) of the non-rich estimate: band entropy `6 log q = O(k^{1-a} log k)` against `pk` |
| R | `a + b < 1` | case (ii) again: run code `e^{O(D log³ k)}` against `pk` |

The coefficient enters only through `2c < γb` with `γ < 1/2`, so
`sup c = sup b / 4`. Case (i) needs neither B nor R (its tail is
`e^{-Ω(k log k)}`).

## Result

| Change | sup b | sup c |
|---|---|---|
| none (current region) | 1/2 | 1/8 |
| relax F to `a < m < 1` | 1/2 | 1/8 |
| drop R | 1/2 | 1/8 |
| drop B | 1 | 1/4 |
| weaken B to `b < θa`, θ ≥ 1 | θ/(1+θ) | θ/(4(1+θ)) |

So, among the three stated inequalities and with the rest of the chain
unchanged, **B is the only one whose relaxation alone raises the supremum.**
R and B together already force `b < 1/2` (`2b < a + b < 1`), independently of
F. `short-period-runs-proof.md` notes that R follows from B and F; the
converse point recorded here is that R becomes binding as soon as F is
relaxed, so improving the first local-lemma family alone cannot raise the
supremum. The README's closing remark (`b < a` and `2a < m < 1` forbid
`b > 1/2`) is correct but incomplete in this respect. Both B and R live in case
(ii), so case (ii) is the step to attack. For example, a case (ii) key count
of `exp(k^{1-2a+o(1)})` (θ = 2) would give every `c < 1/6`.

Combined with `barrier-note.md`, which argues that `q^6` band words are
tight for floor-words of quadratics, the practical consequence is: a gain
past 1/8 needs case (ii) progressions (nearly constant outer color on few
heavy runs, all heavy keys unflipped) to be handled without a union bound
over their band words.

## Reproduce

```sh
python3 -B auto-research/short-period-sensitivity/2026-10-20-erwan-binding-lever/verify.py
```

Expected: exit code 0 and stdout byte-identical to `RESULT.json` (exact vertex enumeration
with `fractions.Fraction`; scipy is an optional floating-point cross-check).
Negative controls: strengthening B to `b < θa` with θ < 1 must lower the
ceiling to θ/8, and does.

## Scope

The rows "drop B" and "b < θa" are hypothetical: no argument achieving them
exists. They assume that a new case (ii) estimate would leave R and every
other inequality unchanged, which need not hold since B and R come from the
same estimate. Nothing here shows that any inequality is necessary.

This is a statement about the listed sufficient inequalities, not about van
der Waerden numbers and not about the validity of the imported lemmas. It
assumes the constraint list in `sp_margins` is complete for `b`. Open PRs
could not be checked for overlap (GitHub API rate limit at time of writing).
