# An effective completion of the pinned van der Waerden construction

**Date:** 13 October 2026.  
**Scope:** a self-contained completion of the attributed construction at the exact OpenAI, PR4, PR6 and PR7 pins listed below. Current public heads were checked separately; no source headline theorem is used as a black box.  
**Status:** correction revision following an Opus review; publication is conditional on exact-revision acceptance. Independent human review and formal verification are not claimed.

**Preparation and attribution:** prepared for Artus Krohn-Grimberghe with OpenAI Pro and Codex assistance. The coefficient range, carry-rank split, matched digit rank and run method are already public proposals by DaysSky with Claude assistance. This submission supplies a full proof completion and exact effectiveness specification, without an independent-discovery or priority claim.

**Contents:** complete analytic proof, strict parameter and all-larger-input certificate, finite outer/key generator, exact arithmetic decisions and output costs. [GENERATOR.md](GENERATOR.md) gives an additional integer-only exhaustive-table implementation specification. [SOURCE-LEDGER.md](SOURCE-LEDGER.md) and [DEPENDENCIES.json](DEPENDENCIES.json) supply the full dependency and attribution ledger.

**Admitted input:** an integer k is admitted for a fixed parameter tuple exactly when k is at least the threshold 2^t returned by Section 12.1 for that tuple. In the general theorem the tuple is the rule in Section 13 for the supplied rational c; in either literal theorem it is that theorem's displayed tuple. There is no subsequence or congruence restriction. A supplied P must independently be a prime with k < P <= 2k^2. A smaller k failing this admission test is outside the guarantee, even if a valid small coloring is found independently.

## 1. Result and interpretation

Write $W_r(k)$ for the least interval length forcing a monochromatic nonconstant $k$-term arithmetic progression in every coloring with at most $r$ colors. The interval convention is $[1,L]$; the generator first colors $[0,L-1]$ and translates by one.

**Theorem 1 (effective digit-rank/run construction).** For every rational $0<c<1/8$, the parameter rule and terminating threshold procedure in Sections 12–13 compute an integer $K(c)$. For every integer $k\ge K(c)$, every prime $k<P\le2k^2$, and every integer $r\ge2$, the finite algorithm in Section 15 constructs a two-coloring of $\mathbb Z/q^D\mathbb Z$ without a monochromatic $k$-term progression of nonzero step. Here $q$ is exactly the prescribed least positive power of $P$. Its digit product colors an interval of the exact integer length
$$
L=N^s,\qquad N=q^D,\qquad s=\lfloor\log_2r\rfloor,
$$
with at most $2^s\le r$ colors, and proves
$$
\boxed{W_r(k)>N^{\lfloor\log_2r\rfloor}\ge k^{ck\lfloor\log_2r\rfloor}.}
$$
There is no dependence of $K(c)$ on $P$ or $r$.

For the **literal PR7 parameters**
$$
a=49/100,\ m=99/100,\ b=\gamma=97/200,\quad
\delta=\epsilon=\epsilon_{\rm reg}=1/200,\quad \delta_s=1/2,\quad c=1/9,
$$
one valid, deliberately conservative threshold is
$$
\boxed{K=2^{33\,554\,432}.}
$$
The threshold is a mathematical all-larger-input certificate, not an executed coloring of a group of that size.

**Theorem 2 (independent PR6 fallback).** Retaining the literal PR6 choices
$$
a=333/1000,\quad m=4/5,\quad b=331/1000,\quad c=1/16,
$$
and the same $\delta,\epsilon,\epsilon_{\rm reg},\gamma$, the carry-rank/anchored-certificate proof in Section 10, followed by the older affine estimate, proves the same conclusion with the same displayed threshold. It does not use the digit-rank improvement or the third outer family/run estimate.

These results do **not** assert the endpoint coefficient $1/8$, a practical construction, a new finite van der Waerden record, or an algorithmic local-lemma running-time improvement. The supremum of the strict region is not an attained coefficient. The end-to-end proof here does not invoke the upstream coefficient-$10^{-5}$ headline theorem as a black box.

The two useful repairs to the terse public presentations are proof-level, with no coefficient loss: (1) justify single runs using distinct real lifts of a *small* circular interval, not an unrestricted assertion about monotone circular paths; (2) turn the continuous pattern families into finite, exactly decidable families, retaining the upstream equality-inclusive counting. For certificate counting we also explicitly encode a deterministic repeated pair in each collision class. This costs only a bounded exponential in $k$ and removes any dependence on an implicit reconstruction of the pairs.

## 2. Provenance and dependency policy

The original 46 source records in the `source_inventory` of [DEPENDENCIES.json](DEPENDENCIES.json) were checked for size, SHA-256 and Git blob identity. The 46 retained exact-pin public API responses were independently decoded and matched to those bytes; this is not a claim to have newly re-fetched all paths. The additional exact base sharpened-region blob is recorded separately in the updated source inventory. The twelve selected current/historical upstream pairs have identical bytes. The source inventory authenticates the inspected bytes relative to the saved receipts; it is not a signed release certificate. Source programs were treated as inert text. The source snapshot, original Pro report and independently reviewed archive remain preserved locally; no raw private chat export is part of this proposal.

The source pins are:

| Code | Repository/revision | Role |
|---|---|---|
| U | `openai/math` at `1581d4cbdd69a0faf34b2089614fe2a814316a6a` | Coordinate model, meshes, arrangements, local patterns, drift, perturbation, product |
| UH | same repository at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` | Historical manifest; selected bytes equal U |
| B | `rohanarun/van-der-waerden-refinement` at `54ac9715fceab938ca77d5980c36ab691765a04d` | Two-point norm-band lemma and sharpened outer construction: shortened dilation, regularity scale, half-balance, light-outside-heavy-blocks family and sharpened dichotomy |
| P4 | PR4 head `4b4e80ea5e0ffec956577004905f22659af0bff5`, served under both `rohanarun/van-der-waerden-refinement` and `artuskg/van-der-waerden-refinement` | Repeated-key structure and anchored certificate precursor |
| P6 | `DaysSky/van-der-waerden-refinement` at `fc5738bfda508566e7b4ce706c22bbb2b9194226` | Carry-rank split (rank-certificate-proof.md Lemmas A–C) and c=1/16 tuple; fork copy of the base sharpened-region note |
| P7 | same fork at `987c96cfda59b65728ae4dcd5adc8a64ff95bab2` | Matched digit rank and short-period runs |

[SOURCE-LEDGER.md](SOURCE-LEDGER.md) maps the definitions and results below to individual files, exact commits, and blobs. It also records the two additional P6 reads: `rank-certificate-proof.md`, blob `33acb0fec1f3c64a27ec60eb60e1be24b7876f89`, and `sharpened-region-proof.md`, blob `7bf21638c2d8ca50e3cd47a6289931f0d45bd80f`. They verify that the included P7 copies are also the intended P6 source statements. No later revision is substituted.

Attribution follows the public files: the basic construction is upstream's; base B supplies the two-point norm-band lemma and sharpened outer construction; P4 supplies the repeated-key/anchored-certificate precursor; P6 supplies the carry-rank split; P7 supplies matching digit rank and the run-based non-rich estimate. The proofs below establish the ingredients used rather than importing their repository status as evidence of correctness. Unrelated matrix-multiplication material is not used. Supplied source programs were inspected, not executed. The earlier reviewer's independently authored exact checks are separate finite corroboration, recorded in [THRESHOLDS.json](THRESHOLDS.json); they do not establish a global premise by sampling.

## 3. Literal finite definitions

Let $\ell=\log k$, with natural logarithm, and use rational parameters satisfying
$$
0<a,b,c,\quad 2a<m<1,\quad b<a,\quad a+b<1,
$$
$$
0<\epsilon<1/2,\quad 0<\epsilon_{\rm reg}\le1/2,\quad
0<\delta,\delta_s<1,\quad
0<\gamma<(1/2-\epsilon)(1-\epsilon_{\rm reg})(1-\delta),\quad
2c<\gamma b. \tag{3.1}
$$
For the carry-affine route replace $a+b<1$ by $2a+b<1$, and $2c<\gamma b$ by $5c/2<\gamma b$. The extra $\delta_s$ is unused on that route.

Set, with these exact ceilings,
$$
D=\lceil k^a\rceil,\ M=\lceil k^m\rceil,\ L_0=\lceil\log k\rceil,
\quad h_0=M_s=DL_0^2,\quad H=k^{-2},\quad p=k^{-b},\quad
\eta=\epsilon_{\rm reg}/(8D).
$$
For each prime $\ell'\le h_0$, include the largest power of $\ell'$ not exceeding $2M$, and multiply these powers to obtain $\lambda$. This is exactly the source dilation; it can be computed by integer multiplication and division without logarithms. If $h\le2M$ and $t\in\mathbb Z$, every prime $\ell'\le h_0$ satisfies $v_{\ell'}(\lambda)\ge v_{\ell'}(h)$. Thus no such prime divides $h/\gcd(h,\lambda t)$. That denominator is either one or has a prime factor exceeding $h_0$, so it exceeds $h_0$. In particular $h\mid\lambda$ for every $h\le h_0$, because every prime factor of such an $h$ is at most $h_0$.

For $k\ge16$ a prime $P\in(k,2k^2]$ exists. Here is an explicit version of the source argument. With $n=k^2$, every prime valuation in $\binom{2n}{n}$ is at most $\lfloor\log_{\ell'}(2n)\rfloor$. If all its prime factors were at most $k$, it would be at most $(2k^2)^k$, whereas the central binomial coefficient is at least $4^{k^2}/(2k^2+1)$. For $k\ge16$,
$\log4>1$, $\log(2k^2),\log(2k^2+1)\le3\log k$, and $\log k\le k/4$. Thus the logarithm of the lower bound is at least $k^2-3k/4$, strictly larger than $3k^2/4$, an upper bound for the other logarithm. Trial division therefore finds an allowed prime.

Let $q=P^e$, with the smallest positive integer $e$ such that $q\ge k^{ck/D}$, and let $N=q^D$. If $c=u/v$ in lowest terms, the exact test is
$$
q^{vD}\ge k^{uk}.
$$
Minimality, including the case $e=1$, gives
$$
ck\ell\le D\log q\le ck\ell+D\log(2k^2). \tag{3.2}
$$
The scale tests in Section 12 imply $h_0<2M<k<P$, so $\gcd(\lambda,q)=1$. Every nonzero element of $G=\mathbb Z/N\mathbb Z$ has order at least $P>k$. Consequently all $k$ terms in every progression considered below are distinct.

For $1\le i\le D$,
$$
x_i(n)=n/q^i\pmod1,\qquad y_i(n)=\lambda n/q^i\pmod1.
$$
Use representatives $\widehat x_i\in[0,1)$, $Y_i=\widetilde y_i\in[-1/2,1/2)$. Write $\rho(y)=\operatorname{dist}_{\mathbb T}(y,1/2)$. Put
$$
H_x=H/\lambda,\quad \alpha=q^{-(D+1)},\quad Q=1+1/(2\alpha),\quad
m_V=\lceil k^2\log Q\rceil,\quad z=Q^{1/m_V},\quad a_j=\alpha(z^j-1).
$$
The notation $m_V$ avoids confusing the mesh count with exponent $m$.

The $U$-intervals are $[tH_x,(t+1)H_x)$, $0\le t<k^2\lambda$. The $V$-intervals, with exactly the source convention, are
$$
[-1/2+a_j,-1/2+a_{j+1}),\qquad
[1/2-a_{j+1},1/2-a_j),\quad 0\le j<m_V.
$$
Thus zero belongs to the interval on its right; the cut belongs to the interval beginning at $-1/2$. Write $J=2m_V$,
$$
\mathcal L=U^D\times V^D,\quad B=|\mathcal L|=(k^2\lambda)^D J^D,
$$
$$
L(n)=((U(x_i(n)))_i,(V(y_i(n)))_i),\qquad
\kappa(n)=((V(y_i(n)))_i,\lfloor f(n)\rfloor),\quad
f(n)=q^2\sum_{i=1}^D Y_i(n)^2. \tag{3.3}
$$
Labels and keys are **literal interval identities**, not names assigned after quotienting a word. There are at most
$J^D(\lfloor Dq^2/4\rfloor+1)$ possible keys, and at most $Z\le N$ keys actually used by group points.

Once $c_*:\mathcal L\to\{0,1\}$ is fixed, independently assign one Bernoulli$(p)$ bit $E_\kappa$ to each used key and define
$$
C(n)=c_*(L(n))\mathbin{\mathsf{xor}}E_{\kappa(n)}. \tag{3.4}
$$
All occurrences of a key share that one bit. Unused keys can equivalently be supplied with independent bits and then ignored.

## 4. Mesh and finite arrangement lemmas

All bounds in this section hold under the scale conditions certified in Section 12. In particular $k\ge16$, $q>k$, $D\le k/64$, $2M/k\le1/16$, and $c<1/8$.

### 4.1 Widths, neighborhoods, and regular outputs

Let $\theta=(\log Q)/m_V$. Since $\log Q\ge1$,
$H/2\le\theta\le H$. On either interval indexed by $j$, if $b_0=\alpha e^{j\theta}$, the value of $\rho+\alpha$ on the closure ranges from $b_0$ to $b_0e^\theta$, and its width is $b_0(e^\theta-1)$. The elementary inequalities
$1-e^{-t}\ge t/2$ and $e^t-1\le2t$, $0\le t\le1$, prove
$$
\tfrac14H(\rho(y)+\alpha)\le |I|\le2H(\rho(y)+\alpha)\le2H
\quad(y\in\overline I). \tag{4.1}
$$
The inequality holds at endpoints as well.

For an interval $I$ of width $w$, let $N(I)$ be the closed circular $w$-neighborhood of $\overline I$. Fix $y_0\in\overline I$ and $r_0=\rho(y_0)+\alpha$. Every point of $N(I)$ is within $2w$ of $y_0$, so its $\rho+\alpha$ is at least $(1-4H)r_0\ge r_0/2$. An interval whose closure meets $N(I)$ has width at least $Hr_0/8\ge w/16$. Successive endpoints in the arc $N(I)$, of length $3w<1$, are therefore separated by at least $w/16$; there are at most **49** such endpoints. This includes the circular cut and closed-neighborhood equalities.

Define $V_\eta(y)=V(y)$ when $\rho(y)\ge\eta$, and dummy $*$ otherwise. On an arc of length at most $4H$, the region $\rho\ge\eta$ has at most two components. Consecutive relevant mesh endpoints are separated by at least $H\eta/4$. Including both threshold points gives at most
$$
16/\eta+4\le B_0D,\qquad B_0=\lceil128/\epsilon_{\rm reg}+4\rceil \tag{4.2}
$$
breakpoints. Equality $\rho=\eta$ produces the actual label, not a dummy; a breakpoint can have an output different from both adjacent open intervals.

### 4.2 Affine sign arrangements, including all faces

For $s$ affine comparisons in $e$ real variables, the number of realized sign vectors in $\{-,0,+\}^s$, on any subset of parameter space, is at most
$$
\mathcal A(e,s)=(e+1)^2(s+1)^e. \tag{4.3}
$$
Indeed, adding hyperplanes one by one gives at most $\sum_{j=0}^e\binom sj$ strict-sign regions by induction and Pascal's identity. A realized set of zero equations has an affine intersection of some codimension $d$; select $d$ independent zero equations defining that intersection. The remaining strict signs occur in dimension $e-d$. Summing
$\binom sd\sum_{j=0}^{e-d}\binom sj$ over $d$ gives (4.3). Identically zero comparisons are forced signs and can be removed; inconsistent equations create no outcomes. Repeated hyperplanes and degenerate cells do not increase the bound. Restriction to a realizable set can only remove sign vectors.

This is a count of outcomes, not an assumption that every formal sign cell is realizable. Section 14 supplies an exact realization test for the event families that actually need enumeration.

### 4.3 Explicit global and anchored counts

A scalar circle word $a+jb$, $a,b\in[0,1)$, in a partition with $F$ endpoints is determined by at most $3k^2F$ affine comparisons with lifted endpoints. Hence
$$
T_{\rm glob}\le[9(3k^2(k^2\lambda+J)+1)^2]^{2D}. \tag{4.4}
$$
Independent scalar starts and steps enlarge the actual family, which is the correct direction for this bound. Equality signs assign the literal half-open intervals.

For eligible long-period patterns, choose $h_0<h\le2M$, $t\in\{0,\ldots,h-1\}^D$, and paths
$$
X_z=x+z(t+u)/h,\qquad Y_z=y+z(\lambda t+v)/h\pmod1,\quad 0\le z<h. \tag{4.5}
$$
Coordinate $i$ is stationary if $s_i=h/\gcd(h,\lambda t_i)=1$, and rotating otherwise. All rotating $s_i$ exceed $h_0$: the dilation contains every small-primary part of $h$. A position is regular precisely when every rotating coordinate has $\rho\ge\eta$. Record its full label, or a dummy at nonregular positions. Eligibility means: at least $h/2$ regular positions; their full labels pairwise distinct; $|u_i|\le H_x$; rotating $|v_i|\le H$; and stationary $|v_i|\le|V(Y_{z,i})|$ at **every regular** position.

Through any fixed full label, the number of pairs $(t,\text{eligible word})$ for a fixed $h$ is at most
$$
A_h=h^{D+1}[9(B_0Dh+1)^2]^{2D}. \tag{4.6}
$$
To prove this, choose the label's position $z_0$, then anchor each scalar start in its specified interval. At another position the expression is
$a+\tau_z+(z-z_0)b/h$, with fixed rational translation $\tau_z$. In an $x$-coordinate its range has width at most $3H_x$, meeting at most four uniform endpoints. In a stationary $y$-coordinate the drift is at most the anchor width, translation is integral, and at most 49 endpoints are relevant. In a rotating coordinate the range has width at most $4H$, and (4.2) bounds its truncated outputs by $B_0D$ breakpoints. Since each real target range has length below one, the magnitude of $\tau_z$, even when it contains $\lambda$, adds no multiplicity of endpoint lifts. Apply (4.3) in two variables for each of $2D$ coordinates, then multiply by $h^Dh$. The scalar truncated outputs determine exactly which positions are dummy; there is **no extra arbitrary mask factor**.

An abstract short-period word is a full-label word of length $k$ admitting, for some $1\le h\le h_0$, $t\in\{0,\ldots,h-1\}^D$,
$$
X_j=x+j(t+u)/h\pmod1,\quad Y_j=A+jw\pmod1,
\quad |u_i|\le2MH_x/k,\quad |w_i|\le4MH/(hk). \tag{4.7}
$$
No condition that $A+jw$ remain in the centered cube is imposed here. Through any fixed full label there are at most
$$
A_s=k h_0^{D+1}
[9(k(4M+4)+1)^2]^D
[9(2k(J+1)+1)^2]^D \tag{4.8}
$$
such words. Anchor at one occurrence. For each $x$-coordinate the target interval has length at most $H_x(1+4M/h)$, so $4M+4$ endpoints per position suffice. For each $y$-coordinate the total possible target range has length below one, and $2(J+1)$ lifted endpoints per position suffice, including any cut. Two-variable arrangements, $k$ anchor positions, and at most $h_0^{D+1}$ choices of $h,t$ give (4.8). Again these are literal labels, and all faces are included.

We will use the following explicit consequences, proved directly from (3.2), $D\le2k^a$, $L_0\le2\ell$, and the scale tests:
$$
J\le k^6,\quad \log q\le k^{1-a}\ell,\quad
\log\lambda\le16k^a\ell^3,\quad
\log T_{\rm glob}\le256k^{2a}\ell^3, \tag{4.9}
$$
$$
\log A_h\le C_LD\ell,\quad C_L=32+4\lceil\log_2(B_0+1)\rceil,
\qquad \log A_s\le40D\ell. \tag{4.10}
$$
For completeness, $(D+1)\log q\le2ck\ell+6D\ell<k\ell$, so $J\le2k^3\ell+2\le k^6$. Also $\log q\le(ck^{1-a}+3)\ell\le k^{1-a}\ell$, since $k^{1-a}\ge128$. The dilation bound is $h_0\log(2M)\le8k^a\ell^2\cdot2\ell$. In (4.4), $k^2\lambda+J\le2k^6\lambda$, giving at most $42D\ell+4D\log\lambda\le212k^{2a}\ell^3<256k^{2a}\ell^3$. For (4.6), use $D,h\le k$ in its displayed logarithm; (4.10)'s constant exceeds $10+2\log9+4\log(B_0+1)$. In (4.8), $h_0,M\le k$, $J\le k^6$; the three logarithmic contributions are bounded by $3D\ell,10D\ell,20D\ell$, respectively. These estimates prove the stated uniform constants.

## 5. Heavy returns, cuts, and actual single runs

### 5.1 Affinity and the closest heavy return

If $z_j=a+jb$ on a torus and representatives at selected indices lie in one box of coordinate widths at most $2H$, then they are affine in the index. For any three selected indices $j_1<j_2<j_3$,
$$
(j_3-j_2)(Z_{j_2}-Z_{j_1})-(j_2-j_1)(Z_{j_3}-Z_{j_2})
$$
is an integer vector of coordinate magnitude at most $2H(j_3-j_1)<1$. It is zero. Interpolation between extreme indices proves the assertion, with the cases of at most two indices immediate.

In an actual progression, call a full label heavy when its **whole-word** multiplicity exceeds $k/M$, and light otherwise. Choose the heavy label of smallest first occurrence. If it has $m_*$ visits and closest positive visit gap $h$, then
$$
1\le h\le2M,\qquad |u_i|\le 2MH_x/k,\qquad |v_i|\le4MH/k,\qquad v=\lambda u, \tag{5.1}
$$
where $u,v$ are the real representative differences at that gap. Indeed, $m_*-1\ge k/(2M)$, the extreme gap is at least $(m_*-1)h$, and affinity gives the two width-over-multiplicity bounds. The torus identity makes $v-\lambda u$ an integer vector of magnitude at most $6MH/k<1$, so it is zero.

There is $t\in\{0,\ldots,h-1\}^D$ with
$$
x(n_j)=x(n_0)+j(t+u)/h,\qquad
y(n_j)=y(n_0)+j(\lambda t+v)/h\pmod1. \tag{5.2}
$$
Moreover $\gcd(t_1,\ldots,t_D,h)=1$. Otherwise a common divisor $e>1$ would put the sample at the shorter gap $h/e$ at the convex combination $(1-1/e)Z_{j'}+(1/e)Z_{j'+h}$ in the same full half-open box, contradicting minimality of $h$. All relevant index positions lie between the two visits, so this is an actual additional visit, not a formal point outside the progression.

The rational vector $t/h$ has order exactly $h$. At indices incongruent modulo $h$, some rational coordinate displacement has circle distance at least $1/h$. Its drift changes this by at most $2MH_x/h$, so the actual distance is at least
$$
(1-2MH)/h\ge(1-2MH)/(2M)>H\ge H_x. \tag{5.3}
$$
Thus every full label occurs in only one residue class modulo $h$.

For **every** heavy label, not only the chosen one, its extreme visits differ by $ah$ with $a\ge m'-1$. Their coordinate difference $\Delta_i$ is congruent to $av_i$, and
$|\Delta_i-av_i|\le2H+4MH/h<1$. Hence it equals $av_i$, and
$$
|v_i|\le(2M/k)|V(y_i(n_{j_*}))| \tag{5.4}
$$
at every heavy index $j_*$.

All inequalities just used follow, for $k\ge16$, from $2M/k\le1/16$, $H=k^{-2}$. In particular $4MH\le1/(8k)<1/2$, $4kH<1$, and (5.3) is strict.

### 5.2 Short periods and the closed-cut argument

If $h\le h_0$, then $h\mid\lambda$, and the $y$-step is $w=v/h$ modulo integers. Its total motion is $k|w_i|\le4MH/h<1/2$. Also $w_i\in q^{-i}\mathbb Z$, so a nonzero coordinate satisfies $|w_i|\ge q^{-i}\ge q^{-D}>\alpha$.

If the centered samples fail to equal $Y(n_0)+jw$, the closed real segment in some nonzero coordinate meets a cut point in $1/2+\mathbb Z$. A cut at the first or last sample is included. Every sample is then within $k|w_i|$ of that cut, and its interval has width at most
$$
2H(k|w_i|+\alpha)\le2H(k+1)|w_i|<|w_i|.
$$
The circle distance between any two distinct samples in this coordinate is their real displacement, between $|w_i|$ and $1/2$. No full label could repeat, contradicting heaviness. Therefore
$$
Y(n_j)=A+jw\quad(0\le j<k) \tag{5.5}
$$
as an exact real identity inside the centered cube.

### 5.3 Long blocks are eligible

For $h_0<h\le2M$, partition the first $h\lfloor k/h\rfloor$ indices into length-$h$ blocks. In a rotating coordinate its undrifted block values form an $s_i$-point grid, each repeated $h/s_i$ times. The bound $4MH/k\le\eta$ implies that a nonregular sample comes from a grid point within $2\eta$ of the cut. An arc of length $4\eta$ has at most $4\eta s_i+1$ grid points, also with endpoints included. The fraction excluded in any coordinate union is at most
$$
D(4\eta+1/h_0)=\epsilon_{\rm reg}/2+1/L_0^2\le\epsilon_{\rm reg}. \tag{5.6}
$$
Thus every block has at least $(1-\epsilon_{\rm reg})h\ge h/2$ regular positions. Its full labels are distinct by (5.3).

If a full block contains a heavy index, fix that index's $y$-interval $I_*$ in a stationary coordinate. Every block sample is at circle distance at most $|v_i|\le(2M/k)|I_*|$ from that sample. The neighborhood lemma gives every such sample's interval width at least $|I_*|/16\ge|v_i|$. The heavy anchor need not be regular. This proves the stationary condition at every regular position, including cut and endpoint cases. The other drift bounds in eligibility follow from (5.1). Hence every heavy-containing full block is one of the patterns of (4.5)–(4.6).

### 5.4 Single runs: exactly the quantifiers needed later

Suppose the chosen heavy return is short. For a fixed residue $r\pmod h$, the $x$-path is the reduction of $\widehat x(n_r)+su$; in each coordinate its entire lifted displacement is at most $k|u_i|/h\le2MH_x/h<1/2$. Two different real lifts of one $U$-interval are separated by a gap of length $1-H_x>1/2$. Such a path cannot meet two of them. In its one possible lift, the preimage of the half-open interval is an interval of the real parameter $s$. The $y$-path (5.5) is already real and affine; the preimage of each $V$-interval is likewise an interval. Intersecting these preimages, the sampled occurrences of a full label are consecutive in that residue. By (5.3), different residues cannot share the label.

**Conclusion:** in an actual progression having this short closest return, each full label occurs in one residue class and in one consecutive run there. Zero coordinate slopes, isolated endpoint visits, and negative slopes are all covered by the preimage argument.

This is **not** claimed for every abstract word in (4.7) with every advertised $h,t$. For example, $h=2,t=0,u=w=0$ gives a constant abstract word, whose label occupies both residues modulo 2. Its advertised period is not the primitive closest return of a nonzero-step actual progression. The larger abstract family is used only for event indexing and the upper count (4.8); the single-run conclusion is applied only after the actual progression's closest heavy return has been established.

## 6. One global outer coloring: all three families together

Here is a finite definition of every event. Assign independent fair bits $\xi_\beta$ to all $B$ full labels. Fix a total order of their literal indices.

**Family 1.** For each distinct actual full-label progression word, make all choices as functions of that word. If there is no heavy label, set $S$ equal to all positions. Otherwise take the chosen heavy label and closest gap from Section 5. Mark every full $h$-block containing any heavy index, and let $S$ be the light positions outside those marked full blocks, including light positions in the remainder. Use this word only when $|S|\ge\delta k$. Group the labels in $S$ in the fixed label order and deal their occurrences cyclically into $w_{\max}$ rows, where $w_{\max}$ is their largest multiplicity in $S$. No label occurs twice in a row, and every row has length
$$
l\ge\lfloor|S|/w_{\max}\rfloor\ge\delta M-1.
$$
For each row the bad event is $|\sum\xi_\beta-l/2|>\epsilon l$. Equality is not bad. There are at most $kT_{\rm glob}$ such indexed events. Duplicated predicates may be merged, but need not be merged between distinct canonical rows.

**Family 2.** For every $h,t$ and every eligible recorded word of Section 4.3, introduce the event that the deviation of the sum over its regular labels exceeds $\epsilon l$, where $l\ge h/2$. Labels tested are distinct. Dummy positions test no variable. One event is indexed by the word and $h,t$, not by every continuous realization. The count incident to a fixed label for a fixed $h$ is at most $A_h$.

**Family 3.** For every distinct abstract full word $W$ of (4.7), call its labels $s$-light when their whole-word multiplicity $w_\beta$ is at most $k/M_s$. Let $k_L=\sum_{\beta\ s\text{-light}}w_\beta$. When $k_L\ge\delta_s k$, introduce
$$
\left|\sum_{\beta\ s\text{-light}}w_\beta(\xi_\beta-1/2)\right|\ge\epsilon k_L. \tag{6.1}
$$
Here equality **is** bad, as in PR7. The support consists only of the distinct $s$-light labels. The number incident to a fixed label is at most $A_s$; counting all words through that label, even when it is not $s$-light, only enlarges the bound. A word with several $h,t$ realizations defines just one third-family event.

All sets just defined are finite. Family 1 can be enumerated through $N(N-1)$ actual progressions with word deduplication. Families 2 and 3 have finite candidate word universes and the exact realization procedures of Section 14. Thus this is more than a finite-existence assertion; it supplies event/support access. There is no sampling or unpriced real feasibility oracle in their definition.

### 6.1 Tail bounds and weights

For fair independent bits, termwise comparison of the series gives $\cosh t\le e^{t^2/2}$. Therefore
$$
\mathbb E\exp\left(s\sum_i w_i(\xi_i-1/2)\right)
\le\exp\left(s^2\sum_iw_i^2/8\right).
$$
Markov's inequality, optimized at $s=4\epsilon l/\sum_iw_i^2$, and the two signs give
$$
\Pr(|\sum_iw_i(\xi_i-1/2)|\ge\epsilon l)
\le2\exp(-2\epsilon^2l^2/\sum_iw_i^2). \tag{6.2}
$$
Thus for Families 1–2 the bound is $2e^{-2\epsilon^2l}$. For Family 3, $\sum w_i^2\le(k/M_s)k_L$, so it is at most $2e^{-2\epsilon^2\delta_sM_s}$.

Assign weights
$$
z_E=e^{-\epsilon^2l(E)}\quad(E\in1,2),\qquad
z_E=e^{-\epsilon^2\delta_s h_0}\quad(E\in3).
$$
The sums incident to any fixed label are bounded by
$$
I_1=kT_{\rm glob}e^{-\epsilon^2(\delta M-1)},\quad
I_2=\sum_{h_0<h\le2M}A_h e^{-\epsilon^2h/2},\quad
I_3=A_s e^{-\epsilon^2\delta_sh_0}. \tag{6.3}
$$
The explicit tests in Section 12 imply, separately,
$$
I_i\le\epsilon^2/(48k),\qquad
I_1+I_2+I_3\le\epsilon^2/(16k). \tag{6.4}
$$
Here is the calculation, with no limiting notation. Put
$L_\epsilon=\lceil\log_2(48/\epsilon^2)\rceil$ and $C_1=260+L_\epsilon$.
The test $C_1k^{2a-m}\ell^3\le\epsilon^2\delta$, together with (4.9), gives
$\epsilon^2\delta k^m\ge256k^{2a}\ell^3+2\ell+\epsilon^2+\log(48/\epsilon^2)$, proving the first bound.
For the second, $\ell\ge4C_L/\epsilon^2$ makes $\log A_h\le\epsilon^2h/4$ for $h>h_0$; hence $I_2\le k e^{-\epsilon^2h_0/4}$. The test $4(2+L_\epsilon)k^{-a}\le\epsilon^2$ proves the desired estimate. For the third, $\ell\ge(42+L_\epsilon)/(\epsilon^2\delta_s)$, (4.10), and $h_0\ge D\ell^2$ give the bound directly.

### 6.2 Dependency graph and the asymmetric criterion

Join distinct indexed events precisely when their supports intersect. Because the underlying label bits are independent, an event is independent of the **joint sigma-algebra** generated by all its nonneighbors. Pairwise independence alone is not the argument.

An event in Families 1–2 has incident neighbor weight at most $l(E)\epsilon^2/(16k)$. A Family 3 event has support size at most $k$, hence neighbor weight at most $\epsilon^2/16$. These estimates include all cross-family neighbors. The scale tests also give
$$
\epsilon^2l(E)\ge4\quad(E\in1,2),\qquad
\epsilon^2\delta_s h_0\ge4,
$$
so every $z_E<1/2$. Using $\log(1-z)\ge-2z$ for $0\le z\le1/2$,
$$
z_E\prod_{F\sim E}(1-z_F)
\ge e^{-\epsilon^2l(E)-\epsilon^2l(E)/(8k)}
\ge2e^{-2\epsilon^2l(E)}\ge\Pr(E)
$$
for Families 1–2. For Family 3, writing $T=\epsilon^2\delta_s h_0$, the corresponding lower bound is $e^{-T-\epsilon^2/8}\ge2e^{-2T}$. The last inequalities follow from $T,\epsilon^2l\ge4$, $k\ge16$, and $\epsilon<1/2$.

For clarity, the finite asymmetric local lemma used here has a short proof. Let $A_T$ denote avoidance of a set of events. Induct on $|T|$ to prove $\Pr(A_T)>0$ and $\Pr(E\mid A_T)\le z_E$ for $E\notin T$. Positivity follows by removing one event. For the conditional estimate, partition $T$ into neighbors $T_1$ of $E$ and nonneighbors $T_2$. Independence gives $\Pr(E\mid A_{T_2})=\Pr(E)$; successive conditional bounds give $\Pr(A_{T_1}\mid A_{T_2})\ge\prod_{F\in T_1}(1-z_F)$. Divide and use the displayed asymmetric criterion. If $T_1$ is empty, independence suffices directly. This completes the induction and proves positive probability of avoiding all events.

Fix any one resulting $c_*$. This is **one coloring of all labels satisfying all three families simultaneously**.

### 6.3 The strengthened dichotomy

Put $A_0=(1/2-\epsilon)(1-\epsilon_{\rm reg})$ and $g=A_0(1-\delta)-\gamma>0$. With no heavy label, Family 1 balances the whole progression. With a short chosen heavy return, (5.5) holds. With a long return let $E$ be the positions in heavy-containing full blocks. Every such block is eligible and has at least $(1-\epsilon_{\rm reg})h$ regular positions, hence contributes at least $A_0h$ positions of each color. Every position outside $E$ lies in $S$ or in the remainder, so $k-|E|\le|S|+h$.

If $|S|\ge\delta k$, Family 1 contributes at least $(1/2-\epsilon)|S|$, disjointly from $E$. The total is at least $A_0(k-h)$. If $|S|<\delta k$, the marked blocks alone contribute at least $A_0(k-h-\delta k)$. The threshold test $4A_0 k^{m-1}\le g$, and $h\le2M\le4k^m$, make this at least $\gamma k$.

Consequently every actual nonzero-step progression is either $\gamma$-rich (each outer bit occurs at least $\gamma k$ times) or has a short chosen heavy return and the affine/run structure in Section 5. The abstract Family 3 can now be applied to that actual word, but no abstract-word run assertion is needed.

**Notation for Sections 7–10.** Their collision return $(h,t)$ is local to
this block and is not identified with the closest heavy return in Section 5.
The return norm is written $W_{\rm ret}$, the lower digit remainder is
$\mathcal R_v$, and the inner product $T_{\rm ip}=\langle t,\beta\rangle$.
The augmented-word count $T_{\rm aug}$ and the label/key $\kappa(n)$ retain
their earlier meanings; Section 9's $\kappa_R$ is explicitly a rank ratio.

## 7. Literal keys and collision classes

### 7.1 Separation and the two-point norm-band lemma

For distinct $n,n'$, write the nonzero residue $\lambda(n-n')\pmod N$ as $q^a u$, with $q\nmid u$ and $a<D$. Coordinate $i=a+1$ has nonzero residue $u/q$, whose circle distance from zero is at least $1/q$. Therefore
$$
\|qY(n)-qY(n')\|_2\ge1. \tag{7.1}
$$
This uses divisibility by the integer base $q$, not a false assumption that $q$ is prime.

All samples in a fixed $V^D$-box are collinear by Section 5.1. Parameterize their scaled line as $v_\perp+t e$, $\|e\|=1$, $v_\perp\perp e$. Their squared norms are $\|v_\perp\|^2+t^2$, and distinct line parameters have distance at least one. Two such points on the same half-line from zero have squared norms differing by at least one. In the half-open band $[b,b+1)$, two values differ by strictly less than one. At most one point on each half-line is possible, hence
$$
\boxed{\text{every literal key occurs at most twice in a progression}.} \tag{7.2}
$$
The convention matters: the collinear points $-1,0,1$ have squared norms $1,0,1$, all in the **closed** band $[0,1]$. This replayed negative control is not a counterexample to (7.2).

### 7.2 A common return and affine collision classes

Suppose some $V^D$-box repeats. For each box-return gap $g$, let $v_g$ be the difference of its representatives. Then $|v_{g,i}|\le2H$ and $v_g=g y(d)\pmod{\mathbb Z^D}$. For any two gaps,
$g'v_g-gv_{g'}$ is an integer vector of magnitude less than $4kH<1$. It is zero, so $v_g=gB$ for a common real vector $B$.

Let $h$ be the gcd of all return gaps. Bezout gives $h(y(d)-B)\in\mathbb Z^D$; write
$$
y(d)=(t+\beta)/h\pmod{\mathbb Z^D},\quad
 t\in\{0,\ldots,h-1\}^D,\quad \beta=hB.
$$
Here $|\beta_i|\le2H$, and $\beta=Y(hd)$. Moreover $h$ is itself a return gap: between any returned pair with gap $g$, the position at gap $h$ is its real convex combination and belongs to the same half-open box. Since $h<k<P$, $hd\ne0$, and (7.1) gives
$$
W_{\rm ret}=q^2\|\beta\|^2\ge1. \tag{7.3}
$$
Every occurrence of a box is in one residue modulo $h$, by the definition of the gcd.

Call a residue class a collision class when it contains a repeated key; write its positions $a+sh$, $0\le s<K_a$, where $K_a\le K_h=\lceil k/h\rceil$. In such a class,
$$
Y(n_{a+sh})=Y(n_a)+s\beta. \tag{7.4}
$$
To see this, its lifted total coordinate motion is less than $2kH<1/2$. If its centered representatives cross a cut, every sample lies within $K_a|\beta_i|$ of that cut in a nonzero coordinate. The lattice bound $|\beta_i|\ge q^{-D}>\alpha$ and (4.1) make every sampled interval narrower than $2H(K_a+1)|\beta_i|<|\beta_i|$. Distinct class samples are at circle distance at least $|\beta_i|$; no box could repeat. This contradicts the repeated key and proves (7.4), including closed-cut endpoint cases.

### 7.3 Carries and finite discrete data

Let $A=Y(n_0)$, and define integer carries by
$$
Y(n_j)=A+j(t+\beta)/h-m_j. \tag{7.5}
$$
The augmented word consists of all its literal $V$-boxes and carries. In one coordinate the centered start is in $[-1/2,1/2)$, and the chosen unreduced slope lies in $[-1,2]$. Endpoint comparisons at all $k$ positions, including the cut that determines the carry, use at most $6k^2J$ lines. Hence
$$
T_{\rm aug}\le[9(6k^2J+1)^2]^D. \tag{7.6}
$$
At starts $0\le a<h$, $-1\le m_{a,i}\le h-1$, so differences of two such carries have magnitude at most $h$.

For every collision class choose a repeated pair by a fixed rule (smallest gap, then smallest first index); encode that pair explicitly and use an absence symbol in noncollision classes. This determines the collision-class set $\Sigma$, $a_0=\min\Sigma$, and every pair sum $\sigma_a$. The number of choices is at most
$\prod_a(1+K_a^2)\le4^{\sum_aK_a}=4^k$. Together with $h,t$ and (7.6), the complete discrete data have at most
$$
B_{\rm disc}=k^{D+1}T_{\rm aug}4^k
\quad\text{possibilities},\qquad
\log B_{\rm disc}\le21D\ell+2k. \tag{7.7}
$$
Unrealizable codes are harmless overcounts. No missing key-pair identification is assumed.

For comparison with P4's nested description, any repeated pair $s<t$ satisfies $|s+t-2x_*|<1/((t-s)W_{\rm ret})\le1$, where $x_*$ is the class parabola's vertex. Two disjoint, nonnested pairs have integer endpoint sums differing by at least two, impossible in this open interval of length two. Thus the actual pairs are nested. The two-point argument also places their vertex between their endpoints, so its point belongs to their half-open boxes. We do not need this extra reconstruction fact for (7.7).

### 7.4 Exact vertex identities

For the chosen pair $s_1<s_2$ in class $a$, let $\sigma_a=s_1+s_2$, $w=\|\beta\|^2$, and
$$
\zeta_a=q^2(2\langle Y(n_a),\beta\rangle+\sigma_aw).
$$
Equality of integer bands gives
$$
|\zeta_a|<1/(s_2-s_1)\le1,\qquad
f_{a+sh}=q^2\|Y(n_a)\|^2+s(s-\sigma_a)W_{\rm ret}+s\zeta_a. \tag{7.8}
$$
Put $Y_0=Y(n_{a_0})$, $v_a=m_a-m_{a_0}$, and $c_a=(a-a_0)/h\in[0,1)$. Then $Y(n_a)=Y_0+c_a(t+\beta)-v_a$. Direct expansion of the norm, and substitution of the definition of $\zeta_a$, yield
$$
q^2\|Y(n_a)\|^2=\Lambda_a+c_a\zeta_a, \tag{7.9}
$$
$$
\Lambda_a=q^2\|Y_0\|^2+2c_aq^2\langle Y_0,t\rangle
-(c_a^2+c_a\sigma_a)W_{\rm ret}-2q^2\langle Y_0,v_a\rangle
+q^2(c_a^2\|t\|^2+\|v_a\|^2-2c_a\langle t,v_a\rangle).
$$
In particular
$$
f_{a+sh}=\Lambda_a+s(s-\sigma_a)W_{\rm ret}+(c_a+s)\zeta_a,
\qquad 0\le c_a+s\le K_h. \tag{7.10}
$$
For example the terms from $c_a\zeta_a$ are
$2c_aq^2\langle Y_0,\beta\rangle+2c_a^2q^2\langle t,\beta\rangle+2c_a^2W_{\rm ret}-2c_aq^2\langle v_a,\beta\rangle+c_a\sigma_aW_{\rm ret}$; combining them with the displayed $W_{\rm ret}$-terms gives exactly the expansion of $\|Y_0+c_a(t+\beta)-v_a\|^2$. This proves the identity, independently of the supplementary algebra tests.

Finally write $T_{\rm ip}=\langle t,\beta\rangle$. Subtracting the vertex equations at $a,a_0$ gives
$$
q^2\langle v_a,\beta\rangle
=c_aq^2T_{\rm ip}+\left(c_a+\frac{\sigma_a-\sigma_{a_0}}2\right)q^2w
+\frac{\zeta_{a_0}-\zeta_a}2. \tag{7.11}
$$
Encoding $\lfloor q^2T_{\rm ip}\rfloor$ and $\lfloor(k+1)q^2w\rfloor$ determines rational numbers $X_a$ within strictly less than 3 of the left side: the two cell errors contribute less than one each, as does the last term. Since $|T_{\rm ip}|\le2DhH$, $w\le4DH^2$, the number of these two cells is at most
$$
100D^2q^4. \tag{7.12}
$$

## 8. Matching digit-rank certificates and progression counts

This section supplies full finite counts, not just symbolic identities. Fix discrete data with $\Sigma\ne\varnothing$. Let
$$
V_0=\operatorname{span}_{\mathbb Q}\{v_a:a\in\Sigma\},\qquad \rho=\dim V_0.
$$
For a vector $v\in\mathbb Z^D$, define vectors on digit positions $0\le l<D$ by
$$
(S_1v)_l=v_{l+1},\qquad (S_2v)_l=v_{l+2},\qquad v_{D+1}=0.
$$
The digit rank is
$$
R=\dim_{\mathbb Q}(S_1V_0+S_2V_0),\qquad
\rho\le R\le\min(2\rho,D). \tag{8.1}
$$
Choose bases and nonsingular minors greedily in the ordered list of actual integer rows. They are determined by the discrete data, so they incur no new multiplicity. Rational dependence coefficients may be large; arrangement counts do not depend on their magnitudes. Exact elimination decides them if requested.

### 8.1 Start and return digits

Because $q$ is odd, the balanced base-$q$ digits $y_0,\ldots,y_{D-1}$ of $\lambda n\pmod{q^D}$ lie in $[-(q-1)/2,(q-1)/2]$. Every prefix sum divided by $q^i$ has magnitude strictly below $1/2$ and is congruent to $y_i(n)$; hence it is the prescribed centered representative. Thus, exactly,
$$
Y_i(n)=\sum_{l<i}y_lq^{l-i},\qquad
q^2\langle Y(n),v\rangle
=q\langle S_1v,y\rangle+\langle S_2v,y\rangle+\langle v,F\rangle, \tag{8.2}
$$
where $F_i=\sum_{l\le i-3}y_lq^{l-i+2}$, and $|F_i|\le1$. Empty sums are zero. The strict centered bound establishes every prefix convention, including carries from negative balanced digits.

For the return $\beta$, define
$$
e_0=q\beta_1,\qquad e_i=q\beta_{i+1}-\beta_i\quad(1\le i<D).
$$
These are integers by coordinate coherence of $y(hd)$. They determine $\beta_i=\sum_{l<i}e_lq^{l-i}$ and satisfy $|e_i|\le2H(q+1)$. The same expansion gives
$$
q^2\langle v,\beta\rangle
=q\langle S_1v,e\rangle+\langle S_2v,e\rangle+\mathcal R_v,
\qquad |\mathcal R_v|\le3\|v\|_1/k^2. \tag{8.3}
$$
Indeed the omitted geometric tail in each coordinate is at most
$2H(q+1)/(q-1)\le3H$ for $q\ge5$.

With $|v_{a,i}|\le h<k$ and $k\ge64D$,
$$
|\langle S_2v_a,e\rangle|\le2Dh(q+1)/k^2<q/8,
\qquad |\mathcal R_{v_a}|<1. \tag{8.4}
$$
Combining (7.11)–(7.12) with (8.3), $\langle S_1v_a,e\rangle$ is the unique nearest integer to $X_a/q$: the possible error is less than $1/8+4/q<1/2$, since $q>k\ge16$. The second form is an integer in the interval
$$
X_a-q\langle S_1v_a,e\rangle+[-4,4], \tag{8.5}
$$
which has at most nine integer values. Exact nearest-integer ties therefore never arise for realized data.

### 8.2 Progression count C*

Encode $n_0$ ($q^D$ choices), the discrete data, and the two cells (7.12). Among the fixed basis rows for (8.1), each first form is known exactly, and each second form has at most nine choices by (8.5). Choose the fixed nonsingular $R$-column minor. Given all other $D-R$ return digits, these $R$ row values determine the remaining digits uniquely over $\mathbb Q$; reject a nonintegral or out-of-range solution. Every free digit has at most
$4H(q+1)+1\le q$ possibilities. The recovered $\beta_D$ determines $d$, because $\beta_D=\lambda hd/N\pmod1$ and $\lambda h$ is a unit modulo $N$. This is an injective encoding of actual progressions.

Thus, for a fixed digit rank, the number is at most
$$
q^{2D-R}\, B_{\rm disc}\,(100D^2q^4)\,9^D. \tag{8.6}
$$
In particular it is at most
$$
\exp((2D-R)\log q+E_k),\qquad
E_k=1000(k+D\ell+\log q). \tag{8.7}
$$
No continuous-to-discrete multiplicity is omitted: free digits are explicitly counted; independent row equations give at most one completion; unrealizable cell codes are discarded or overcounted.

### 8.3 Literal key-set certificate A*

We count all sets of keys at arbitrary selected positions in collision classes; the positions need not themselves belong to repeated pairs. In (7.9)–(7.10), encode the $R$ integers $\langle u_i,y\rangle$ for a basis $u_i$ selected among $S_1v_a,S_2v_a$. Each has magnitude at most $Dhq$, so their number of choices is at most
$$
q^R(3Dk)^D. \tag{8.8}
$$
They determine both integer forms for every $v_a$. Codes producing nonintegral dependent forms may be discarded. The tail $\tau_a=\langle v_a,F\rangle$ is one linear functional on $V_0$, hence depends on $\rho$ real parameters, and $|\tau_a|\le Dh$.

Every band value now has the form
$$
f_j=K_j+G_j(\Theta)-2\tau_a(\phi)+(c_a+s)\zeta_a,\quad j=a+sh, \tag{8.9}
$$
Here the known integer and the affine term are explicitly
$$
K_j=-2\bigl(q\langle S_1v_a,y\rangle+\langle S_2v_a,y\rangle\bigr)+q^2\|v_a\|^2,
$$
$$
G_j(\Theta)=\Theta_1+2c_a\Theta_2+
\bigl[s(s-\sigma_a)-c_a^2-c_a\sigma_a\bigr]\Theta_3
+q^2c_a^2\|t\|^2-2c_aq^2\langle t,v_a\rangle.
$$
The last two terms are known rational constants, placed in $G_j$ rather than
incorrectly declaring their sum integral. Thus $K_j$ is genuinely integral;
$G_j$ remains affine in
$\Theta=(q^2\|Y_0\|^2,q^2\langle Y_0,t\rangle,W_{\rm ret})$,
$\phi$ has dimension $\rho$, and $\zeta_a\in(-1,1)$.
The band identity and the lengths of the known translated intervals are
unchanged. All boxes are already fixed literally by the augmented word.

Here is an explicit four-stage count of all possible **integer band words**. It avoids assigning one independent real parameter to every $f_j$.

1. From $0\le f_j\le Dq^2/4$, $|\tau_a|\le Dh$, and $0\le c_a+s\le K_h$, the possible $G_j$'s lie in known translated intervals of length at most $Dq^2/4+4Dh+2K_h$. At most
   $s_G=k(Dq^2+8Dk+4k+20)$
   integer-threshold comparisons suffice. Their signs in dimension three determine all $\lfloor G_j\rfloor$, with at most $\mathcal A(3,s_G)$ outcomes.
2. In one such outcome, $\operatorname{frac}(G_j)=G_j-\lfloor G_j\rfloor$ is affine. At most
   $s_\phi=k(4Dk+7)$
   comparisons against integers determine $\lfloor\operatorname{frac}(G_j)-2\tau_a\rfloor$. The variables are $(\Theta,\phi)$ of dimension at most $D+3$. This contributes at most $\mathcal A(D+3,s_\phi)$.
3. The remaining fractional quantities are affine within the preceding cell. For $c_a+s>0$, all changes of $\lfloor f_j\rfloor$ as $\zeta_a$ varies in $(-1,1)$ occur at at most $2K_h+5$ explicitly given affine threshold values divided by the fixed positive number $c_a+s$. Comparisons between two such thresholds in the same class, and with $-1,1$, use at most
   $s_\times=2k^2(2K_h+5)^2$
   affine signs in $(\Theta,\phi)$, after clearing positive denominators. Thus their weak order, all ties included, has at most $\mathcal A(D+3,s_\times)$ possibilities. Positions with zero coefficient of $\zeta_a$ were already fixed and create no division.
4. Once this order is fixed, a class has at most
   $2K_a(2K_h+5)+1$
   possible band words, counting open intervals between thresholds and the thresholds themselves. Choose independently for different classes, which is an upper bound even if their true parameters are correlated. Since
   $4K_h^2+10K_h+1\le16^{K_h}$ and $hK_h\le2k$, the product is at most $256^k$.

Finally there are at most $2^k$ subsets of positions. Different subsets or discrete data may encode the same key set, but that is only overcounting. Conversely each actual selected key set has a code: its integer projections, its realized sign faces, its per-class threshold choices, and its selected positions. Decoding determines the literal boxes and exact floor bands, hence the set, without a start point or a full-label word.

Combining the displayed factors with (7.7) gives the uniform bound
$$
\#\{\text{such key sets of rank }R\}
\le \exp(R\log q+E_k). \tag{8.10}
$$
Here is a numerical check on the *symbolic upper bound*, not a substitute for the preceding encoding proof. After the leading $R\log q$, the factors contribute at most:

| Factor | Additional logarithm |
|---|---:|
| Discrete data | $21D\ell+2k$ |
| Integer projections | $3D\ell$ |
| First arrangement | $6\log q+9\ell$ |
| Second arrangement | $20D\ell$ |
| Crossing-order arrangement | $28D\ell$ |
| Class choices and position subset | $7k$ |

For instance $s_G+1\le3k^2q^2$, $s_\phi+1\le6k^3$, and $s_\times+1\le19k^4$. The table sums to less than $6\log q+100D\ell+10k$, well below $E_k$. The analogous excess in (8.6) is at most $4\log q+26D\ell+2k$. Every ceiling and equality sign has been paid for in these finite factors.

## 9. Rich progressions and shared-key correlations

Fix the outer coloring and a target bit. A progression prescribes $E_\kappa=1$ at positions of the opposite outer bit and $E_\kappa=0$ at positions of the target outer bit. If a key is prescribed both ways, the event is empty and can be discarded.

For a consistent event, let $r_2$ be the number of flipped keys occurring twice, $s_\Sigma$ the flipped singleton keys in collision classes, and $s_{\rm out}$ the remaining flipped singletons. Then
$$
|P_1|=2r_2+s_\Sigma+s_{\rm out},\qquad
|F|=r_2+s_\Sigma+s_{\rm out}. \tag{9.1}
$$
In a rich progression $|P_1|\ge\gamma k$. Define
$$
\mu=(\gamma b-2c)/2>0,\quad \kappa_R=R/D,\quad \nu_R=(2D-R)/D,
\quad \theta_R=\frac{\kappa_Rc+\gamma b-\nu_Rc}{2b}.
$$
Then $0<\theta_R<\gamma$ and
$$
b\theta_R-\kappa_Rc=b(\gamma-\theta_R)-\nu_Rc=\mu. \tag{9.2}
$$
If $r_2+s_\Sigma\ge\theta_Rk$, choose exactly $\lceil\theta_Rk\rceil$ distinct flipped keys in collision classes by a fixed ordered-position rule. The monochromatic event is contained in the event that all these keys flip, of probability $p^{\lceil\theta_Rk\rceil}$. Equation (8.10) bounds the number of such **literal key-set** events. Different full monochromatic events sharing this certificate are covered by one event, not falsely identified as equal.

Otherwise $r_2<\theta_Rk$, so by (9.1) the number of distinct required flips exceeds $(\gamma-\theta_R)k$. Count the progressions by (8.7). If there is no repeated key at all, put $R=0$ and use the trivial bound $q^{2D}$; it obeys the same estimate. Independence is used only among distinct keys *within* each prescribed event. No independence between different progression or certificate events is asserted.

Using (3.2), summing the two cases, two targets and $D+1$ possible ranks yields
$$
\boxed{R_k\le4(D+1)\exp[-\mu k\ell+E_k+2D\log(2k^2)].} \tag{9.3}
$$
The ceiling in the number of selected keys only decreases its probability. Both $R=0$ and $R=D$, including $\rho=0$ with nonempty collision classes, are covered. A class with repeated unflipped keys still belongs to $\Sigma$; it is not silently removed when defining the rank.

## 10. PR6's separate carry-rank route

This section proves the earlier coefficient without the digit-rank improvement.

**Projection certificate A.** Choose a basis $v_1,\ldots,v_\rho$ of the carry span. In (7.9) the values $\langle Y_0,v_a\rangle$ are linear combinations of $\rho$ projections. Thus (7.10) is affine in $3+\rho$ global parameters, plus one bounded $\zeta_a$ per class. Count $\lfloor\Lambda_j\rfloor$ using at most $k(Dq^2+4K_h+6)$ thresholds in dimension $3+\rho$. The crossing-order refinement and per-class choices are exactly the ones proved in Section 8.3. The result is
$$
\exp(2\rho\log q+E_k). \tag{10.1}
$$
The excess over $2\rho\log q$ is at most $6\log q+65D\ell+9k$. The start is not encoded.

**Anchored certificate B.** Encode $n_0$, the discrete data, and put
$B'=\beta/h$, $C_a=at/h-m_a$. Equation (7.4) implies $m_{a+sh}=m_a+st$; hence $Y(n_j)=A+C_a+jB'$ throughout a collision class. If its chosen pair has global indices $j_1<j_2$, equality of bands gives
$$
f_j=\vartheta_a+j(j-j_1-j_2)u+j\eta_a,
\quad \vartheta_a=q^2\|A+C_a\|^2,
\quad u=q^2\|B'\|^2,
\quad |\eta_a|<1/(j_2-j_1)\le1/h. \tag{10.2}
$$
The $\vartheta_a$'s are fixed by the encoded start and discrete data. Replace $h\eta_a$ by a parameter in $(-1,1)$. There is now just one global real parameter $u$, with error coefficient $j/h\le K_h$. The same integer-threshold and crossing-order argument has one-dimensional global arrangements; it costs $2\log q$ plus polynomial-in-$k$ logarithms and the $256^k$ class factor. Including $n_0$ gives
$$
\exp(D\log q+E_k). \tag{10.3}
$$
This counts singles inside collision classes too, not only the paired positions.

**Progression count C.** Use (7.11)–(7.12) and (8.3)–(8.4) only to determine the first digit forms $\langle S_1v_a,e\rangle$. Their rank is $\rho$, since $S_1$ is a coordinate relabeling. A fixed nonsingular minor recovers $\rho$ digits from the others; the latter have at most $q^{D-\rho}$ choices. Encoding $n_0$ and the cells gives
$$
\exp((2D-\rho)\log q+E_k). \tag{10.4}
$$
This is the promised progression count, with no unspecified lattice multiplicity.

For the rich split use
$$
\kappa_\rho=\min(2\rho,D)/D,\quad
\nu_\rho=(2D-\rho)/D,\quad
\kappa_\rho+\nu_\rho\le5/2,
\quad \mu_6=(\gamma b-5c/2)/2.
$$
Use the smaller of (10.1) and (10.3) for certificates and (10.4) for progressions. The argument of Section 9 gives (9.3) with $\mu_6$ replacing $\mu$. The minimum is a legitimate bound on the same set of objects; no simultaneous choice of incompatible encodings is assumed.

The ordinary affine signature count is
$$
T_{\rm aff}\le T_{\rm glob}\,16\,[k(Dq^2+2)+1]^3. \tag{10.5}
$$
The full label word fixes the outer-bit word and the $y$-boxes. For an affine $Y_j=A+jB$, its norm is a quadratic in $j$; three real coefficients and at most $k(Dq^2+2)$ integer thresholds fix the bands. This proves (10.5), including faces and exact bands.

Each nonempty prescribed monochromatic event uses at least $k/2$ distinct keys. With $p\le1/2$, its probability is at most $(1-p)^{k/2}\le e^{-pk/2}$, even with arbitrary consistent mixtures of zero and one prescriptions. Thus
$$
A_k\le2T_{\rm aff}e^{-k^{1-b}/2}. \tag{10.6}
$$
The explicit tests in Section 12 make (9.3) at most $1/4$ and (10.6) at most $1/4$. Families 1–2 and the dichotomy suffice. This closes PR6 independently of Sections 8.2–8.3's matched-rank improvement and Section 11's run estimate.

## 11. The two non-rich cases in PR7

Fix the global outer coloring from Section 6. Every non-rich actual progression has the short-period, affine, single-run structure of Section 5. Its **key word alone** has at most
$$
T_K=[9(3k^2J+1)^2]^D\,16\,[k(Dq^2+2)+1]^3
\quad\text{possibilities},\qquad
\log T_K\le6\log q+32D\ell. \tag{11.1}
$$
The first factor counts just the $y$-box word using scalar two-variable arrangements; the second counts its quadratic norm bands. For the bound, the first logarithm is at most $19D\ell$; the second is at most $6\log q+9\ell$, comfortably within the displayed constant. No $x$-label word, $\lambda$-entropy, or outer-bit word is paid for in (11.1).

### 11.1 Many $s$-light positions

If $k_L\ge\delta_sk$, Family 3 supplies at least $(1/2-\epsilon)\delta_sk$ $s$-light positions opposite any fixed target. By (7.2), at least
$$
x=\left\lceil\alpha_0k\right\rceil,\qquad
\alpha_0=(1/2-\epsilon)\delta_s/2 \tag{11.2}
$$
distinct keys must flip. For a fixed literal key word, cover all such events by “at least $x$ of the distinct keys in this word flip.” It is a union of at most $2^k$ events, each of probability $p^x$. Which positions were light and which outer bits they had need not be encoded. The total for both targets is at most
$$
2T_K 2^k p^{\lceil\alpha_0k\rceil}. \tag{11.3}
$$
Repeated keys are counted once in each prescribed subset; pretending occurrences were independent would be incorrect.

### 11.2 Few $s$-light positions: a run prescription code

If $k_L<\delta_sk$, more than $(1-\delta_s)k$ positions belong to labels with multiplicity exceeding $k/M_s$. There are at most $M_s$ such labels. For this **actual** progression each is a single run, with period $h\le h_0$, one residue $r<h$, first and last global index, and one outer bit.

Encode $h$, the number of runs, and these run records in order of their first positions. A record has at most $2k^3$ possibilities. The total number of codes is at most
$$
B_{\rm run}=h_0(M_s+1)(2k^3)^{M_s},\qquad
\log B_{\rm run}\le36k^a\ell^3. \tag{11.4}
$$
For the last bound, $h_0=M_s\le8k^a\ell^2<k$, $\log(2k^3)\le4\ell$, and the two short prefactors add at most $3\ell$.

Given the target bit, a key word, and a run code, the prescribed bit of **each key appearing at a run position** is determined. Reject records with invalid residues, indices, or overlaps; reject a key assigned both bits. Ignore unprescribed positions, thereby enlarging the event. Only keep codes whose covered positions exceed $(1-\delta_s)k$, and key words satisfying the multiplicity bound two. These restrictions are finite exact tests. Every actual event in this case is covered, and its code specifies at least $(1-\delta_s)k/2$ distinct key bits. Each prescribed bit has probability at most $1-p$, so the probability of the code event is at most
$$
(1-p)^{(1-\delta_s)k/2}\le e^{-\beta_0 k^{1-b}},\qquad \beta_0=(1-\delta_s)/2. \tag{11.5}
$$
There is no hidden reconstruction of a full label or its numerical coordinates: the run bit is explicitly in the code, and the literal keys come from the separately counted key word. Two different progressions that induce the same prescriptions are covered by the same event; their multiplicity is not repaid as full-word entropy.

Combining the cases gives the finite bound
$$
\boxed{A'_k\le2T_K\left[2^kp^{\lceil\alpha_0k\rceil}
+B_{\rm run}e^{-\beta_0 k^{1-b}}\right].} \tag{11.6}
$$
The two bracketed contributions are each at most $1/4$ under Section 12's tests. With (9.3), the probability of any bad progression is at most $3/4<1$. This establishes the cyclic coloring, without an outer-coloring hypothesis remaining.

## 12. A completely specified all-larger-$k$ threshold

This section replaces every asymptotic assertion needed for the conclusion by a finite checklist. All constants are displayed. [GENERATOR.md](GENERATOR.md) specifies this checklist using rational and integer arithmetic only.

Let
$$
A_0=(1/2-\epsilon)(1-\epsilon_{\rm reg}),\quad
g=A_0(1-\delta)-\gamma,\quad
\alpha_0=(1/2-\epsilon)\delta_s/2,\quad \beta_0=(1-\delta_s)/2,
$$
$$
B_0=\lceil128/\epsilon_{\rm reg}+4\rceil,\quad
C_L=32+4\lceil\log_2(B_0+1)\rceil,\quad
L_\epsilon=\lceil\log_2(48/\epsilon^2)\rceil,\quad C_1=260+L_\epsilon.
$$
The base-two ceilings here are exact rational comparisons against integer powers of two.

Require $k\ge16$, $\ell=\log k\ge1$, the strict parameter region, and all of the following inequalities:

| Purpose | Required finite inequality |
|---|---|
| Local anchored entropy | $\ell\ge4C_L/\epsilon^2$ |
| Third-family incident entropy | $\ell\ge(42+L_\epsilon)/(\epsilon^2\delta_s)$ |
| Regular fraction | $2/\ell^2\le\epsilon_{\rm reg}$ |
| Digit bounds and dimension | $128k^{a-1}\le1$ |
| Short cutoff | $8k^{a-m}\ell^2\le1$ |
| Small block/drift ratio | $64k^{m-1}\le1$ |
| Rotating drift below threshold | $128k^{a+m-3}\le\epsilon_{\rm reg}$ |
| Dichotomy remainder | $4A_0k^{m-1}\le g$ |
| Flip bias | $k^{-b}\le1/2$ |
| First-family row size | $(1+4/\epsilon^2)k^{-m}\le\delta$ |
| Second-family size | $(8/\epsilon^2)k^{-a}\le1$ |
| Third-family size | $(4/(\epsilon^2\delta_s))k^{-a}\le1$ |
| First-family incident weight | $C_1 k^{2a-m}\ell^3\le\epsilon^2\delta$ |
| Second-family incident weight | $4(2+L_\epsilon)k^{-a}\le\epsilon^2$ |

These imply every geometric condition used above. For example $D\le2k^a$ gives $64D\le k$; $h_0\le8k^a\ell^2\le k^m\le M<2M$; $2M/k\le4k^{m-1}\le1/16$. Also $4MH/k\le8k^{m-3}$ and $\eta\ge\epsilon_{\rm reg}/(16k^a)$, so the rotating-drift test gives $4MH/k\le\eta$. The regular-fraction test gives $1/L_0^2\le\epsilon_{\rm reg}/2$.

For the digit/run route put
$$
\mu=(\gamma b-2c)/2,\qquad \mathfrak b=\min(\mu,b\alpha_0),
$$
and additionally require
$$
10000\bigl(1/\ell+k^{a-1}+k^{-a}\bigr)\le\mathfrak b, \tag{12.1}
$$
$$
200\bigl(k^{a+b-1}\ell^3+k^{b-a}\ell\bigr)\le\beta_0. \tag{12.2}
$$
For the carry-affine route replace $\mu$ by $\mu_6=(\gamma b-5c/2)/2$, use $\mathfrak b=\mu_6$ in (12.1), and replace (12.2) by
$$
300\bigl(k^{2a+b-1}\ell^3+k^{b-a}\ell\bigr)\le1/2. \tag{12.3}
$$
Including the third-family checklist on the carry route is harmless; that route does not have to enumerate those events.

Here is a direct verification of the probability targets. From (4.9),
$$
E_k+2D\log(2k^2)+\log(16(D+1))
\le10000[k+k^a\ell+k^{1-a}\ell]. \tag{12.4}
$$
For instance the three coefficients on the right needed to bound the left are no larger than $1000,2012,1000$, apart from the displayed small logarithmic prefactor, which also fits the factor 10000. The same upper bound covers
$$
6\log q+32D\ell+k\log2+\log8. \tag{12.5}
$$
Thus (12.1) makes (9.3) at most $1/4$, and on the digit/run route makes (11.3) at most $1/4$.

Further,
$$
\log T_K+\log B_{\rm run}+\log8
\le200[k^a\ell^3+k^{1-a}\ell], \tag{12.6}
$$
because its contributions are bounded by $6k^{1-a}\ell$, $64k^a\ell$, $36k^a\ell^3$, and $\log8$. Equation (12.2) makes the second term in (11.6) at most $1/4$. Finally
$$
\log T_{\rm aff}+\log8\le300[k^{2a}\ell^3+k^{1-a}\ell], \tag{12.7}
$$
by (4.9), (10.5), and the three-dimensional band arrangement. Equation (12.3) makes (10.6) at most $1/4$. This proves the strict total bounds $3/4$ and $1/2$, respectively, rather than leaving a limit of an unnamed error term.

### 12.1 Exact certification at $K=2^t$

A rational-power/log monomial $A x^{-d}(\log x)^j$, with $A\ge0,d>0,j\ge0$, is decreasing once $\log x\ge j/d$. If $t/2\ge j/d$, then for all $x\ge2^t$,
$$
A x^{-d}(\log x)^j\le A t^j 2^{-\lfloor dt\rfloor}, \tag{12.8}
$$
using $1/2\le\log2\le1$. Its comparison with any positive rational target is therefore an integer comparison. The implementation first compares bit lengths, so it need not allocate an integer with $\lfloor dt\rfloor$ bits when that number is enormous.

The threshold procedure starts with $t=4$, doubles $t$, and tests the checklist with (12.8), explicitly testing its monotonicity condition for **every** monomial. The first two logarithmic lower bounds are certified by $t/2$; regularity is certified by $8/t^2\le\epsilon_{\rm reg}$. For (12.1), certify each of its three terms against $\mathfrak b/3$: the inverse-log test is $60000/t\le\mathfrak b$, and the other two are (12.8). Split (12.2) equally against $\beta_0/2$, and (12.3) equally against $1/4$. These are exactly the tests in the implementation.

This procedure **terminates** for every parameter tuple in the stated strict region. All decay exponents are positive; the only other requirements are finite lower bounds on $t$ or upper bounds tending to zero as inverse powers of $t$. For a fixed $d>0,j$, the exponential series, for example, bounds $2^{dt}$ below by an arbitrarily higher-degree polynomial in $t$, proving $t^j2^{-dt}\to0$. Therefore a sufficiently large doubled $t$ passes all finitely many tests. More importantly, the returned certificate proves them for **every larger $k$** by monotonicity, not just for the tested endpoint. No numerical logarithm or unverifiable eventual assertion is part of the acceptance test.

### 12.2 Executed explicit certificates

For both literal choices $\epsilon=\epsilon_{\rm reg}=\delta=1/200$,
$$
B_0=25604,\qquad C_L=92,\qquad L_\epsilon=21,\qquad C_1=281,
\quad g=40499/8000000.
$$
At $t=33\,554\,432$, the logarithmic anchored requirement is the exact inequality
$16\,777\,216\ge14\,720\,000$. The two rich budgets are
$$
\mu_7=4681/720000,\qquad \mu_6=857/400000.
$$
The independent reviewer's newly authored checker passed **all 21 tests for each literal tuple**, not just these displayed inequalities. [THRESHOLDS.json](THRESHOLDS.json) retains each rational coefficient, decay exponent, logarithmic degree, target, integer $\lfloor dt\rfloor$, and monotonicity check. Thus both literal parameter tuples admit the claimed $K=2^{33\,554\,432}$. This value was not optimized.

## 13. Every fixed positive rational $c<1/8$, and the digit product

For arbitrary such $c$, define the rational
$$
s_0=\min\left(1/100,(1/8-c)/4\right),
$$
$$
a=1/2-2s_0,\quad b=\gamma=1/2-3s_0,\quad m=1-3s_0,
\quad \epsilon=\epsilon_{\rm reg}=\delta=s_0,\quad \delta_s=1/2. \tag{13.1}
$$
All parameters are fixed before $k$ varies. The gaps $m-2a,a-b,1-a-b$ are $s_0,s_0,5s_0$; $1-m=3s_0$. The balance gap is
$$
(1/2-s_0)(1-s_0)^2-(1/2-3s_0)
=s_0+(5/2)s_0^2-s_0^3>0.
$$
If $\Delta=1/8-c$, then
$$
\gamma b/2-c=\Delta-(3/2)s_0+(9/2)s_0^2\ge5\Delta/8>0.
$$
Hence the threshold procedure terminates and defines $K(c)$. This proves every coefficient below the supremum. The rule (13.1) is a general-purpose parameter family, not a replacement for the separately instantiated literal PR7 tuple at $c=1/9$.

Now let $C$ be any valid cyclic coloring supplied by the proof. Put $s=\lfloor\log_2r\rfloor$, and for $0\le n<N^s$, write
$n=\sum_{i=0}^{s-1}n_iN^i$, $0\le n_i<N$. Give it the color
$$
(C(n_0),\ldots,C(n_{s-1}))\in\{0,1\}^s. \tag{13.2}
$$
Suppose an integer progression $a+jd$, $0\le j<k$, lies in this interval and has $d>0$. Then $d<N^s$. Let $i<s$ be the largest exponent for which $N^i\mid d$, and write $d=N^ie$ with $N\nmid e$. The exact identity
$$
\left\lfloor\frac{a+jd}{N^i}\right\rfloor
=\left\lfloor\frac a{N^i}\right\rfloor+je \tag{13.3}
$$
shows that the $i$-th digits form a cyclic progression of nonzero step $e\pmod N$. Lower digits are constant; any carries into higher digits are irrelevant. If (13.2) were monochromatic, $C$ would be monochromatic on this cyclic progression, a contradiction. No assumption that $N$ itself is prime is made. Translate by one and embed the $2^s$ tuples into $r$ colors. Equations (3.2) and (13.3) complete Theorems 1–2 with the exact integer interval length.

## 14. Exact decisions: no real-number oracle

The construction's real quantities are used either through proved inequalities or through the following exact finite procedures. In particular, the exponential-looking mesh does not require an exponential oracle.

### 14.1 Integer and logarithmic ceilings

For rational exponent $u/v>0$, compute $\lceil k^{u/v}\rceil$ by integer binary search for the least $d$ with $d^v\ge k^u$. This handles perfect powers exactly. Compute prime powers in $\lambda$, primality, and the rounding of $q$ by integer division and the test in Section 3.

For a positive rational $x$, range-reduce $x=2^j y$ with $1\le y<2$, by exact rational comparisons. For $1\le y\le2$, put $v=(y-1)/(y+1)$. The first $t$ terms of
$$
\log y=2\sum_{i=0}^\infty\frac{v^{2i+1}}{2i+1}
$$
are a rational lower bound; the remaining tail is at most
$$
\frac{2v^{2t+1}}{(2t+1)(1-v^2)}. \tag{14.1}
$$
Compute the same enclosure for $\log2$, combine, multiply by the required integer, and double $t$ until the lower and upper bounds have the same ceiling. Inverting $x$ handles $x<1$; $x=1$ is treated exactly.

Here is a proof that the ceiling procedure terminates, rather than an assumption about equality of computable reals. For every nonzero rational $t$, $e^t$ is irrational. It suffices to prove this for $t=p/q>0$. Define
$$
f_n(x)=x^n(p-qx)^n/n!,\quad
F_n(x)=\sum_{j=0}^{2n}(-1)^jf_n^{(j)}(x).
$$
All derivatives at zero are integers, by expanding the polynomial and multiplying its coefficients by the derivative factorial. The symmetry $f_n(t-x)=f_n(x)$ gives integer derivatives at $t$ as well. Since $F_n+F_n'=f_n$,
$$
0<I_n:=\int_0^t e^xf_n(x)\,dx=e^tF_n(t)-F_n(0)
\le t e^t\frac{(p^2/(4q))^n}{n!}\longrightarrow0.
$$
If $e^t=A/B$ were rational, $BI_n$ would be a positive integer tending to zero, impossible. Negative $t$ follows by reciprocation. Thus a positive rational $x\ne1$ cannot have a nonzero rational logarithm. Neither $\log k$ nor $k^2\log Q$ is an integer, and the shrinking enclosures must decide their ceilings.

A fully computable precision bound is available as well. On $[t/4,3t/4]$,
$$
I_n\ge\frac t2\frac{(3p^2/(16q))^n}{n!}. \tag{14.2}
$$
Choose $n$ until the upper bound with $e^t$ replaced by $3^{\lceil t\rceil}$ is below $1/(2B)$, for a proposed rational comparator $A/B$. Then $F_n(t)\ne0$, and
$$
|e^t-A/B|\ge
\frac{\min\{(t/2)(3p^2/(16q))^n/n!,\ 1/(2B)\}}{|F_n(t)|}. \tag{14.3}
$$
Indeed $(A/B)F_n(t)-F_n(0)$ is an integer multiple of $1/B$: if zero, use (14.2); otherwise use the upper bound for $I_n$. Dividing (14.3) by $A/B+3^{\lceil t\rceil}$ bounds the logarithmic separation. Testing the finitely many integer ceiling comparators in the known range therefore gives an explicit precision bound using rational arithmetic only.

For a supplementary candidate bit-cost envelope, let $b$ exceed the total binary lengths of the positive rational argument and the positive integer multiplier. The proposed closed envelope for either logarithmic ceiling is
$$
\mathsf L(b)=2^{\,2^{100(b+1)^2}}. \tag{14.4}
$$
One direct justification is to bound the integer ceiling candidates by $2^b b+1$, take $n=2^{16(b+1)^2}$ in (14.2)–(14.3), and use $n!\ge(n/2)^{n/2}$, $n!\le n^n$. These give logarithmic separation exceeding $2^{-2^{32(b+1)^2}}$. At most $2^{40(b+1)^2}$ series terms in (14.1) then suffice. Even bounding coefficient-bit growth by doubling at every rational operation, followed by schoolbook arithmetic, stays below (14.4). The special comparator zero is decided by $x>1$. This sketch is supplementary and uncertified; finiteness is proved above by irrationality and (14.2)–(14.3).

### 14.2 The exact mesh is algebraic

After $m_V$ is known, all endpoints are in $\mathbb Q(z)$, where
$$
z^{m_V}=Q=(q^{D+1}+2)/2.
$$
Because $q$ is odd, the reciprocal polynomial
$(q^{D+1}+2)X^{m_V}-2$ is Eisenstein at 2. For completeness, in a putative primitive integer factorization the leading coefficients would be odd; reduction modulo 2 makes both nonconstant factors monomials, so their constant coefficients are both even, contradicting the constant coefficient $-2$. The standard passage from rational to primitive integer factors follows by clearing denominators and observing modulo each prime that the product of two primitive polynomials is primitive. Thus $2X^{m_V}-(q^{D+1}+2)$ is irreducible over $\mathbb Q$.

An endpoint or a linear combination of endpoints is represented by a rational polynomial of degree below $m_V$ evaluated at its unique positive root $z$. Such an expression is zero precisely when that reduced polynomial is zero. To determine a nonzero sign, bisect a rational enclosing interval for $z$ and use rational interval Horner evaluation. Here $1<z\le e^{H}<2$; the sign is eventually fixed. A general gcd/Sturm fallback is unnecessary for this theorem: its literal mesh uses the irreducibility argument above.

This sign procedure has an explicit precision bound. If the comparison polynomial has rational numerator and denominator bit lengths at most $b$, clear its at most $m_V$ denominators. For a nonzero integer polynomial $P$ of degree below $m_V$, the resultant with $2X^{m_V}-(q^{D+1}+2)$ is a nonzero integer. It equals $2^{\deg P}\prod_\omega P(z\omega)$, where $\omega$ ranges over the $m_V$-th roots of unity. All these roots have modulus below two. Bounding the other factors by $m_V\operatorname{height}(P)2^{m_V}$, and then restoring the cleared denominator, gives a lower bound of $2^{-4(m_V+1)^2(b+1)}$ for the magnitude of a nonzero original comparison. An interval Horner error bound from the coefficient absolute values shows that
$$
8(m_V+1)^2(b+1)+1 \tag{14.5}
$$
bisections suffice. The determinant definition of the resultant establishes its integrality; irreducibility ensures it is nonzero. This argument supplies the required quantitative separation, not an oracle assumption.

A supplementary, uncertified bit-operation envelope covering the rational operations, normalizations, and sign tests is
$$
\mathsf A(m_V,b)=2^{10000(m_V+b+2)^5}. \tag{14.6}
$$
For example (14.5) needs at most $240(m_V+1)^3(b+1)$ rational elementary operations using repeated multiplication as a deliberately slow power algorithm. Bounding bit length after each operation by four times the previous length plus four, and integer arithmetic by schoolbook multiplication/division and the Euclidean algorithm, is the intended justification of (14.6), not a certified claim; termination and (14.5) do not depend on it.

### 14.3 Direct membership and exact bands

For querying an actual point, even algebraic sign isolation is unnecessary. For rational distance $r$ from the cut,
$$
a_j\mathrel{\lessgtr}r
\quad\Longleftrightarrow\quad
Q^j\mathrel{\lessgtr}(1+r/\alpha)^{m_V}. \tag{14.7}
$$
The right side is an exact rational power comparison. Binary search finds the interval. On the negative half use $a_j\le r<a_{j+1}$; on the positive half use $a_j<r\le a_{j+1}$. The reversed inequality is essential to put zero in the interval on its right. The endpoints $a_0=0,a_{m_V}=1/2$ are treated explicitly.

Coordinates use integer residues, with $2r\ge q^i$ deciding whether to subtract $q^i$. Uniform labels are integer floors. The norm band in (3.3) is a rational floor, computable after putting all squared terms over denominator $N^2$. Perfect squares, integer bands, and equalities are decided exactly.

### 14.4 Exact realization of event words

All scalar path constraints have just two unknown real variables: a start $a$ in its half-open representative interval and a drift $b$. Their coefficients are rational; their right sides are algebraic constants of Section 14.2. An interval condition on
$a+\tau+\nu b\pmod1$ is the disjunction over its possible integer lifts of two linear inequalities with the correct open/closed endpoints. All allowed total drifts are below one. With $z_0=\lfloor\tau\rfloor$, the seven lifts $z_0-3,\ldots,z_0+3$ contain every possibility. The large integer part of $\lambda t z/h$ is computed, not searched without a bound.

For Family 2 enumerate candidate words in $(\mathcal L\cup\{*\})^h$, and first check at least $h/2$ regular labels and their distinctness. The $x$-constraints use drift bound $H_x$. In a stationary $y$-coordinate use the minimum of the widths of its finitely many recorded regular intervals as the drift bound. In a rotating coordinate intersect each regular interval with the **closed** interval $[-1/2+\eta,1/2-\eta]$. At each dummy position, choose a rotating coordinate witnessing $\rho<\eta$; its allowed sets are $[-1/2,-1/2+\eta)$ and $(1/2-\eta,1/2)$. Other coordinates at that dummy position are unrestricted. Try all finitely many witnesses and lifts. Existence of one successful choice is exactly eligibility. These witness choices affect enumeration **time**, not the number of indexed events: a realizable word is included once for its $h,t$.

For Family 3 enumerate full words in $\mathcal L^k$, test multiplicities and $k_L$, and try all $h\le h_0,t$. Check the two scalar path systems (4.7), reducing $Y$ modulo one and imposing no global cube condition. Again include the word once, regardless of the number of realizations.

For a chosen set of lifts, decide feasibility by Fourier–Motzkin elimination. Store every inequality as $c\cdot x\le u$ or $c\cdot x<u$, with rational $c$ and algebraic $u$. Pair each lower bound on the eliminated variable with each upper bound; the resulting comparison is strict when either originating bound is strict. Constraints with zero coefficient are retained. If one side has no bounds, discard the other bounds on that variable after retaining the zero-coefficient constraints. After eliminating both variables, exact signs decide the remaining constants. This criterion is exact: finite upper and lower intervals intersect iff every lower endpoint is below every upper endpoint, with equality permitted only when neither relevant bound is strict. It preserves singleton feasible sets and all lower-dimensional faces.

Thus neither an arrangement drawing nor a floating-point feasibility decision is used. Cross-coordinate feasibility separates once $h,t$, the word, and the dummy witnesses are fixed, just as the source enlarged families permit. These exact primitive procedures specify all event membership decisions, without invoking an implementation or a feasibility oracle.

## 15. Deterministic finite generator and independent validation

Here is the complete baseline algorithm in mathematical pseudocode. Binary counters, tapes, and integer arithmetic implement these finite searches uniformly. The mathematical specification is distinct from any supplied reference program.

```
Input: integer k; either literal PR7 parameters, literal PR6 parameters,
       or rational c in (0,1/8) with rule (13.1); optionally an allowed P.
1. Compute and verify the all-larger-k threshold certificate. Reject k below it.
2. Compute D, M, h0, lambda, P, q, N, and the literal meshes exactly.
3. For every n in [0,N), compute its full label and key.
   Deduplicate the used keys and give them canonical sorted indices 0,...,Z-1.
4. Enumerate all outer events exactly, retaining one canonical copy per
   prescribed index. Use Families 1-3 for PR7; Families 1-2 suffice for PR6.
5. Enumerate all B-bit outer tables in increasing binary order.
   Take the first table violating no event. The global LLL proof guarantees one.
6. Enumerate all Z-bit shared-key flip tables in increasing binary order.
   Form C(n)=outer[L(n)] xor flip[key(n)] for every n.
   For every a in [0,N), every d in [1,N), test all k cyclic samples.
   Take the first table with no monochromatic progression.
7. Return C, or the outer/flip tables and exact query routines.
   For r>=2, answer interval queries by the digit product (13.2).
```

Step 5 terminates by Section 6. For that fixed outer table, Section 9 plus Section 11, or the independent Section 10 route, gives positive probability of a successful flip assignment. Since $0<p<1$, every finite assignment to the used keys has positive probability. Thus Step 6 terminates within its finite search domain. No biased random-bit sampler is needed; the deterministic construction uses **zero random bits**.

The independent validation specification in [GENERATOR.md](GENERATOR.md) uses only a binary table, $k$, modular arithmetic, and equality. It has no dependency on the mesh, rank counts, outer proof, or the perturbation estimate. It explicitly includes every nonzero cyclic step; a zero-step test would be inappropriate and is excluded. On failure it returns an actual start and step. Its interval validator independently tests all ordinary positive-step progressions.

The output can store the full $N$-bit cyclic table, or store the $B$-bit outer table and $Z$-bit flip table together with the exact key-index map and query routine. These are computed data, not free nonuniform advice. All finite key sharing is explicit. A much simpler existence-based variant can exhaust all $2^N$ cyclic tables and run the same independent validator; it terminates by the theorem, but does not expose the requested outer/flip decomposition. Steps 3–7 specify that decomposition explicitly.

This is a specification of an unbounded finite search, not a promise that present hardware can hold a theorem-sized table. A concrete implementation is subject to its memory, address space and allocation limits. The mathematical implementation is an ordinary Turing-machine search with binary counters and finite tapes; Section 16 records supplementary estimates; the certified quantitative bound is the DIRECT search bound in GENERATOR.md.

## 16. Complexity boundaries and resource accounting

**Resource scope.** Exact termination of the structured procedure is part of
the theorem. The closed structured resource envelopes (14.4), (14.6) and
(16.1)–(16.8), and every other numerical time/storage bound in Section 16, including $T_{\rm threshold}$, the setup costs, query and full-output time, are supplementary conservative estimates, not independently
certified quantitative complexity claims of this release. The sketches below
explain their intended accounting and need separate verification. The accepted
ordinary bit/Turing bound is the integer-only DIRECT procedure in
[GENERATOR.md](GENERATOR.md), together with its stated storage and output
accounting. The cyclic-validation bound is certified only as the per-candidate part of that DIRECT bound; the output size $sL$ bits is exact. No theorem, threshold or coefficient uses these supplementary
envelopes, and no unpriced oracle is needed for effective termination.


All estimates below concern standard bit/Turing computation with ordinary exact integer arithmetic. They are intentionally conservative. A unit-cost real RAM is not used. A unit-cost integer/array RAM would conceal both operand sizes and table access; its cheaper operation counts are identified separately where useful.

Write $\ell_X=\lceil\log_2(X+1)\rceil$. Besides $k,D,P,q,N,\lambda,m_V,J$, name:
$$
B=(k^2\lambda)^DJ^D,\quad Z=|\{\kappa(n):n\in G\}|\le N,
\quad E=E_1+E_2+E_3,
$$
where $E_i$ are the actual enumerated event counts, and $E_3=0$ for the direct PR6 route. Let $b_{\rm par}$ be the sum of binary lengths of the rational parameter numerators and denominators. An endpoint descriptor uses a root index, a polynomial degree, and rational coefficients with bit length at most
$$
b_{\rm end}=4+(D+1)\ell_q.
$$
For a common loose arithmetic bound use
$$
b_*=64(1+\ell_k+\ell_N+\ell_\lambda+\ell_{m_V}+\ell_B+b_{\rm par}). \tag{16.1}
$$
It bounds the scalar feasibility coefficients after both eliminations as well: they are obtained by a constant-depth sequence of rational scalings and additions of endpoint polynomials and rational translations. There are no algebraic coefficients on the unknown variables, only on the right sides.

### 16.1 Setup and point labels

Include threshold computation in preprocessing. On an admitted input, its returned exponent $t$ satisfies $t\le\ell_k$. There are at most $1+\ell_k$ doubling rounds, fewer than 10000 rational/integer elementary operations per round, and operand bit lengths bounded by $1000(b_{\rm par}+\ell_k+1)$. The `le_shift` comparison never allocates a longer shift than its already stored left operand. A conservative threshold cost is therefore
$$
T_{\rm threshold}=10^{12}(b_{\rm par}+\ell_k+1)^5.
$$
For an input below its threshold, the same bound with the returned exponent $t$ in place of $\ell_k$ prices threshold computation followed by rejection. Add this cost to the setup bounds below.

Primality by trial division over $k<P\le2k^2$ takes at most $10k^3(\ell_k+1)^3$ bit operations. A conservative dilation cost is
$$
10[h_0^3+2Mh_0](\ell_\lambda+\ell_M+1)^3.
$$
For each rational power $k^{u/v}$ used in $D,M$, integer-root binary search is bounded by $10(u\ell_k+1)^4(v+1)$ bit operations. For rounding $q$, put
$$
b_{\rm pow}=1+c_{\rm num}k\ell_k+c_{\rm den}D\ell_q.
$$
Repeated powers and comparisons are bounded by
$10\ell_q(\ell_{c_{\rm den}D}+\ell_{c_{\rm num}k}+1)b_{\rm pow}^3$.
The two logarithmic ceilings cost at most the sum of (14.4) for their rational input descriptions, with the multiplier $k^2$ included. Computing $N$ and the needed $q$-powers is covered by another $10(D+1)(\ell_N+1)^3$. Add $10(D+m_V+1)(b_*+1)^3$ for the remaining integer label-space parameters and initial endpoint descriptors. Denote the sum of these displayed setup bounds, including threshold computation, by $T_{\rm setup}$.

Direct label/key computation using (14.7), modular arithmetic, and a rational norm floor has the bound
$$
Q_{\rm lab}=10^4(D+1)^2(\ell_{m_V}+1)^2[m_V(b_*+1)+1]^4 \tag{16.2}
$$
bit operations per point. The powers in one endpoint comparison have $O(m_Vb_*)$ bits; the explicit expression (16.2) also covers schoolbook Euclidean normalization and the binary search, without making unit-cost assumptions. Forming all point records costs at most $NQ_{\rm lab}$; sorting/deduplicating keys by an intentionally slow comparison procedure costs at most $20N^2(b_*+1)^3$.

Dense endpoint-polynomial caching can use $(m_V+1)^2(b_*+1)$ bits. A compact symbolic representation could reduce this, but no such optimization is assumed.

### 16.2 Event enumeration and support access

Finite candidate counts for the long and short families are
$$
C_2=\sum_{h=h_0+1}^{2M}h^D(B+1)^h,
\qquad C_3=B^k h_0^{D+1}. \tag{16.3}
$$
The second expression includes the trials of $h,t$; the resulting third-family events still number at most $B^k$. Family 1 starts from $N(N-1)$ words. In particular
$E\le kN(N-1)+C_2+B^k$.

One fixed scalar lift assignment begins with at most $2k+4$ inequalities. Two Fourier–Motzkin eliminations create at most $(2k+4)^4$ scalar comparisons. There are at most $14^k$ choices of lifts and low-cut sides per scalar test. The long-family dummy witnesses introduce at most $D^k$ trials. Using (14.6), a supplementary enumeration estimate is
$$
\begin{split}
T_{\rm events}\le{}&20k^2N^4(b_*+1)^3\\
&+200D(2k+4)^6\,[C_2D^k14^k+C_3 14^k]\,
\mathsf A(m_V,b_*).
\end{split} \tag{16.4}
$$
The first term allows slow full-word deduplication and sequential table access. The second prices the exact feasibility tests, not merely an abstract event oracle. Label decoding and interval comparisons are dominated by the same bound. The large $D^k$ witness factor is an enumeration-time factor, **not** an entropy factor added to (4.6).

Event storage is bounded by $10kE(b_*+1)$ bits, in addition to point and endpoint tables. Storing the Family 1 word-deduplication set requires allowing a further $10kN(N-1)(b_*+1)$ bits for it. The algebraic sign cache is capped at 64 entries and is covered by the live feasibility workspace below. The dependency graph is an exact support-intersection graph. A pairwise edge test costs at most $10k^2(b_*+1)^3$ bit operations by direct support comparisons, so an explicit whole graph, if desired, costs at most $10E^2k^2(b_*+1)^3$ and $E^2$ adjacency bits. The generator does not need to store it: exhaustive checking of event predicates suffices. This is not an algorithmic LLL claim.

### 16.3 Search, randomness, and storage

Exhaustive outer search costs at most
$$
T_{\rm outer}=100\,2^B k(E+1)(B+b_*+1)^3 \tag{16.5}
$$
bit operations, allowing sequential access to a $B$-bit candidate table. Store the resulting pullback $c_0(n)$ and key indices at the $N$ group points. Exhaustive flip search, including construction and full cyclic validation for each candidate, costs at most
$$
T_{\rm flip}=100\,2^Z kN^3(Z+b_*+1)^3. \tag{16.6}
$$
These formulas estimate uniform computations, not a nonuniform choice of an unexplained good seed. No random bits are required. A stored outer/flip description uses $B+Z$ bits plus point/key-index and algebraic mesh data; a compiled cyclic coloring uses exactly $N$ color bits, with $k,N$ metadata. The optional simpler direct cyclic exhaustion has at most $2^N$ candidates instead.

A conservative total working-storage bound for the specified decomposition search is
$$
10\{B+Z+N(b_*+1)+k[E+N(N-1)](b_*+1)+(m_V+1)^2(b_*+1)
 +(2k+4)^4m_V(b_*+1)\}, \tag{16.7}
$$
plus the exact-arithmetic workspace from (14.4)–(14.6). For an unconditional workspace cap one may bound those workspaces by their displayed time bounds. The search reuses candidate storage; it does not store all $2^B$ or $2^Z$ candidates.

### 16.4 Querying, output, and validation

With a stored cyclic table on a sequential tape, one cyclic query takes at most $10(N+\ell_N+1)^2$ bit operations, including reduction of a group-sized query. With the outer/key representation instead, use (16.2), a sequential outer-table lookup, and at most $Z$ literal key comparisons; a bound is
$Q_{\rm lab}+20(B+Zb_*+1)(b_*+1)^3$.

For $r\ge2$, let $s=\lfloor\log_2r\rfloor$ and $L=N^s$. Using the compiled cyclic table, one product query for an $s\ell_N$-bit integer is bounded by
$$
10s\bigl[(s\ell_N+1)^2+(N+\ell_N+1)^2\bigr] \tag{16.8}
$$
bit operations and returns an $s$-bit color. The base divisions account for carries exactly. Full output by successive queries costs at most $L$ times (16.8), plus its metadata. Any explicit listing requires at least $L$ color symbols; in the specified fixed-width tuple encoding it requires **exactly $sL$ color bits**, and therefore at least $sL$ bit-writing steps. A tiny formula for $L$ is not an explicit output of that coloring.

On a unit-cost array RAM, cyclic validation uses at most $kN(N-1)$ color accesses, and ordinary interval validation at most $kL^2$. On a sequential bit/Turing implementation, safe bounds are respectively
$10kN^3(\ell_N+1)^3$ and $10kL^3(\ell_L+\ell_r+1)^3$.
One may instead validate the base cyclic table and use the proved digit-product construction, without separately scanning every progression in the much longer product interval.

The bounds distinguish preprocessing, enumeration, exhaustive derandomization, representation size, query cost, full output, and validation. They are not polynomial or practical claims about the overall construction. No finite record is asserted.
