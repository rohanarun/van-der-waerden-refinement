# Counting dangerous traces: the sparse case is Door 1, and the dense case lives at the fine scale

**Status:** a scoping note, with one proved equivalence and an exact statement of the scales. It concerns
the open question (Q-S1b) of `2026-10-27-ChaloupeMusic-colour-correlated-rules` (S1b). The question asks
whether every frozen set `X` passing (I′) realises many distinct **dangerous** traces on one label word or
one pattern. No lower bound on that count is proved here, in either regime.

**Base commit:** `pr/door-one` (`00375ff`) on `63bef9c`, through
`colour-correlated-rules` (this PR).

## Setting

As in S1b. For `P ∈ 𝒫_long`, the positions of `S_all` (or of `S_out`) are dealt into at most `k/M` rows
of at least `δM − 1` distinct labels, as in family 1. Long-period progressions are cut into eligible
heavy blocks (patterns) of length `h`, with `h_0 < h <= 2M`. A trace `X_P` is **dangerous** at a row `r`
when `|X_P ∩ r| >= εM/4`. It is dangerous at a block of length `h` when it has at least `εh/8` regular
positions there. These are the thresholds of families 4a and 4b. `𝒮_dang(W)` and `𝒮_dang(π)` are the
dangerous traces realised on a label word `W` and on a pattern `π`.

Three counts frame the question.

| count per label word | what it decides |
|---|---|
| `log\|𝒮_dang(W)\| <= εM/64` | Theorem B of S1b applies, in its weakened form that counts dangerous traces only |
| `log\|𝒮_dang(W)\| = O(k)` | necessary for every certificate of the clique class (Proposition E of S1b, with `μ >= 2^{−k}`) |
| `log\|𝒮_dang(W)\| = ω(k)` | what a closure of S1b in the certificate class needs to prove for every `X` passing (I′) |

## 1. The sparse case is Door 1

Call `X` **row-sparse** when every `P ∈ 𝒫_long` has `|X_P ∩ r| < εM/4` on each row of both dealings, and
fewer than `εh/8` regular positions of `X` on each of its eligible heavy blocks.

**Proposition 1.** The following are equivalent, for fixed region parameters and `ε`.

1. Some row-sparse `X` passes (I′).
2. Some `X` passing (I′) has `𝒮_dang(W) = ∅` and `𝒮_dang(π) = ∅` for every label word `W` and every
   pattern `π`.

Each implies, at these parameters, that the template proves `c` for every `b` beyond which `X` passes
(I′), by Theorem B of S1b and Theorem 2 of `exact-door-one-condition` (`2c < θb`, `θ = γ − ε`). (I′)
only gets easier as `b` grows. So the method would have no ceiling on `c`. That needs such an `X` at each
`c`, since `X` is built at fixed `c` (`N`, `q` and the keys depend on it).

*Proof.* (1) and (2) say the same thing: a trace is dangerous exactly when some row carries `εM/4` points of
it, or some block carries `εh/8` of its regular points. For the consequence, every `P ∈ 𝒫_long` has
`|X_P| < εk`: its rows number at most `k/M` per dealing, and its heavy blocks cover the rest. In the
heavy-label case, S1b's proof takes `X_P`'s points in `S_out` or in the heavy blocks, and those are bounded
the same way. So `|C_{¬β}(P) \ X_P| >= (γ − ε)k`, which is (II′_θ) on `𝒫_long`. Together with (I′),
Theorem 2 of `exact-door-one-condition` applies for every `b`. ∎

**Corollary.** For every threshold `f >= 1`, the claim "every `X` passing (I′) realises more than `f`
dangerous traces on some `W` or `π`" implies that **no row-sparse `X` passes (I′)**. That is Door 1 in the
row form of (II): a set of keys hitting every slow word, with relative density below `ε/4` on every row of
every long progression. It is open. P1a only places three keys of `X` in arithmetic position on some rich
progression. P1b closes uniform laws. S6-63 splits it into (D) and (S). On the sparse side, S1b therefore
adds no difficulty and removes none: the sparse half of Q-S1b **is** the row form of Door 1. It is also
what (D) and S7 look for: a sparse transversal of density `k^{−a}`, which would here have to stay below
`ε/4` on rows.

## 2. The dense case: where the count must come from

Call `X` **band-dense** when, for every label `L` the template uses and every band window `I` of length at
least `ℓ`, the set `T_L = {t : (L, t) ∈ X}` has relative density in `[2ε, 1 − 2ε]` on `I`. Here `ℓ` is the
largest run length allowed by the proof of Theorem C of S1b, `ℓ_* = 3(m_* + 2)kqλ = q^{1+o(1)}`. For such
`X`, a typical realisation of a label word puts about a `2ε` fraction of every row in `X`, so dangerous
traces are the typical ones. The question is only how many distinct traces a label word realises.

**Upper bound (Lemma D1 of S1b).** With `R <= q^2` band intervals per label,
`log|𝒮(W)| = O(D log(kR)) = O(D log q) = O(ck log k)`, since `D log q = log N`.

**Consequence for the target.** A closure in the certificate class needs `log|𝒮_dang(W)| = ω(k)`, which is
`ω(1/log k)` times the largest count the dimension allows. Spread over the `2D` real parameters of a label
word, that means each direction must resolve `q^{ω(1/log k)} = e^{ω(k^{1−a})}` distinct traces. The coarse
structure cannot supply this. `2D` positions with independent linear forms give at most `2^{2D} = e^{O(k^a)}`
traces, and any argument that uses only bounded resolution per direction stays at `e^{O(D)}`. Since
`D = o(k)`, such arguments do not even reach Theorem B's threshold `εM/64`, because `D = o(M)` too. A
closure must therefore use the fine alternations of `T_L`, at scale `ℓ_* = q^{1+o(1)}` inside windows of
length `q^2/(80k^2)`.

**The dense form of Theorem B (radar-3a, a sketch here).** radar-3a has committed it as Corollary B′ of
`colour-correlated-rules` (in this PR), refereed after this note was written. Each row of `S_all(W)` and
`S_out(W)` is cut into consecutive pieces. A row shorter than `2M` stays whole, and the others give pieces of
length `M` to `2M`. So each piece has length between `δM − 1` and `2M` and distinct labels, and a word has
at most `2k` pieces. A trace is dense when it has density at least `ε/4` on a piece, or at least `ε/8` on a
pattern. Theorem B then holds when the dense traces number at most `e^{εδM/80}` per word and `e^{εh/128}`
per pattern. This is the version a dense lower bound has to beat. This note uses it only to fix the target.

**What Theorem C gives on the dense side (radar-3a).** Applied to every subinterval of `J_L`, its proof
bounds the length of each run of `T_L` and of its complement by `ℓ_* = 3(m_* + 2)kqλ`. So both are present
in every window of that length. That is a uniform two-sided presence, but not a density, and no lower
bound on run lengths.

**A warning on the frequency heuristic.** Pulverising points as `sign sin(θx)` does needs either a
periodic `T_L`, or a **lower** bound on run lengths. Theorem C bounds runs only from above. With runs of
arbitrary shortness, a nested-interval argument along one direction controls a position only if its
frequency exceeds the previous one by a factor `ℓ_*` or more. So it fixes `O(log(q^2)/log ℓ_*) = O(1)`
positions. radar-3a sharpens this. The sensitivities of the positions to the step `B` (`∂t_j ∝ j`, or `j^2`)
differ by factors `k^{O(1)}` only. So even for a periodic `T_L` the nested intervals fix about `log k`
positions per direction, hence `2^{O(D log k)}` traces. With the Jacobian, `2D` independent directions
give `2D` positions without any lower bound on runs, hence `2^{Θ(D)}` traces. Both are far below
`e^{εM}`, because `M = k^m >> D log k`. Pulverising will not produce the count. What would is a count of
the cells of the arrangement of the `~kR` hypersurfaces `{t_j = end of a run}`, up to
`(kR/D)^{2D} = e^{Θ(D log q)}`, followed by a proof that distinct cells give many distinct **dense**
traces. Band-density (two-sided, at scale `ℓ_*`) is the hypothesis that should replace periodicity. A
proof would show that, under it, the `h` bands of a pattern behave like independent coordinates at scale
`ℓ_*` across `e^{ω(k)}` cells. This note does not prove it, and the answer is not known to be no. If the
dense traces of every working `X` were counted like a family of low VC dimension, `e^{O(D log k)}`,
Theorem B would hold and S1b would open Door 1 on the rich side.

## What is claimed

* Proposition 1 and its corollary: the sparse half of Q-S1b is equivalent to the row form of Door 1.
* The scale statements of § 2, which are arithmetic on S1b's Lemma D1, Theorem C and Proposition E.
* Nothing about the dense case beyond its scales. No lower bound on dangerous traces is proved.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-dangerous-traces-scope/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, JSON summary equal to `RESULT.json`.

## Checks in `verify.py`

1. Proposition 1 on random toys: positions dealt into rows and blocks, random `X`. A trace has a dangerous
   row or block exactly when the row-sparse condition fails, and row-sparse traces have `|X_P| < εk`.
2. The scale ledger at the template points of `ap-free-frozen-sets` (`D = ⌈k^a⌉`, `ln q = ck ln k/D`):
   `log₂` of `D`, of `M = k^m` for `m` midway between `2a` and `1`, of `k`, and of `D log q`. The order
   `D < M < k < D log q` is checked at every point.
3. A control: with `m = a` (so `M = D`), the inequality `D log k << M` fails at every point. The region's
   condition `m > 2a` is what puts `M` above `D log k`.
