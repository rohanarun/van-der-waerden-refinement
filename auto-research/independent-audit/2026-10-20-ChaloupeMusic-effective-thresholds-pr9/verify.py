#!/usr/bin/env python3
"""Independent checks for an adversarial audit of PR #9 (effective-completion).

PR #9 head 89660352f5dfcf1180a47b224610d444b2ce8701, base 54ac9715fceab938ca77d5980c36ab691765a04d.
Repository base of this audit: 63bef9ca996786a41169de4a0c3d6b3b47b0fe96.
Standard library only, no network. Run with `python3 -B verify.py` (assertions are
load-bearing; never run with -O). The JSON printed on stdout is RESULT.json.
`python3 -B verify.py --thresholds PATH` additionally compares, field by field, with the
THRESHOLDS.json file of PR #9 (sha256 pinned below).

Part A, exact (integers and fractions). The threshold checklist of PR #9, Section 12,
recomputed from the parameter tuples alone: region (3.1), derived constants, all 21 tests
at K = 2^t with the monomial certificate (12.8) decided by exact integer comparison, and
the minimality of the doubling (the test fails at t/2). Six tuples: literal PR7, literal
PR6, and the four general-rule tuples PR #9 records. The recomputed values are compared
with a transcription of PR #9's records embedded below.

Part B, exact polynomial identities over Q: (7.8), (7.9), (7.10), (7.11), the band
decomposition (8.9), the digit expansions (8.2)/(8.3), the rich-split identity (9.2) and
the gap identities of rule (13.1). A coordinatewise identity checked with two symbolic
coordinates holds in every dimension, since both sides are sums over coordinates.

Part C, finite exact replays (not proofs): separation (7.1) and balanced digits (8.1)
exhaustively on small groups; the digit product (13.3) exhaustively on small intervals;
and the whole chain of Sections 7 and 8 on actual progressions of a group in the literal
small regime k = 128 >= 64D, D = 2, q = 1021^2, with the half-open geometric V-mesh
(4.1): common return, two-point key lemma, single-class affinity (7.4), carries, vertex
identities, the cell estimate (7.11)-(7.12), digit forms (8.3)-(8.5), the C* decoding
(the step is recovered from the encoded data), and the A* band decomposition.

Part D, mutations: one per decisive constant or step. Each mutated check must fail.
"""
from decimal import Decimal as Dec, getcontext
from fractions import Fraction as Q
from math import gcd
import hashlib
import json
import random
import sys

PR9_HEAD = "89660352f5dfcf1180a47b224610d444b2ce8701"
THRESHOLDS_SHA256 = "a1820e5e6655746248171fc3cd23b2e1e24b99be52a75da80625581e7c900093"


def ceil_log2(x):
    """Least integer j with x <= 2^j, for a positive rational x (exact)."""
    x = Q(x)
    j = 0
    while x > Q(2) ** j:
        j += 1
    while j > -10**6 and x <= Q(2) ** (j - 1):
        j -= 1
    return j


def ceil_q(x):
    x = Q(x)
    return -((-x.numerator) // x.denominator)


def le_shift(lhs, rhs, shift):
    """Exact test lhs <= rhs * 2^shift for positive rationals, without allocating 2^shift
    when the bit lengths already decide it."""
    lhs, rhs = Q(lhs), Q(rhs)
    L = lhs.numerator * rhs.denominator
    R = rhs.numerator * lhs.denominator
    if L.bit_length() <= shift + R.bit_length() - 1:
        return True
    if L.bit_length() > shift + R.bit_length():
        return False
    return L <= (R << shift)


# --------------------------------------------------------------------------------------
# Part A. Threshold certificates.
TUPLES = {
    "literal_PR7": dict(route="digit-runs", a=Q(49, 100), m=Q(99, 100), b=Q(97, 200), gamma=Q(97, 200),
                        c=Q(1, 9), eps=Q(1, 200), eps_reg=Q(1, 200), delta=Q(1, 200), delta_s=Q(1, 2)),
    "literal_PR6": dict(route="carry-affine", a=Q(333, 1000), m=Q(4, 5), b=Q(331, 1000), gamma=Q(97, 200),
                        c=Q(1, 16), eps=Q(1, 200), eps_reg=Q(1, 200), delta=Q(1, 200), delta_s=Q(1, 2)),
}
GENERAL_C = {"general_1/100": Q(1, 100), "general_1/9": Q(1, 9),
             "general_1249/10000": Q(1249, 10000), "general_near_endpoint": Q(124999999999, 10**12)}


def rule_13_1(c):
    s0 = min(Q(1, 100), (Q(1, 8) - c) / 4)
    return dict(route="digit-runs", a=Q(1, 2) - 2 * s0, b=Q(1, 2) - 3 * s0, gamma=Q(1, 2) - 3 * s0,
                m=1 - 3 * s0, c=c, eps=s0, eps_reg=s0, delta=s0, delta_s=Q(1, 2))


for _name, _c in GENERAL_C.items():
    TUPLES[_name] = rule_13_1(_c)


def region(P):
    a, m, b, g_, c = P["a"], P["m"], P["b"], P["gamma"], P["c"]
    eps, er, de, ds = P["eps"], P["eps_reg"], P["delta"], P["delta_s"]
    conds = [0 < a, 0 < b, 0 < c, 2 * a < m, m < 1, b < a, 0 < eps < Q(1, 2), 0 < er <= Q(1, 2),
             0 < de < 1, 0 < ds < 1, 0 < g_ < (Q(1, 2) - eps) * (1 - er) * (1 - de)]
    if P["route"] == "digit-runs":
        conds += [a + b < 1, 2 * c < g_ * b]
    else:
        conds += [2 * a + b < 1, Q(5, 2) * c < g_ * b]
    return all(conds)


def constants(P):
    eps, er, de, ds, g_, b, c = P["eps"], P["eps_reg"], P["delta"], P["delta_s"], P["gamma"], P["b"], P["c"]
    A0 = (Q(1, 2) - eps) * (1 - er)
    K = dict(A0=A0, g=A0 * (1 - de) - g_, alpha0=(Q(1, 2) - eps) * ds / 2, beta0=(1 - ds) / 2)
    K["B0"] = ceil_q(Q(128) / er + 4)
    K["CL"] = 32 + 4 * ceil_log2(K["B0"] + 1)
    K["Leps"] = ceil_log2(Q(48) / eps**2)
    K["C1"] = 260 + K["Leps"]
    if P["route"] == "digit-runs":
        K["mu"] = (g_ * b - 2 * c) / 2
        K["frak_b"] = min(K["mu"], b * K["alpha0"])
    else:
        K["mu"] = (g_ * b - Q(5, 2) * c) / 2
        K["frak_b"] = K["mu"]
    return K


def checklist(P, K):
    """The 21 tests, in PR #9's order. Monomial rows are (name, A, d, j, target)."""
    a, m, b, eps, er, de, ds = P["a"], P["m"], P["b"], P["eps"], P["eps_reg"], P["delta"], P["delta_s"]
    e2 = eps**2
    rows = [
        ("k>=16", "t", None), ("logk>=1", "t/2", None),
        ("anchor entropy", "t/2", 4 * K["CL"] / e2),
        ("third incidence entropy", "t/2", (42 + K["Leps"]) / (e2 * ds)),
        ("regular fraction", "8/t^2", er),
        ("dimension", Q(128), 1 - a, 0, Q(1)),
        ("short period cutoff", Q(8), m - a, 2, Q(1)),
        ("small blocks", Q(64), 1 - m, 0, Q(1)),
        ("rotating drift", Q(128), 3 - a - m, 0, er),
        ("dichotomy remainder", 4 * K["A0"], 1 - m, 0, K["g"]),
        ("flip bias", Q(1), b, 0, Q(1, 2)),
        ("first row size", 1 + 4 / e2, m, 0, de),
        ("second size", 8 / e2, a, 0, Q(1)),
        ("third size", 4 / (e2 * ds), a, 0, Q(1)),
        ("first incidence", Q(K["C1"]), m - 2 * a, 3, e2 * de),
        ("second incidence", Q(4 * (2 + K["Leps"])), a, 0, e2),
        ("rich inverse log", "20000/t", K["frak_b"] / 3),
        ("rich dimension error", Q(10000), 1 - a, 0, K["frak_b"] / 3),
        ("rich digit error", Q(10000), a, 0, K["frak_b"] / 3),
    ]
    if P["route"] == "digit-runs":
        rows += [("heavy run entropy", Q(200), 1 - a - b, 3, K["beta0"] / 2),
                 ("affine key entropy", Q(200), a - b, 1, K["beta0"] / 2)]
    else:
        rows += [("affine full-label entropy", Q(300), 1 - 2 * a - b, 3, Q(1, 4)),
                 ("affine band entropy", Q(300), a - b, 1, Q(1, 4))]
    return rows


def run_tests(P, t, K=None):
    K = K or constants(P)
    out = []
    for row in checklist(P, K):
        name = row[0]
        if len(row) == 3:
            kind, val = row[1], row[2]
            if name == "k>=16":
                rec = dict(name=name, lhs=Q(4), rhs=Q(t), passed=t >= 4)
            elif name == "logk>=1":
                rec = dict(name=name, lhs=Q(1), rhs=Q(t, 2), passed=Q(t, 2) >= 1)
            elif kind == "t/2":
                rec = dict(name=name, lhs=val, rhs=Q(t, 2), passed=val <= Q(t, 2))
            elif kind == "8/t^2":
                rec = dict(name=name, lhs=Q(8, t * t), rhs=val, passed=Q(8, t * t) <= val)
            else:  # 20000/t: the inverse-log term 10000/log k against frak_b/3, with log k >= t/2
                rec = dict(name=name, lhs=Q(20000, t), rhs=val, passed=Q(20000, t) <= val)
        else:
            A, d, j, u = row[1], row[2], row[3], row[4]
            fl = (d * t).numerator // (d * t).denominator
            mono = d > 0 and Q(t, 2) >= Q(j) / d
            ratio = A * Q(t) ** j / u
            ok = mono and le_shift(A * Q(t) ** j, u, fl)
            rec = dict(name=name, A=A, decay=d, log_degree=j, target=u, floor_decay_t=fl,
                       monotone_for_all_larger_k=mono, passed=ok,
                       ratio_numerator_bits=ratio.numerator.bit_length(),
                       ratio_denominator_bits=ratio.denominator.bit_length())
        out.append(rec)
    return out


def threshold_t(P, limit_exp=200):
    """PR #9's procedure: t = 4, doubled until all tests pass. Returns (t, rounds)."""
    t, rounds = 4, 0
    while True:
        rounds += 1
        if all(r["passed"] for r in run_tests(P, t)):
            return t, rounds
        t *= 2
        assert t < 2**limit_exp


# Transcription of PR #9's THRESHOLDS.json (sha256 above), literal tuples: per test,
# (A, decay, log_degree, target, floor_decay_t) for monomials and (lhs, rhs) otherwise.
RECORDED_LITERAL = {
    "literal_PR7": dict(t=33554432, rounds=24, B0=25604, CL=92, Leps=21, C1=281,
                        g="40499/8000000", mu="4681/720000", tests=[
        ("k>=16", "4", "33554432"), ("logk>=1", "1", "16777216"),
        ("anchor entropy", "14720000", "16777216"), ("third incidence entropy", "5040000", "16777216"),
        ("regular fraction", "1/140737488355328", "1/200"),
        ("dimension", "128", "51/100", 0, "1", 17112760),
        ("short period cutoff", "8", "1/2", 2, "1", 16777216),
        ("small blocks", "64", "1/100", 0, "1", 335544),
        ("rotating drift", "128", "38/25", 0, "1/200", 51002736),
        ("dichotomy remainder", "19701/10000", "1/100", 0, "40499/8000000", 335544),
        ("flip bias", "1", "97/200", 0, "1/2", 16273899),
        ("first row size", "160001", "99/100", 0, "1/200", 33218887),
        ("second size", "320000", "49/100", 0, "1", 16441671),
        ("third size", "320000", "49/100", 0, "1", 16441671),
        ("first incidence", "281", "1/100", 3, "1/8000000", 335544),
        ("second incidence", "92", "49/100", 0, "1/40000", 16441671),
        ("rich inverse log", "625/1048576", "4681/2160000"),
        ("rich dimension error", "10000", "51/100", 0, "4681/2160000", 17112760),
        ("rich digit error", "10000", "49/100", 0, "4681/2160000", 16441671),
        ("heavy run entropy", "200", "1/40", 3, "1/8", 838860),
        ("affine key entropy", "200", "1/200", 1, "1/8", 167772)]),
    "literal_PR6": dict(t=33554432, rounds=24, B0=25604, CL=92, Leps=21, C1=281,
                        g="40499/8000000", mu="857/400000", tests=[
        ("k>=16", "4", "33554432"), ("logk>=1", "1", "16777216"),
        ("anchor entropy", "14720000", "16777216"), ("third incidence entropy", "5040000", "16777216"),
        ("regular fraction", "1/140737488355328", "1/200"),
        ("dimension", "128", "667/1000", 0, "1", 22380806),
        ("short period cutoff", "8", "467/1000", 2, "1", 15669919),
        ("small blocks", "64", "1/5", 0, "1", 6710886),
        ("rotating drift", "128", "1867/1000", 0, "1/200", 62646124),
        ("dichotomy remainder", "19701/10000", "1/5", 0, "40499/8000000", 6710886),
        ("flip bias", "1", "331/1000", 0, "1/2", 11106516),
        ("first row size", "160001", "4/5", 0, "1/200", 26843545),
        ("second size", "320000", "333/1000", 0, "1", 11173625),
        ("third size", "320000", "333/1000", 0, "1", 11173625),
        ("first incidence", "281", "67/500", 3, "1/8000000", 4496293),
        ("second incidence", "92", "333/1000", 0, "1/40000", 11173625),
        ("rich inverse log", "625/1048576", "857/1200000"),
        ("rich dimension error", "10000", "667/1000", 0, "857/1200000", 22380806),
        ("rich digit error", "10000", "333/1000", 0, "857/1200000", 11173625),
        ("affine full-label entropy", "300", "3/1000", 3, "1/4", 100663),
        ("affine band entropy", "300", "1/500", 1, "1/4", 67108)]),
}
RECORDED_GENERAL = {  # name: (t, rounds, B0, CL, Leps, C1, outer balance g, rich mu)
    "general_1/100": (8388608, 22, 12804, 88, 19, 279, "10249/1000000", "2009/20000"),
    "general_1/9": (67108864, 25, 36868, 96, 22, 282, "83663/23887872", "161/18432"),
    "general_1249/10000": (2199023255552, 40, 5120004, 124, 37, 297, "1600099999/64000000000000", None),
    "general_near_endpoint": (39614081257132168796771975168, 94, 512000000000004, 228, 90, 350, None, None),
}


def compare_recorded(name, P, tests, K, t, rounds):
    rec = RECORDED_LITERAL[name]
    assert (t, rounds) == (rec["t"], rec["rounds"]), (name, t, rounds)
    assert (K["B0"], K["CL"], K["Leps"], K["C1"]) == (rec["B0"], rec["CL"], rec["Leps"], rec["C1"])
    assert K["g"] == Q(rec["g"]) and K["mu"] == Q(rec["mu"])
    assert len(tests) == len(rec["tests"]) == 21
    for mine, theirs in zip(tests, rec["tests"]):
        assert mine["name"] == theirs[0], (mine["name"], theirs[0])
        if len(theirs) == 3:
            assert (mine["lhs"], mine["rhs"]) == (Q(theirs[1]), Q(theirs[2])), (name, theirs)
        else:
            got = (mine["A"], mine["decay"], mine["log_degree"], mine["target"], mine["floor_decay_t"])
            want = (Q(theirs[1]), Q(theirs[2]), theirs[3], Q(theirs[4]), theirs[5])
            assert got == want, (name, mine["name"], got, want)
    return True


def part_a():
    res = {}
    for name, P in TUPLES.items():
        assert region(P), name
        K = constants(P)
        t, rounds = threshold_t(P)
        tests = run_tests(P, t, K)
        assert len(tests) == 21 and all(r["passed"] for r in tests), name
        failing_half = [r["name"] for r in run_tests(P, t // 2, K) if not r["passed"]]
        assert failing_half, name  # t is the first passing doubling
        # Exact margins of the conditions that only hold for large k, at the threshold.
        if name in RECORDED_LITERAL:
            compare_recorded(name, P, tests, K, t, rounds)
        else:
            rt, rr, B0, CL, Le, C1, g, mu = RECORDED_GENERAL[name]
            assert (t, rounds, K["B0"], K["CL"], K["Leps"], K["C1"]) == (rt, rr, B0, CL, Le, C1), name
            assert g is None or K["g"] == Q(g)
            assert mu is None or K["mu"] == Q(mu)
        binding = [r["name"] for r in run_tests(P, t // 2, K) if not r["passed"]]
        res[name] = dict(t=str(t), K="2^" + str(t), rounds=rounds, tests_passed=21,
                         failing_at_half_t=binding, B0=K["B0"], CL=K["CL"], L_eps=K["Leps"], C1=K["C1"],
                         outer_balance=str(K["g"]), rich_mu=str(K["mu"]), frak_b=str(K["frak_b"]))
    # Rule (13.1) gaps, exactly, on the four general tuples.
    for name, c in GENERAL_C.items():
        P = TUPLES[name]
        s0 = P["eps"]
        D_ = Q(1, 8) - c
        assert P["m"] - 2 * P["a"] == s0 and P["a"] - P["b"] == s0 and 1 - P["a"] - P["b"] == 5 * s0
        assert 1 - P["m"] == 3 * s0
        assert P["gamma"] * P["b"] / 2 - c >= 5 * D_ / 8 > 0
    return res


def compare_file(path):
    raw = open(path, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == THRESHOLDS_SHA256, "not PR #9's THRESHOLDS.json"
    data = json.loads(raw)
    n = 0
    for name, P in TUPLES.items():
        theirs = data["finite_corroboration_only"]["thresholds"][name]
        K = constants(P)
        t = int(theirs["t"])
        mine = run_tests(P, t, K)
        assert theirs["route"] == P["route"] and theirs["passed"] and theirs["valid_region"]
        assert theirs["doubling_rounds"] == threshold_t(P)[1]
        for k_, v in theirs["parameters"].items():
            assert Q(v) == P[k_], (name, k_)
        for x, y in zip(mine, theirs["checks"]):
            assert x["name"] == y["name"] and x["passed"] == y["passed"] is True
            for f in ("A", "decay", "target", "lhs", "rhs"):
                if f in y:
                    assert x[f] == Q(y[f]), (name, x["name"], f)
            for f in ("log_degree", "floor_decay_t", "ratio_numerator_bits", "ratio_denominator_bits",
                      "monotone_for_all_larger_k"):
                if f in y:
                    assert x[f] == y[f], (name, x["name"], f, x[f], y[f])
            n += 1
    lit = data["literal_certificates"]
    for name in RECORDED_LITERAL:
        assert lit[name] == data["finite_corroboration_only"]["thresholds"][name]
    return n


# --------------------------------------------------------------------------------------
# Part B. Exact polynomial identities.
class Poly:
    __slots__ = ("t",)

    def __init__(self, terms=None):
        self.t = {k: v for k, v in (terms or {}).items() if v != 0}

    @staticmethod
    def var(name):
        return Poly({((name, 1),): Q(1)})

    @staticmethod
    def const(c):
        return Poly({(): Q(c)})

    def _co(self, o):
        return o if isinstance(o, Poly) else Poly.const(o)

    def __add__(self, o):
        o = self._co(o)
        r = dict(self.t)
        for k, v in o.t.items():
            r[k] = r.get(k, 0) + v
        return Poly(r)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) - self

    def __mul__(self, o):
        o = self._co(o)
        r = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                d = dict(k1)
                for n, e in k2:
                    d[n] = d.get(n, 0) + e
                k = tuple(sorted(d.items()))
                r[k] = r.get(k, 0) + v1 * v2
        return Poly(r)

    __rmul__ = __mul__

    def __pow__(self, n):
        r = Poly.const(1)
        for _ in range(n):
            r = r * self
        return r

    def is_zero(self):
        return not self.t


def dot(u, v):
    r = Poly.const(0)
    for x, y in zip(u, v):
        r = r + x * y
    return r


def vertex_identities(mutant=None):
    """(7.8)-(7.11) and (8.9) with two symbolic coordinates. Returns the list of identities
    that hold; `mutant` perturbs one formula (negative control)."""
    V = Poly.var
    q, c, s, sa, s0, P1, P2 = (V(x) for x in ("q", "c", "s", "sa", "s0", "P1", "P2"))
    Y0 = [V("Y01"), V("Y02")]
    t = [V("t1"), V("t2")]
    be = [V("b1"), V("b2")]
    v = [V("v1"), V("v2")]
    q2 = q * q
    w = dot(be, be)
    W = q2 * w
    Ya = [Y0[i] + c * (t[i] + be[i]) - v[i] for i in range(2)]
    zeta_a = q2 * (2 * dot(Ya, be) + sa * w)
    zeta_0 = q2 * (2 * dot(Y0, be) + s0 * w)
    f = q2 * dot([Ya[i] + s * be[i] for i in range(2)], [Ya[i] + s * be[i] for i in range(2)])
    lam_coef = (c * c + c * sa) if mutant != "Lambda" else (c * c - c * sa)
    Lam = (q2 * dot(Y0, Y0) + 2 * c * q2 * dot(Y0, t) - lam_coef * W - 2 * q2 * dot(Y0, v)
           + q2 * (c * c * dot(t, t) + dot(v, v) - 2 * c * dot(t, v)))
    half = Q(1, 2) if mutant != "7.11" else Q(1)
    ok = {}
    ok["7.8"] = (f - (q2 * dot(Ya, Ya) + s * (s - sa) * W + s * zeta_a)).is_zero()
    ok["7.9"] = (q2 * dot(Ya, Ya) - (Lam + c * zeta_a)).is_zero()
    ok["7.10"] = (f - (Lam + s * (s - sa) * W + (c + s) * zeta_a)).is_zero()
    ok["7.11"] = (q2 * dot(v, be) - (c * q2 * dot(t, be) + (c + (sa - s0) * half) * q2 * w
                                     + (zeta_0 - zeta_a) * Q(1, 2))).is_zero()
    tau = q2 * dot(Y0, v) - q * P1 - P2
    K = -2 * (q * P1 + P2) + q2 * dot(v, v)
    G = (q2 * dot(Y0, Y0) + 2 * c * (q2 * dot(Y0, t)) + (s * (s - sa) - c * c - c * sa) * W
         + q2 * c * c * dot(t, t) - 2 * c * q2 * dot(t, v))
    ok["8.9"] = (f - (K + G - 2 * tau + (c + s) * zeta_a)).is_zero()
    return ok


def digit_identity(Dd=5, mutant=False):
    """(8.2)/(8.3): q^2<Y,v> = q<S1 v,y> + <S2 v,y> + <v,F>, Y_i = sum_{l<i} y_l q^{l-i},
    multiplied through by q^Dd to stay polynomial."""
    V = Poly.var
    q = V("q")
    y = [V("y%d" % l) for l in range(Dd)]
    v = [None] + [V("v%d" % i) for i in range(1, Dd + 1)] + [Poly.const(0), Poly.const(0)]
    lhs = Poly.const(0)
    for i in range(1, Dd + 1):
        Yi_scaled = Poly.const(0)  # q^Dd * Y_i
        for l in range(i):
            Yi_scaled = Yi_scaled + y[l] * q ** (Dd + l - i)
        lhs = lhs + q * q * v[i] * Yi_scaled
    S1y = Poly.const(0)
    S2y = Poly.const(0)
    for l in range(Dd):
        S1y = S1y + v[l + 1] * y[l]
        S2y = S2y + v[l + 2 if not mutant else l + 3] * y[l]
    vF = Poly.const(0)
    for i in range(1, Dd + 1):
        for l in range(0, i - 2):
            vF = vF + v[i] * y[l] * q ** (Dd + l - i + 2)
    rhs = q ** Dd * (q * S1y + S2y) + vF
    return (lhs - rhs).is_zero()


def part_b():
    ok = vertex_identities()
    assert all(ok.values()), ok
    assert digit_identity(5)
    # (9.2) for both routes' budgets with kappa + nu = 2, every R <= D, D <= 40.
    n92 = 0
    for P in (TUPLES["literal_PR7"], TUPLES["general_1/9"], TUPLES["general_near_endpoint"]):
        g_, b, c = P["gamma"], P["b"], P["c"]
        mu = (g_ * b - 2 * c) / 2
        for D in range(1, 41):
            for R in range(0, D + 1):
                kap, nu = Q(R, D), Q(2 * D - R, D)
                th = (kap * c + g_ * b - nu * c) / (2 * b)
                assert 0 < th < g_
                assert b * th - kap * c == mu == b * (g_ - th) - nu * c
                n92 += 1
    # Rule (13.1) gap identities, symbolic in s0 and c.
    s, c = Poly.var("s"), Poly.var("c")
    gap = (Q(1, 2) - s) * (1 - s) ** 2 - (Q(1, 2) - 3 * s)
    assert (gap - (s + Q(5, 2) * s * s - s ** 3)).is_zero()
    rich = (Q(1, 2) - 3 * s) ** 2 * Q(1, 2) - c
    assert (rich - ((Q(1, 8) - c) - Q(3, 2) * s + Q(9, 2) * s * s)).is_zero()
    return dict(vertex_identities=sorted(ok), digit_expansion_dimension=5, rich_split_cases=n92,
                rule_13_1_identities=2)


# --------------------------------------------------------------------------------------
# Part C. Finite exact replays.
def centered(r, mod):
    """Centered representative in [-1/2, 1/2) of r/mod (r an integer residue)."""
    r %= mod
    return Q(r, mod) if 2 * r < mod else Q(r, mod) - 1


def Ycoords(lam, n, q, D):
    return tuple(centered(lam * n, q**i) for i in range(1, D + 1))


def balanced_digits(x, q, D):
    x %= q**D
    out = []
    for _ in range(D):
        r = x % q
        if r > (q - 1) // 2:
            r -= q
        out.append(r)
        x = (x - r) // q
    return out


def part_c_small():
    cases = 0
    tight = 0
    for q, D in ((5, 2), (5, 3), (7, 3), (9, 2), (9, 3), (11, 2)):
        N = q**D
        for m in range(1, N):
            Y = Ycoords(1, m, q, D)
            nrm = sum((q * y) ** 2 for y in Y)
            assert nrm >= 1  # (7.1)
            tight += nrm == 1
            dg = balanced_digits(m, q, D)
            for i in range(1, D + 1):
                assert Y[i - 1] == sum(Q(dg[l]) * Q(q) ** (l - i) for l in range(i))  # (8.1)
                F = sum(Q(dg[l]) * Q(q) ** (l - i + 2) for l in range(0, i - 2))
                assert abs(F) <= Q(1, 2)
            cases += 1
    assert tight > 0  # equality in (7.1) is attained: the constant is sharp
    return cases, tight


def mono_free_cyclic(N, k):
    for mask in range(2**N):
        C = [(mask >> n) & 1 for n in range(N)]
        if all(len({C[(a + j * d) % N] for j in range(k)}) > 1 for a in range(N) for d in range(1, N)):
            return C
    return None


def product_monochromatic(C, N, s, k, digit_rule="all"):
    L = N**s

    def color(n):
        dg = []
        for _ in range(s):
            dg.append(n % N)
            n //= N
        if digit_rule == "all":
            return tuple(C[x] for x in dg)
        if digit_rule == "top":
            return C[dg[-1]]
        return C[dg[0]]

    col = [color(n) for n in range(L)]
    checked = 0
    for d in range(1, L):
        for a in range(0, L - (k - 1) * d):
            checked += 1
            c0 = col[a]
            if all(col[a + j * d] == c0 for j in range(1, k)):
                return (a, d), checked
    return None, checked


def part_c_product():
    N, k = 7, 4
    C = mono_free_cyclic(N, k)
    assert C is not None
    total = 0
    for s in (1, 2, 3):
        bad, checked = product_monochromatic(C, N, s, k)
        assert bad is None
        total += checked
    return C, total


# The Section 7-8 chain on actual progressions.
class Mesh:
    """Half-open geometric V-mesh: endpoints a_j = alpha((1+H)^j - 1) for j < m_V and
    a_{m_V} = 1/2. In rho, interval j is [a_j, a_{j+1}) on the negative half and
    (a_j, a_{j+1}] on the positive half. Its width is at most alpha z^j (z - 1) = H alpha z^j
    <= H(rho + alpha) on its closure, inside the upper bound of (4.1); this is all that
    Sections 7 and 8 use. Membership is decided by a correctly rounded 80-digit logarithm
    when it is at least 1e-40 away from an endpoint, and by exact integers otherwise."""

    def __init__(self, k, q, D):
        self.K = k * k
        self.Qa = q ** (D + 1)  # 1/alpha
        getcontext().prec = 80
        self.lnz = (Dec(self.K + 1) / Dec(self.K)).ln()
        self.exact_calls = 0
        x = Q(2 + self.Qa, 2)  # z^j >= 1 + 1/(2 alpha)  <=>  a_j >= 1/2
        g = (Dec(x.numerator) / Dec(x.denominator)).ln() / self.lnz
        j = int(g) + 1
        while not self._pow_ge(j, x):
            j += 1
        while self._pow_ge(j - 1, x):
            j -= 1
        self.mV = j

    def _pow_ge(self, j, x):  # exact z^j >= x
        self.exact_calls += 1
        return (self.K + 1) ** j * x.denominator >= x.numerator * self.K ** j

    def _pow_le(self, j, x, strict):  # exact z^j <= x (or <)
        self.exact_calls += 1
        lhs, rhs = (self.K + 1) ** j * x.denominator, x.numerator * self.K ** j
        return lhs < rhs if strict else lhs <= rhs

    def count_le(self, rho, strict):
        """Largest j < m_V with a_j <= rho (or a_j < rho): a_j <= rho iff z^j <= 1 + rho/alpha."""
        x = Q(1) + rho * self.Qa
        g = (Dec(x.numerator) / Dec(x.denominator)).ln() / self.lnz
        j = int(g)
        frac = g - j
        if not (Dec("1e-40") < frac < 1 - Dec("1e-40")):
            j += 1
            while j > 0 and not self._pow_le(j, x, strict):
                j -= 1
        return min(j, self.mV - 1)

    def box(self, y):
        if y < 0:
            return (-1, self.count_le(y + Q(1, 2), strict=False))
        return (1, self.count_le(Q(1, 2) - y, strict=True))


def chain_on_progression(n0, d, k, q, D, lam, mesh, stats, band=1, window=4):
    N = q**D
    H = Q(1, k * k)
    Y = [Ycoords(lam, n0 + j * d, q, D) for j in range(k)]
    boxes = [tuple(mesh.box(y) for y in Yj) for Yj in Y]
    keys = [(boxes[j], (q * q * sum(y * y for y in Y[j])) // band) for j in range(k)]
    mult = {}
    for kk in keys:
        mult[kk] = mult.get(kk, 0) + 1
    assert max(mult.values()) <= 2, "two-point key lemma (7.2)"
    pos = {}
    for j, bx in enumerate(boxes):
        pos.setdefault(bx, []).append(j)
    gaps = {}
    for js in pos.values():
        for i1 in range(len(js)):
            for i2 in range(i1 + 1, len(js)):
                g = js[i2] - js[i1]
                vg = tuple(Y[js[i2]][i] - Y[js[i1]][i] for i in range(D))
                assert all(abs(x) <= 2 * H for x in vg)
                assert gaps.setdefault(g, vg) == vg
    if not gaps:
        stats["no_box_return"] += 1
        return
    stats["with_return"] += 1
    gl = sorted(gaps)
    for g1 in gl:  # common return vector: v_g = g B
        for g2 in gl:
            assert all(g2 * gaps[g1][i] == g1 * gaps[g2][i] for i in range(D))
    h = 0
    for g in gl:
        h = gcd(h, g)
    B = tuple(gaps[gl[0]][i] / gl[0] for i in range(D))
    beta = Ycoords(lam, h * d, q, D)
    assert beta == tuple(h * x for x in B) and all(abs(x) <= 2 * H for x in beta)
    W = q * q * sum(x * x for x in beta)
    assert W >= 1  # (7.3)
    for js in pos.values():  # each box in one residue; h is itself a return gap
        assert len({j % h for j in js}) == 1
        for i1 in range(len(js)):
            for i2 in range(i1 + 1, len(js)):
                assert js[i1] + h < k and boxes[js[i1] + h] == boxes[js[i1]]
    ydh = tuple(Q((lam * d) % q**i, q**i) * h for i in range(1, D + 1))
    t = tuple(ydh[i] - beta[i] for i in range(D))
    assert all(x.denominator == 1 for x in t)
    t = tuple(int(x) % h for x in t)
    slope = tuple((t[i] + beta[i]) / h for i in range(D))
    A = Y[0]
    m = []
    for j in range(k):  # carries (7.5)
        mj = tuple(A[i] + j * slope[i] - Y[j][i] for i in range(D))
        assert all(x.denominator == 1 for x in mj)
        m.append(tuple(int(x) for x in mj))
    for a in range(min(h, k)):
        assert all(-1 <= x <= h - 1 for x in m[a])
    classes = {}
    for a in range(h):
        js = list(range(a, k, h))
        ks = [keys[j] for j in js]
        if len(set(ks)) < len(ks):
            classes[a] = js
    for kk, c_ in mult.items():  # a repeated key lies in a collision class
        if c_ == 2:
            j1, j2 = [j for j in range(k) if keys[j] == kk]
            assert (j1 % h) in classes
    if not classes:
        stats["return_without_collision"] += 1
        return
    stats["with_collision"] += 1
    for a, js in classes.items():  # (7.4)
        for s_, j in enumerate(js):
            assert Y[j] == tuple(Y[a][i] + s_ * beta[i] for i in range(D))
    w = sum(x * x for x in beta)
    sigma, zeta = {}, {}
    for a, js in classes.items():
        best = None
        for s1 in range(len(js)):
            for s2 in range(s1 + 1, len(js)):
                if keys[js[s1]] == keys[js[s2]]:
                    cand = (s2 - s1, s1, s2)
                    best = cand if best is None or cand < best else best
        _, s1, s2 = best
        sigma[a] = s1 + s2
        zeta[a] = q * q * (2 * sum(Y[a][i] * beta[i] for i in range(D)) + sigma[a] * w)
        assert abs(zeta[a]) < Q(1, s2 - s1)  # (7.8)
    a0 = min(classes)
    Y0 = Y[a0]
    Tip = sum(t[i] * beta[i] for i in range(D))
    cellT = (q * q * Tip).__floor__()
    cellW = ((k + 1) * q * q * w).__floor__()
    e = balanced_digits(lam * h * d, q, D)
    assert all(abs(x) <= 2 * H * (q + 1) for x in e)
    assert beta == tuple(sum(Q(e[l]) * Q(q) ** (l - i) for l in range(i)) for i in range(1, D + 1))
    ydig = balanced_digits(lam * (n0 + a0 * d), q, D)
    rows, vals = [], []
    for a, js in classes.items():
        ca = Q(a - a0, h)
        va = tuple(m[a][i] - m[a0][i] for i in range(D))
        if any(va):
            stats["nonzero_carry_difference"] += 1
        assert Y[a] == tuple(Y0[i] + ca * (t[i] + beta[i]) - va[i] for i in range(D))
        Lam = (q * q * sum(x * x for x in Y0) + 2 * ca * q * q * sum(Y0[i] * t[i] for i in range(D))
               - (ca * ca + ca * sigma[a]) * W - 2 * q * q * sum(Y0[i] * va[i] for i in range(D))
               + q * q * (ca * ca * sum(x * x for x in t) + sum(x * x for x in va)
                          - 2 * ca * sum(t[i] * va[i] for i in range(D))))
        for s_, j in enumerate(js):
            f = q * q * sum(y * y for y in Y[j])
            assert f == Lam + s_ * (s_ - sigma[a]) * W + (ca + s_) * zeta[a]  # (7.10)
        lhs = q * q * sum(va[i] * beta[i] for i in range(D))
        assert lhs == (ca * q * q * Tip + (ca + Q(sigma[a] - sigma[a0], 2)) * q * q * w
                       + (zeta[a0] - zeta[a]) / 2)  # (7.11)
        Xa = ca * cellT + (ca + Q(sigma[a] - sigma[a0], 2)) * Q(cellW, k + 1)
        assert abs(Xa - lhs) < 3
        # (S1 v)_l = v_{l+1} and (S2 v)_l = v_{l+2} in PR #9's 1-based coordinates, v_{D+1} = 0;
        # va is 0-based (va[i] = v_{i+1}).
        S1 = [va[l] for l in range(D)]
        S2 = [va[l + 1] if l + 1 < D else 0 for l in range(D)]
        f1 = sum(S1[l] * e[l] for l in range(D))
        f2 = sum(S2[l] * e[l] for l in range(D))
        Rv = lhs - q * f1 - f2
        assert abs(Rv) <= Q(3 * sum(abs(x) for x in va), k * k)  # (8.3)
        assert abs(Xa / q - f1) < Q(1, 2)  # (8.4): nearest integer
        assert -window <= f2 - (Xa - q * f1) <= window, "window (8.5)"
        # A*: band decomposition (8.9) with the integer forms of the start digits.
        P1 = sum(S1[l] * ydig[l] for l in range(D))
        P2 = sum(S2[l] * ydig[l] for l in range(D))
        Fv = [sum(Q(ydig[l]) * Q(q) ** (l - i + 2) for l in range(0, i - 2)) for i in range(1, D + 1)]
        tau = sum(va[i] * Fv[i] for i in range(D))
        assert q * q * sum(Y0[i] * va[i] for i in range(D)) == q * P1 + P2 + tau
        assert abs(tau) <= sum(abs(x) for x in va) * Q(1, 2)
        Kj = -2 * (q * P1 + P2) + q * q * sum(x * x for x in va)
        for s_, j in enumerate(js):
            G = (q * q * sum(x * x for x in Y0) + 2 * ca * q * q * sum(Y0[i] * t[i] for i in range(D))
                 + (s_ * (s_ - sigma[a]) - ca * ca - ca * sigma[a]) * W
                 + q * q * ca * ca * sum(x * x for x in t) - 2 * ca * q * q * sum(t[i] * va[i] for i in range(D)))
            assert q * q * sum(y * y for y in Y[j]) == Kj + G - 2 * tau + (ca + s_) * zeta[a]
        rows += [S1, S2]
        vals += [f1, f2]
    # C*: the R basis rows and their values recover the digits of the return from the
    # other D - R digits, and hence the step d.
    basis, bvals, piv = [], [], []
    for r, val in zip(rows, vals):
        r = [Q(x) for x in r]
        val = Q(val)
        for (br, bv, pc) in zip(basis, bvals, piv):
            if r[pc] != 0:
                fct = r[pc] / br[pc]
                r = [x - fct * y for x, y in zip(r, br)]
                val -= fct * bv
        nz = [i for i, x in enumerate(r) if x != 0]
        if nz:
            basis.append(r)
            bvals.append(val)
            piv.append(nz[0])
        else:
            assert val == 0  # consistency of the dependent forms
    R = len(basis)
    stats["rank_hist"][R] = stats["rank_hist"].get(R, 0) + 1
    known = {i: Q(e[i]) for i in range(D) if i not in piv}
    sol = dict(known)
    for br, bv, pc in reversed(list(zip(basis, bvals, piv))):
        acc = bv - sum(br[i] * sol[i] for i in range(D) if i != pc and br[i] != 0)
        sol[pc] = acc / br[pc]
    assert [sol[i] for i in range(D)] == [Q(x) for x in e]
    lamhd = sum(int(sol[l]) * q**l for l in range(D)) % N
    assert (lamhd * pow(lam * h, -1, N)) % N == d % N
    stats["decoded"] += 1


# Progressions found by a seeded search (vertex construction for one class, h in {2,3,4},
# return digits |e_l| <= 3) whose chain has two or more collision classes and a nonzero
# carry difference: (n0, d), in Z/q^3 with k = 192, q = 1031^2, lambda = 30030.
MULTI_CLASS = [
    (1175961843997444353, 1197398707650348206), (791097964867294896, 3626137827061475),
    (699151383238243856, 3626137827061475), (1017411609070694455, 3626137827061475),
    (2239670474381459, 3626137827061475), (119542575222367815, 542280915091735828),
    (151604542531044780, 1197398707650348206),
]


def vertex_instance(rnd, k, q, D, lam):
    """A progression whose class 0 passes through its vertex: return digits e, gap h, and a
    start whose leading digits y satisfy 2<y,e> + sigma |e|^2 = 0."""
    N = q**D
    while True:
        h = rnd.choice([1, 2, 2, 3, 4])
        e = [rnd.randint(-3, 3) for _ in range(D)]
        idx = [i for i in range(D) if abs(e[i]) == 1]
        if not idx:
            continue
        ee = sum(x * x for x in e)
        sigma = rnd.randrange(10, 2 * (k // h) - 10)
        sigma += (sigma * ee) % 2
        i0 = rnd.choice(idx)
        y = [rnd.randint(-400, 400) for _ in range(D)]
        rest = sum(y[i] * e[i] for i in range(D) if i != i0)
        y[i0] = (-sigma * ee // 2 - rest) * e[i0]
        x = sum(y[l] * q**l for l in range(D)) % N
        E = sum(e[l] * q**l for l in range(D))
        d = (E * pow(lam * h, -1, N)) % N
        n0 = (x * pow(lam, -1, N) - rnd.randrange(h) * d) % N
        return n0, d


def part_c_chain(n_gen=150, seed=20261020, band=1, window=4, multi=True):
    k, P, D = 192, 1031, 3
    q = P * P
    lam = 2 * 3 * 5 * 7 * 11 * 13
    assert gcd(lam, P) == 1 and k >= 64 * D and k < P <= 2 * k * k
    mesh = Mesh(k, q, D)
    assert mesh.box(Q(-1, 2)) == (-1, 0) and mesh.box(Q(0)) == (1, mesh.mV - 1)
    rnd = random.Random(seed)
    stats = dict(no_box_return=0, with_return=0, return_without_collision=0, with_collision=0,
                 nonzero_carry_difference=0, decoded=0, rank_hist={})
    cases = list(MULTI_CLASS) if multi else []
    cases += [vertex_instance(rnd, k, q, D, lam) for _ in range(n_gen)]
    for n0, d in cases:
        chain_on_progression(n0, d, k, q, D, lam, mesh, stats, band=band, window=window)
    multi_seen = stats["rank_hist"].copy()
    stats["rank_hist"] = {str(r): c for r, c in sorted(stats["rank_hist"].items())}
    if multi:
        assert stats["nonzero_carry_difference"] >= 7 and max(multi_seen) >= 3
    stats.update(k=k, P=P, q=q, D=D, lam=lam, m_V=mesh.mV, progressions=len(cases),
                 multi_class_progressions=len(MULTI_CLASS) if multi else 0, seed=seed,
                 exact_mesh_decisions=mesh.exact_calls)
    return stats


# --------------------------------------------------------------------------------------
# Part D. Mutations: each must make a check fail.
def expect_failure(fn, message=None):
    """True when fn fails an assertion (whose text contains `message`, if given)."""
    try:
        fn()
    except AssertionError as error:
        return message is None or message in str(error)
    return False


def mutated_tuple(name, **changes):
    P = dict(TUPLES[name])
    P.update(changes)
    return P


def part_d():
    out = {}
    P7, P6 = TUPLES["literal_PR7"], TUPLES["literal_PR6"]
    t = 33554432

    def all_pass(P, t_, K=None):
        assert region(P)
        assert all(r["passed"] for r in run_tests(P, t_, K))

    def recorded(name, P, K=None):
        K = K or constants(P)
        t_, rounds = threshold_t(P)
        compare_recorded(name, P, run_tests(P, t_, K), K, t_, rounds)

    # The threshold K = 2^t itself.
    out["K halved (PR7): t = 2^24"] = expect_failure(lambda: all_pass(P7, t // 2))
    out["K halved (PR6): t = 2^24"] = expect_failure(lambda: all_pass(P6, t // 2))
    # Coefficients: c pushed to the endpoint of each route.
    out["PR7 c = 1/8"] = expect_failure(lambda: all_pass(mutated_tuple("literal_PR7", c=Q(1, 8)), t))
    out["PR6 c = 1/15"] = expect_failure(lambda: all_pass(mutated_tuple("literal_PR6", c=Q(1, 15)), t))
    # Constants of Section 12, each recomputed differently: the recorded certificate no longer matches.
    for label, key, val in (("B0 with 64/eps_reg", "B0", 12804), ("C_L = 88", "CL", 88),
                            ("L_eps = 20", "Leps", 20), ("C_1 = 280", "C1", 280)):
        def f(key=key, val=val):
            K = constants(P7)
            K[key] = val
            if key == "Leps":
                K["C1"] = 260 + val
            recorded("literal_PR7", P7, K)
        out["PR7 " + label] = expect_failure(f)
    # Decisive inequality constants: 10000 in (12.1) -> 20000 on PR6; 4C_L/eps^2 with C_L doubled.
    def f_12_1():
        K = constants(P6)
        K["frak_b"] = K["frak_b"] / 2  # equivalent to doubling 10000
        assert all(r["passed"] for r in run_tests(P6, t, K))
    out["PR6 (12.1) constant 10000 -> 20000"] = expect_failure(f_12_1)

    def f_anchor():
        K = constants(P7)
        K["CL"] = 2 * K["CL"]
        assert all(r["passed"] for r in run_tests(P7, t, K))
    out["PR7 anchored entropy C_L doubled"] = expect_failure(f_anchor)
    # Balance gap g: gamma raised to the balance limit.
    out["PR7 gamma = A0(1-delta)"] = expect_failure(
        lambda: all_pass(mutated_tuple("literal_PR7", gamma=(Q(1, 2) - Q(1, 200)) * Q(199, 200) ** 2), t))
    # Identities.
    out["(7.9) Lambda with -c*sigma"] = not vertex_identities("Lambda")["7.9"]
    out["(7.11) factor (sigma_a - sigma_0) without 1/2"] = not vertex_identities("7.11")["7.11"]
    out["(8.2) S_2 shifted by three"] = not digit_identity(5, mutant=True)
    # Finite replays.
    out["(7.2) band of width 4 instead of 1"] = expect_failure(
        lambda: part_c_chain(n_gen=40, seed=7, band=4), "two-point key lemma (7.2)")
    out["(8.5) window [-4,4] shrunk to [0,0]"] = expect_failure(
        lambda: part_c_chain(n_gen=0, window=0), "window (8.5)")
    C = mono_free_cyclic(7, 4)
    out["(13.3) top digit only"] = product_monochromatic(C, 7, 2, 4, "top")[0] is not None
    out["(13.3) lowest digit only"] = product_monochromatic(C, 7, 2, 4, "low")[0] is not None
    assert all(out.values()), {k_: v for k_, v in out.items() if not v}
    return out


def main():
    res = {}
    res["part_a_thresholds"] = part_a()
    res["part_b_identities"] = part_b()
    cases, tight = part_c_small()
    C, aps = part_c_product()
    res["part_c_small_groups"] = dict(nonzero_elements_checked=cases, equality_cases_in_7_1=tight,
                                      base_coloring_Z7_k4=C, ordinary_4APs_checked_s_1_to_3=aps)
    res["part_c_sections_7_8_chain"] = part_c_chain()
    res["part_d_mutations"] = part_d()
    res["pins"] = dict(pr9_head=PR9_HEAD, thresholds_sha256=THRESHOLDS_SHA256,
                       base="63bef9ca996786a41169de4a0c3d6b3b47b0fe96")
    if len(sys.argv) == 3 and sys.argv[1] == "--thresholds":
        n = compare_file(sys.argv[2])
        print("file comparison: %d recorded tests match field by field" % n, file=sys.stderr)
    print(json.dumps(res, indent=2, sort_keys=True))
    print("Test passé", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
