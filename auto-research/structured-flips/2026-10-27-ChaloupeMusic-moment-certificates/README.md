# Moment certificates for Door 1: independence buys nothing, and two moments certify only through extreme clustering

**Status:** structural research, with proofs. It answers one question about Door 1. Could a random frozen
set `X` with designed correlations (blocks, `d`-wise independent hashing) be certified to satisfy (II′)
and (I′) by a second moment or by Janson's inequality, beyond what the first moment certifies? Three
exact statements answer it. Independence of any order reproduces the iid certificate. Two moments
certify `S_1 >= 1` only when the failures are extremely clustered. No admissible `X` and no new bound on `c` is claimed.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, through `pr/door-one` (`00375ff`). It
uses the exact conditions (II′_θ), (I′_η), (I′_w) and Theorem 2 of
`2026-10-26-ChaloupeMusic-exact-door-one-condition`.

## Setting

`𝒦` is the key set, `X ⊆ 𝒦` is drawn from a law `L`, and `𝓔` is the family of failure events of
(II′_θ), (I′_η) and (I′_w), one for each pair (progression, target colour) whose event is not empty. Each
`E ∈ 𝓔` depends only on `X ∩ κ(P_E)`, a set of at most `k` keys. `Z` is the number of events of `𝓔`
that occur, so `X` is admissible exactly when `Z = 0`. Write `S_j = E[C(Z, j)]` for the binomial moments
(`S_1 = E Z`), and `n^* = max_X Z(X)` for the largest possible value of `Z`.

## Results

**Theorem 1 (independence is invisible to moments).** `S_j` depends only on the joint law of `X` on sets
of at most `jk` keys. So every lower bound on `P(Z = 0)` computed from `S_1, …, S_m` is the same for all
laws that agree on `mk`-sets. In particular, an `mk`-wise independent law gives exactly the certificate of
the iid law with the same marginals. Independence of order `d >= k` reproduces the iid first moment, and
order `d >= 2k` the iid second moment. More independence buys nothing.

**Theorem 2 (the exact second-moment certificate).** The first two moments certify `P(Z = 0) > 0`, that
is, every integer variable `W` in `{0, …, n^*}` with the same `S_1, S_2` has `P(W = 0) > 0`, if and only
if

```math
 S_1<1\qquad\text{or}\qquad S_1-\frac{2S_2}{n^*}<1 .
```

**Theorem 3 (what a second-moment certificate looks like).** Suppose the second moment certifies `L`,
with margin `π = 1 − S_1 + 2S_2/n^* > 0`. Then for every `δ` in `(0, 1]`,
`E[Z ; Z <= (1 − δ)n^*] <= (1 − π)/δ`. So all the failure mass beyond `O(1)` sits on catastrophes, draws
where more than a `1 − δ` fraction of the largest possible number of events fail. With `S_1 >> 1`, this
needs `S_2 >~ n^* S_1/2`. A designed correlation can certify through two moments only by clustering its
failures this extremely. This is a description of the certificates, not a closure: the law conditioned
on non-catastrophe leaves every computable class, and conditioning on `{Z = 0}` would trivially give
`E[Z] = 0`.

**Corollary 4 (hashing).** A `d`-wise independent law with `d >= k` and marginal `ρ = k^{−b_X}` has the
iid first moment. With Theorem 2 of the exact-condition note, its rich part certifies at least

```math
 c<\min\Bigl(\frac{b_X(\gamma-\theta)}4,\ \frac{\theta b}2\Bigr),\qquad b_X<a ,
```

with `b_X < a` from the iid hitting cost of (I′), whose supremum is `γa/4`. This is a sufficient
condition, not a ceiling. The proved ceiling is Proposition 5 of the exact-condition note,
`2c <= (1/2 − θ)b_X`, so a `k`-wise independent `X` is certified somewhere between `γa/4` and `a/4`, and in
every case below `1/8`. Such laws exist with the available keys: a uniform polynomial of
degree `< d` over `F_Q`, `Q >= |𝒦|` prime, thresholded at `ρQ`, is exactly `d`-wise independent, with a
seed of `d log Q` bits (Proposition 7). The obstacle is therefore Theorems 1 and 3, not the supply of
hash functions.

**Proposition 5 (blocks).** A law that is constant on the blocks of a partition of `𝒦`, and iid across
blocks, is the iid law on a coarser key system. If no block meets both colour classes of `P`, a failure at
`P` needs fewer independent choices, and its probability can only grow. A block that meets both classes of
`P` makes (II′) hold at `P` for every draw. Asking this of every rich `P` is a deterministic condition, with
no probability left in it.

**Proposition 6 (Janson).** Janson's inequality bounds the probability that no increasing event occurs
from **above**. It can show that a law fails, never that it succeeds. The failure events of (II′) are not
monotone: they ask `X` to avoid one class and to cover the other. Harris's inequality, the lower-bound
counterpart, needs monotone events of one direction. The event that every hitting condition of (I′)
holds is increasing, and the event that no covering event `U` occurs is decreasing, so Harris correlates
them **negatively**. (II′) only forbids `U ∩ V`, which is weaker than forbidding `U`, so this is a remark
and not a proved obstacle.

## Answer to the question

| asked | answer |
|---|---|
| independence needed for the first moment | `k`-wise. It certifies at least `c < γa/4`, and never beyond `a/4 < 1/8` (Corollary 4) |
| independence needed for the second moment | `2k`-wise gives exactly the iid second moment. No `d` changes it (Theorem 1) |
| what the second moment needs | `S_1 − 2S_2/n^* < 1` (Theorem 2): all failure mass beyond `O(1)` on catastrophes (Theorem 3) |
| can a clustering help | only an extreme one: with `S_1 >> 1`, `S_2 >~ n^* S_1/2`, the failures piling onto draws where almost every event fails (Theorems 2 and 3). No such law is known, and the note does not exclude one |
| Janson | upper bounds only, and the events are not monotone (Proposition 6) |
| a hash family with the keys at hand | yes, for every `d` (Proposition 7). It is not the bottleneck |

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-moment-certificates/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and a JSON summary equal to
`RESULT.json`. Standard library only, exact rationals, a few seconds.
