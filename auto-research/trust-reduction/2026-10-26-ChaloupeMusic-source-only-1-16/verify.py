"""Exact checks for the source-only region (every c < 1/16, explicit 1/17).

Checks, in exact rational arithmetic:
  1. the explicit tuple lies strictly inside the region, with the margins
     printed in README.md section 9;
  2. the side conditions of the source-lemma transfer (README section 2) hold
     at the tuple;
  3. the supremum of c over the region is 1/16: a sequence of admissible
     tuples approaches it, and the endpoint is rejected;
  4. seven negative controls are rejected;
  5. the files match MANIFEST.json.
The asymptotic estimates are proved in README.md, not checked here.
"""

import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ICI = Path(__file__).resolve().parent

TUPLE = dict(a=F(497, 1000), m=F(999, 1000), b=F(99, 200), eps=F(1, 1000),
             eps_r=F(1, 1000), delta=F(1, 1000), delta_s=F(1, 2),
             gamma=F(497, 1000), c=F(1, 17))

# The repository's headline tuple (short-period-runs-proof.md), for control 6.
TUPLE_1_9 = dict(a=F(49, 100), m=F(99, 100), b=F(97, 200), eps=F(1, 200),
                 eps_r=F(1, 200), delta=F(1, 200), delta_s=F(1, 2),
                 gamma=F(97, 200), c=F(1, 9))


def marges(t):
    """Each region inequality as (name, rhs - lhs); all must be > 0."""
    cap = (F(1, 2) - t["eps"]) * (1 - t["eps_r"]) * (1 - t["delta"])
    return [
        ("b > 0", t["b"]),
        ("b < a", t["a"] - t["b"]),
        ("a + b < 1", 1 - t["a"] - t["b"]),
        ("2a < m", t["m"] - 2 * t["a"]),
        ("m < 1", 1 - t["m"]),
        ("0 < eps < 1/2", min(t["eps"], F(1, 2) - t["eps"])),
        ("0 < eps_r", t["eps_r"]),
        ("0 < delta < 1", min(t["delta"], 1 - t["delta"])),
        ("0 < delta_s < 1", min(t["delta_s"], 1 - t["delta_s"])),
        ("0 < gamma < cap", min(t["gamma"], cap - t["gamma"])),
        ("0 < c < gamma*b/4", min(t["c"], t["gamma"] * t["b"] / 4 - t["c"])),
    ]


def admis(t):
    return all(v > 0 for _, v in marges(t)) and t["eps_r"] <= F(1, 2)


def transfert(t):
    """Side conditions of README section 2, as strict linear inequalities."""
    a, m = t["a"], t["m"]
    return [
        ("h_0 < P: a < 1", 1 - a),
        ("m < 2 (path, heavy width, short periods)", 2 - m),
        ("m < 3 (drift)", 3 - m),
        ("a + m < 3 (rotating drift below eta)", 3 - a - m),
        ("a > 0 (case (i), log q = o(k log k))", a),
    ]


def main():
    echecs = []

    print("1. Explicit tuple, c = 1/17")
    for nom, v in marges(TUPLE):
        print(f"   {nom:22s} margin {v}")
        if v <= 0:
            echecs.append(f"tuple: {nom}")
    attendu = {"b < a": F(1, 500), "a + b < 1": F(1, 125), "2a < m": F(1, 200),
               "m < 1": F(1, 1000), "0 < gamma < cap": F(1002499, 10**9),
               "0 < c < gamma*b/4": F(36451, 13600000)}
    for nom, v in marges(TUPLE):
        if nom in attendu and v != attendu[nom]:
            echecs.append(f"margin {nom}: {v} != README {attendu[nom]}")
    if 1 - TUPLE["b"] - 2 * TUPLE["a"] >= 0:
        echecs.append("tuple should violate 2a < 1 - b (PR #2 region)")
    print(f"   ratio over the source 1/100000: {F(100000) * TUPLE['c']}")

    print("2. Source-lemma transfer conditions")
    for nom, v in transfert(TUPLE):
        print(f"   {nom:42s} margin {v}")
        if v <= 0:
            echecs.append(f"transfer: {nom}")

    print("3. Supremum 1/16")
    for n in (10, 100, 1000, 10000):
        e = F(1, n)
        t = dict(a=F(1, 2) - e, m=1 - e, b=F(1, 2) - 2 * e, eps=e * e,
                 eps_r=e * e, delta=e * e, delta_s=F(1, 2),
                 gamma=F(1, 2) - e, c=None)
        t["c"] = t["gamma"] * t["b"] / 4 - e * e * e
        if not admis(t):
            echecs.append(f"sup sequence n={n} not admissible")
        print(f"   n={n:5d}  c = {float(t['c']):.10f}  gap to 1/16 = {float(F(1, 16) - t['c']):.2e}")
        if t["c"] >= F(1, 16):
            echecs.append("sequence reached 1/16")

    print("4. Negative controls")
    controles = {
        "c = 1/16": dict(TUPLE, c=F(1, 16)),
        "b = a": dict(TUPLE, b=TUPLE["a"]),
        "m = 2a": dict(TUPLE, m=2 * TUPLE["a"]),
        "gamma at the balance cap": dict(
            TUPLE, gamma=(F(1, 2) - TUPLE["eps"]) * (1 - TUPLE["eps_r"]) * (1 - TUPLE["delta"])),
        "c = gamma*b/4": dict(TUPLE, c=TUPLE["gamma"] * TUPLE["b"] / 4),
        "repository 1/9 tuple (needs the rich chain K)": TUPLE_1_9,
        "eps = 1/2": dict(TUPLE, eps=F(1, 2)),
    }
    rejetes = 0
    for nom, t in controles.items():
        ok = admis(t)
        print(f"   {nom:46s} {'ACCEPTED (bad)' if ok else 'rejected'}")
        if ok:
            echecs.append(f"control accepted: {nom}")
        else:
            rejetes += 1

    print("5. Manifest")
    manifeste = json.loads((ICI / "MANIFEST.json").read_text())
    for nom, h in sorted(manifeste.items()):
        reel = hashlib.sha256((ICI / nom).read_bytes()).hexdigest()
        print(f"   {nom:12s} {'ok' if reel == h else 'MISMATCH'}")
        if reel != h:
            echecs.append(f"hash {nom}")

    print()
    if echecs:
        print("FAIL")
        for e in echecs:
            print("  -", e)
        return 1
    print(f"PASS ({rejetes} negative controls rejected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
