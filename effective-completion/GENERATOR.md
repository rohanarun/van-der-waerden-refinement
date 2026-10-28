# Exact finite generator specification

This specification defines a uniform terminating computation on the theorem's
admitted inputs. It supplies an integer-only cyclic-table implementation and
the more structured outer/key implementation proved in [PROOF.md](PROOF.md).
Neither uses a supplied program, nonuniform advice, a random-bit sampler, or a
real-number oracle. No theorem-sized execution is claimed.

## Input and admission

The input consists of integers $k,r$, one of the three parameter modes below,
and optionally an integer $P$.

| Mode | Fixed rational parameters | Admission threshold |
| --- | --- | --- |
| General | Rational $0<c<1/8$, with rule (13.1) of PROOF | Compute $t$ by the exact procedure below; use $K(c)=2^t$ |
| Literal PR7 | $a=49/100$, $m=99/100$, $b=\gamma=97/200$, $c=1/9$, $\epsilon=\epsilon_{\rm reg}=\delta=1/200$, $\delta_s=1/2$ | $2^{33,554,432}$, with all 21 recorded tests checked |
| Literal PR6 | $a=333/1000$, $m=4/5$, $b=331/1000$, $\gamma=97/200$, $c=1/16$, $\epsilon=\epsilon_{\rm reg}=\delta=1/200$ | $2^{33,554,432}$, with all 21 recorded tests checked; the harmless third-family checks use $\delta_s=1/2$ |

Reject unless $r\ge2$, the selected strict parameter region holds, and
$k\ge2^t$ for its own threshold certificate. This last comparison can use the
binary length of $k$; there is no need to allocate a second huge threshold
integer. All integers at least that threshold are admitted. A below-threshold
input is outside this guarantee; it is not proof that its desired coloring is
impossible. The literal PR7 tuple is not replaced by the general-rule tuple
when $c=1/9$ is selected.

For a supplied $P$, test by trial division that $P$ is prime and
$k<P\le2k^2$. Without a supplied $P$, enumerate that finite interval in
increasing order and select its first prime. The elementary binomial argument
in PROOF 3 guarantees that one exists on admitted inputs.

## Rational threshold algorithm

Represent every rational by coprime signed numerator and positive denominator.
All comparisons below are exact cross-multiplications of integers.

1. For general $c$, compute
   $s_0=\min(1/100,(1/8-c)/4)$ and the full rule (13.1). The explicit positive
   gaps proved there justify eventual acceptance. For either literal mode,
   use its displayed tuple without alteration.
2. Compute $A_0,g,\alpha_0,\beta_0,B_0,C_L,L_\epsilon,C_1$ exactly as in
   PROOF 12. A rational base-two logarithmic ceiling means the least integer
   $j$ for which the rational argument is at most $2^j$; it uses integer
   comparisons, not floating-point logarithms.
3. On PR7 set $\mu=(\gamma b-2c)/2$ and
   $\mathfrak b=\min(\mu,b\alpha_0)$. On PR6 set
   $\mu_6=(\gamma b-5c/2)/2$ and $\mathfrak b=\mu_6$.
4. Set $t=4$. Test $t\ge4$, $t/2\ge1$,
   $t/2\ge4C_L/\epsilon^2$,
   $t/2\ge(42+L_\epsilon)/(\epsilon^2\delta_s)$, and
   $8/t^2\le\epsilon_{\rm reg}$.
5. For every monomial $A k^{-d}(\log k)^j$ in the complete checklist of
   PROOF 12, require $d>0$ and $t/2\ge j/d$. Certify its allotted positive
   rational target $u$ by
   $A t^j 2^{-\lfloor dt\rfloor}\le u$. Split (12.1) into three equal
   targets $\mathfrak b/3$, with its inverse-log test
   $60000/t\le\mathfrak b$. Split (12.2) into two targets $\beta_0/2$ on
   PR7; split (12.3) into two targets $1/4$ on PR6. Include every row, rather
   than testing only the decisive rich margin.
6. If any test fails, double $t$ and repeat. Otherwise return $t$ and the
   full rational/integer certificate. Monotonicity in PROOF 12.1 proves all
   the inequalities for every $k\ge2^t$. The strictly positive decay gaps
   prove this loop terminates for every admitted parameter mode.

To compare the shifted rational inequality without allocating $2^h$ for huge
$h=\lfloor dt\rfloor$, first compare integer binary lengths after clearing
denominators; shift only if their lengths can still overlap. This is an
ordinary finite integer decision. [THRESHOLDS.json](THRESHOLDS.json) records
all 21 tests for each literal tuple, independently computed before this
submission. Those certificates establish admission, not an executed coloring.

## Integer setup for the cyclic-table search

Compute $D=\lceil k^a\rceil$ by integer root search: if $a=u/v$ in lowest
terms, $D$ is the least positive integer satisfying $D^v\ge k^u$.
For $c=u/v$, start with $q=P$ and multiply repeatedly by $P$ until
$q^{vD}\ge k^{uk}$. This is exactly the prescribed least positive $P$-power,
including a perfect-power equality. Then compute $N=q^D$.

The coloring-existence proof uses the meshes, outer events and shared-key
perturbation. Once that existence is established, the following simpler
search does not need to construct those intermediate objects.

```text
VALID(k, N, C):
    for a = 0,...,N-1:
        for d = 1,...,N-1:
            bit = C[a]
            monochromatic = true
            x = a
            for j = 1,...,k-1:
                x = (x+d) mod N
                if C[x] != bit:
                    monochromatic = false
                    break
            if monochromatic:
                return false, (a,d)
    return true

DIRECT(k, N):
    for binary counter m = 0,...,2^N-1:
        C[n] = bit n of m, for n = 0,...,N-1
        if VALID(k,N,C): return C
    return CONSTRUCTION_FAILURE
```

The validator includes every nonzero cyclic step. It excludes the zero step,
which would make every coloring fail. Since $N$ is a power of $P>k$, every
nonzero step has order at least $P$, so the tested progressions have distinct
terms. Any failure certificate gives an actual start and step.

The analytic proof establishes that a valid table exists. DIRECT enumerates
every table once, so on admitted inputs it returns before its finite exhaustion
ends; CONSTRUCTION_FAILURE is unreachable there. Each candidate has finite
validation cost. After the exact integer setup, a deliberately conservative
ordinary sequential bit/Turing bound is

$$
100\,2^N kN^3(\lceil\log_2(N+1)\rceil+1)^3.
$$

The extra factor $N$ prices sequential table access; random-access indexing
is not free. Search storage is $O(N+\log N+\log k)$ bits, with reusable
candidate and counter tapes. Integer setup and output costs are additional.
This bound is finite, not polynomial or practical.

## Structured outer and shared-key search

For the decomposition in PROOF 15, compute $M,L_0,h_0,\lambda$, the exact
adaptive mesh, every point's literal label and key, and the ordered used-key
set of size $Z\le N$. All ceilings, root comparisons, half-open memberships
and rational norm-band floors are specified in PROOF 14. At equality, retain
the stated endpoint side; do not perturb it numerically.

Enumerate the finite outer events exactly. Family 1 uses actual progression
words and deterministic light rows outside heavy-containing blocks. Family 2
uses each eligible recorded word once for its $h,t$. Family 3 uses each
realizable abstract short word once, irrespective of its number of
realizations. PR7 uses all three; PR6 needs only the first two.

The continuous feasibility test is the exact strict/non-strict
Fourier–Motzkin decision over rational coefficients and algebraic right-hand
sides in PROOF 14.4. It retains singleton faces and distinguishes the strict
dummy condition from closed regularity. Finitely many lift and dummy-witness
choices price enumeration time; they do not multiply indexed event counts.
The abstract word family does not assert the actual single-run theorem.

Enumerate all $B$-bit outer tables, where $B$ is the entire finite label-space
size in PROOF 3. Return the first table avoiding every event. The combined
finite local lemma proves this loop terminates within $2^B$ candidates. Its
dependency graph is support intersection over independent label bits; all
cross-family incidences are included in PROOF 6.2.

For that fixed outer table, enumerate all $2^Z$ flip assignments and form
$C(n)=c_*(L(n))\mathbin{\mathsf{xor}}E_{\kappa(n)}$. The same key uses the
same bit at every occurrence. Validate every resulting table with VALID and
return the first successful assignment. The strict probability total is at
most $3/4$ on PR7 and $1/2$ on PR6. Since $0<p<1$, every assignment has
positive probability, so this finite search terminates. There is no claim of
independence between different bad events. Conflicting shared-key
prescriptions are empty; consistent ones are bounded as proved.

PROOF 16 records supplementary closed resource-envelope estimates for this
decomposition; those estimates are not independently certified complexity
claims. Exact finite termination uses the proved decision procedures and
finite searches. The accepted quantitative ordinary bit/Turing bound is the
integer-only DIRECT procedure above. Neither events nor a good seed are
supplied as free advice.

## Product output and independent verification

Compute $s=\lfloor\log_2r\rfloor$ by binary length and $L=N^s$ by integer
multiplication. For $0\le n<L$, repeated division by $N$ yields the unique
digits $n_0,\ldots,n_{s-1}$. Return the $s$-bit tuple
$(C(n_0),\ldots,C(n_{s-1}))$, or its ordinary binary integer in
$\{0,\ldots,2^s-1\}$. These are at most $r$ colors. Translate the interval
by one for the convention $[1,L]$.

For every positive-step ordinary progression contained in this interval,
the least nonzero $N$-adic digit of its step is a nonzero cyclic progression
in the validated base table (PROOF 13). This proves the product, including
all carries and composite $N$, without another enormous interval scan.
Alternatively, a validator can directly test every positive step and start
with $a+(k-1)d<L$; this is again a finite independent check.

Metadata must distinguish a formula for $L$, a query description, a fully
stored cyclic table, and a fully listed interval coloring. Listing the
product in fixed-width tuple encoding requires exactly $sL$ color bits.
Any finite examples below the theorem threshold are corroboration only.
