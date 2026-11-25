"""The answer key's rules for the Guide to Missions and Authorised Travel (Commission Decision C(2025) 2495, applied
by Europe's Rail Joint Undertaking through Governing Board Decision 11/2025), as exact integer code.
Byte-identical in src/plugin/rules.py and verifier/rules.py; it imports only modules a verifier may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. The PDF text layer splits some
words ("m anifestly", "missi on"); quotes keep the frozen text as it is. Where the text leaves an answer open, the
rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each unclear phrase at most
once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a new scenario cannot fall
silently into untested logic.

The duration hook. Lines 707-710: premium economy or business "if the outward or return journey includes at least
one segment involving at least five-hours of continuous flying time" (line 665 repeats it: "when one segment of the
travel involves at least five hours' continuous flying time"). Inclusive ("at least"), measured on one segment's
scheduled minutes: continuous flying time is never two flights added together, and one qualifying segment
qualifies the journey. Lines 815-818 set a second threshold, the rest period, on "the total duration of the
flights" (at least 10 hours, the flights added together, ground time left out); it decides no ticket.

The world has flights only: a rail alternative appears as facts in the trip record (its distance, first-class fare
and time), never as something to search.
"""

from contract import (
    Accompanied,
    Approver,
    Cabin,
    Clause,
    Decision,
    EventRole,
    Journey,
    ReasonCode,
    SignOffSubject,
    TravelKind,
)

from .world import clock_minutes, utc_minute

HANDBOOK = "Guide to Missions and Authorised Travel, Commission Decision C(2025) 2495 (EU-Rail Decision 11/2025)"

# Each closed-list section and the heading it names in the frozen text (tests check every heading is there).
CLAUSE_HEADINGS = {
    Clause.SCOPE: "1.1 Scope",
    Clause.PRINCIPLES_AND_ROLES: "1.2 Principles and roles (5)",
    Clause.LINE_MANAGER_ROLE: "1.2.2. The mission performer's line manager decides whether the mission or authorised travel is",
    Clause.AUTHORISING_OFFICER_ROLE: "1.2.4. The authorising officer for commitments (in the Directorate-General or service (14) to which",
    Clause.MISSION_DEFINITION: "2.1 Definition",
    Clause.SMART_ORGANISATION: "2.2 Smart organisation of missions",
    Clause.ORGANISATION_OF_MISSIONS: "2.3.1. General information on the organisation of missions",
    Clause.BOOKING_METHODS: "Booking methods",
    Clause.MISSION_ORDERS: "2.3.2. Mission orders",
    Clause.PERSONAL_CHANGES: "Changes made for personal reasons",
    Clause.RECALL_FROM_LEAVE: "Recall from leave (31)",
    Clause.CANCELLATION: "Cancellation",
    Clause.DEPARTURE_RETURN: "2.5.1. Departure / return",
    Clause.TRANSPORT_BETWEEN_PLACES: "2.5.4. Transport between the place of employment and the place of the",
    Clause.SMART_TRAVELLING: "Smart travelling",
    Clause.TRAVEL_BY_RAIL: "Travel by rail",
    Clause.TRAVEL_BY_AIR: "Travel by air",
    Clause.AIR_PASSENGER_RIGHTS: "Air passenger rights",
    Clause.ACCOMMODATION: "2.6. Rules on accommodation",
    Clause.MISSION_DURATION: "2.7.1. Duration of the mission",
    Clause.DAILY_ALLOWANCE: "2.7.2. Calculation of the daily subsistence allowance",
    Clause.LONG_STAY: "2.9. Long-stay missions",
    Clause.THIRD_PARTY_EXPENSES: "2.10. Expenses paid by third parties",
    Clause.SECONDED_EXPERTS: "2.11. Travel by Seconded National Experts (SNEs)",
    Clause.STATEMENT_OF_EXPENSES: "2.12 Statement of mission expenses",
    Clause.AUTHORISED_TRAVEL: "3 AUTHORISED TRAVEL",
    Clause.AUTHORISED_TRAVEL_RULES: "3.1. General rules",
    Clause.AUTHORISED_TRAVEL_TRANSPORT: "3.3.2. Rules on transport",
    Clause.AUTHORISATION_TO_TRAVEL: "3.4.1. Authorisation to travel",
    Clause.AUTHORISED_TRAVEL_EXPENSES: "3.4.2. Statement of expenses (if applicable)",
    Clause.GENERAL_PROVISIONS: "4 GENERAL PROVISIONS",
    Clause.SAFETY_AND_SECURITY: "4.2. Safety and security",
}

# The handbook's duration thresholds (the per-handbook duration hook; tests/test_duration.py tests both sides of
# each). ">=" is inclusive ("at least").
DURATION_RULES = (
    {"name": "long-segment", "minutes": 300, "operator": ">=", "lines": [707, 710],
     "quote": "if the outward or return journey includes at least one segment involving at least five-hours of "
              "continuous flying time."},
    {"name": "rest-period", "minutes": 600, "operator": ">=", "lines": [815, 818],
     "quote": "if the total duration of the flights is at least 10 hours, the authorising officer for commitments may "
              "decide to grant the mission performer a rest period of up to 24 hours before the meetings"},
)
LIMITS = {rule["name"]: rule["minutes"] for rule in DURATION_RULES}

# Handbook-specific conventions shown by booking_requirements, beyond the template's (none here).
CONVENTIONS = ()

# Lines 577-582: a mission performer "cannot be required to leave before 8:00 or arrive after 22:00", take-off and
# landing times (strict: 08:00 is not before 8:00, 22:00 is not after 22:00).
EARLIEST_MINUTE = 8 * 60
LATEST_MINUTE = 22 * 60
# Lines 583-585: a return by air "must be, in principle, started ... not more than three-and-a-half hours after the
# end of the meeting(s)" (inclusive), measured to the take-off.
RETURN_START_MINUTES = 210
# Lines 630-636: rail "for distances up to 550km" (inclusive) where its price "is not more than 40% above" the
# economy plane ticket (inclusive). Footnote 38 (lines 652-655) lets both be read "in a flexible manner" (600 km
# and 43% in its own example), so rail cases keep wide margins: no rail distance between 550 and 700 km, and no
# rail price between 130% and 150% of the air fare.
RAIL_KM = 550
RAIL_FLEX_KM = 700
RAIL_PERCENT = 140
FLEX_LOW, FLEX_HIGH = 130, 150
# Lines 663-664: direct flights "favoured when available, and within reasonable cost variations (40%)"; lines
# 684-687: "Direct flights are the norm", though the authorising officer may refuse a manifestly unreasonable one.
DIRECT_PERCENT = 140
# Lines 367-368: "more than three staff members from the same Directorate-General" (strict) need an authorisation
# at Director-General level, which may be delegated (lines 369-371).
PARTICIPANT_LIMIT = 3
# An outward flight is taken only if it lands before the first meeting starts (lines 689-691: "taking into account
# the times of meetings"); cases keep every landing at least this far from the start, or after it.
MEETING_MARGIN = 30

DIRECT_PHRASE = "direct flights favoured when available, and within reasonable cost variations (40%)"
PREMIUM_PHRASE = ("This should also be the choice, for example, if the flight is not overnight or when there is no "
                  "meeting immediately after arrival")

# Who a hold over unclear words may name: the guide names nobody to settle its text; the authorising officer for
# commitments approves the practical arrangements (lines 254-256) and may refuse a direct flight (lines 684-686).
UNCLEAR_ROLES = [Approver.NOT_NAMED, Approver.AUTHORISING_OFFICER]
# Such a hold also waits on that sign-off, so APPROVAL_REQUIRED may stand beside UNCLEAR_POLICY_TEXT.
UNCLEAR_REASONS = [ReasonCode.UNCLEAR_POLICY_TEXT, ReasonCode.APPROVAL_REQUIRED]
# Lines 368-371: the Director-General, or senior management or the HR Correspondent by delegation.
PARTICIPATION_ROLES = [Approver.DIRECTOR_GENERAL, Approver.SENIOR_MANAGEMENT, Approver.HR_CORRESPONDENT]


def over(rule, offer):
    """True or False: whether ``offer``'s outbound flights reach the handbook's ``rule`` (long-segment: one
    segment of 300 scheduled minutes or more; rest-period: the flights' scheduled minutes added together, 600 or
    more). Neither rule leaves a reading open."""
    if rule == "long-segment":
        return any(segment.scheduled_minutes >= LIMITS[rule] for segment in offer.segments)
    if rule == "rest-period":
        return offer.flying_minutes >= LIMITS[rule]
    raise ValueError(f"unknown duration rule {rule!r}")


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted(offer.offer_id for offer in offers),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(clauses),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def on_file(trip):
    """NONE and every role on file: a decision that relies on a sign-off already given accepts that role and NONE
    (SYNC_NOTES 4'), and a sign-off on file that the decision does not use is accepted beside NONE (4(b)). The
    exception is a sign-off whose invalidity the case tests: a written request for the same class from anyone but
    the Member of the Commission or their Cabinet (lines 711-714)."""
    return [Approver.NONE, *(record.role for record in trip.sign_offs
                             if record.subject != SignOffSubject.SAME_CLASS_REQUEST
                             or record.role in (Approver.MEMBER_OF_COMMISSION, Approver.CABINET))]


def refuse(trip, reasons, clauses, why):
    return answer(Decision.REFUSE, [], reasons, on_file(trip), clauses, why)


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def in_cabin(offers, cabin):
    return [offer for offer in offers if offer.cabin == cabin]


def signed(trip, subject, roles):
    return sorted({record.role for record in trip.sign_offs if record.subject == subject and record.role in roles},
                  key=lambda role: role.value)


def clock(text):
    return clock_minutes(text[11:])


def protected(offer):
    """Lines 577-582: whether the offer leaves before 08:00 or lands after 22:00 (take-off and landing, local)."""
    first, last = offer.segments[0], offer.segments[-1]
    if last.arrive_local[:10] != first.depart_local[:10]:
        raise ValueError("an overnight flight under the 08:00/22:00 rule is not modelled")
    return clock(first.depart_local) < EARLIEST_MINUTE or clock(last.arrive_local) > LATEST_MINUTE


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers on its route and date: the decision, and every accepted offer
    id, cabin, reason, approver and section. ``hidden`` (the scenario's answer_key_inputs) is unused by this
    handbook."""
    if hidden:
        raise ValueError("this handbook's scenarios carry no answer_key_inputs")
    if any(offer.return_segments for offer in offers):
        raise ValueError("round-trip fares are not modelled: every case buys a one-way ticket")
    seated = [offer for offer in offers if offer.seats_available]
    if trip.travel_kind == TravelKind.PRIVATE:
        return refuse(trip, [ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE],
                      [Clause.MISSION_DEFINITION, Clause.SCOPE],
                      "Lines 174-175 and 323-325: a mission is travel solely in the interests of the service on a line "
                      "manager's instructions, paid from the mission budget; lines 191-193: authorised travel is also "
                      "linked to the traveller's professional tasks. A private visit is neither, so the organisation "
                      "buys no ticket.")
    if trip.travel_kind == TravelKind.AUTHORISED_TRAVEL and not trip.authorisation_pays_transport:
        return refuse(trip, [ReasonCode.TRAVEL_COSTS_NOT_COVERED, ReasonCode.PERSONAL_TRAVEL_NOT_COVERED,
                             ReasonCode.OUTSIDE_POLICY_SCOPE],
                      [Clause.AUTHORISED_TRAVEL_RULES, Clause.AUTHORISATION_TO_TRAVEL, Clause.AUTHORISED_TRAVEL_EXPENSES],
                      "Lines 1085-1088: the organisation may finance none, part or all of authorised travel; lines "
                      "1199-1201: the signed authorisation allows expenses only within its limits; lines 1210-1213: one "
                      "approved without expenses must be cancelled and a new one approved before costs are covered. This "
                      "authorisation was signed without expenses, so the organisation buys no ticket.")
    if trip.travel_kind == TravelKind.MISSION and trip.authorisation_pays_transport:
        raise ValueError("an authorisation's transport flag on a mission is not modelled")
    rail = rail_check(trip, seated)
    if rail.get("decision"):
        return rail
    pick = choose(trip, seated)
    if trip.travel_kind == TravelKind.AUTHORISED_TRAVEL:
        pick["clauses"] = [*pick["clauses"], Clause.AUTHORISED_TRAVEL_TRANSPORT, Clause.AUTHORISATION_TO_TRAVEL]
        pick["why"] += (" Lines 1143-1149: the rules for missions apply to authorised travel by analogy, and the signed "
                        "authorisation has the organisation pay the transport (lines 1199-1203).")
    pick["reasons"] = [*pick["reasons"], *rail["reasons"]]
    pick["clauses"] = [*pick["clauses"], *rail["clauses"]]
    pick["why"] = " ".join([pick["why"], *rail["why"]])
    return gate(trip, pick)


def rail_check(trip, seated):
    """Lines 630-636 and 663: rail is encouraged up to 550 km per segment, and favoured where it costs no more
    than 40% above the economy plane ticket; air travel for distances up to 550 km must be appropriately justified
    (footnote 40, lines 693-694: e.g. security reasons or particularly heavy schedules). Returns a refusal, or the
    reasons and sections to add to the booking."""
    extra = {"reasons": [], "clauses": [], "why": []}
    if not trip.rail_km:
        if trip.rail_fare_cents or trip.rail_minutes:
            raise ValueError("rail facts without a rail distance are not modelled")
        if trip.air_justification:
            raise ValueError("an air justification without a rail alternative is not modelled")
        return extra
    low = cheapest(in_cabin(seated, Cabin.ECONOMY))
    if not low:
        raise ValueError("a rail comparison with no economy fare is not modelled")
    percent = trip.rail_fare_cents * 100 / low[0].fare_cents
    if FLEX_LOW <= percent <= FLEX_HIGH:
        raise ValueError("a rail price near the 40% line is not modelled (footnote 38: read flexibly)")
    if trip.rail_km <= RAIL_KM:
        if percent > RAIL_PERCENT:
            raise ValueError("a short rail journey much dearer than the flight is not modelled")
        if not trip.air_justification:
            return refuse(trip, [ReasonCode.RAIL_PREFERRED, ReasonCode.DISTANCE_BELOW_MINIMUM,
                                 ReasonCode.NO_COMPLIANT_OFFER],
                          [Clause.SMART_TRAVELLING, Clause.TRANSPORT_BETWEEN_PLACES],
                          "Lines 630-636: rail is encouraged up to 550 km, and the greener alternative is favoured "
                          "where rail costs no more than 40% above the economy plane ticket; line 663: air travel for "
                          "distances up to 550 km must be appropriately justified. The journey is within 550 km, the "
                          "first-class rail fare is within 40% of the lowest economy fare, and nothing on file "
                          "justifies flying: the organisation buys no air ticket.")
        extra["reasons"] = [ReasonCode.AIR_TRAVEL_JUSTIFIED]
        extra["clauses"] = [Clause.SMART_TRAVELLING, Clause.TRANSPORT_BETWEEN_PLACES]
        extra["why"] = [("Line 663 and footnote 40 (lines 693-694): air travel up to 550 km must be justified, for "
                        "example by a particularly heavy schedule with meetings in several places, which is on file.")]
        return extra
    if trip.rail_km < RAIL_FLEX_KM:
        raise ValueError("a rail distance just over 550 km is not modelled (footnote 38: read flexibly)")
    if percent <= FLEX_HIGH:
        raise ValueError("a long rail journey within the price variation is not modelled (a soft preference)")
    if trip.air_justification:
        raise ValueError("a justification for a long journey is not modelled")
    extra["clauses"] = [Clause.SMART_TRAVELLING]
    extra["why"] = [("Lines 630-636: above 550 km rail is only encouraged where it is an efficient alternative, and "
                    "here it costs far more than 40% above the plane ticket and takes most of a day, so the flight "
                    "needs no justification.")]
    return extra


def pick_of(offers, reasons, clauses, why, approvers=()):
    return {"offers": offers, "reasons": reasons, "clauses": clauses, "why": why, "approvers": list(approvers),
            "unclear": None}


def choose(trip, seated):
    """Which offer the handbook buys, before the sign-offs are checked."""
    if trip.accompanies == Accompanied.MEMBER_OF_COMMISSION:
        return same_class(trip, seated)
    if trip.accompanies == Accompanied.NOBODY and trip.accompanied_cabin != Cabin.NONE:
        raise ValueError("an accompanied cabin with nobody accompanied is not modelled")
    if trip.requested_cabin == Cabin.BUSINESS:
        return business(trip, seated)
    if trip.requested_cabin == Cabin.PREMIUM_ECONOMY:
        return premium(trip, seated)
    if trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError(f"a {trip.requested_cabin.value} request is not modelled")
    return economy(trip, seated)


def same_class(trip, seated):
    """Lines 711-714: as a derogation from (a), (b) and (c), on written request of the Member of the Commission or
    their Cabinet, for exceptional overriding service reasons justified in the mission order, staff may travel in
    the same class as the Member they accompany."""
    asked = signed(trip, SignOffSubject.SAME_CLASS_REQUEST, [Approver.MEMBER_OF_COMMISSION, Approver.CABINET])
    if not asked or trip.requested_cabin != trip.accompanied_cabin or trip.accompanied_cabin != Cabin.BUSINESS:
        raise ValueError("a same-class derogation without the written request, or outside business, is not modelled")
    offered = in_cabin(seated, Cabin.BUSINESS)
    if not offered or any(over("long-segment", offer) for offer in offered):
        raise ValueError("a derogation where business is allowed anyway, or not sold, is not modelled")
    return pick_of(cheapest(offered), [ReasonCode.SAME_CLASS_AS_MEMBER], [Clause.TRAVEL_BY_AIR],
                   "Lines 711-714: the Member's Cabinet asked in writing for the traveller to fly in the same class as "
                   "the Member they accompany, for reasons set out in the mission order, which is authorised: the "
                   "cheapest business fare. Without it, lines 664 and 689-691 would give economy (no segment of five "
                   "hours).", approvers=[Approver.MEMBER_OF_COMMISSION, Approver.CABINET])


def declined_upgrade(trip, seated, cabin_words):
    base = economy(trip, seated)
    if base["unclear"]:
        raise ValueError("a declined upgrade on an unclear routing is not modelled")
    base["reasons"] = [ReasonCode.UPGRADE_NOT_ELIGIBLE, ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET]
    base["clauses"] = [Clause.TRAVEL_BY_AIR, Clause.SMART_TRAVELLING]
    base["why"] = (f"Lines 707-710 and 665: {cabin_words} only if the journey includes a segment of at least five hours' "
                   "continuous flying time (300 minutes), and no segment reaches it; line 664: economy class remains "
                   "the default. " + base["why"])
    return base


def business(trip, seated):
    """A business request. Lines 707-710 (c): premium economy when suitable, or business, at the lowest rates, if
    the journey includes a segment of at least five hours' continuous flying; lines 665-668: when business is
    allowed premium economy should be envisaged when available, and should also be the choice if the flight is
    not overnight or there is no meeting immediately after arrival."""
    offered = in_cabin(seated, Cabin.BUSINESS)
    qualifying = [offer for offer in offered if over("long-segment", offer)]
    if not qualifying:
        if any(over("long-segment", offer) for offer in seated):
            raise ValueError("a qualifying flight without a business seat is not modelled")
        return declined_upgrade(trip, seated, "premium economy or business is allowed")
    if len(qualifying) != len(offered) or any(offer.stops for offer in qualifying):
        raise ValueError("business offers on both sides of the rule, or on connections, are not modelled")
    premium_offers = [offer for offer in in_cabin(seated, Cabin.PREMIUM_ECONOMY) if over("long-segment", offer)]
    best = cheapest(qualifying)
    if premium_offers:
        lands = utc_minute(best[0].segments[-1].arrive_local)
        overnight = best[0].segments[-1].arrive_local[:10] != best[0].segments[0].depart_local[:10]
        meeting_soon = utc_minute(trip.meeting_start_local) - lands < 6 * 60
        if overnight or meeting_soon:
            raise ValueError("business against premium economy on an overnight flight or before a meeting is not "
                             "modelled")
        pick = pick_of([*cheapest(premium_offers), *best], UNCLEAR_REASONS, [Clause.TRAVEL_BY_AIR, Clause.SMART_TRAVELLING],
                       "Lines 707-710: a segment of at least five hours allows 'premium economy class when suitable, or "
                       "business class'; lines 665-668: when business is allowed premium economy should be envisaged "
                       "when available, and 'should also be the choice' when the flight is not overnight or no meeting "
                       "follows arrival, as here. The text does not say whether 'should' rules out the business seat "
                       "the traveller asked for, which (c) allows: hold the premium economy fare or the business fare.")
        pick["unclear"] = PREMIUM_PHRASE
        return pick
    return pick_of(best, [ReasonCode.LONG_FLIGHT_APPROVED, ReasonCode.INTERNATIONAL_LONG_FLIGHT], [Clause.TRAVEL_BY_AIR],
                   "Lines 707-710 (c): the journey includes a segment of at least five hours' continuous flying time (300 "
                   "minutes or more), so business may be booked at the lowest rate; no premium economy is sold on it "
                   "(lines 665-666: 'when available'). The cheapest business fare.")


def premium(trip, seated):
    """A premium economy request: lines 707-710 (c) allow it on a journey with a segment of at least five hours."""
    offered = in_cabin(seated, Cabin.PREMIUM_ECONOMY)
    if not offered:
        raise ValueError("a premium economy request with no premium economy offer is not modelled")
    qualifying = [offer for offer in offered if over("long-segment", offer)]
    if not qualifying:
        return declined_upgrade(trip, seated, "premium economy is allowed")
    if len(qualifying) != len(offered):
        raise ValueError("premium economy offers on both sides of the rule are not modelled")
    return pick_of(cheapest(qualifying), [ReasonCode.PREMIUM_ECONOMY_ALLOWED], [Clause.TRAVEL_BY_AIR],
                   "Lines 707-710 (c): the journey includes a segment of at least five hours' continuous flying time (300 "
                   "minutes or more), so premium economy may be booked at the lowest rate: the cheapest premium economy "
                   "fare.")


def economy(trip, seated):
    """An economy booking: (a) lines 688-691, economy including non-refundable tickets at the lowest available
    rates, taking into account the times of meetings; (b) lines 704-706, the lowest flexible rates if there is a
    risk that the mission will be cancelled or amended; then the time rules of lines 577-587 and the direct-flight
    norm of lines 663-664 and 684-687."""
    pool = in_cabin(seated, Cabin.ECONOMY)
    reasons, clauses, notes = [ReasonCode.LOWEST_FARE], [Clause.TRAVEL_BY_AIR, Clause.TRANSPORT_BETWEEN_PLACES], []
    if trip.wants_refundable:
        if trip.risk_of_change:
            pool = [offer for offer in pool if offer.refundable]
            reasons = [ReasonCode.FLEXIBLE_FARE_JUSTIFIED, ReasonCode.LOWEST_FARE]
            notes.append("lines 704-706 (b): the trip may be called off or moved, so the lowest flexible economy rate")
        else:
            pool = [offer for offer in pool if not offer.refundable]
            # The ground for declining the changeable fare is (b)'s risk condition, not the bare lowest-fare rule.
            reasons = [ReasonCode.REFUNDABLE_FARE_NOT_ALLOWED]
            notes.append("lines 704-706: flexible tickets only where the mission risks being cancelled or amended, and "
                         "nothing on file says so; (a), lines 689-691: economy including non-refundable tickets at the "
                         "lowest available rate")
    else:
        if trip.risk_of_change:
            raise ValueError("a risk of change without a changeable-fare wish is not modelled")
        if any(offer.refundable for offer in cheapest(pool)):
            raise ValueError("a refundable fare that is the lowest is not modelled")
        notes.append("lines 664 and 689-691: economy is the default, at the lowest available rate")
    if not pool:
        raise ValueError("no economy offer can be bought")
    pool, timing = timing_rules(trip, pool)
    reasons += timing["reasons"]
    clauses += timing["clauses"]
    notes += timing["notes"]
    if timing["replace_reasons"]:
        reasons = timing["replace_reasons"]
    if trip.chosen_airline:
        low = cheapest(pool)
        if any(offer.carrier == trip.chosen_airline for offer in low):
            raise ValueError("a chosen airline at the lowest fare is not modelled")
        if not any(offer.carrier == trip.chosen_airline for offer in pool):
            raise ValueError("a chosen airline with no offer is not modelled")
        # The ground for declining the airline is the lowest-rate rule itself, with line 407 on airmiles.
        reasons = [ReasonCode.LOYALTY_PROGRAM_PREFERENCE, ReasonCode.LOWEST_FARE]
        clauses.append(Clause.BOOKING_METHODS)
        notes.append("line 407: staff may not draw any private benefit from airmiles of professional travel, so the "
                     "airline chosen for its miles is not booked above the lowest rate")
    return direct_norm(pool, reasons, clauses, notes)


def timing_rules(trip, pool):
    """Lines 689-691 (meeting times), 577-582 (08:00 and 22:00) and 583-587 (the return's start)."""
    out = {"reasons": [], "clauses": [], "notes": [], "replace_reasons": []}
    if trip.journey == Journey.OUTWARD:
        if trip.meeting_end_local or not trip.meeting_start_local:
            raise ValueError("an outward flight needs a meeting start and no meeting end")
        start = utc_minute(trip.meeting_start_local)
        for offer in pool:
            gap = start - utc_minute(offer.segments[-1].arrive_local)
            if 0 < gap < MEETING_MARGIN:
                raise ValueError("a landing just before the meeting is not modelled")
        late = [offer for offer in pool if utc_minute(offer.segments[-1].arrive_local) >= start]
        if late:
            pool = [offer for offer in pool if offer not in late]
            out["notes"].append("lines 689-691: taking into account the times of meetings, a flight landing after the "
                                "first meeting starts is not taken")
    else:
        if trip.meeting_start_local or not trip.meeting_end_local:
            raise ValueError("a return flight needs a meeting end and no meeting start")
        end = utc_minute(trip.meeting_end_local)
        gaps = {offer.offer_id: utc_minute(offer.segments[0].depart_local) - end for offer in pool}
        if any(gap <= 0 for gap in gaps.values()):
            raise ValueError("a return flight leaving before the meeting ends is not modelled")
        pool = [offer for offer in pool if gaps[offer.offer_id] <= RETURN_START_MINUTES]
        out["reasons"].append(ReasonCode.RETURN_START_LIMIT)
        out["clauses"].append(Clause.DEPARTURE_RETURN)
        out["notes"].append("lines 583-585: the return by air starts not more than three and a half hours (210 "
                            "minutes) after the end of the meeting, so a later take-off is not booked")
    if trip.avoids_unrequired_hours:
        justified = signed(trip, SignOffSubject.TRAVEL_HOURS, [Approver.LINE_MANAGER])
        out["clauses"].append(Clause.DEPARTURE_RETURN)
        if justified:
            low = cheapest(pool)
            if not all(protected(offer) for offer in low):
                raise ValueError("a line manager's reasons that the cheapest flight does not need are not modelled")
            # The traveller's wish is declined on the line manager's justifiable reasons (lines 577-579).
            out["replace_reasons"] = [ReasonCode.EARLY_LATE_HOURS_JUSTIFIED]
            out["notes"].append("lines 577-579: the line manager gave justifiable reasons, on file, for leaving before "
                                "08:00, so the traveller can be required to take the early flight")
        else:
            pool = [offer for offer in pool if not protected(offer)]
            out["reasons"].append(ReasonCode.EARLY_LATE_HOURS_PROTECTED)
            out["notes"].append("lines 577-582: the traveller cannot be required to take off before 08:00 or land after "
                                "22:00, and asks not to be; such flights are left out")
    elif trip.journey == Journey.RETURN and any(protected(offer) for offer in cheapest(pool)):
        raise ValueError("a return case at protected hours without the traveller's wish is not modelled")
    if not pool:
        raise ValueError("no economy offer is left after the time rules")
    return pool, out


def direct_norm(pool, reasons, clauses, notes):
    """Lines 684-687: direct flights are the norm, though the authorising officer may refuse a direct flight that
    would be a manifestly unreasonable expense; lines 663-664: direct flights favoured within reasonable cost
    variations (40%)."""
    low = cheapest(pool)
    direct = cheapest([offer for offer in pool if offer.stops == 0])
    why = "; ".join(notes)
    if all(offer.stops == 0 for offer in low) or not direct:
        return pick_of(low, reasons, clauses, why[:1].upper() + why[1:] + ".")
    if len({offer.stops == 0 for offer in low}) != 1:
        raise ValueError("a tie between a direct flight and a connection is not modelled")
    percent = direct[0].fare_cents * 100 / low[0].fare_cents
    if FLEX_LOW <= percent <= FLEX_HIGH:
        raise ValueError("a direct flight near 40% above the connection is not modelled")
    if percent <= DIRECT_PERCENT:
        if ReasonCode.LOWEST_FARE not in reasons or len(reasons) != 1:
            raise ValueError("the direct-flight norm beside another booking reason is not modelled")
        return pick_of(direct, [ReasonCode.DIRECT_FLIGHT_NORM, ReasonCode.ALTERNATE_ROUTE_WITHIN_MARGIN],
                       [*clauses, Clause.SMART_TRAVELLING],
                       "Lines 684-687: direct flights are the norm, and lines 663-664 favour them within reasonable cost "
                       "variations (40%); the direct flight costs less than 40% more than the cheapest connection, so "
                       "the cheapest direct flight.")
    pick = pick_of([*low, *direct], UNCLEAR_REASONS, [Clause.TRAVEL_BY_AIR, Clause.SMART_TRAVELLING],
                   "Lines 684-687: direct flights are the norm, and only the authorising officer may refuse one that would "
                   "be a manifestly unreasonable expense; lines 663-664 favour direct flights 'within reasonable cost "
                   "variations (40%)' in a sentence about journeys up to 550 km. The direct flight costs more than 40% "
                   "above the connection on a longer route: the text does not say whether the 40% applies here or "
                   "whether the direct flight stays the norm until the authorising officer refuses it. Hold the "
                   "connection or the direct flight.")
    pick["unclear"] = DIRECT_PHRASE
    return pick


def gate(trip, pick):
    """The sign-offs a booking relies on. Lines 326-331: the mission order is signed by the line manager and, if
    they are not the same person, by the authorising officer for commitments (footnote 15, lines 273-275: they may
    be); lines 426-428: final reservations only once the authorising officer has signed (for authorised travel,
    lines 1199-1203). Lines 364-372: more than three staff of one Directorate-General at a single meeting need an
    authorisation at Director-General level (footnote 25, lines 399-400: not where specific rules set the number of
    participants, as for interpreters)."""
    subject = SignOffSubject.MISSION_ORDER if trip.travel_kind == TravelKind.MISSION else SignOffSubject.AUTHORISATION_TO_TRAVEL
    signers = signed(trip, subject, [Approver.LINE_MANAGER, Approver.AUTHORISING_OFFICER])
    if Approver.LINE_MANAGER not in signers:
        raise ValueError("a trip without the line manager's signature is not modelled")
    if trip.line_manager_is_authorising_officer and Approver.AUTHORISING_OFFICER in signers:
        raise ValueError("two signatures by one person are not modelled")
    budget_signed = Approver.AUTHORISING_OFFICER in signers or trip.line_manager_is_authorising_officer
    crowded = trip.same_dg_participants > PARTICIPANT_LIMIT and trip.event_role != EventRole.INTERPRETER
    allowed = signed(trip, SignOffSubject.PARTICIPATION, PARTICIPATION_ROLES)
    clauses = list(pick["clauses"])
    why = pick["why"]
    approvers = [*on_file(trip), *pick["approvers"]]
    if trip.line_manager_is_authorising_officer:
        clauses += [Clause.MISSION_ORDERS, Clause.MISSION_DEFINITION]
        approvers.append(Approver.AUTHORISING_OFFICER)
        why += (" Lines 326-331 and footnote 15 (lines 273-275): the line manager, who signed, is also the authorising "
                "officer for commitments, so the mission order is signed.")
    if trip.same_dg_participants > PARTICIPANT_LIMIT and trip.event_role == EventRole.INTERPRETER:
        clauses.append(Clause.SMART_ORGANISATION)
        why += (" Footnote 25 (lines 399-400): the Director-General's authorisation for more than three staff does not "
                "apply where specific rules set the number of participants, as for interpreters.")
    if pick["unclear"]:
        if not budget_signed or (crowded and not allowed):
            raise ValueError("an unclear hold that also lacks a sign-off is not modelled")
        return answer(Decision.FLAG_FOR_APPROVAL, pick["offers"], pick["reasons"], UNCLEAR_ROLES, clauses, why,
                      phrase=pick["unclear"])
    if not budget_signed:
        if crowded:
            raise ValueError("two missing sign-offs are not modelled")
        return answer(Decision.FLAG_FOR_APPROVAL, pick["offers"],
                      [ReasonCode.APPROVAL_REQUIRED, ReasonCode.MISSION_ORDER_NOT_SIGNED], [Approver.AUTHORISING_OFFICER],
                      [Clause.MISSION_ORDERS, Clause.MISSION_DEFINITION],
                      why + " But lines 328-331: the line manager is not the authorising officer, so the mission order "
                      "must also be signed by the authorising officer for commitments, and lines 426-437: tickets are "
                      "reserved only once they have signed (an unrefundable ticket bought without their approval may be "
                      "recovered). Hold the fare for the authorising officer.")
    if crowded and not allowed:
        return answer(Decision.FLAG_FOR_APPROVAL, pick["offers"],
                      [ReasonCode.APPROVAL_REQUIRED, ReasonCode.PARTICIPANTS_ABOVE_LIMIT], PARTICIPATION_ROLES,
                      [Clause.SMART_ORGANISATION],
                      why + " But lines 367-371: more than three staff of the Directorate-General take part in this one "
                      "meeting, which needs an authorisation at Director-General level (or by its delegate), and none is "
                      "on file. Hold the fare.")
    if crowded:
        raise ValueError("a participation authorisation on file is not modelled")
    return answer(Decision.BOOK, pick["offers"], pick["reasons"], approvers, clauses, why)
