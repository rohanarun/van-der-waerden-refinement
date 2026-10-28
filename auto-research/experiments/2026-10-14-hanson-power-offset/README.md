# A power-and-offset family of matrix profiles

**Result.** There is a continuum of abstract profiles interpolating between
`P(a,b)=ab` and the repository's `P_*`. Within the two-parameter family below,
separate **discrete** concavity and shifted tripling force exactly this
continuum. Its smallest diagonal exponent is **4/3**, uniquely at `P_*`.
Thus changing these two parameters cannot improve that obstruction.

This is an analytic research note with supplementary exact finite checks.
It has not received independent human review or formal proof checking.
It changes neither the van der Waerden coefficient nor a matrix multiplication
algorithm or tensor-character construction.

Base: `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.
Assignment seed: **46**, structural research. The initial hypothesis was that
varying the affine offset together with the power could reduce diagonal
growth while keeping the listed scalar constraints. The calculation below
closes that particular family rather than reporting an unsuccessful search.

From the repository root, run:

```sh
python3 -B auto-research/experiments/2026-10-14-hanson-power-offset/verify.py
```

Expected result: exit 0 and a JSON report with `status: "passed"`; the report
must equal the saved `RESULT.json`. The command reads and hashes its package
and pinned base files, uses only the Python standard library, writes no files,
and remains effective under `python3 -O`. See `RESULT.json` for exact counts,
parameters, negative witnesses, and scope. `MANIFEST.json` hashes all other
regular contribution files; it necessarily excludes itself. The shared track
index is outside the contribution manifest so later index appends do not
invalidate this package.

## Family and precise statement

For real `a,b >= 1`, put `u=min(a,b)`, `v=max(a,b)`. For fixed real
`lambda,s >= 0`, define

```math
F(x)=(1+\lambda)x-\lambda,\qquad
P_{\lambda,s}(a,b)=F(u)^s\bigl(v+\lambda(u-1)\bigr).
```

The domain `lambda,s >= 0` is part of the claim, not a conclusion about every
possible profile. Every member is positive and symmetric and has
`P(1,b)=b`. Separate discrete concavity means, for integers `a>=1,b>=2`,

```math
P(a,b-1)-2P(a,b)+P(a,b+1)\le0,
```

and the same inequality with the coordinates exchanged. Shifted tripling is
`P(a,3h+a-1) >= 3P(a,h)` for all positive integers `a,h`.

**Proposition.** A member of this family has these two properties if and only if

```math
0\le\lambda\le\tfrac12,\qquad
s=\frac{1-\lambda}{1+\lambda}.
```

Every such member is also nondecreasing and separately concave on the real
domain, and obeys

```math
P(a,b)\le(a+b-1)^{p},\quad
P(a,a)=F(a)^p=\Theta(a^p),\quad
p=1+s=\frac{2}{1+\lambda}.
```

It therefore fits the rank envelope at `t=1/p=(1+lambda)/2`. The smallest `p`
in this family is `4/3`, and the largest such `t` is `3/4`, uniquely at
`lambda=1/2,s=1/3`. At the other endpoint `lambda=0,s=1`, the profile is `ab`.
No assertion about optimality over profiles outside this family is made.

## Necessity, using only integer constraints

Write `d=1+lambda`. For integers `h>=a>=2`, both evaluations in shifted
tripling use the branch whose smaller coordinate is `a`, so

```math
P(a,3h+a-1)-3P(a,h)=F(a)^s(1-2\lambda)(a-1).
```

Hence `lambda<=1/2` is necessary. It is not sufficient by itself.

Let `T=F(n)`, with integers `n` tending to infinity. The second difference
centered at the diagonal in the row with first coordinate `n` is exactly

```math
\frac{P(n,n-1)-2P(n,n)+P(n,n+1)}{T^s}
=(1-d/T)^s(T-\lambda)-T+1.
```

For each fixed `lambda,s`, its limit is `1-lambda-sd`, by the first-order
Taylor expansion of `(1-x)^s` at zero. Discrete concavity forces this limit
to be nonpositive. Therefore `sd>=1-lambda`. In particular `s>0`, since
`lambda<=1/2`.

For the second difference centered at `b=n` in the row `a=n+1`, all three
points use the lower branch (including its endpoint). The exact expression is

```math
\Delta_n=(T-d)^s(T+1-\lambda)-2T^s(T+1)
                      +(T+d)^s(T+1+\lambda).
```

Taylor expansion to second order, with fixed parameters, gives

```math
\frac{\Delta_n}{T^{s-1}}
\longrightarrow s d\bigl((s-1)d+2\lambda\bigr)
=s d\bigl(sd+\lambda-1\bigr).
```

For completeness, divide the displayed expression for `Delta_n` by `T^s`
and expand `(1 +/- d/T)^s` through its quadratic term. The constant terms
cancel; the linear terms contribute `2sd lambda/T`; the quadratic terms
contribute `s(s-1)d^2(T+1)/T^2`. After multiplication by `T`, the remainder
is `O(1/T)`. This uses the usual Taylor remainder for a smooth real power
in a fixed neighborhood of 1, not any assumption that `s` is integral.

Discrete concavity makes the limit nonpositive. Since `s,d>0`, this gives
`sd<=1-lambda`. Together the two integer stencils force equality. Thus
necessity does not silently strengthen the repository's discrete concavity
assumption to continuous concavity.

## Sufficiency and the rank envelope

Assume the displayed parameter condition. Then `1/3<=s<=1` and
`sd=1-lambda`. Fix `a`. For `1<=b<=a`, put `G=a+lambda(b-1)`. Differentiation
gives

```math
\partial_b P=s d F(b)^{s-1}G+\lambda F(b)^s>0,
```

```math
\partial_b^2 P
=s d F(b)^{s-2}\bigl((s-1)dG+2\lambda F(b)\bigr)
=2s d\lambda F(b)^{s-2}(b-a)\le0.
```

For `b>=a` the profile is affine, with positive slope `F(a)^s`. The derivative
from the lower branch at `b=a` is `(sd+lambda)F(a)^s=F(a)^s`. There is no
upward jump in slope. These facts prove monotonicity and continuous concavity
in each coordinate, hence the required discrete inequalities.

Shifted tripling for `h>=a` follows from the difference already computed.
For `1<=h<a`, set `A=F(a)`, `B=F(h)>=1`, and `z=A/B>1`. A direct substitution
shows that the tripling difference, multiplied by the positive factor
`d/B^(s+1)`, is

```math
z^s\bigl(dz+3+(2\lambda-1)/B\bigr)-3(z+\lambda).
```

Because `2lambda-1<=0` and `B>=1`, this is at least

```math
f(z)=d z^s(z+2)-3(z+\lambda).
```

Here `f(1)=0`, `f'(1)=1-2lambda>=0`, and

```math
f''(z)=d s z^{s-2}\bigl((s+1)z+2(s-1)\bigr)\ge0
\qquad(z\ge1),
```

because the bracket is at least `3s-1>=0`. Hence `f(z)>=0` and tripling
holds. This also proves it for real `a,h>=1`.

Finally, with `S=a+b-1` and `u<=v`, both `F(u)` and `v+lambda(u-1)` are
at most `S`, since `lambda<=1/2<=1`. Their product with the stated powers
is at most `S^(s+1)`. The diagonal formula follows by substitution.
Since `2/(1+lambda)` decreases strictly with `lambda`, its unique minimum
on this interval is `4/3` at the repository's profile. An envelope with
`t>1/p` is impossible even on the diagonal: its right-hand side has exponent
`1/t<p`, whereas `P(a,a)=Theta(a^p)`.

## Exact computational evidence and controls

`verify.py` is a new implementation; it does not import `audit_math.py`,
`profile_lp.py`, SymPy, NumPy, or SciPy. For rational `s=m/n`, it computes
`P(a,b)^n = F(u)^m (v+lambda(u-1))^n` as a `Fraction`. Tripling, monotonicity,
and the rank envelope are compared after taking positive integer powers.
For concavity, where two radicals are added, it brackets each radical by
rational dyadic intervals using integer root bounds and accepts only when
the intervals certify the sign. Linear equalities are checked algebraically.
An unresolved interval fails the run; floating-point tolerances are absent.

An optional separate algebra check is available with SymPy 1.14.0:

```sh
python3 -B auto-research/experiments/2026-10-14-hanson-power-offset/check_identities.py
```

It checks six derivative and Taylor-coefficient identities. It does not prove
the domain inequalities or remainder bounds; those are in the written proof.

The finite domain and stopping rule are fixed in the verifier and reported
in `RESULT.json`. The seed-derived offsets supplement the two endpoints and
several simple interior parameters. All sampled points are checked; there is
no optimization, early-success stopping, or claim that this finite domain
proves the proposition.

Negative controls require **actual discrete violations**, not just failed
parameter screens: too large an offset violates tripling; too small a power
violates the diagonal stencil; too large a power violates an interior stencil.
The endpoints are included, as are exact interval checks and a polynomial
`ab` control. The verifier also replays the base profile's 10,000 tripling
and envelope comparisons with its independently defined family.

## Review scope and provenance

The base README and `parameters.json` describe the conditional van der Waerden
choice `c=1/9` and a supremum `1/8`; the launch text's `1/25` is historical.
The construction is traced through `short-period-runs-proof.md`, the digit-rank
rich-event cover, the sharpened outer coloring, and the pinned source inputs.
That proof chain is context only for this contribution. The result here uses
only the explicitly listed scalar matrix inequalities from `research-note.tex`.

The earlier finite LP output `experiments/matrix-profile.json` is exploratory;
it is neither a premise of the proposition nor an optimality certificate.
This work adds a continuous family and a necessity proof within it, rather
than rerunning the same LP with more computation. Prior Sidorenko searches
reported no smaller certificate and are unrelated to this family.

After the workspace migration restored access, live open PRs #9 and #10 and
PR10's conditional-review ledger were inspected at the pins in `SOURCES.json`.
Their listed work concerns the van der Waerden chain; no overlap was found
with this matrix-family contribution. The all-state issue list was empty, so
there was no coordination issue to comment on. `CLAIM.json` records the local
scope; `RESEARCH_HANDOFF.md` records commands, failures, baseline results and
remaining obligations.
Pinned sources, attribution, and AI disclosure are in `NOTICE.md`.
