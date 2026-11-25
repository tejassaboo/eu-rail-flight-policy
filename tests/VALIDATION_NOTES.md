# Validation notes: eu-rail-flight-policy (paid wave 3 validation, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w3_2026-11-25/eu-rail-flight-policy@w3/`, arm
`full`, DeepSeek V4 Flash (Nebius fp8), temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin
head 7715599. Line numbers are lines of `src/plugin/data/policy.txt`.

## Results

27/32 valid (84.4%), mean field score 0.927, **easy 5/6** (elm-sounding fails). By category: boundary 8/8,
distractor 3/3, easy 5/6, flag 2/4, hidden 2/3, multi 5/5, refusal 2/3. $0.00192 billed per run, 3.97 calls per run,
25,435 prompt tokens per call. `full` would exceed the hosted 65,536 cap on 31 of 32 runs (before step 4); not changed
here.

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| elm-sounding | **easy** | KLM connection 5S8F-8KBN (EUR 154), LOWEST_FARE; key Air France nonstop U5QS-PZYP (EUR 182) | model slip | All three offers were in the search it received; the nonstop was second of three. "The cheapest is KLM at 15400 ... No reason to choose a more expensive one." It never read lines 684-687 ("Direct flights are the norm"; only the authorising officer may refuse one as manifestly unreasonable). The nonstop is 18% dearer, inside the 40% of lines 663-664 on either reading, so the connection is not a defensible equal. The key and record are right; the always-cheapest agent fails it, as designed. |
| basil-ridge | refusal | FLAG Aer Lingus EUR 118, APPROVAL_REQUIRED, AUTHORISING_OFFICER; key REFUSE | **scenario defect: the record left a hold open** | It quoted lines 1210-1213 ("if the line manager and authorising officer ... ultimately wish to cover the cost ... a new authorisation to travel with expenses must be entered and approved") and held for that new authorisation: "the ticket cannot be booked now; it must wait for that new approval". The traveller asks the organisation to pay "anyway", and nothing on file says whether the line manager and authorising officer wish to cover it, so a hold for their sign-off is a fair reading of the FLAG definition ("the ticket must wait ... for someone's sign-off"). The key's own note relied on "which nobody has asked for", which the record did not state. |
| dahlia-spindle | flag | BOOK KLM connection, LOWEST_FARE; key FLAG either offer | model slip | It quoted lines 684-686 and then decided the open question itself: "the direct flight would be a manifestly unreasonable expense". Lines 685-686 give that call to the authorising officer, and it never weighed whether the 40% of lines 663-664 reaches a 2,058 km route. The flag twin nutmeg-spire passed. |
| ember-thimble | flag | BOOK Lufthansa business, LONG_FLIGHT_APPROVED; key FLAG premium or business | model slip | "355 minutes ... business class is allowed" under (c) (lines 707-710). It never read lines 665-668 (premium economy "should also be the choice ... if the flight is not overnight or when there is no meeting immediately after arrival"); the flight lands 19:00 and the review is next morning. The flag twins cedar-mosaic and dune-orchard passed. |
| thistle-forge | hidden_clause | FLAG AA economy, PARTICIPANTS_ABOVE_LIMIT, DIRECTOR_GENERAL; key BOOK AA economy, LOWEST_FARE | model slip | It applied lines 367-368 ("more than three staff members from the same Directorate-General ... authorisation at Director-General level") and never read footnote 25 (lines 399-400): "This principle should not be applied when there are specific rules about the number of participants, such as is the case for interpreters." The traveller is a conference interpreter. This is the hidden clause working as designed; the flag twin alder-quay (no interpreter exception) passed. |

## Fixes (this commit)

1. **basil-ridge (scenario):** the head of unit's sign-off note now reads "Authorisation to travel signed without
   expenses; the unit will not cover any cost of this trip". The request, key, decision and id are unchanged; the
   design note now cites the note instead of "which nobody has asked for". `tests/build_scenarios.py`, regenerated
   `basil-ridge.json`. No rules change.

Not loosened: elm-sounding, dahlia-spindle, ember-thimble, thistle-forge.

## Q2

The always-cheapest agent is unchanged: **10/32 (31%)** (`MAX_PASS_ALWAYS_LOWEST = 10`). basil-ridge is a refusal,
which it fails before and after.

## Re-score

Stored answers against the new head: 27/32, easy 5/6 (basil-ridge's record changed, so its stored hold is not
evidence either way).

## Re-run

Required: basil-ridge (record changed); elm-sounding (easy; a slip, nothing changed, must come back valid).
Optional: dahlia-spindle, ember-thimble (flags), thistle-forge.

Category note for the lead: elm-sounding is easy but turns on the direct-flight norm (lines 684-687) over a cheaper
connection. If it fails again, consider whether it belongs in `distractor` or `hidden_clause`; that is a category
call, not a key change.

## Checks

`uv run pytest -q` (257 passed), `uv run ruff check .`, `uv lock --check`, `check_shared.py`,
`tools/stock_verify.py` (32 scenarios, 0 failures), stock `nanoagent plugin inspect .` (exit 0).
