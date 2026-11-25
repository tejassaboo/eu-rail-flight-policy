# Independent audit: eu-rail-flight-policy (2026-11-25)

Audited the builder's commit bb43b72 against WAVE3_BUILD_BRIEF (all 12 lessons), MASTER_PLAN section 4, EDGE_CASES
1-3 and 5, and `_template/SYNC_NOTES.md` 4'. No money spent, nothing pushed. Line numbers are lines of the frozen
handbook (`src/plugin/data/policy.txt`).

## Method

I printed each scenario's `get_trip` record and every pinned `search_flights` listing through the plugin's own tools.
Then I answered each case from the handbook alone: lines 577-587, 630-668, 684-714, 326-331, 364-372, 407, 426-437,
1085-1088 and 1143-1213, footnotes 15, 25, 38 and 40, and section 1.2.4 (lines 247-259). Only after that did I compare
my answers with the key: decision, offer, cabin, reason, approver and clause.

## Verdict

**Pass after fixes.** On all 28 non-flag cases, my decision and offer agree with the key. The defects were:

- one flag whose request wording closed the open question;
- accept sets for clauses and reasons that were too narrow;
- one sign-off note that left a derogation's authorisation implicit.

The two approval holds are clear on the text:

- `fennel-quarry`: lines 328-331 and 426-428 say the ticket waits for the authorising officer's signature.
- `gorse-lattice`: lines 367-371 require an authorisation at Director-General level.

`dahlia-spindle` is a genuine two-reading flag: the 40% sentence at 663-664 is about trips up to 550 km, while 684-687
make the direct flight the norm everywhere. Twins differ in one fact. In `vesper-hollow` and `aspen-wicket` the
purpose line also differs, but only as the statement of the justification fact itself (meetings in three cities).

## The builder's unsure list, settled

- **`kestrel-mallow` / `linden-ferrule` ("must be, in principle, started", line 584): kept as a twin, with the key
  unchanged.**
  - The operator is "must". In this guide, "in principle" marks a default rule that holds unless someone with the
    power to do so makes an exception. Two examples:
    - Line 577: "in principle cannot be required ... unless the line manager gives justifiable reasons".
    - Line 593: departures and returns are "in principle" from the place of employment, and lines 597-598 then say
      only the authorising officer may authorise otherwise, "on an exceptional basis".
  - Lines 254-256 (1.2.4) gives derogations from the general rules to the authorising officer.
  - Nobody has authorised a later return here, a compliant flight exists, and the booker cannot grant the exception
    itself. So the 18:35 flight (215 minutes after the meeting) is not defensible.
  - The opening words "while respecting the principles of ... cost efficiency" govern how the return is arranged
    inside the limit. They do not license breaking it.
  - Reading "started" as take-off is the only reading that makes the 3.5 h (air) versus 2 h (other) split sensible,
    and lines 580-582 define departure as take-off.
  - If "in principle" were read as advisory, the twins would collapse: the always-cheapest agent would pass both. So
    accepting both offers would defeat the pair without any textual warrant.
- **`aspen-wicket`: REFUSE only.**
  - Line 663: air "must be appropriately justified". Footnote 40 says what counts (security, particularly heavy
    schedules). "I simply prefer flying" is not a justification, and none is on file.
  - A hold for the authorising officer would wait on a justification that does not exist.
  - The traveller has said they will take the train if the guide asks for it. The organisation buys no air ticket.
- **`ember-thimble`: as built, not genuinely two-reading. Fixed by request wording.**
  - The request ended "If the guide wants something else, book that."
  - Lines 665-668 say premium economy "should also be the choice" on a daytime flight with no meeting on arrival.
    Whether "should" binds or only advises, it is plainly what the guide *wants*.
  - So the traveller's own fallback made BOOK premium economy the clear answer, and the FLAG key would have failed a
    correct booking.
  - Now the request ends "If business isn't allowed on this flight, book what the policy allows."
    - If "should" is binding, business is not allowed, so book premium economy.
    - If "should" is advisory, (c) allows business, so book business.
  - The question is open again, and both held offers stay as they were. The request names no rule wording or
    threshold, and it carries the lesson-3 fallback.
- **`full` over the hosted cap**: a budget matter, not a defect (section 6 of BUILD_NOTES).

## Defects found and fixed

1. **`ember-thimble`: the request closed the flag.** Changed the request's last sentence, as above. The world, the key
   and the id are unchanged.
2. **Parent-section clauses refused.** "Smart travelling" and "Travel by air" are sub-headings of 2.5.4 (lines
   625-714), so a correct answer may cite `TRANSPORT_BETWEEN_PLACES`. The economy bookings already accepted it, but
   these cases did not:
   - business: `cedar-mosaic`, `garnet-reach`
   - premium economy: `dune-orchard`, `maple-tern`
   - same class: `oriel-saffron`
   - declined upgrades: `heron-cobble`, `nutmeg-spire`, `zinnia-crest`
   - both unclear flags: `dahlia-spindle`, `ember-thimble`

   It is now accepted in all of them.
3. **Authorising officer's section refused.** Footnote 15 (the line manager may be the authorising officer) hangs on
   section 1.2.4, the authorising officer's role. That section also says they authorise the mission on a cost
   estimate. `AUTHORISING_OFFICER_ROLE` is now accepted on `umber-glade` and `fennel-quarry`.
4. **`elm-sounding` refused LOWEST_FARE.** The traveller asks for nothing in particular ("I don't mind which airline"),
   so nothing is declined. The key books the cheapest direct fare, so `LOWEST_FARE` is now accepted beside
   `DIRECT_FLIGHT_NORM` and `ALTERNATE_ROUTE_WITHIN_MARGIN` (lesson 5). The always-cheapest agent still fails, because
   it books the connection.
5. **`oriel-saffron`: the derogation's authorisation was only implicit.**
   - Lines 711-714 say staff "may be authorised" to fly in the Member's class, with reasons "justified in the mission
     order".
   - Lines 254-256 (1.2.4) gives approval of such derogation requests to the authorising officer.
   - The `SignOff` subject text says a mission order's ticket "is chosen when booking". So a careful reader could ask
     whether the business seat itself is authorised, and hold it.
   - The Cabinet's note now ends "the reasons are set out in the mission order, which the authorising officer has
     signed". This restates a fact already on file (the authorising officer's mission order signature) next to the
     derogation. The one twin fact against `zinnia-crest` (Member of the Commission or Director-General) is unchanged,
     and the key is unchanged.

## Seen and kept

- `cedar-mosaic` and `garnet-reach` (daytime, meeting the next morning, no premium economy sold): line 666's "when
  available" leaves business, which the traveller asked for, as the answer. Economy is not the answer, because (c)
  allows business and the request asks for it if allowed.
- `pewter-vale` accepts only `EARLY_LATE_HOURS_JUSTIFIED`. The dawn-flight wish is declined on the line manager's
  reasons (lines 577-579), not on the lowest-fare rule (lesson 12). The 06:45 flight is the cheapest that lands before
  the 09:30 hearing, so the answer does not hinge on the 07:30's margin.
- `zinnia-crest` does not accept `SAME_CLASS_AS_MEMBER`. That code says why business would be granted, not why it is
  declined (same treatment as Georgia's falcon-spire).
- `gorse-lattice` accepts the Director-General and the two named delegates only. Lines 369-371 name them, so
  `NOT_NAMED` would be wrong for a hold awaiting a sign-off (4').
- `alder-quay`: "two colleagues ... too" makes 3 staff, which is not "more than three". The cheaper Air France 13:00
  is sold out.
- Requests leak no thresholds. "an hour the guide says I can't be made to travel" names the rule's subject, not its
  hours. Every BOOK that declines a cabin, fare or airline carries a fallback. The decline-reason sentence is in the
  `book-eu-rail-flight` instructions.
- The always-flag baseline passes 2 (the two unclear flags).

`MAX_PASS_ALWAYS_LOWEST`: **10 -> 10** (31%). No decision or offer changed, and the only reason set that grew
(`elm-sounding`) belongs to a case the degenerate agent fails on the offer.

## Files changed

- `src/plugin/rules.py` and `verifier/rules.py`, byte-identical: the clause sets, the `elm-sounding` reasons, and the
  authorising-officer role section.
- `tests/build_scenarios.py`: the `ember-thimble` request, the `oriel-saffron` Cabinet note and the accept sets.
- All 32 scenario JSON files, regenerated. 13 of them changed.
- `README.md`: the `elm-sounding` reason column.

## Check outputs (audit commit)

- `uv run pytest -q`: 257 passed.
- `uv run ruff check .`: all checks passed.
- `uv lock --check`: ok.
- `python3 ../_template/check_shared.py .`: ok.
- `tools/stock_verify.py .` (nanoagent venv python): 32 scenarios, 0 failures.
- `nanoagent plugin inspect .`: exit 0.
