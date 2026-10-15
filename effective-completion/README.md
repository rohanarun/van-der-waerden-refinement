# Effective van der Waerden construction

This proposed completion proves that, for each fixed rational $0<c<1/8$, a
computable integer $K(c)$ works for every integer $k\ge K(c)$ and every $r\ge2$:

$$
W_r(k)>k^{ck\lfloor\log_2 r\rfloor}.
$$

The threshold is independent of the allowed prime and the number of colors.
There is no congruence or subsequence restriction on $k$. The endpoint $c=1/8$
is excluded. “Admitted” means exactly that $k$ passes the threshold for the
selected parameter tuple, as defined in [the proof](PROOF.md).

The two literal choices, $c=1/9$ from
[PR7](https://github.com/rohanarun/van-der-waerden-refinement/pull/7) and the
independent $c=1/16$ route from
[PR6](https://github.com/rohanarun/van-der-waerden-refinement/pull/6), both admit
$K=2^{33,554,432}$. This common threshold applies to those displayed tuples;
other coefficients use their separately computed $K(c)$.

The proof supplies one global outer coloring, treats all cross-family
dependencies, closes the geometric and counting steps, and specifies exact
finite searches that terminate. The generator first finds a cyclic binary
table and then uses its digit product to color an interval of exact length
$N^{\lfloor\log_2 r\rfloor}$ with at most $r$ colors. This is an effective
existence result with enormous finite costs, without a practical algorithm,
finite coloring record, or formal proof-assistant certificate.

The coefficient range and core methods are prior public proposals. Credit
OpenAI's [upstream construction](https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026),
Rohan Arun's base repository, supplying the two-point norm-band lemma and
sharpened outer construction, Artus Krohn-Grimberghe's
[PR4 precursor](https://github.com/artuskg/van-der-waerden-refinement/blob/4b4e80ea5e0ffec956577004905f22659af0bff5/repeated-key-certificate-proof.md),
and DaysSky's Claude-assisted
[carry-rank](https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/rank-certificate-proof.md),
[digit-rank](https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/digit-rank-proof.md), and
[short-period](https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/short-period-runs-proof.md)
refinements. Prepared for Artus Krohn-Grimberghe with OpenAI Pro and Codex
assistance. No independent-discovery or priority claim is made.

Read the self-contained [proof](PROOF.md), exact [generator specification](GENERATOR.md),
[source ledger](SOURCE-LEDGER.md), [dependency ledger](DEPENDENCIES.json), and
[threshold certificates](THRESHOLDS.json). The original completed draft received
independent local mathematical review and an Opus review requiring attribution
and ledger corrections. This corrected revision is subject to exact-version
acceptance before publication. Human review and formal certification remain
unclaimed. The structured closed resource envelopes are supplementary
estimates; the DIRECT generator carries the stated ordinary bit/Turing bound
for its search phase, after exact integer setup (GENERATOR.md).
