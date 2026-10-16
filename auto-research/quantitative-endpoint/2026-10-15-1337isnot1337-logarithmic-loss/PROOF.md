# A logarithmic loss at the conditional 1/8 endpoint

## 1. Claim, status, and inherited assumptions

All logarithms are natural. This is a conditional proof draft, not an independently reviewed theorem.

The source construction uses a cyclic group, two coordinate systems, literal interval labels, and literal keys.
The keys receive independent Bernoulli flips after the outer coloring is fixed.
The geometric and digit-rank encoding results remain imported assumptions.
Section 2 states their finite forms. Sections 3-9 prove the new quantitative transfer.

**Conditional theorem.** Assume the finite source interfaces in Section 2.
For every integer `k >= 2^1024` and every integer `r >= 2`,

```math
 W_r(k)>
 \left(\frac{k^{1/8}}{e^{20}\log k}\right)^{k\lfloor\log_2 r\rfloor}.
 \tag{1}
```

The construction works for every prime `k < P <= 2k^2`.
In particular, for every integer `k >= 2^4096`,

```math
 W_r(k)>k^{(k/9)\lfloor\log_2 r\rfloor}.
 \tag{2}
```

These bounds do not assert `c > 1/8` or the literal bound `W_2(k) > k^(k/8)`.
The denominator in (1) matters.
They do not provide a practical coloring, a finite coloring record, or a runtime improvement.

The base repository only states an unspecified threshold for each fixed coefficient below 1/8.
The open PR #9 states `K = 2^33554432` for its literal `c = 1/9` tuple.
Equation (2) replaces that tuple with variable parameters.
It reduces the sufficient value of `log_2 K` by a factor of 8192.
It does not improve PR #9's guarantee for its unchanged literal tuple.

The new ingredients are an additive light-position test, an explicit prime-counting bound for the dilation, and variable cutoffs.
The proof also separates the short-period balance tolerance from the near-half long-period tolerance.
The finite digit-rank factors come from prior work. Their smaller common error bound is audited in Appendix A.

## 2. Finite source interfaces

The pins and file identities appear in `SOURCES.json`.
The base pin is `rohanarun/van-der-waerden-refinement@63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.
The finite factors below appear in PR #9, `effective-completion/PROOF.md`, Sections 4-11.
Their head pin is `89660352f5dfcf1180a47b224610d444b2ce8701`.
They elaborate the base repository's digit-rank and short-period arguments.

Let `k >= 16`, `1 <= D <= k/64`, `q = P^e`, and `N = q^D`.
Let `H = k^-2` and let the source dilation `lambda` be a unit modulo `N`.
Use the source's uniform first-coordinate mesh and adaptive second-coordinate mesh.
Their widths are `H/lambda` and at most `2H`, respectively.
Write `J` for the adaptive mesh's interval count.
The proof below establishes `J <= k^6`.

A label records both systems of intervals. A key records the second-system box and the band

```math
 \kappa(n)=(V(y(n)),\lfloor q^2\|Y(n)\|^2\rfloor),
 \qquad Y(n)\in[-1/2,1/2)^D.
```

The following interfaces retain their original scope.

**Geometry.** A key occurs at most twice on a nonzero-step progression of length `k`.
A full label with multiplicity greater than `k/M` determines a closest return `h <= 2M`.
The source drift and path arguments apply when the explicit smallness conditions in Section 5 hold.
If `h <= h_0`, the second-coordinate representatives are affine throughout the progression.
Each full label then occupies one consecutive run in one residue class modulo `h`.
This run statement concerns actual progressions, not all abstract short-period words.

**Word counts.** With literal labels, equality signs, and half-open endpoints retained,

```math
 T_{\rm glob}\le
 [9(3k^2(k^2\lambda+J)+1)^2]^{2D}.                    \tag{3}
```

For fixed `h > h_0`, the count of eligible patterns through a specified label is at most

```math
 A_h=h^{D+1}[9(B_0Dh+1)^2]^{2D},
 \qquad B_0=\lceil128/\epsilon_{\rm reg}+4\rceil.      \tag{4}
```

The short-period word count through a specified label is at most

```math
 A_s=k h_0^{D+1}
 [9(k(4M+4)+1)^2]^D[9(2k(J+1)+1)^2]^D.              \tag{5}
```

These counts do not require `h_0 = D ceil(log k)^2`.
Their proofs only use the displayed drift ranges, the mesh bounds, and the permitted periods.
For `D,h_0,M <= k` and `J <= k^6`, (5) gives `log A_s <= 40D log k`.

**Digit-rank counts.** Write `t = log k`.
For each digit rank `0 <= R <= D`, the literal collision-class key sets number at most

```math
 \exp(R\log q+E),\qquad E=10k+100Dt+6\log q.        \tag{6}
```

The progressions of that rank with a repeated key number at most

```math
 \exp((2D-R)\log q+E).                              \tag{7}
```

The no-repeat class has the trivial count `q^(2D)`.
The key sets in (6) include singles in collision classes and arbitrary subsets of those positions.
They are not equivalence classes of full monochromatic events.
Appendix A derives the common error `E` from the prior finite encoding factors.
This derivation does not replace an independent review of those encodings.

**Affine key words.** For a progression with affine second-coordinate representatives,

```math
 T_K\le[9(3k^2J+1)^2]^D\,16[k(Dq^2+2)+1]^3,
 \qquad \log T_K\le6\log q+32Dt.                   \tag{8}
```

The digit product transfers any valid cyclic two-coloring to an interval with `2^s` colors and length `N^s`.
Here `s = floor(log_2 r)`. Its threshold does not depend on `r`.

The imported results are finite geometric and counting statements.
We do not substitute variable exponents into a theorem with an unspecified parameter-dependent threshold.

## 3. A smaller bound for the dilation

**Lemma.** For real `x >= 16`,

```math
 \pi(x)\le\frac{10x}{\log x}.                       \tag{9}
```

**Proof.** Every prime in `(n,2n]` divides the integer `binom(2n,n)`.
This integer is at most `4^n`.
Summing over dyadic intervals gives `theta(x) <= 4x`.
Indeed, take `2^(j-1) < x <= 2^j` and sum the bounds up to `2^j`.
The result is less than `2^(j+1) log 2 <= 4x`.

There are at most `sqrt(x)` primes at most `sqrt(x)`.
Every larger prime contributes at least `(log x)/2` to `theta(x)`.
Consequently,

```math
 \pi(x)\le\sqrt x+\frac{2\vartheta(x)}{\log x}
 \le\sqrt x+\frac{8x}{\log x}\le\frac{10x}{\log x}.
```

The last step uses `log x <= 2 sqrt x`. This follows by elementary differentiation. QED.

The dilation contains the full prime-primary part up to `2M` for each prime at most `h_0`.
Therefore

```math
 \log\lambda
 =\sum_{\ell\le h_0,\ \ell\ {\mathrm{prime}}}
   \left\lfloor\frac{\log(2M)}{\log\ell}\right\rfloor\log\ell
 \le\pi(h_0)\log(2M).                              \tag{10}
```

For the scales below, `log h_0 >= t/3` and `log(2M) <= 2t`.
Thus

```math
 \boxed{\log\lambda\le60h_0.}                     \tag{11}
```

The crude estimate `h_0 log(2M)` loses a factor comparable to `log k` here.
Equation (11) removes that loss without changing the dilation.

## 4. Variable parameters

For real `t = log k >= 512`, set

```math
 u=\frac{e^{t/2}}{4096t^3},\qquad D=\lceil u\rceil,
 \qquad M=\left\lfloor\frac{k}{t}\right\rfloor,
```
```math
 h_0=\lceil256Dt^3\rceil,\qquad
 M_s=\lceil4096Dt\rceil,
```
```math
 \epsilon=\epsilon_{\rm reg}=\frac1t,\qquad
 \eta=\frac1{8Dt},\qquad
 \epsilon_s=\frac14,\qquad\delta_s=\frac12,
```
```math
 \gamma=\frac12-\frac4t,\qquad
 p=\frac{65536t^4}{\sqrt k},\qquad
 F=k\left(\frac t8-\log t-20\right).              \tag{12}
```

Construct `lambda` from `M,h_0` as in Section 3.
Choose any source prime `k < P <= 2k^2`.
Let `q` be the least positive power of `P` with `D log q >= F`.
Then

```math
 F\le D\log q\le F+D\log P\le F+3Dt.             \tag{13}
```

The number `M_s` is independent of `h_0`.
The third outer family only needs `M_s` to dominate its anchored entropy.
It does not need the long-period tolerance `epsilon = 1/t`.

The following bounds hold for every `t >= 512`:

```math
 1\le u\le D\le2u,\quad
 \frac{k}{2t}\le M\le\frac{k}{t},\quad
 \frac{\sqrt k}{16}\le h_0\le\frac{\sqrt k}{4},\quad
 M_s\le4097Dt\le k,                               \tag{14}
```
```math
 D\le k/64,\quad 0<p\le1/2,\quad
 Q:=\log q\le512\sqrt k\,t^4+3t,\quad
 6Q+100Dt\le k.                                   \tag{15}
```

The last inequality implies `E <= 11k` and `log T_K <= k`.
Also `3Dt <= k`.

Here are explicit ways to verify these estimates.
For nonnegative `j`, the function `t^j exp(-dt)` decreases when `t >= j/d`.
For negative `j`, it decreases for all positive `t`.
At `t=512`, use `exp(-d t) <= 2^(-d t)`.
The largest terms in (14)-(15) are

```math
 4096t^3e^{-t/2},\quad 65536t^4e^{-t/2},\quad
 3072t^4e^{-t/2}+18te^{-t}
       +\frac{200}{4096t^2}e^{-t/2}.
```

The first is less than 1, the second less than 1/2, and each term in the last sum is less than 1/4.
The verifier checks their exact rational upper bounds and monotonicity.
The remaining bounds use smaller terms, which the verifier also checks.

For later use, `log t <= t/32` throughout this range.
At 512 this follows from `log 512 = 9 log 2 <= 9 < 16`.
The difference `t/32 - log t` is increasing for `t >= 512`.
This proves `F >= kt/32 > 0` and

```math
 L:=\log(1/p)=t/2-4\log t-\log65536\ge t/4.       \tag{16}
```

The mesh bound follows uniformly from these scales.
Indeed, `(D+1) log q <= kt/4+6Dt < kt`.
The literal mesh formula gives `J <= 2k^3 t+2 <= k^6`.
No fixed power-law exponent is used.

## 5. Geometry and entropy at these scales

Equations (14)-(15) give `h_0 < 2M < k < P`.
Thus `lambda` is a unit modulo `N`, and the source dilation removes all denominators at most `h_0`.
Also

```math
 \frac{2M}{k}\le\frac2t\le\frac1{16},\qquad
 \frac{4MH}{k}\le\frac4{k^2t}\le\eta,\qquad
 D(4\eta+1/h_0)\le\frac1{2t}+\frac1{256t^3}\le\frac1t.
 \tag{17}
```

These are the small-block, rotating-drift, and regularity conditions used in the source geometry.
The other small-width inequalities follow from `H=k^-2`, `k>=16`, and `M<=k/t`.
The closed-cut and single-run arguments retain their original quantifiers.

The global count (3), `J <= k^6`, and (11) yield

```math
 \log T_{\rm glob}\le42Dt+4D\log\lambda
 \le42Dt+240Dh_0\le\frac{k}{16t^3}.               \tag{18}
```

For the last step, `h_0 <= 257Dt^3` and `D <= 2u` give

```math
 \frac{t^3}{k}(42Dt+240Dh_0)
 \le\frac{84}{4096}\frac{t}{\sqrt k}
       +\frac{246720}{4096^2}
 \le\frac{84}{4096}+\frac{246720}{4096^2}<\frac1{16}.
```

For the local count, `B_0 <= 256t`.
Since `D,h <= k`, equation (4) gives

```math
 \log A_h\le15Dt\quad(h_0<h\le2M).               \tag{19}
```

In detail, its three contributions are at most `2Dt`, `Dt`, and `12Dt`.
The last bound uses `log(B_0Dh+1) <= log(512t)+2t <= 3t`.
Equation (5) gives

```math
 \log A_s\le40Dt.                                 \tag{20}
```

For example, its anchor, first-coordinate, and second-coordinate factors contribute at most `3Dt`, `5Dt`, and `15Dt`.
These bounds do not conceal constants that depend on `t`.

## 6. Additive light-position balance

Assign an independent fair bit to each literal full label.
The event supports contain distinct label variables, even when labels repeat in a word.

For each actual word, define `S` exactly as in the sharpened argument.
If there is no heavy label, `S` is the entire word.
Otherwise, remove every full closest-return block that contains a heavy index.
The set `S` consists of the remaining light positions, including light positions in the remainder.
Every choice depends only on the full label word.

Let `w_beta` be the multiplicity of a label in `S`.
Since these labels are light,

```math
 \sum_\beta w_\beta^2
 \le\frac{k}{M}|S|\le\frac{k^2}{M}.               \tag{21}
```

**Family 1.** For every nonempty `S`, exclude the event

```math
 \left|\sum_\beta w_\beta(\xi_\beta-1/2)\right|>k/t.
 \tag{22}
```

Weighted Hoeffding gives probability at most `2 exp(-2M/t^2)`.
Assign the weight `z_1=exp(-M/t^2)`.
There is at most one such event per actual word.

There is no minimum `delta k` for `|S|`.
Small sets have a vacuous lower balance bound and cause no difficulty.
This is an additive tolerance on the whole progression, not a relative tolerance on `S`.

**Family 2.** For each eligible long-period pattern, exclude deviations greater than `l/t` on its `l >= h/2` regular labels.
Its probability is at most `2 exp(-2l/t^2)`.
Assign the weight `z_2=exp(-l/t^2)`.

**Family 3.** In each abstract short-period word, call a label s-light when its multiplicity is at most `k/M_s`.
When s-light positions occupy at least `k/2` positions, demand a 1/4 fraction of each outer bit there.
Weighted Hoeffding gives probability at most `2 exp(-M_s/16)`.
Assign the weight `z_3=exp(-M_s/32)`.

The three incident weights at any fixed label satisfy

```math
 I_1\le\exp\left(-\frac{7k}{16t^3}\right),\qquad
 I_2\le k\exp(-112Dt),\qquad
 I_3\le\exp(-88Dt).                               \tag{23}
```

For `I_1`, use (18) and `M >= k/(2t)`.
For `I_2`, use `15Dt <= h/(16t^2)` and sum over at most `k` periods.
For `I_3`, use (20) and `M_s >=4096Dt`.

Each term in (23) is at most `1/(48k)`.
For the first, the monotone bound `8t^4 exp(-t) <=1` gives `7k/(16t^3) >= (7/2)t`.
For the other two, use `D>=1` and `t>=512`.
Thus the total incident weight is at most `1/(16k)`.

Every event uses at most `k` variables.
Its total neighbor weight is at most `1/16`, including all cross-family neighbors.
Every assigned weight has the form `exp(-w)` with `w>=1`.
Since `log(1-z)>=-2z` for `0<=z<=1/2`,

```math
 z_E\prod_{F\sim E}(1-z_F)\ge e^{-w-1/8}\ge2e^{-2w}.
 \tag{24}
```

Here `log 2 +1/8 <=3/4+1/8 <1 <=w`.
The finite asymmetric local lemma gives one coloring that avoids all three families.

## 7. The outer dichotomy

Let `E_pos` be the union of heavy-containing full blocks in a long-period progression.
At least `(1-1/t)h` positions in each such block are regular.
The second family gives each bit at least

```math
 A_0h,\qquad A_0=(1/2-1/t)(1-1/t)
```

positions per block.
The first family gives each bit at least `|S|/2-k/t` positions in `S`.
The sets are disjoint and satisfy `|E_pos|+|S| >= k-h`.
Consequently each bit occupies at least

```math
 A_0(k-h)-k/t
 \ge (1/2-3.5/t)k
 > (1/2-4/t)k=\gamma k.                           \tag{25}
```

The estimate uses `h<=2M<=2k/t` and `A_0<=1/2`.
It remains valid when the lower bound on the contribution of `S` is negative.
If no heavy label exists, Family 1 gives the stronger bound `(1/2-1/t)k` directly.

Every progression that is not gamma-rich therefore has a heavy label with short closest return.
Its second-coordinate representatives are affine, and every full label occupies one actual run.

## 8. Rich events: a finite split without fixed exponents

Now assign independent Bernoulli-`p` bits to the literal keys.
The final color is the outer color xor the key bit.
Define

```math
 \Gamma=\frac{\gamma kL}{2}-D\log q,
 \qquad L=\log(1/p).
```

Using (12)-(13),

```math
 \Gamma\ge k\left[19-\frac14\log65536
              +\frac{8\log t+2\log65536}{t}\right]-3Dt
 \ge15k-3Dt\ge14k.                               \tag{26}
```

For rank `R`, put

```math
 T_R=\frac{R\log q+\Gamma}{L}.
```

Then `0<T_R<gamma k` and

```math
 T_RL-R\log q
 =(\gamma k-T_R)L-(2D-R)\log q=\Gamma.            \tag{27}
```

For a fixed target, discard inconsistent prescriptions on repeated keys.
If at least `T_R` distinct flipped keys lie in collision classes, select `ceil(T_R)` of them.
Equation (6) counts their literal certificates, each with probability at most `exp(-T_R L)`.

Otherwise, fewer than `T_R` flipped keys lie in collision classes.
The multiplicity-two identity implies more than `gamma k-T_R` distinct required flips in total.
Equation (7) counts these progressions.
The no-repeat case uses its trivial count.

No independence between different events is needed.
Independence only applies to distinct keys within one prescribed event.
Summing over both cases, targets, and ranks gives

```math
 R_k\le4(D+1)e^{E-\Gamma}
 \le4(D+1)e^{-3k}<1/4.                           \tag{28}
```

The selected-key ceiling only decreases its event probability.
This finite split replaces the fixed-parameter limiting calculation.

## 9. Non-rich events

All such progressions have the structure from Section 7.
Their affine key words satisfy (8).

**Many s-light positions.** If s-light positions occupy at least `k/2` positions, Family 3 supplies at least `k/8` opposite-color positions.
At least `k/16` distinct keys must flip.
For each key word, a union over its subsets costs at most `2^k`.
Using `log T_K<=k` and `L>=t/4`, the total for both targets is at most

```math
 2T_K2^kp^{k/16}\le2e^{2k-kt/64}<1/4.             \tag{29}
```

**Few s-light positions.** More than `k/2` positions carry labels of multiplicity greater than `k/M_s`.
There are at most `M_s` such labels.
Each is one run in an actual short-period progression.
Encode the period, the number of runs, and each run's residue, endpoints, and outer bit.
The number of codes is at most

```math
 B_{\rm run}=h_0(M_s+1)(2k^3)^{M_s}.               \tag{30}
```

Together with the key word, the code prescribes at least `k/4` distinct key bits.
Reject conflicting prescriptions and ignore positions outside the recorded runs.
Each remaining event has probability at most `exp(-pk/4)`.

The finite estimates give

```math
 \log B_{\rm run}\le3t+4M_st,
```
```math
 \log T_K+\log B_{\rm run}+\log8
 \le3072\sqrt k\,t^4+21t+9\sqrt k/t+\sqrt k/(64t^2)+3
 \le3106\sqrt k\,t^4<4096\sqrt k\,t^4=pk/16.      \tag{31}
```

The corresponding total is therefore less than `1/4`.
Equations (28)-(31) make the probability of any bad progression less than `3/4`.
A valid cyclic two-coloring exists.

Its size satisfies `N >= exp(F)`.
The source digit product gives (1), since `t>=512` whenever `k>=2^1024`.

For (2), the function `t/72-log t-20` increases for `t>=2048`.
At 2048 it is at least `2048/72-33/4-20=7/36>0`.
Here `log 2048=11 log 2<=33/4`.
Therefore `F>=kt/9` in that range.
The condition `k>=2^4096` guarantees `t>=2048`.
This proves the stated finite threshold. QED, conditional on Section 2.

## 10. Dependence of the threshold on the target coefficient

Let `0<c<1/8` and put `Delta=1/8-c`.
Let `j` be the least integer with `2^j >= 2/Delta`.
Define the integer

```math
 n(c)=\max\left(1024,\left\lceil\frac{4(j+20)}{\Delta}\right\rceil\right),
 \qquad K(c)=2^{n(c)}.                            \tag{32}
```

This is an integer/rational formula for rational `c`.
For `k>=K(c)`, both `t>=512` and `t>=2(j+20)/Delta` hold.
At `t_*=2(j+20)/Delta`,

```math
 \log t_*+20
 \le j+\log(j+20)+20
 \le2(j+20)=\Delta t_*.
```

The difference `Delta t-log t-20` increases for `t>=t_*`.
Thus (1) gives `W_r(k)>k^{ck floor(log_2 r)}` for every `k>=K(c)`.
In particular,

```math
 \log K(c)=O\!\left(\frac{\log(1/\Delta)}{\Delta}\right)
 \quad(\Delta\downarrow0).                       \tag{33}
```

The special threshold `2^4096` at `c=1/9` is smaller than the generic formula.
Both thresholds concern the new variable-parameter construction.

## Appendix A. Audit of the finite digit-rank error

The underlying encoding proofs remain the imported assumptions in Section 2.
This appendix verifies that their explicit finite factors permit the error used here.
All estimates apply to `t>=512`, `D<=k/64`, `q>k`, and `J<=k^6`.

For the certificate count, the excess after `R log q` has these bounds:

| Factor | Excess logarithm |
|---|---:|
| Discrete words and repeated-pair choices | `21Dt+2k` |
| Integer start projections | `3Dt` |
| Three-parameter arrangement | `6 log q+9t` |
| Tail arrangement | `20Dt` |
| Crossing-order arrangement | `28Dt` |
| Class choices and subsets | `7k` |

Their sum is at most `6 log q+81Dt+9k`, less than `E` in (6).
The progression count's excess is at most `4 log q+26Dt+2k`, also less than `E`.

For clarity, the three arrangement threshold counts are

```math
 s_G=k(Dq^2+8Dk+4k+20),\quad
 s_\phi=k(4Dk+7),\quad
 s_\times=2k^2(2\lceil k/h\rceil+5)^2.
```

They satisfy `s_G+1<=3k^2q^2`, `s_phi+1<=6k^3`, and `s_cross+1<=19k^4`.
The equality-inclusive arrangement bound is `(d+1)^2(s+1)^d`.
Its dimensions are 3, `D+3`, and `D+3`, respectively.
These formulas give the table directly.

For a class length bound `K_h=ceil(k/h)`, its word choices are at most `4K_h^2+10K_h+1`.
This polynomial is at most `16^K_h` for every positive integer `K_h`.
The base case is `15<=16`.
The induction difference is `16P(n)-P(n+1)=60n^2+142n+1>0`.
Since `hK_h<=2k`, all classes cost at most `256^k`.
Subsets cost at most `2^k`, so their joint logarithm is at most `9k log2<7k`.
The elementary bound `log2<=3/4` suffices.
Indeed, `exp(3/4)>1+3/4+(3/4)^2/2>2`.

## Appendix B. Verification boundary

`verify.py` uses exact fractions and integer arithmetic.
It verifies all-larger-`t` monomial bounds using derivative thresholds and rational endpoint bounds.
It also verifies the coefficient transfer, constant accounting, and rejection controls.
Independent finite tests examine dilation products, weighted tails, and the rich-event split.

These checks do not formalize the local lemma or the geometric and digit-rank encodings.
No full theorem-sized coloring is generated.
The repository's original programs are unchanged and were not rerun for this additive package.
Independent mathematical review must examine the new event families and the inherited finite interfaces.
