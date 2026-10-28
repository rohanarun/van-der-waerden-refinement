#!/bin/sh
# Rebuilds and writes evidence/ in one pass, so that the evidence carries the
# fingerprint of the sources that produced it (verify.py checks it). Every
# command runs under the sprint's compute guard, borne.py.
set -e
cd "$(dirname "$0")"
BORNE=${BORNE:-$HOME/Downloads/bigospeedrun/vdw/outils/borne.py}
SOURCES="KeyMultiplicity.lean KeyMultiplicity/Basic.lean Axioms.lean lakefile.toml lean-toolchain lake-manifest.json"
# The package's own build only (Mathlib stays): the record is of a fresh build,
# not of an up-to-date one that would print no "Built" line.
rm -rf .lake/build
python3 "$BORNE" 30m evidence/build.log --but "lake build of KeyMultiplicity for evidence/; a few minutes at most" -- lake build
grep -E 'Built KeyMultiplicity|Build completed' evidence/build.log > evidence/build.txt
python3 "$BORNE" 20m evidence/axioms.log --but "print axioms of every KeyMultiplicity constant; one minute at most" -- lake env lean Axioms.lean
grep -v '^borne' evidence/axioms.log > evidence/axioms.txt
rm evidence/build.log evidence/axioms.log
shasum -a 256 $SOURCES > evidence/sources.sha256
lean --version > evidence/lean-version.txt
