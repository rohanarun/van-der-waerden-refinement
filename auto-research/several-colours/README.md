# Track: several-colours

Goal: the coefficient `c_r = liminf ln W_r(k)/(k ln k)` at a **fixed** number
`r ≥ 3` of colours. The source reaches `r` colours only through its digit
product, `c_r ≥ c⌊log₂ r⌋`. This track asks whether a construction that uses
the `r` colours directly does better.

| Date | Author | Note | Status | PR |
|---|---|---|---|---|
| 2026-10-27 | ChaloupeMusic | [The template with r colours: W_3(k) > k^{k/7}, relative to the source and PR #19](2026-10-27-ChaloupeMusic-three-colour-template/README.md): an outer colouring and flips in `ℤ/r` make the rich cost `(1 − 1/r)k` instead of `k/2`, while the slow side (`b < a`, `a + b < 1`) does not depend on `r`; so every `c < (1 − 1/r)/4` at fixed `r`, cyclic, hence composable in mixed base: `c_3 ≥ 1/7`, `c_{3·2^m} ≥ 1/7 + m/9`, against `⌊log₂ r⌋/9` | research note (proof relative to the source and #19, replayed at `r` colours) | – |
