# EU Rail Guide to Missions Flight Booking

**No affiliation with Europe's Rail Joint Undertaking or the European Commission.** The handbook is Governing Board
Decision N°11/2025 of Europe's Rail Joint Undertaking, which applies by analogy Commission Decision C(2025) 2495, the
*Guide to Missions and Authorised Travel* (publicly posted on the Joint Undertaking's website), bundled verbatim for
research. It is an adopted public decision of an EU body with no confidential or draft marking.

A `nanoagent.plugin/v0001` plugin. An agent handles one staff member's flight request under the guide: it reads the
trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or **FLAG_FOR_APPROVAL** with the
offer, cabin, reason, approver and guide section. A deterministic Python verifier, with no LLM, rebuilds the offers
and the guide's answer itself and checks every field. Built from the original-handbook template
(`handbook_plugins/_template`); `tests/build_scenarios.py` writes the scenario files.

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 16,083 words, 1,360 lines, 107,288 bytes, sha256
`c6436958...1292e9`, equal to `pilot_work/originals/eu-rail-missions/frozen/SHA256SUMS`) is never paraphrased, and
the task text restates no rule. The PDF text layer left about 30 split words ("missi on", "m anifestly") and
footnotes interleaved at page breaks; they are kept as they are, and `must_keep` quotes use them. Under stock
NanoAgent the agent does not see the text: the plugin then runs as the `off` baseline. The `harness.policy` switch of
the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it to the system prompt:
`harness.policy: full` adds all of it, and the selection methods add parts of it. These plugins are meant to run with
`query: instructions+input`, so a selector sees the traveller's request.

**Size.** At 1.33 tokens a word the guide alone is about 21,400 tokens; on the Thornton/NJC calibration (about 0.2
tokens a character plus 1,800) the first `full` call is about 23,300 input tokens. A run makes 3 calls (`get_trip`,
`search_flights`, `submit`) of about 23,300, 24,000 and 24,500 to 25,500: about 72,000 input tokens per run. That
crosses the hosted cap of 65,536 during the third call, so `full` cannot finish hosted (like NJC v328); the selection
methods at 35% budget or less fit.

## Task

- **Input:** `TaskInput`: `scenario` (one of 32 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on the trip's route and date (every case buys one one-way ticket),
  then `submit`.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when refusing),
  `reason_code`, `approver` and `clause`, each from a closed list. The reason list is the template's shared list plus
  ten codes of this guide (`DIRECT_FLIGHT_NORM`, `FLEXIBLE_FARE_JUSTIFIED`, `SAME_CLASS_AS_MEMBER`,
  `AIR_TRAVEL_JUSTIFIED`, `EARLY_LATE_HOURS_PROTECTED`, `EARLY_LATE_HOURS_JUSTIFIED`, `RETURN_START_LIMIT`,
  `TRAVEL_COSTS_NOT_COVERED`, `MISSION_ORDER_NOT_SIGNED`, `PARTICIPANTS_ABOVE_LIMIT`) and eleven decoy codes from
  other handbooks' rules. Fares are in euro cents (`currency: EUR`).
- **Rail.** The shared world sells flights only. Where the guide's rail-against-air rules matter, the trip record
  states the rail alternative (distance, first-class fare, time) and any justification for flying on file; the agent
  never searches for a train.
- **Places of employment.** The shared world has no Brussels or Luxembourg airport, so travellers work in Commission
  cities the world has (Paris, Madrid, Rome, Munich, Dublin); see `tests/BUILD_NOTES.md`, template change requests.
- **Success:** every field is one the answer key accepts; the cabin is graded as the chosen offer's own. Score =
  fields right / 6.
- **Reasons on a declined request.** The task instructions say that when the booking is not what the traveller asked
  for, the reason code gives why the request is declined; such bookings accept the codes that name the guide's
  ground, not `LOWEST_FARE` (`heron-cobble`, `nutmeg-spire`, `zinnia-crest`, `sorrel-gantry`, `pewter-vale`).
  `birch-lantern` keeps `LOWEST_FARE` beside `LOYALTY_PROGRAM_PREFERENCE`: the airline is declined on the
  lowest-rate rule itself, with line 407 on airmiles.
- **No hidden facts:** no scenario has `answer_key_inputs`.

| Scenario | Category | Expected decision (offer; cabin) | Reason (any of) | Frozen lines |
|---|---|---|---|---|
| `alder-quay` | easy | BOOK (midday-economy; ECONOMY) | LOWEST_FARE | 688-691, 663-664, 426-428, 364-372 |
| `birch-lantern` | easy | BOOK (iberia-am-economy; ECONOMY) | LOWEST_FARE or LOYALTY_PROGRAM_PREFERENCE | 688-691, 407, 663-664 |
| `cedar-mosaic` | easy | BOOK (airfrance-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED | 707-710, 665-668 |
| `dune-orchard` | easy | BOOK (iberia-premium; PREMIUM_ECONOMY) | PREMIUM_ECONOMY_ALLOWED | 707-710 |
| `elm-sounding` | easy | BOOK (direct-economy; ECONOMY) | ALTERNATE_ROUTE_WITHIN_MARGIN, DIRECT_FLIGHT_NORM or LOWEST_FARE | 684-687, 663-664, 688-691 |
| `fern-ledger` | easy | BOOK (morning-flex; ECONOMY) | FLEXIBLE_FARE_JUSTIFIED or LOWEST_FARE | 704-706, 688-691 |
| `garnet-reach` | boundary_twin | BOOK (morning-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED | 707-710, 665-668 |
| `heron-cobble` | boundary_twin | BOOK (afternoon-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | 707-710, 688-691, 663-664 |
| `iris-pennant` | boundary_twin | BOOK (evening-economy; ECONOMY) | EARLY_LATE_HOURS_PROTECTED or LOWEST_FARE | 577-582, 688-691 |
| `jasper-wold` | boundary_twin | BOOK (first-economy; ECONOMY) | EARLY_LATE_HOURS_PROTECTED or LOWEST_FARE | 577-582, 688-691 |
| `kestrel-mallow` | boundary_twin | BOOK (mid-economy; ECONOMY) | LOWEST_FARE or RETURN_START_LIMIT | 583-587, 688-691 |
| `linden-ferrule` | boundary_twin | BOOK (saver-economy; ECONOMY) | LOWEST_FARE or RETURN_START_LIMIT | 583-587, 688-691 |
| `maple-tern` | boundary_twin | BOOK (first-premium; PREMIUM_ECONOMY) | PREMIUM_ECONOMY_ALLOWED | 707-710 |
| `nutmeg-spire` | boundary_twin | BOOK (second-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | 707-710, 688-691, 663-664 |
| `oriel-saffron` | multi_rule | BOOK (iberia-business; BUSINESS) | SAME_CLASS_AS_MEMBER | 711-714, 707-710, 663-664 |
| `pewter-vale` | multi_rule | BOOK (first-economy; ECONOMY) | EARLY_LATE_HOURS_JUSTIFIED | 577-582, 688-691 |
| `quill-harrow` | multi_rule | BOOK (morning-economy; ECONOMY) | LOWEST_FARE | 1147-1149, 1199-1203, 1085-1088, 688-691 |
| `rowan-thatch` | multi_rule | BOOK (second-economy; ECONOMY) | EARLY_LATE_HOURS_PROTECTED or LOWEST_FARE or RETURN_START_LIMIT | 583-587, 577-582, 688-691 |
| `sorrel-gantry` | multi_rule | BOOK (noon-saver; ECONOMY) | REFUNDABLE_FARE_NOT_ALLOWED | 688-691, 704-706 |
| `thistle-forge` | hidden_clause | BOOK (american-economy; ECONOMY) | LOWEST_FARE | 364-372, 399-400, 688-691 |
| `umber-glade` | hidden_clause | BOOK (midday-economy; ECONOMY) | LOWEST_FARE | 326-331, 273-275, 426-428, 688-691 |
| `vesper-hollow` | hidden_clause | BOOK (evening-economy; ECONOMY) | AIR_TRAVEL_JUSTIFIED or LOWEST_FARE | 630-637, 663-664, 693-694, 688-691 |
| `willow-tamber` | distractor | BOOK (singapore-economy; ECONOMY) | LOWEST_FARE | 688-691, 663-664 |
| `yarrow-brook` | distractor | BOOK (afternoon-economy; ECONOMY) | LOWEST_FARE | 630-637, 688-691 |
| `zinnia-crest` | distractor | BOOK (iberia-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | 711-714, 707-710, 688-691, 663-664 |
| `aspen-wicket` | refusal | REFUSE (none; NONE) | DISTANCE_BELOW_MINIMUM or NO_COMPLIANT_OFFER or RAIL_PREFERRED | 630-637, 663-664 |
| `basil-ridge` | refusal | REFUSE (none; NONE) | OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED or TRAVEL_COSTS_NOT_COVERED | 1085-1088, 1199-1203, 1210-1213, 191-193 |
| `cobalt-meadow` | refusal | REFUSE (none; NONE) | OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED | 174-175, 323-325, 191-193 |
| `dahlia-spindle` | flag | FLAG_FOR_APPROVAL (amsterdam-economy or direct-economy; ECONOMY) | APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT | 684-687, 663-664, 688-691 |
| `ember-thimble` | flag | FLAG_FOR_APPROVAL (lufthansa-business or lufthansa-premium; BUSINESS or PREMIUM_ECONOMY) | APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT | 707-710, 665-668 |
| `fennel-quarry` | flag | FLAG_FOR_APPROVAL (midday-economy; ECONOMY) | APPROVAL_REQUIRED or MISSION_ORDER_NOT_SIGNED | 326-331, 426-428, 432-437, 688-691 |
| `gorse-lattice` | flag | FLAG_FOR_APPROVAL (midday-economy; ECONOMY) | APPROVAL_REQUIRED or PARTICIPANTS_ABOVE_LIMIT | 364-372, 399-400, 688-691 |

Every accepted approver and section per case is in the scenario files and `tests/BUILD_NOTES.md`.

Mix (EDGE_CASES.md 5.2): 6 easy, 8 boundary twins, 5 multi-rule, 3 hidden clause, 3 distractor, 3 refusal, 4 flags
(12.5%). Decisions: 25 BOOK, 3 REFUSE, 4 FLAG_FOR_APPROVAL. Two flags are unclear words, each once with clear twins on
both sides: "direct flights favoured when available, and within reasonable cost variations (40%)" (`dahlia-spindle`,
twins `elm-sounding` and `nutmeg-spire`) and "This should also be the choice, for example, if the flight is not
overnight or when there is no meeting immediately after arrival" (`ember-thimble`, twins `cedar-mosaic` and
`dune-orchard`). Two are approval holds, never "no compliant offer": the authorising officer's signature on the
mission order (`fennel-quarry`) and the Director-General level authorisation for more than three staff of one DG
(`gorse-lattice`).

**Duration (`rules.over`).** Lines 707-710: premium economy or business "if the outward or return journey includes at
least one segment involving at least five-hours of continuous flying time". Inclusive, measured on one segment's
scheduled minutes (300 or more); flights are never added together, and one qualifying segment qualifies the journey.
The rest period of lines 815-818 ("total duration of the flights is at least 10 hours", flights added, ground time
left out) is coded too, but decides no ticket.

**Approvers.** Every booking relies on the signed mission order (or authorisation to travel), so it accepts the
signers' roles and `NONE` (SYNC_NOTES 4'); a same-class request from anyone but the Member of the Commission or their
Cabinet is not accepted for its giver (`zinnia-crest`). Holds awaiting a sign-off accept only the awaited roles
(`AUTHORISING_OFFICER`; `DIRECTOR_GENERAL`, `SENIOR_MANAGEMENT` or `HR_CORRESPONDENT`). Holds over unclear words
accept `NOT_NAMED` or `AUTHORISING_OFFICER` and `UNCLEAR_POLICY_TEXT` or `APPROVAL_REQUIRED`.

Degenerate agents (`tests/test_verifier.py`): always holding the right offer as unclear passes 2 cases (the two
unclear flags); always booking the cheapest seat with `LOWEST_FARE`, `NONE` and the right section passes 10.

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller, home city, route, date, meeting times, purpose, requested cabin, airline, fare type and hours, whom they accompany, any rail alternative and justification on file, sign-offs | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date: the pinned scenario offers only (no background offers); a search the case does not pin lists nothing and says so | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-eu-rail-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this guide's scenario ids, approvers, sections, reason codes and
  trip record.
- `src/plugin/`: `world.py`, `scenarios.py`, `guide.py`, `answer.py`, `tools.py` (shared), `rules.py` (this guide's
  rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of the shared modules and `rules.py`, plus `booking.py` and `tools.py`.
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this guide's settings.
- `tests/build_scenarios.py`: writes the scenario files (an authoring aid, not a test).
- `tests/BUILD_NOTES.md`: design choices, the blind read and the acceptance outputs.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
python3 ../_template/check_shared.py .
# from a NanoAgent checkout (read-only use):
nanoagent plugin inspect <this folder>
nanoagent plugin pack <this folder> /tmp/eu-rail-flight-policy.tar.gz
# from this folder, with that checkout's Python:
/path/to/nanoagent/nanoagent/.venv/bin/python ../_template/tools/stock_verify.py .
```

Under stock NanoAgent the plugin runs as `off` (the guide is not shown); the fork's `harness.policy` flag
(`off`, `full` or a selection method) decides how much of it the agent sees.

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`).
