# Repeated-key certificates: a conditional coefficient 1/19

This research note develops a literal repeated-key certificate count and a
probability cover for the cyclic construction of the pinned van der Waerden
manuscript. It retains the sharpened outer-coloring input from this
repository. All newly used geometric, counting, probability, and parameter
steps are proved below; the imported outer input is stated precisely in
Section 6. The resulting van der Waerden claim remains conditional on that
input. All logarithms are natural unless a base is indicated.

**Provenance and scope.** The initial argument was produced in a ChatGPT
Pro research response by GPT-6 Pro (internal run label "O1"), captured on
October 10, 2026. This publication
draft was assembled and reviewed with Codex, with explicit definitions and
boundary clarifications added. This is AI-produced mathematical research,
not a claim of original human theorem discovery or an official OpenAI
publication. The original manuscript's authors retain credit for their
construction; the existing refinement retains credit for the two-point
norm-band lemma, shortened dilation, sharper balance, and modified light
family. No literature-priority, formal-verification, practical finite
threshold, or explicit coloring claim is made. Finite tests are not premises
of any proof here.

The unpublished initial response has SHA-256
`7dc62dba8a177e452ae25b788ab841df155c64a8fa339553fae487f3c8ea3314`.
This is a private commitment, verifiable only against the retained response
text; it is not publicly inspectable evidence for the proof.
The source dependencies are pinned to
[`openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026)
and the prior refinement
[`54ac9715fceab938ca77d5980c36ab691765a04d`](https://github.com/rohanarun/van-der-waerden-refinement/tree/54ac9715fceab938ca77d5980c36ab691765a04d).

## Result and quantifiers

The new certificate cover replaces the rich-event sufficient condition by
```math
\boxed{c<\frac{\gamma b}{3}}
```
instead of $`c<\gamma b/4`$. With the sharpened outer construction retained, this admits every fixed $`c<1/18`$. One exact choice gives
```math
\boxed{
W_r(k)>k^{(1/19)k\lfloor\log_2r\rfloor}
}
```
for every integer $`k\ge k_0`$ and every integer $`r\ge2`$, for one
parameter-dependent $`k_0`$ independent of $`r`$, **conditional on the
pinned sharpened global outer-color dichotomy**. Here $`W_r(k)`$ is the
least interval length forcing a monochromatic $`k`$-term arithmetic
progression in every coloring with at most $`r`$ colors.

The improvement is a weighted **cover** of distinct consistent rich events, not a bound on their ungrouped probability sum. Different full prescriptions $`(F,Z)`$ remain different events. But when they share a suitable literal set $`S\subseteq F`$ of repeated keys, their union is contained in the single event
```math
\{E_\kappa=1\text{ for every }\kappa\in S\}.
```
The new theorem counts these certificates with leading entropy $`q^D`$, rather than $`q^{2D}`$.

The improvement concerns a cover of events, not an identification of distinct
full prescriptions or a smaller number of all progressions.

---

## 1. The finite counting theorem

Let integers $`k\ge8`$, $`D\ge1`$, and $`e\ge1`$ be given, and put $`q=P^e`$, where $`P>k`$ is prime, and let $`\lambda`$ be an integer unit modulo $`N=q^D`$. Put
$`G=\mathbb Z/N\mathbb Z`$, and for $`1\le i\le D`$ define
```math
x_i(n)=n/q^i\pmod1,\qquad y_i(n)=\lambda n/q^i\pmod1.
```
These maps are well defined because $`q^i\mid N`$. For every nonzero
$`d\in G`$, its order is at least $`P>k`$; thus
$`n_j=n_0+jd`$, $`0\le j<k`$, has distinct terms. Let
$`Y(n)\in[-1/2,1/2)^D`$ be the centered representative of $`y(n)`$.
The distance from the centered cut is
$`\rho(z)=\operatorname{dist}_{\mathbb R/\mathbb Z}(z,1/2)`$.
Write
```math
Y(n)=\widetilde y(n),\qquad
f(n)=q^2\|Y(n)\|^2,
```
and retain the literal keys
```math
\kappa(n)=\left((V(y_i(n)))_{i=1}^D,\lfloor f(n)\rfloor\right).
```

Put $`H=k^{-2}`$ and $`\alpha=q^{-(D+1)}`$. To fix the
literal mesh completely, set
```math
R_0=\log(1+(2\alpha)^{-1}),\quad m_V=\lceil k^2R_0\rceil,
\quad a_\ell=\alpha(e^{\ell R_0/m_V}-1)\quad(0\le\ell\le m_V).
```
The $`J=2m_V`$ intervals of $`V`$ are
```math
[-1/2+a_\ell,-1/2+a_{\ell+1}),\qquad
[1/2-a_{\ell+1},1/2-a_\ell)\quad(0\le\ell<m_V).
```
In particular the cut belongs to the interval beginning at $`-1/2`$,
and zero belongs to the interval on its right. A literal interval means
the interval at its actual location, not a renamed symbol.

The mesh property needed below is
```math
|I|\le 2H\bigl(\rho(Y)+\alpha\bigr)\le2H
\quad(Y\in\overline I),
\tag{1}
```
This follows directly from the mesh definition: with
$`\theta=R_0/m_V\le H`$ and $`b=\alpha+a_\ell`$ for the
corresponding reflected pair of intervals, each interval has width
$`b(e^\theta-1)`$, while $`\rho(z)+\alpha\ge b`$ on its closure.
Since $`e^\theta-1\le2\theta`$ and $`\rho(z)+\alpha\le1`$ here,
the displayed bound follows, including endpoints. This is the upper-width
bound of the pinned adaptive mesh in [upstream Section 02](https://raw.githubusercontent.com/openai/math/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/02-setup.tex).
The key definition is the one in [upstream Section 06](https://raw.githubusercontent.com/openai/math/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/06-perturbation.tex).

For a fixed outer coloring $`c_0:G\to\{0,1\}`$, call a progression
**$`\gamma`$-rich** if each outer bit occurs at least $`\gamma k`$ times.
An **affine** progression will mean one for which all the centered second
coordinates follow a single real affine progression over all $`k`$ indices.

A **repeated-key certificate** is a nonempty literal set $`S`$ of keys such that, on some one nonzero-step $`k`$-term progression, every key in $`S`$ occurs twice. Let $`\mathcal C_R`$ be the family of distinct such sets of cardinality $`R`$.

Define
```math
T_{\mathrm{aug}}
=\left[9(6k^2J+1)^2\right]^D
```
and
```math
\boxed{
\mathfrak B_k
=16D\,k^{D+4}q^{D+2}T_{\mathrm{aug}}\,512^k.
}
\tag{2}
```

### Theorem — literal repeated-key certificate bound

Under the finite hypotheses above,
```math
\boxed{
\left|\bigcup_{R\ge1}\mathcal C_R\right|\le\mathfrak B_k.
}
\tag{3}
```

Consequently, for **any fixed outer coloring** $`c_0:G\to\{0,1\}`$, independent Bernoulli-$`p`$ key bits, and
```math
C(n)=c_0(n)+E_{\kappa(n)}\pmod2,
```
one has, for $`0<p\le1/2`$ and $`0<\tau<\gamma\le1/2`$,
```math
\boxed{
\Pr(\text{some }\gamma\text{-rich progression is monochromatic})
\le
2q^{2D}p^{(\gamma-\tau)k}
+\mathfrak B_k\,p^{\lceil\tau k\rceil}.
}
\tag{4}
```

In particular, the bound is uniform over outer colorings that use the **full** label, including the first coordinates.

The proof follows.

---

## 2. All small-box returns share one direction

Fix a progression $`n_j=n_0+jd`$ having a repeated second-coordinate box. Let $`\mathcal H`$ contain every positive gap $`g<k`$ at which such a box repeats.

For $`g\in\mathcal H`$, let $`v_g`$ be the difference of the centered representatives at a corresponding pair. Each coordinate satisfies
```math
|(v_g)_i|\le2H.
```
This lift is unique: its residue modulo $`\mathbb Z^D`$ is $`g\,y(d)`$, and two possible lifts differ coordinatewise by less than $`4H<1`$.

For $`g,g'\in\mathcal H`$,
```math
g'v_g-gv_{g'}\in\mathbb Z^D.
```
Its coordinatewise absolute value is less than
```math
2H(g+g')<4kH<1.
```
It therefore vanishes. Hence there is a common real vector $`B`$ such that
```math
v_g=gB\qquad(g\in\mathcal H).
\tag{5}
```

Let $`h=\gcd\mathcal H`$. Bézout’s identity gives
```math
y(d)=\frac{\mathbf t}{h}+B\pmod{\mathbb Z^D},
\qquad
\mathbf t\in\{0,\ldots,h-1\}^D,
\tag{6}
```
and
```math
|B_i|\le\frac{2H}{h}.
\tag{7}
```

In fact, $`h`$ itself is a return gap. If a box repeats between indices $`j`$ and $`j+g`$, then $`h\mid g`$, and the sample at $`j+h`$ is represented by
```math
Y_j+\frac hg(Y_{j+g}-Y_j).
```
This convex combination belongs to the same half-open box. Thus $`h=\min\mathcal H`$, and **the two indices of each same-box pair lie in a common residue class
modulo $`h`$**; different pairs may lie in different classes.

Two arithmetic facts are essential:
```math
hB_i\in q^{-i}\mathbb Z,
\qquad
hB_i\ne0\Longrightarrow |hB_i|\ge q^{-D}\ge\alpha,
\tag{8}
```
and
```math
\boxed{q\|hB\|\ge1.}
\tag{9}
```

For (9), $`hd\ne0`$, since $`h<P`$. Write a nonzero representative of $`\lambda hd`$ as $`q^a u`$, with $`a<D`$ maximal and $`q\nmid u`$. Coordinate $`a+1`$ has circle displacement $`u/q`$, whose distance from zero is at least $`1/q`$. Its real lift is $`hB_{a+1}`$. This argument allows $`q`$ to be a proper prime power.

---

## 3. Collision-bearing residue classes are affine, and their pairs are nested

Fix a residue class $`r\bmod h`$, with $`0\le r<h`$, containing a
same-box pair. Its samples are congruent to
```math
Y_r+s\,hB.
```
Their total coordinate motion is at most
```math
k|B_i|\le2/k<1/2.
```

Suppose their centered representatives fail to follow this real affine segment. Then, in some coordinate with $`B_i\ne0`$, the closed segment meets a representative cut. Every sample of that residue class consequently satisfies
```math
\rho(y_i(n_j))\le k|B_i|.
```
Using (1) and (8),
```math
|V(y_i(n_j))|
\le2H(k|B_i|+\alpha)
\le2H(k+h)|B_i|
<h|B_i|.
\tag{10}
```
The last inequality follows from
```math
2H(k/h+1)\le\frac{2(k+1)}{k^2}<1.
```

But distinct samples in this coordinate have circle distance at least $`h|B_i|`$: their entire real displacement is less than $`1/2`$. They cannot share an interval satisfying (10), contradicting the same-box pair.

Therefore **the entire collision-bearing residue class is affine in the centered representatives**.

Its norm sequence has the form
```math
f_{r+sh}=u(s-s_*)^2+C,
\qquad
u=q^2\|hB\|^2\ge1.
\tag{11}
```

On either side of $`s_*`$, different integer samples have squared norms differing by at least one. Consequently, a pair in one unit norm band must strictly straddle $`s_*`$. This uses the sharp two-point phenomenon; it does not improve that phenomenon. The corresponding two-point lemma is also explicitly proved in the pinned refinement. [GitHub](https://raw.githubusercontent.com/rohanarun/van-der-waerden-refinement/54ac9715fceab938ca77d5980c36ab691765a04d/research-note.tex)

The segment joining a repeated-key pair contains the closest point at $`s_*`$. Convexity puts that point in the same box. Thus all repeated-key pairs in this residue class use the same box.

Their matching is **nested**: norms decrease on the left of $`s_*`$ and increase on its right, with distinct integer bands on each side. If the occurrence indices of $`r`$ selected repeated keys are
```math
j_1<\cdots<j_{2r},
```
the pairs must be
```math
(j_\ell,j_{2r+1-\ell}),
\qquad 1\le\ell\le r.
\tag{12}
```
Their gaps satisfy
```math
j_{2r+1-\ell}-j_\ell
\ge h\bigl(2(r-\ell)+1\bigr).
\tag{13}
```

This nesting is what makes the eventual rounding cost exponential in $`k`$, rather than $`k^{\Theta(k)}`$.

---

## 4. Counting certificates without enumerating the step

Write
```math
A=Y(n_0),\qquad
b=\frac{\mathbf t}{h}+B,
```
and introduce the integer representative carries $`m_j`$:
```math
Y_j=A+jb-m_j=A+jB+C_j,
\qquad
C_j=\frac{j\mathbf t}{h}-m_j.
\tag{14}
```

The preceding argument also proves that a literal key has multiplicity
at most two in any progression. All its occurrences lie in one residue
class modulo $`h`$, that class is affine, and each half-line of its
quadratic norm contains at most one occurrence in a unit band. A key
occurring only once causes no issue. This two-point conclusion is the
elementary sharpening already present in the prior refinement.

A certificate can be encoded by its actual start $`n_0`$, the data $`h,\mathbf t`$, the augmented word consisting of literal boxes and carries, its selected occurrence positions, and its integer norm bands.

The numbers of choices for the first four components are bounded by
```math
q^D,\qquad k^{D+1},\qquad T_{\mathrm{aug}},\qquad 2^k,
\tag{15}
```
respectively: there are at most $`k`$ possible $`h`$'s and at most
$`k^D`$ vectors $`\mathbf t`$; the last factor records the set of all
selected occurrence positions. An encoding may represent unrealizable
data, which only enlarges the upper bound.

### Why the augmented-word count is small

For one scalar coordinate allow
```math
A_i\in[-1/2,1/2),\qquad b_i\in[-1,2].
```
These ranges contain every actual value. All unreduced samples $`A_i+jb_i`$ lie between $`-k`$ and $`2k`$. Comparisons with the relevant real translates of mesh endpoints use at most
```math
k(3k+3)J\le6k^2J
```
lines in the two parameters. Their signs determine both the **literal interval** and the representative carry, including endpoint equalities.

An equality-inclusive arrangement of $`s`$ hyperplanes in dimension $`e`$ has at most
```math
(e+1)^2(s+1)^e
```
sign vectors. Indeed, choose independent zero equations defining a face’s affine hull, and count strict regions on that hull; summing gives
```math
\sum_{d=0}^e\binom sd\sum_{j=0}^{e-d}\binom sj
\le(e+1)^2(s+1)^e.
```
This is the arrangement bound used in pinned Section 03, including its treatment of equality. In dimension two, multiplying over coordinates gives $`T_{\mathrm{aug}}`$. [GitHub](https://raw.githubusercontent.com/openai/math/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/03-counting.tex)

### The repeated-pair identity

For a selected pair $`j<\ell`$, equality of its box and (5) imply
```math
C_j=C_\ell.
```
Set
```math
u=q^2\|B\|^2,\qquad
\theta_j=q^2\|A+C_j\|^2,\qquad
\Delta=f_\ell-f_j.
```
Equality of the integer norm bands means $`|\Delta|<1`$. Expanding the two squared norms gives the exact identity
```math
\boxed{
f_j=\theta_j-j\ell u+\frac{j}{\ell-j}\Delta.
}
\tag{16}
```

For fixed start, $`h,\mathbf t`$, and augmented word, every $`\theta_j`$ is fixed. **The orientation of $`B`$ has disappeared from (16); the only remaining scalar parameter is $`u`$**, apart from the bounded errors.

For every realizable code,
```math
|A_i+C_{j,i}|
\le\tfrac12+2/k\le1,
```
so
```math
0\le\theta_j\le Dq^2,\qquad 0\le u\le Dq^2.
```
As $`u`$ varies over this deliberately enlarged interval, consider
```math
\theta_j-j\ell u.
```
When $`j=0`$, the function is constant and its floor is fixed, including
when its value is an integer; it creates no threshold crossing. For every
nonconstant function, the value range has length at most $`Dk^2q^2`$,
so there are at most $`Dk^2q^2+1`$ integer-level crossings. There are
at most $`k/2`$ selected pairs. Thus fewer than $`3Dk^3q^2`$
threshold points suffice altogether. Including equality points, fewer than
```math
16Dk^3q^2
\tag{17}
```
one-dimensional cells determine all their integer parts.

Inside one cell, the band for a pair of gap $`g=\ell-j`$ has at most
```math
2\left\lceil\frac{k}{g}\right\rceil+1
\le\frac{5k}{g}
\tag{18}
```
possibilities.

Suppose the selected certificate has $`r_a`$ pairs in residue class $`a\bmod h`$. By nesting,
```math
\prod_{\text{pairs in class }a}g\ge h^{r_a}r_a!.
```
Therefore the total rounding cost is at most
```math
\prod_{a=0}^{h-1}\frac{(5k/h)^{r_a}}{r_a!}
\le \exp(5k).
\tag{19}
```
Here each factor is bounded by the exponential series with argument $`5k/h`$.

The selected position set determines its matching uniquely by (12); there is no additional matching factor. Finally,
```math
2^k\exp(5k)<512^k,
```
since $`\exp(1)<3`$ and $`2\cdot3^5=486<512`$.

Multiplying (15), (17), and (19) proves
```math
|\mathcal C|
\le q^Dk^{D+1}T_{\mathrm{aug}}
(16Dk^3q^2)512^k
=\mathfrak B_k.
```

All boxes and bands remain literal. Unrealizable codes and duplicate descriptions merely enlarge this upper bound.

---

## 5. From consistent full prescriptions to the weighted cover

Form the family of literal pairs $`(F,Z)`$ for rich progressions and targets. First discard $`F\cap Z\ne\varnothing`$, then remove duplicate pairs. Their exact probabilities are
```math
p^{|F|}(1-p)^{|Z|}.
\tag{20}
```

Here, for a prescribed target bit, $`F`$ is the set of literal keys at
positions whose outer bit differs from that target, and $`Z`$ is the set
at positions whose outer bit equals it. Thus $`F\cap Z\ne\varnothing`$
would require the same perturbation variable to be both zero and one.
All these families and selections are fixed before the key bits are sampled.

Fix $`0<\tau<\gamma`$.

If
```math
|F|\ge(\gamma-\tau)k,
```
the event has probability at most $`p^{(\gamma-\tau)k}`$. There are at most $`2N(N-1)`$ distinct full events, giving the first term of (4).

Otherwise, take a witnessing rich progression. Let $`r_F`$ be the number of its flipped keys appearing twice. Consistency and multiplicity two give the exact count
```math
\#\{\text{opposite-outer-bit positions}\}=|F|+r_F.
\tag{21}
```
Hence
```math
r_F\ge\gamma k-|F|>\tau k.
```

Select $`R=\lceil\tau k\rceil`$ of these repeated flipped keys, using any fixed deterministic ordering. Their literal set $`S`$ belongs to $`\mathcal C_R`$, and the full event implies
```math
B_S=\{E_\kappa=1\text{ for every }\kappa\in S\}.
```
Thus
```math
\Pr(B_S)=p^R,\qquad
\sum_{S\in\mathcal C_R}\Pr(B_S)
\le\mathfrak B_kp^R.
\tag{22}
```

Full events assigned to the same $`S`$ need not agree: their **union is contained in** $`B_S`$. This is why omitting their remaining flip and nonflip prescriptions is legitimate. Opposite-outer-bit collisions were already discarded by consistency; no first-coordinate information is assumed recoverable from a key.

Equations (20)–(22) prove (4). No independence between events, progressions, or certificates is asserted.

---

## 6. Exact rational parameters and the unchanged transfers

Retain
```math
D=\lceil k^a\rceil,\quad M=\lceil k^m\rceil,\quad p=k^{-b},
```
with
```math
a,b,c>0,\qquad 2a<m<1,\qquad b<a,\qquad 2a+b<1,
\tag{23}
```
Fix also
```math
0<\varepsilon<1/2,\quad 0<\varepsilon_{\rm reg}\le1/2,
\quad 0<\delta<1,\quad
0<\gamma<(1/2-\varepsilon)(1-\varepsilon_{\rm reg})(1-\delta).
```
All these constants are fixed before $`k`$ grows. Set
```math
L=\lceil\log k\rceil,\quad h_0=DL^2,\quad
\eta=\varepsilon_{\rm reg}/(8D),\quad
\lambda=\prod_{\substack{\ell\le h_0\\\ell\ {\mathrm{prime}}}}
\ell^{\lfloor\log(2M)/\log\ell\rfloor}.
```
For any source prime $`P\in(k,2k^2]`$, let $`q`$ be the least positive
power of $`P`$ at least $`k^{ck/D}`$. The source's elementary prime
bound supplies such a $`P`$ for all sufficiently large $`k`$. Since
$`h_0<2M<k<P`$ eventually, $`\lambda`$ is a unit modulo $`q^D`$.
Each prime-power component with prime at most $`h_0`$ of any
$`h\le2M`$ divides $`\lambda`$, and
$`\log\lambda\le h_0\log(2M)`$. In particular $`h\mid\lambda`$
for every $`h\le h_0`$.

Let $`U`$ partition $`[0,1)`$ into the $`k^2\lambda`$ half-open
intervals of length $`1/(k^2\lambda)`$, and write the **full** label as
```math
\mathcal L(n)=((U(x_i(n)))_{i=1}^D,(V(y_i(n)))_{i=1}^D).
```

The remaining imported input is:

> **Sharpened outer input.** For sufficiently large $`k`$, one globally defined full-label coloring $`c_*`$ has a pullback $`c_0`$ for which every nonzero-step cyclic progression is either $`\gamma`$-rich or affine in all centered second coordinates, provided
> ```math
> \gamma<
> \left(\tfrac12-\varepsilon\right)
> (1-\varepsilon_{\rm reg})(1-\delta).
> ```

Precisely, the imported assertion has the quantifiers: for each fixed
choice of $`a,m,c,\varepsilon,\varepsilon_{\rm reg},\delta,\gamma`$
above, there is $`K_{\rm outer}`$, uniform over the allowed source primes,
such that for every $`k\ge K_{\rm outer}`$ there is **one** map
$`c_*:U^D\times V^D\to\{0,1\}`$. Its pullback
$`c_0(n)=c_*(\mathcal L(n))`$ satisfies the alternative for **every**
nonzero-step cyclic progression simultaneously. This coloring is frozen
before introducing the independent key bits.

This is the assertion obtained in
[sharpened-region-proof.md](sharpened-region-proof.md) from the upstream
outer local lemma and rich/affine dichotomy. It is an explicit dependency
of this note, not a new theorem proved here. The corresponding pinned
upstream source is [GitHub](https://raw.githubusercontent.com/openai/math/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/04-outer.tex)

For the prescribed prime-power rounding,
```math
ck\log k\le D\log q
\le ck\log k+D\log(2k^2).
```
Also the actual mesh satisfies
```math
J
=2\left\lceil k^2\log(1+q^{D+1}/2)\right\rceil
\le2k^2(D+1)\log q+2
=O_c(k^3\log k).
```
Consequently, the explicit bound (2) gives
```math
\log\mathfrak B_k
\le ck\log k+O_c(k+D\log k+\log q)
=ck\log k+o(k\log k).
\tag{24}
```

Both rich-event terms therefore tend to zero when
```math
\boxed{
2c<b(\gamma-\tau),\qquad c<b\tau.
}
\tag{25}
```
Taking $`\tau=\gamma/3`$ gives $`c<\gamma b/3`$.

### An explicit choice

Use exactly the given outer exponents and balance constants, changing the coefficient to
```math
\begin{gathered}
a=\frac{333}{1000},\quad m=\frac45,\quad b=\frac{331}{1000},\\
\varepsilon=\varepsilon_{\rm reg}=\delta=\frac1{200},\\
\gamma=\frac{97}{200},\quad
\tau=\frac{97}{600},\quad
\boxed{c=\frac1{19}}.
\end{gathered}
```

The margins are:

| Requirement | Exact positive margin |
|---|---:|
| $`m-2a`$ | $`67/500`$ |
| $`1-m`$ | $`1/5`$ |
| $`a-b`$ | $`1/500`$ |
| $`1-2a-b`$ | $`3/1000`$ |
| $`(\frac12-\varepsilon)(1-\varepsilon_{\rm reg})(1-\delta)-\gamma`$ | $`40499/8000000`$ |
| $`b(\gamma-\tau)-2c`$ | $`10033/5700000`$ |
| $`b\tau-c`$ | $`10033/11400000`$ |

For comparison with the earlier sufficient region, $`c-1/24=5/456`$.
This is a comparison, not a required margin.

For every fixed $`0<c<1/18`$, first choose $`0<b<1/3`$
sufficiently close to $`1/3`$ that $`c<b/6`$. Choose
$`b<a<(1-b)/2`$ and $`2a<m<1`$. Next choose
$`3c/b<\gamma<1/2`$, and positive fixed
$`\varepsilon,\varepsilon_{\rm reg},\delta`$ sufficiently small
that the outer balance inequality holds. With $`\tau=\gamma/3`$,
all required inequalities are strict. Thus every fixed positive
$`c<1/18`$ is admitted. Neither the endpoint $`1/18`$ nor an intrinsic
barrier is asserted.

### Affine events remain unchanged

For completeness, explicit bounds are available without introducing another conditional counting hypothesis. Put
```math
F_{\rm full}=k^2\lambda+J,\qquad
T_{\rm glob}^{*}
=\left[9(3k^2F_{\rm full}+1)^2\right]^{2D},
```
and $`s_{\rm aff}=k(Dq^2+2)`$.

For completeness, $`T_{\rm glob}^*`$ is an explicit bound on literal
full-label words. For one circle coordinate and a partition of size at
most $`F_{\rm full}`$, the $`k`$ samples are represented by
$`A+jb`$ with $`A`$ in a unit interval and $`b\in[0,1)`$.
At most $`3k^2F_{\rm full}`$ translated-endpoint lines determine
its word. The dimension-two arrangement bound, multiplied over the
$`2D`$ coordinates, gives the displayed bound. Allowing the first
and second coordinates to vary independently only enlarges the family.

An affine norm sequence is
```math
f_j=\theta_0+\theta_1j+\theta_2j^2.
```
For the actual centered points $`0\le f_j\le Dq^2/4`$.
Comparisons with the possible integer norm levels use at most
$`s_{\rm aff}`$ hyperplanes in the three real coefficients.
The three-parameter equality-inclusive arrangement count gives
```math
T_{\rm aff}\le16T_{\rm glob}^{*}(s_{\rm aff}+1)^3.
```
A full-label word determines the frozen outer bits and the literal
second-coordinate boxes; together with the norm-band word it determines
the full signature $`((c_0(n_j),\kappa(n_j)))_j`$. This is why the
affine count requires the full-label pullback hypothesis even though the
finite rich-event theorem allows any fixed outer coloring.

A consistent signature and a target prescribe at least $`k/2`$
distinct key variables by multiplicity two. Since $`p\le1/2`$, each
prescribed value has probability at most $`1-p`$; the event has
probability at most $`(1-p)^{k/2}`$. Inconsistent prescriptions are
empty. There are two targets per signature. This is the pinned
affine-signature argument with the prior refinement's two-point
sharpening. [GitHub](https://raw.githubusercontent.com/openai/math/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/06-perturbation.tex)

Thus a sufficient finite probability criterion, conditional on the stated
outer input and using the other pinned lemmas proved in the source, is
```math
\boxed{
2q^{2D}p^{(\gamma-\tau)k}
+\mathfrak B_kp^{\lceil\tau k\rceil}
+32T_{\rm glob}^{*}(s_{\rm aff}+1)^3(1-p)^{k/2}
<1.
}
\tag{26}
```

The unchanged dilation estimate yields
```math
\log T_{\rm aff}
=O\!\left(k^{2a}\log^3k+k^{1-a}\log k\right)
=o(k^{1-b})
```
under precisely $`2a+b<1`$ and $`b<a`$. Therefore the last term also tends to zero. All estimates are uniform over the permitted source primes $`P`$.

All events are evaluated in one product space of literal-key bits after
the outer coloring is fixed. Rich and affine classes may overlap, which
only enlarges their union bound. Once (26) holds, the complement of the
bad-event union has positive probability. One deterministic choice of
all key bits therefore gives **one global two-coloring** of $`G`$
without a monochromatic nonzero-step $`k`$-term progression.

For fixed parameters the three terms in (26) tend to zero uniformly over
the allowed primes: the first two have negative leading coefficients
times $`k\log k`$, and the third has logarithm
$`-k^{1-b}/2+o(k^{1-b})`$. Choose one $`k_0`$ exceeding the outer
threshold, the prime and scale thresholds, the threshold $`p\le1/2`$,
and a threshold making (26) less than one. No subsequent choice of
$`r`$ affects $`k_0`$. This proves existence of a threshold, not a
numerical value for it.

### Digit product, uniform in $`r`$

Let $`r\ge2`$ be any integer and $`s=\lfloor\log_2r\rfloor`$.
Color each integer in $`[0,N^s)`$ with base-$`N`$ digits $`n_0,\ldots,n_{s-1}`$ by
```math
(C(n_0),\ldots,C(n_{s-1})).
```
For a positive progression difference $`d<N^s`$, choose the largest $`i`$ with $`N^i\mid d`$, and put $`e=d/N^i`$. The identity
```math
\left\lfloor\frac{a+jd}{N^i}\right\rfloor
=
\left\lfloor\frac a{N^i}\right\rfloor+je
```
shows that the $`i`$-th digits form a cyclic progression of nonzero step. It cannot be monochromatic. This is the unchanged digit product of Section 07. [GitHub](https://raw.githubusercontent.com/openai/math/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/07-transfers.tex)

There are at most $`2^s\le r`$ color tuples. Translation by one
gives a coloring of $`\{1,\ldots,N^s\}`$ with no monochromatic
$`k`$-term progression. Hence, conditional on the sharpened outer input,
```math
W_r(k)>N^{\lfloor\log_2r\rfloor}
\ge k^{(1/19)k\lfloor\log_2r\rfloor}.
```
The threshold on $`k`$ is fixed before $`r`$ is introduced.

---


## 7. Dependency and review boundary

The proof chain is:

1. The explicit cyclic coordinates and mesh give the common-return
   geometry, affine collision classes, multiplicity two, and nested pairs
   in Sections 1–3. The basic two-point observation is credited to the
   existing refinement, not claimed anew.
2. The augmented word and repeated-pair identity in Section 4 eliminate
   the step's directional entropy and prove the finite certificate count.
   All identities keep actual interval and norm-band labels.
3. Section 5 proves a weighted cover of consistent rich events. It never
   identifies different full prescriptions or requires independent events.
4. The single imported outer assertion of Section 6 covers every cyclic
   progression by the rich or affine class. Its separate proof depends on
   literal global/anchored pattern counts, the asymmetric local lemma,
   long-period eligibility and regularity, and the short-period lift.
   Those dependencies are in the pinned source Sections 02–05 and
   [sharpened-region-proof.md](sharpened-region-proof.md).
5. The affine signature count, strict parameter inequalities, and digit
   product are proved in Section 6, following the pinned source's
   Sections 06–07. They yield the conditional interval theorem uniformly
   for every integer $`r\ge2`$.

For the imported shortened cutoff, the exact logarithmic expression is
$`6\log(CD^2L^2)/L^2`$, with $`L=\lceil\log k\rceil`$; replacing
$`L`$ by $`\log k`$ is an asymptotic estimate, not an equality. In the
no-heavy-label branch of the imported outer argument, all positions form
the light family and are balanced directly; a closest-return gap is only
chosen in the branch with a heavy label. These clarifications do not
strengthen the imported theorem.

The new claim relative to the pinned repository is the certificate cover
with leading entropy $`q^D`$, the region $`c<\gamma b/3`$, and its
conditional $`c=1/19`$ (more generally every fixed $`0<c<1/18`$)
application. It does not prove a stronger key-multiplicity lemma, construct
a finite coloring at a practical size, or settle mathematical priority.
Conventional source review and exact finite arithmetic can support the
draft, but neither is a formal proof certificate. No finite experiment is
used to infer a universal geometric or asymptotic statement.
