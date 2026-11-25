# Build notes: eu-rail-flight-policy (wave 3, 2026-11-24)

Built from `_template` with `instantiate.py` (slug `eu-rail-missions`, `--task-id book-eu-rail-flight`,
`--currency EUR`, `--background 0`, `--scenarios 32`). Frozen handbook:
`pilot_work/originals/eu-rail-missions/frozen/eu-rail-missions_policy.txt`, 16,083 words (over 10,000, so 32
scenarios), 1,360 lines, sha256 `c6436958...1292e9`. Decisions were taken without asking (the lead was away); each is
recorded here. `handbook.json` also records the raw PDF's sha256 and the freeze date from the originals' README.

## 1. What the handbook supports

Checkable flight clauses (frozen line numbers; the text keeps the PDF's split words, e.g. "m anifestly" on line 685):

| Lines | Clause | Operator / force | Used by |
|---|---|---|---|
| 688-691 | (a) economy, including non-refundable, "at the lowest available rates, taking into account the times of meetings" | general rule | every economy booking |
| 704-706 | (b) economy at the lowest flexible rates "if there is a risk that the mission will be cancelled or amended" | condition | fern-ledger, sorrel-gantry |
| 707-710, 665 | (c) premium economy or business if the journey "includes at least one segment involving at least five-hours of continuous flying time" | inclusive, per segment | cedar, dune, garnet/heron, maple/nutmeg, oriel, zinnia, ember, thistle, willow |
| 665-668 | when business is allowed, premium economy "should be envisaged, when available" and "should also be the choice" if not overnight / no meeting on arrival | soft, unclear against (c) | ember-thimble (flag) |
| 711-714 | same class as the accompanied Member of the Commission, on the Member's or Cabinet's written request | derogation | oriel-saffron, zinnia-crest |
| 684-687, 663-664 | direct flights are the norm; favoured "within reasonable cost variations (40%)"; AO may refuse a manifestly unreasonable one | norm; 40% unclear in scope | elm-sounding, dahlia-spindle (flag) |
| 630-636, 663, 693-694 | rail encouraged up to 550 km and favoured within 40% of the economy fare; air up to 550 km "must be appropriately justified" (footnote 40: heavy schedules, security) | mandatory justification | aspen-wicket, vesper-hollow, yarrow-brook |
| 577-582 | cannot be required to leave before 8:00 or arrive after 22:00 (take-off/landing), unless the line manager gives justifiable reasons | strict both sides | iris/jasper, pewter-vale, rowan-thatch |
| 583-585 | return by air started "not more than three-and-a-half hours after the end of the meeting(s)" | inclusive | kestrel/linden, rowan-thatch |
| 326-331, 426-437, footnote 15 (273-275) | mission order signed by the line manager and, if another person, the authorising officer; reservations only after the AO signs | mandatory | fennel-quarry (flag), umber-glade, every booking |
| 364-372, footnote 25 (399-400) | more than three staff of one DG at one meeting need a DG-level authorisation (delegable); not for interpreters | strict | alder-quay, gorse-lattice (flag), thistle-forge |
| 407 | no private benefit from airmiles of professional travel | mandatory | birch-lantern |
| 174-175, 191-193, 323-325 | missions and authorised travel defined | scope | cobalt-meadow |
| 1085-1088, 1147-1149, 1199-1203, 1210-1213 | authorised travel: financed none/part/full; mission rules by analogy; expenses within the signed authorisation | mandatory | quill-harrow, basil-ridge |
| 815-818 | rest period up to 24 h after flights totalling at least 10 hours (AO's decision) | distractor | willow-tamber |

Not used: booking channels (lines 391-406: the world is the agency), cancellation records (535), "book at the earliest
opportunity" (591-592, soft; a distractor in alder-quay and fennel-quarry), changes for personal reasons and recall
from leave (459-475: they decide reimbursement and departure points, not which ticket is bought), third-party
payment (951-1009: no case needs it), hired/private cars and boats. No rule on overnight stops within a journey, so
that overlay is not required.

## 2. Unclear points and how they are handled

- **"direct flights favoured when available, and within reasonable cost variations (40%)" (lines 663-664)**. The
  sentence's subject is "Air travel for distances up to 550 km", while lines 684-687 make direct flights the norm
  everywhere, refusable only by the authorising officer as "manifestly unreasonable". Flag `dahlia-spindle`: a
  2,058 km route where the nonstop is 82% above the connection; hold either offer. A direct flight within 40% is
  booked on both readings (`elm-sounding`, 18%). Rules raise for a gap between 30% and 50%.
- **"This should also be the choice ..." (lines 665-668)** against (c)'s "premium economy class when suitable, or
  business class". Flag `ember-thimble`: daytime flight, review the next morning, premium economy sold, business
  asked; hold the premium economy or business fare. Every other business case sells no premium economy ("when
  available"), so both readings agree there. A business request on an overnight flight or before a meeting is not
  modelled (rules raise).
- **Footnote 38 (lines 652-655)**: "These two elements (price variation and distance) may be interpreted in a
  flexible manner" (its own example: 600 km and 43%). No twin sits on 550 km or 40%: rail cases use 505 km with rail
  20% dearer (aspen-wicket, vesper-hollow) and 920 km with rail 81% dearer (yarrow-brook). Rules raise for rail
  between 550 and 700 km or a price ratio between 130% and 150%.
- **"must be, in principle, started"** (line 584): read as binding on the take-off time. "In principle" softens it,
  but the alternative (the cheaper later flight) has no textual support. Risk noted for kestrel-mallow.
- **Approval holds**: `fennel-quarry` (AO signature missing, the line manager is not the AO) and `gorse-lattice` (five
  staff of one DG, no DG-level authorisation). Both have clear sides: `umber-glade` and `alder-quay`, and
  `alder-quay` (3 staff) and `thistle-forge` (interpreters).

Numeric twin pairs: 300/295 minutes (garnet-reach/heron-cobble), a 300/290-minute second segment on a connection
(maple-tern/nutmeg-spire), take-off 07:55/08:00 (iris-pennant/jasper-wold), take-off 215/210 minutes after the
meeting (kestrel-mallow/linden-ferrule). One-fact twins outside the boundary category: fern-ledger/sorrel-gantry
(risk of change), oriel-saffron/zinnia-crest (who is accompanied), vesper-hollow/aspen-wicket (justification on
file), quill-harrow/basil-ridge (authorisation pays transport or not). The 22:00 landing is tested inside
rowan-thatch (22:10 left out), not as a twin. The participant count (more than three) is tested by the flag and its
twins (3 and 5).

## 3. Choices made without asking

1. **Places of employment.** The JU is in Brussels, which the shared world lacks (no BRU, no LUX, no Brussels
   Airlines). The guide is the Commission's and applies to staff in every Commission city; travellers work in Paris,
   Madrid, Rome, Munich or Dublin, stated in a `place_of_employment` field. See section 7.
2. **Rail as facts.** `rail_km`, `rail_fare_cents` (first class, which line 675 reimburses), `rail_minutes` and
   `air_justification` sit in the trip record; nothing asks the agent to search rail. Other intra-European routes
   carry no rail facts and are over 550 km.
3. **Sign-offs.** Every booking needs the signed mission order (or authorisation to travel). The `MISSION_ORDER`
   subject says the ticket is chosen when booking, so a signed order does not pre-approve a flight (aspen-wicket).
   SYNC_NOTES 4': bookings and refusals accept `NONE` and the signers' roles; `umber-glade` also accepts
   `AUTHORISING_OFFICER` (the line manager is the AO); `oriel-saffron` also accepts `MEMBER_OF_COMMISSION` and
   `CABINET`; `zinnia-crest` does not accept the Director-General, whose same-class request is the invalid one.
4. **Reasons on declines (lesson 12).** heron-cobble, nutmeg-spire, zinnia-crest: `UPGRADE_NOT_ELIGIBLE` or
   `LONG_FLIGHT_CONDITION_NOT_MET`; sorrel-gantry: `REFUNDABLE_FARE_NOT_ALLOWED`; pewter-vale:
   `EARLY_LATE_HOURS_JUSTIFIED` (the "rather not take a dawn flight" wish is declined on the line manager's reasons).
   birch-lantern keeps `LOWEST_FARE` beside `LOYALTY_PROGRAM_PREFERENCE` (declined on the lowest-rate rule). Cases
   where the traveller's request is conditional ("cheapest, but not at hours I can't be made to travel") are not
   declines and accept `LOWEST_FARE` beside the rule's own code.
5. **Refusal reason sets.** aspen-wicket accepts `RAIL_PREFERRED`, `DISTANCE_BELOW_MINIMUM`, `NO_COMPLIANT_OFFER`;
   basil-ridge `TRAVEL_COSTS_NOT_COVERED`, `PERSONAL_TRAVEL_NOT_COVERED`, `OUTSIDE_POLICY_SCOPE`; cobalt-meadow
   `PERSONAL_TRAVEL_NOT_COVERED`, `OUTSIDE_POLICY_SCOPE`.
6. **Accompanied flight named.** oriel-saffron and zinnia-crest say the senior person "flies Iberia that morning", so
   the same-class seat is on a named flight (it is also the cheapest of its cabin).
7. **Background offers 0** on every search: the listings are exactly the pinned offers.
8. **Decoy reason codes** (grepped; no subject a case could defend): WEEKEND_TRAVEL_HOME, WEEKEND_TRIP_NOT_EARNED,
   NEXT_OF_KIN_TRAVEL, FLY_AMERICA_US_CARRIER_REQUIRED, OPEN_SKIES_AGREEMENT, CREATIVE_TICKETING,
   CHANCELLOR_WRITTEN_AUTHORIZATION, DOUBLE_BOOKING_PROHIBITED, PRIVATE_AIRCRAFT_NOT_APPROVED,
   CANDIDATE_TRIP_NOT_COVERED, TRAVEL_PACKAGE_NOT_ITEMIZED. Dropped: EXTENDED_TRAVEL_SAVINGS (lines 813-814 extend a
   mission to lower the travel cost), DENIED_BOARDING_NOT_ALLOWED (line 719 covers denied boarding),
   SAME_CLASS_AS_CUSTOMER (too close to the same-class derogation). Approver decoys: CHIEF_FINANCIAL_OFFICER,
   CHIEF_EXECUTIVE, VICE_PRESIDENT; PMO, DG_HR and HEAD_OF_CABINET are named in the text but used by no case.

## 4. Mix and overlays

6 easy, 8 boundary_twin, 5 multi_rule, 3 hidden_clause, 3 distractor, 3 refusal, 4 flag (12.5%). Decisions: 25 BOOK
(3 business, 2 premium economy, 20 economy), 3 REFUSE, 4 FLAG. Overlays: multi_leg 4, date_arithmetic 5 (month_end 1),
personal_travel 2, multi_traveller 3, dearer_option 12, upgrade_not_taken 4, outside_air_section 9. Hidden clauses are
footnotes: 15 (umber-glade), 25 (thistle-forge), 40 (vesper-hollow). Degenerate agents: always-flag passes 2,
always-cheapest passes 10 (alder-quay, birch-lantern, jasper-wold, linden-ferrule, quill-harrow, thistle-forge,
umber-glade, vesper-hollow, willow-tamber, yarrow-brook); `MAX_PASS_ALWAYS_LOWEST = 10`.

## 5. Independent blind read (non-flag scenarios)

Re-derived from the frozen text and the tool outputs only (the `get_trip` record and the `search_flights` listing,
dumped per scenario with a script that calls only `get_trip` and `search_flights`), then compared with `expected`.

| Scenario | My reading from text + offers | Agrees |
|---|---|---|
| alder-quay | all direct; AF 13:00 EUR 119 sold out; lowest seated IB 11:15 EUR 132; 3 staff of the DG is not "more than three" | yes |
| birch-lantern | Lufthansa EUR 214 vs Iberia EUR 189; lowest rate (689-691), no airmiles benefit (407): IB 09:40 | yes |
| cedar-mosaic | 405/395-minute nonstops reach five hours; no premium economy sold; cheapest business AF EUR 2,890 | yes |
| dune-orchard | 440/450 minutes; premium economy allowed; cheapest IB EUR 1,090 | yes |
| elm-sounding | nonstop EUR 182 is 18% over the EUR 154 connection: direct is the norm and within 40%: AF nonstop | yes |
| fern-ledger | audit may move: (b) lowest flexible fare: LH 09:00 refundable EUR 249 | yes |
| garnet-reach | 300 minutes = "at least five-hours": cheapest business QR 09:05 EUR 2,240 | yes |
| heron-cobble | 295 minutes: no business; economy default; QR 13:40 EUR 498 | yes |
| iris-pennant | 07:55 is before 8:00 and the traveller declines it, no line manager reasons: AF 18:20 EUR 158 | yes |
| jasper-wold | 08:00 is not before 8:00: AF 08:00 EUR 119 | yes |
| kestrel-mallow | meeting ends 15:00; 18:35 is 215 minutes later, over 210; cheapest within: AF 17:25 EUR 176 | yes |
| linden-ferrule | 18:30 is exactly 210 minutes: "not more than": IB 18:30 EUR 128 | yes |
| maple-tern | Cairo-Nairobi 300 minutes qualifies the journey: cheapest premium MS 08:15 EUR 1,120 | yes |
| nutmeg-spire | 260 + 290: no five-hour segment, flights not added: cheapest economy MS 09:05 EUR 585 | yes |
| oriel-saffron | short flight, but the Cabinet's written request and the mission order's reasons are on file (711-714): IB business EUR 598 | yes |
| pewter-vale | 09:10 lands after the 09:30 hearing; line manager's reasons on file allow the 06:45: LH EUR 138 | yes |
| quill-harrow | authorisation pays transport; mission rules by analogy: lowest EI 10:40 EUR 118 | yes |
| rowan-thatch | 21:45 starts 225 min after 18:00 and lands 23:05; 20:50 lands 22:10 (after 22:00, declined): LH 20:05 EUR 171 | yes |
| sorrel-gantry | no risk on file: flexible fare not allowed; lowest non-refundable IB 12:40 EUR 159 | yes |
| thistle-forge | 6 interpreters: footnote 25 sets the DG authorisation aside; economy asked: AA EUR 471 | yes |
| umber-glade | only the line manager signed, but they are the AO (footnote 15): lowest EI 11:40 EUR 149 | yes |
| vesper-hollow | 505 km, rail 20% dearer, but a heavy-schedule justification is on file (footnote 40): lowest KL 18:25 EUR 91 | yes |
| willow-tamber | economy asked on an overnight 760/775-minute flight; rest period changes no ticket: SQ EUR 695 | yes |
| yarrow-brook | 920 km rail, 81% dearer and 9 h 45: no justification needed: LH 15:40 EUR 119 | yes |
| zinnia-crest | the derogation is for a Member of the Commission, not a Director-General; short flight: IB economy EUR 139 | yes |
| aspen-wicket | 505 km, rail within 40%, no justification, traveller will take the train: refuse | yes |
| basil-ridge | authorisation without expenses: the organisation buys nothing | yes |
| cobalt-meadow | family visit is neither a mission nor authorised travel: refuse | yes |

28 of 28 non-flag scenarios agree. Things the read flagged and fixed before this table: oriel-saffron and
zinnia-crest now name the flight the senior person takes; cobalt-meadow carries no meeting time.

## 6. Hosted-cap estimate

Full-handbook prompt: 107,288 bytes, 16,083 words. About 21,400 tokens at 1.33 a word; about 23,300 for the first
`full` call on the Thornton/NJC calibration (0.2 a character plus 1,800). A 3-call run is about 23,300 + 24,000 +
25,000 = about 72,000 input tokens: over the 65,536 hosted cap during the third call, so `full` cannot finish hosted
(like NJC v328). Selection at 35% or less of the handbook fits.

## 7. Template change requests

1. **Add Brussels (BRU) and Luxembourg (LUX), with Brussels Airlines (SN, hub BRU)**, to the shared `world.py`. EU
   bodies' places of employment are mostly Brussels and Luxembourg; wave 3's EU guides (this one, ENISA in Athens/
   Heraklion: ATH, HER) need them for realistic trips. Until then this plugin uses other Commission cities. Adding an
   airport without hubs changes no existing route (`tools/world_diff.py` should confirm).
2. Observation, no change needed: the skeleton's `search-flights` task text says "one-way"; every case here is
   one-way.

## 8. Unsure

- kestrel-mallow / linden-ferrule rest on "must be, in principle, started"; a model may treat "in principle" as
  advice and book the cheaper later flight. The key follows the text's "must".
- aspen-wicket could be read as a hold for the AO to accept a justification; the request offers to take the train,
  and the text's "must be appropriately justified" with none on file supports REFUSE only.
- ember-thimble's flag rests on "should" in a guide that uses "should" for recommendations; it is the only case on
  that phrase.
- `full` exceeds the hosted cap (section 6).

## 9. Acceptance outputs

```
$ uv run pytest -q
257 passed in 2.59s
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 10ms
$ python3 ../_template/check_shared.py .
: ok
$ nanoagent plugin inspect .
exit 0
$ nanoagent plugin pack . <scratch>/eu-rail-flight-policy.tar.gz
packed . into <scratch>/eu-rail-flight-policy.tar.gz (201714 bytes)
$ python ../_template/tools/stock_verify.py .  (nanoagent venv python)
alder-quay           right=True score=1.00 identical=True wrong-decision-rejected=True
aspen-wicket         right=True score=1.00 identical=True wrong-decision-rejected=True
basil-ridge          right=True score=1.00 identical=True wrong-decision-rejected=True
birch-lantern        right=True score=1.00 identical=True wrong-decision-rejected=True
cedar-mosaic         right=True score=1.00 identical=True wrong-decision-rejected=True
cobalt-meadow        right=True score=1.00 identical=True wrong-decision-rejected=True
dahlia-spindle       right=True score=1.00 identical=True wrong-decision-rejected=True
dune-orchard         right=True score=1.00 identical=True wrong-decision-rejected=True
elm-sounding         right=True score=1.00 identical=True wrong-decision-rejected=True
ember-thimble        right=True score=1.00 identical=True wrong-decision-rejected=True
fennel-quarry        right=True score=1.00 identical=True wrong-decision-rejected=True
fern-ledger          right=True score=1.00 identical=True wrong-decision-rejected=True
garnet-reach         right=True score=1.00 identical=True wrong-decision-rejected=True
gorse-lattice        right=True score=1.00 identical=True wrong-decision-rejected=True
heron-cobble         right=True score=1.00 identical=True wrong-decision-rejected=True
iris-pennant         right=True score=1.00 identical=True wrong-decision-rejected=True
jasper-wold          right=True score=1.00 identical=True wrong-decision-rejected=True
kestrel-mallow       right=True score=1.00 identical=True wrong-decision-rejected=True
linden-ferrule       right=True score=1.00 identical=True wrong-decision-rejected=True
maple-tern           right=True score=1.00 identical=True wrong-decision-rejected=True
nutmeg-spire         right=True score=1.00 identical=True wrong-decision-rejected=True
oriel-saffron        right=True score=1.00 identical=True wrong-decision-rejected=True
pewter-vale          right=True score=1.00 identical=True wrong-decision-rejected=True
quill-harrow         right=True score=1.00 identical=True wrong-decision-rejected=True
rowan-thatch         right=True score=1.00 identical=True wrong-decision-rejected=True
sorrel-gantry        right=True score=1.00 identical=True wrong-decision-rejected=True
thistle-forge        right=True score=1.00 identical=True wrong-decision-rejected=True
umber-glade          right=True score=1.00 identical=True wrong-decision-rejected=True
vesper-hollow        right=True score=1.00 identical=True wrong-decision-rejected=True
willow-tamber        right=True score=1.00 identical=True wrong-decision-rejected=True
yarrow-brook         right=True score=1.00 identical=True wrong-decision-rejected=True
zinnia-crest         right=True score=1.00 identical=True wrong-decision-rejected=True
32 scenarios, 0 failures
```
