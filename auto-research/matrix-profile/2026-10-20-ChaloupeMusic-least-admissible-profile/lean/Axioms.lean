import Profile

/-! `lake env lean Axioms.lean`: `#print axioms` on every declaration of `Profile`; any axiom
other than `propext`, `Classical.choice`, `Quot.sound` (`sorryAx`, `Lean.ofReduceBool`, a new
`axiom`) is an error. -/

open Lean Elab Command in
elab "#check_all_axioms" : command => do
  let env ← getEnv
  let mut names := #[]
  for (name, _) in env.constants.toList do
    if (`Profile).isPrefixOf name && !name.isInternal then names := names.push name
  let mut bad := #[]
  for name in names do
    for a in ← liftCoreM (collectAxioms name) do
      unless a == ``propext || a == ``Classical.choice || a == ``Quot.sound do
        bad := bad.push m!"{name}: {a}"
  if bad.isEmpty then
    logInfo m!"{names.size} declarations, axioms within propext, Classical.choice, Quot.sound"
  else
    logError m!"non-standard axioms: {bad}"

#check_all_axioms
