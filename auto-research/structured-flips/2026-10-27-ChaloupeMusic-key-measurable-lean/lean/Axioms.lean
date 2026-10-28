import KeyMeasurable

-- `#print axioms` on every constant of the `KeyMeasurable` namespace, auxiliary
-- `_proof_*` and compiler constants included, so that no declaration added
-- later escapes the audit (model: the referee's AllAxioms-L.lean).
open Lean Elab Command in
elab "#audit_ns" : command => do
  let env ← getEnv
  let mut names := #[]
  for (n, _) in env.constants.toList do
    if (`KeyMeasurable).isPrefixOf n then names := names.push n
  logInfo m!"{names.size} constants"
  for n in names.qsort (·.toString < ·.toString) do
    elabCommand (← `(#print axioms $(mkIdent n)))

#audit_ns
