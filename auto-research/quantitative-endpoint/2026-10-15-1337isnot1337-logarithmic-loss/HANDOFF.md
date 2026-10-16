# Review handoff

## Proposed PR title

Conditional logarithmic endpoint bound and c=1/9 threshold 2^4096

## Mathematical review priorities

The first priority is the finite interface in `PROOF.md`, Section 2.
The new proof needs uniform finite counts, rather than limits with constants that depend on fixed exponents.
The explicit factors in PR #9 support that use. Their source proofs still need independent review.

The second priority is the new weighted event in Section 6.
Its variance uses distinct label variables and squared multiplicities.
Its tolerance is additive in the total progression length.
The dependence graph includes all three event families.

The third priority is the independent short-period cutoff `M_s`.
The count of abstract words uses `h_0`, whereas the s-light threshold uses `M_s`.
The run conclusion applies only to actual short-period progressions.

The fourth priority is the finite rich split in Section 8.
It uses the actual numbers `log q` and `log(1/p)`, without a fixed-power exponent substitution.
The selected certificates retain literal keys and all shared-key correlations.

## Reproduction and limits

Run the command in `README.md`.
The tests use exact arithmetic and include all-larger-t certificates and finite negative controls.
They do not certify the source encodings or the full geometric theorem.
The paper proof, not the finite samples, establishes the new conditional transfer.

No baseline source is modified.
The patch contains only the new track and contribution files.
The repository's original test suite was not rerun.
The patch apply, byte comparison, and reverse-apply checks are recorded in the delivery receipt.

## Distinguish the claims

The new result is not `c>1/8`.
It is a quantified approach to 1/8, plus a smaller sufficient threshold for `c=1/9`.
The comparison threshold belongs to the open PR #9 and is not a previously established finite coloring record.
The new `2^4096` threshold is still computationally impractical.
