"""Writes the EU Rail Guide to Missions scenario JSON files (an authoring aid, not a test; the JSON files are the
truth).

    uv run python tests/build_scenarios.py

Expected answers are hand-written here; tests/test_scenarios.py checks them against rules.solve.
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

POLICY = (ROOT / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = ROOT / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def aside(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- clauses the answers rest on (quotes keep the frozen text's split words, e.g. "m anifestly") -----
MISSION = keep(174, 175, "A mission (instruction to travel) is defined as travel away from the place of employment "
               "solely in the interests of the service on the instructions of a line manager.",
               "a mission is work travel on a line manager's instruction")
MISSION_BUDGET = keep(323, 325, None, "a mission is paid from the mission budget")
AUTH_DEF = keep(191, 193, None, "authorised travel: an outside event of personal and institutional interest")
LM_IS_AO = keep(273, 275, "The authorising officer for commitments may be the same person as the line manager.",
                "footnote 15: the line manager may be the authorising officer")
ORDER_SIGNERS = keep(326, 331, None, "the mission order is signed by the line manager and, if another person, the "
                     "authorising officer")
RESERVE = keep(426, 428, None, "final reservations only once the authorising officer has signed the mission order")
RECOVER = keep(432, 437, None, "unrefundable tickets chosen without the authorising officer's approval may be recovered")
PARTICIPANTS = keep(364, 372, None, "more than three staff of one DG at one meeting need a Director-General level "
                    "authorisation, which may be delegated")
INTERPRETERS = keep(399, 400, None, "footnote 25: not where specific rules set the number, as for interpreters")
AIRMILES = keep(407, 407, None, "no private benefit from airmiles of professional travel")
HOURS = keep(577, 582, None, "a mission performer cannot be required to take off before 8:00 or land after 22:00, "
             "unless the line manager gives justifiable reasons")
RETURN = keep(583, 587, None, "a return by air starts not more than three-and-a-half hours after the meeting ends")
RAIL = keep(630, 637, None, "rail encouraged up to 550 km and favoured within 40% of the economy plane ticket")
SHORT_AIR = keep(663, 664, None, "air up to 550 km must be justified; direct flights favoured within 40%; economy "
                 "the default")
PREMIUM_FIRST = keep(665, 668, None, "when business is allowed, premium economy should be envisaged and chosen in "
                     "some cases")
DIRECT = keep(684, 687, None, "direct flights are the norm; the authorising officer may refuse a manifestly "
              "unreasonable one")
TIER_A = keep(688, 691, None, "(a) economy, including non-refundable, at the lowest available rates")
JUSTIFY = keep(693, 694, None, "footnote 40: justifications include security or particularly heavy schedules")
TIER_B = keep(704, 706, None, "(b) economy at the lowest flexible rates if the mission risks cancellation")
TIER_C = keep(707, 710, None, "(c) premium economy or business if a segment has at least five hours' continuous "
              "flying")
SAME_CLASS = keep(711, 714, None, "derogation: same class as the accompanied Member, on the Member's or Cabinet's "
                  "written request")
AUTH_FINANCE = keep(1085, 1088, None, "authorised travel may be financed in none, part or full")
AUTH_ANALOGY = keep(1147, 1149, None, "the rules for missions apply to authorised travel by analogy")
AUTH_SIGNED = keep(1199, 1203, None, "the signed authorisation allows expenses within its limits")
AUTH_NONE = keep(1210, 1213, None, "an authorisation without expenses must be cancelled and replaced to cover costs")

# ----- nearby clauses that must not change the answer -----
REST = aside(815, 818, "if the total duration of the flights is at least 10 hours, the authorising officer for "
             "commitments may decide to grant the mission performer a rest period of up to 24 hours before the "
             "meetings", "a rest period after long flights, granted by the authorising officer; not a ticket rule")
FLEX = aside(652, 655, "These two elements (price variation and distance) may be interpreted in a flexible manner",
             "footnote 38: the 550 km and 40% figures are read flexibly; the cases keep wide margins")
RAIL_TIME = aside(650, 651, "The duration difference between rail and air travels should remain reasonable.",
                  "footnote 37: rail and air times should stay comparable")
EARLY_BOOK = aside(591, 592, "staff should book their tickets at the earliest opportunity",
                   "book early for missions planned well ahead; not a reason to hold or refuse")
NONREF_RECORD = aside(535, 536, "The mission performer must record (in the IT tool) where tickets or reservations "
                      "are not refundable", "a cancellation duty, not a fare rule")
ALLOWANCE = aside(844, 847, "more than 6 hours but not more than 12 hours: 50% of the daily allowance",
                  "daily allowance hours, not flight hours")
OTHER_MEANS = aside(586, 587, "in the case of travel by any other means of transport, not more than two hours after "
                    "the end of the meeting(s)", "the two-hour limit is for other transport, not air")

# ----- builders -----

LM, AO = "LINE_MANAGER", "AUTHORISING_OFFICER"


def sign(role, name, subject, note):
    return {"role": role, "name": name, "subject": subject, "note": note}


def order(lm="Head of unit", ao="Authorising officer"):
    return [sign(LM, lm, "MISSION_ORDER", "Mission order signed: purpose, dates and place of the mission"),
            sign(AO, ao, "MISSION_ORDER", "Mission order signed for the budget: the mission's cost estimate")]


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_title": "", "place_of_employment": "", "travel_kind": "MISSION",
        "authorisation_pays_transport": False, "journey": "OUTWARD", "origin": "", "destination": "",
        "travel_date": "", "booking_date": "", "meeting_start_local": "", "meeting_end_local": "", "purpose": "",
        "event_role": "PARTICIPANT", "same_dg_participants": 1, "requested_cabin": "ECONOMY",
        "wants_refundable": False, "risk_of_change": False, "chosen_airline": "", "avoids_unrequired_hours": False,
        "accompanies": "NOBODY", "accompanied_cabin": "NONE", "rail_km": 0, "rail_fare_cents": 0, "rail_minutes": 0,
        "air_justification": "", "line_manager_is_authorising_officer": False, "sign_offs": None,
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    if base["sign_offs"] is None:
        base["sign_offs"] = order()
    return base


def offer(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    return {"decision": decision, "offer_slots": slots, "cabins": cabins, "reason_codes": reasons,
            "approvers": approvers, "clauses": clauses, "unclear_phrase": phrase}


def search(origin, destination, date, flights, offers):
    # No background offers: handbook.json background_offers is 0 and every search sets 0, so each listing is
    # exactly the pinned offers, and a search the case does not pin lists nothing.
    return {"name": "main", "origin": origin, "destination": destination, "date": date, "return_date": "",
            "background": 0, "flights": flights, "offers": offers}


S = []


def scenario(id, category, overlays, request, trip_, search_spec, exp, must_keep, notes, twin_of="", twin_fact="",
             flag_twins=(), ambiguity="none", distractors=()):
    S.append({
        "id": id, "category": category, "overlays": list(overlays), "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": list(flag_twins), "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": [search_spec]}, "expected": exp, "must_keep": list(must_keep),
        "distractors": list(distractors), "design_notes": notes,
    })


BOOKED = ["AUTHORISING_OFFICER", "LINE_MANAGER", "NONE"]
LOW_CLAUSES = ["TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]
NOT_ELIGIBLE = ["LONG_FLIGHT_CONDITION_NOT_MET", "UPGRADE_NOT_ELIGIBLE"]
DECLINED_CLAUSES = ["SMART_TRAVELLING", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]
LONG_OK = ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED"]
UNCLEAR_ROLES = ["AUTHORISING_OFFICER", "NOT_NAMED"]
UNCLEAR_REASONS = ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"]
TIME_CLAUSES = ["DEPARTURE_RETURN", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]

# Shared worlds of twin pairs.


def munich_madrid():
    return search("MUC", "MAD", "2027-02-16", {
        "morning": {"carrier": "LH", "depart": "09:00", "minutes": [140]},
        "noon": {"carrier": "IB", "depart": "12:40", "minutes": [135]},
        "evening": {"carrier": "LH", "depart": "17:20", "minutes": [140]},
    }, [
        offer("morning-saver", "morning", "ECONOMY", 16800),
        offer("morning-flex", "morning", "ECONOMY", 24900, refundable=True),
        offer("noon-saver", "noon", "ECONOMY", 15900),
        offer("noon-flex", "noon", "ECONOMY", 26200, refundable=True),
        offer("evening-saver", "evening", "ECONOMY", 18100),
    ])


def doha(minutes):
    return search("FCO", "DOH", "2027-03-02", {
        "morning": {"carrier": "QR", "depart": "09:05", "minutes": [minutes]},
        "afternoon": {"carrier": "QR", "depart": "13:40", "minutes": [minutes]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 51200),
        offer("morning-business", "morning", "BUSINESS", 224000),
        offer("afternoon-economy", "afternoon", "ECONOMY", 49800),
        offer("afternoon-business", "afternoon", "BUSINESS", 239000),
    ])


def rome(first):
    return search("CDG", "FCO", "2027-02-03", {
        "first": {"carrier": "AF", "depart": first, "minutes": [120]},
        "morning": {"carrier": "AF", "depart": "09:35", "minutes": [120]},
        "noon": {"carrier": "AF", "depart": "12:50", "minutes": [120]},
        "evening": {"carrier": "AF", "depart": "18:20", "minutes": [120]},
    }, [
        offer("first-economy", "first", "ECONOMY", 11900),
        offer("morning-economy", "morning", "ECONOMY", 16400),
        offer("noon-economy", "noon", "ECONOMY", 17100),
        offer("evening-economy", "evening", "ECONOMY", 15800),
    ])


def madrid_home(cheap):
    return search("MAD", "CDG", "2026-12-11", {
        "early": {"carrier": "IB", "depart": "16:50", "minutes": [110]},
        "mid": {"carrier": "AF", "depart": "17:25", "minutes": [105]},
        "saver": {"carrier": "IB", "depart": cheap, "minutes": [110]},
        "late": {"carrier": "AF", "depart": "20:05", "minutes": [105]},
    }, [
        offer("early-economy", "early", "ECONOMY", 18200),
        offer("mid-economy", "mid", "ECONOMY", 17600),
        offer("saver-economy", "saver", "ECONOMY", 12800),
        offer("late-economy", "late", "ECONOMY", 13900),
    ])


def nairobi(minutes):
    return search("CDG", "NBO", "2027-02-22", {
        "first": {"carrier": "MS", "via": ["CAI"], "depart": "08:15", "minutes": [260, minutes], "layovers": [95]},
        "second": {"carrier": "MS", "via": ["CAI"], "depart": "09:05", "minutes": [260, minutes], "layovers": [75]},
    }, [
        offer("first-economy", "first", "ECONOMY", 61000),
        offer("first-premium", "first", "PREMIUM_ECONOMY", 112000),
        offer("second-economy", "second", "ECONOMY", 58500),
        offer("second-premium", "second", "PREMIUM_ECONOMY", 118000),
    ])


def ministerial():
    return search("CDG", "MAD", "2027-03-09", {
        "airfrance": {"carrier": "AF", "depart": "09:20", "minutes": [105]},
        "iberia": {"carrier": "IB", "depart": "10:05", "minutes": [110]},
    }, [
        offer("airfrance-economy", "airfrance", "ECONOMY", 15200),
        offer("airfrance-business", "airfrance", "BUSINESS", 64000),
        offer("iberia-economy", "iberia", "ECONOMY", 13900),
        offer("iberia-business", "iberia", "BUSINESS", 59800),
    ])


def amsterdam():
    return search("CDG", "AMS", "2027-01-19", {
        "morning": {"carrier": "KL", "depart": "10:05", "minutes": [70]},
        "afternoon": {"carrier": "AF", "depart": "13:40", "minutes": [70]},
        "evening": {"carrier": "KL", "depart": "18:25", "minutes": [70]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 9600),
        offer("afternoon-economy", "afternoon", "ECONOMY", 10400),
        offer("evening-economy", "evening", "ECONOMY", 9100),
    ])


def dublin():
    return search("CDG", "DUB", "2027-02-10", {
        "morning": {"carrier": "EI", "depart": "10:40", "minutes": [90]},
        "noon": {"carrier": "AF", "depart": "12:15", "minutes": [90]},
        "evening": {"carrier": "EI", "depart": "16:55", "minutes": [90]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 11800),
        offer("noon-economy", "noon", "ECONOMY", 13100),
        offer("evening-economy", "evening", "ECONOMY", 12400),
    ])


# ===== easy (6) =====

scenario(
    "alder-quay", "easy", ["multi_traveller"],
    "I'm going to Madrid for the rail interoperability workshop, which opens at 09:30 on 10 December; two colleagues "
    "from my DG are coming too. Please book my flight from Paris on the 9th.",
    trip(traveller_name="Claire Dubois", traveller_title="Policy officer, interoperability unit",
         place_of_employment="Paris", origin="CDG", destination="MAD", travel_date="2026-12-09",
         booking_date="2026-11-25", meeting_start_local="2026-12-10 09:30",
         purpose="Rail interoperability workshop in Madrid", same_dg_participants=3),
    search("CDG", "MAD", "2026-12-09", {
        "morning": {"carrier": "AF", "depart": "08:30", "minutes": [105]},
        "midday": {"carrier": "IB", "depart": "11:15", "minutes": [110]},
        "noon": {"carrier": "AF", "depart": "13:00", "minutes": [105]},
        "afternoon": {"carrier": "AF", "depart": "17:40", "minutes": [105]},
        "evening": {"carrier": "IB", "depart": "19:10", "minutes": [110]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 14800),
        offer("midday-economy", "midday", "ECONOMY", 13200),
        offer("noon-economy", "noon", "ECONOMY", 11900, seats=False),
        offer("afternoon-economy", "afternoon", "ECONOMY", 17100),
        offer("evening-economy", "evening", "ECONOMY", 13900),
    ]),
    expected("BOOK", ["midday-economy"], ["ECONOMY"], ["LOWEST_FARE"], BOOKED, LOW_CLAUSES),
    [TIER_A, SHORT_AIR, RESERVE, PARTICIPANTS],
    "Every flight is direct; economy at the lowest available rate (lines 664, 689-691): Iberia 11:15 at EUR 132. The "
    "cheaper 13:00 fare is sold out. Three staff of the DG attend, which is not more than three (lines 367-368), and "
    "the mission order is signed by the line manager and the authorising officer (lines 326-331, 426-428).",
    distractors=[EARLY_BOOK])

scenario(
    "birch-lantern", "easy", ["outside_air_section"],
    "Please book me Madrid to Frankfurt on 12 January for the programme board the next morning. I'd like Lufthansa so "
    "the miles go on my card. If that isn't allowed, book what the policy allows; I have to be at the board.",
    trip(traveller_name="Javier Morales", traveller_title="Programme manager, research programmes",
         place_of_employment="Madrid", origin="MAD", destination="FRA", travel_date="2027-01-12",
         booking_date="2026-12-01", meeting_start_local="2027-01-13 10:00",
         purpose="Programme board meeting in Frankfurt", chosen_airline="Lufthansa"),
    search("MAD", "FRA", "2027-01-12", {
        "iberia-am": {"carrier": "IB", "depart": "09:40", "minutes": [130]},
        "lufthansa-am": {"carrier": "LH", "depart": "10:20", "minutes": [130]},
        "iberia-pm": {"carrier": "IB", "depart": "16:15", "minutes": [130]},
        "lufthansa-pm": {"carrier": "LH", "depart": "18:05", "minutes": [130]},
    }, [
        offer("iberia-am-economy", "iberia-am", "ECONOMY", 18900),
        offer("lufthansa-am-economy", "lufthansa-am", "ECONOMY", 21400),
        offer("iberia-pm-economy", "iberia-pm", "ECONOMY", 19700),
        offer("lufthansa-pm-economy", "lufthansa-pm", "ECONOMY", 22800),
    ]),
    expected("BOOK", ["iberia-am-economy"], ["ECONOMY"], ["LOWEST_FARE", "LOYALTY_PROGRAM_PREFERENCE"], BOOKED,
             ["BOOKING_METHODS", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [TIER_A, AIRMILES, SHORT_AIR],
    "Economy at the lowest available rate (lines 689-691): Iberia 09:40 at EUR 189. Lufthansa costs EUR 25 more, and "
    "line 407 (Booking methods, outside the air section) forbids any private benefit from airmiles, so the airline "
    "chosen for its miles is not booked. The ground for declining it is the lowest-rate rule itself, so LOWEST_FARE "
    "stands beside LOYALTY_PROGRAM_PREFERENCE.")

scenario(
    "cedar-mosaic", "easy", ["dearer_option"],
    "I'm presenting at the Middle East rail summit in Dubai, which opens the morning after I land. Business class "
    "please, if the guide allows it on this flight; otherwise economy.",
    trip(traveller_name="Lukas Brenner", traveller_title="Head of sector, international relations",
         place_of_employment="Paris", origin="CDG", destination="DXB", travel_date="2027-02-02",
         booking_date="2026-12-15", meeting_start_local="2027-02-03 09:00",
         purpose="Speaking at the Middle East rail summit in Dubai", event_role="SPEAKER", requested_cabin="BUSINESS"),
    search("CDG", "DXB", "2027-02-02", {
        "airfrance": {"carrier": "AF", "depart": "09:45", "minutes": [405]},
        "emirates": {"carrier": "EK", "depart": "11:50", "minutes": [395]},
    }, [
        offer("airfrance-economy", "airfrance", "ECONOMY", 62000),
        offer("airfrance-business", "airfrance", "BUSINESS", 289000),
        offer("emirates-economy", "emirates", "ECONOMY", 58500),
        offer("emirates-business", "emirates", "BUSINESS", 314000),
    ]),
    expected("BOOK", ["airfrance-business"], ["BUSINESS"], LONG_OK, BOOKED, ["TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [TIER_C, PREMIUM_FIRST],
    "Both nonstops fly 395-405 minutes, a segment of at least five hours' continuous flying (lines 707-710), so "
    "business may be booked at the lowest rate: Air France at EUR 2,890. No premium economy is sold on these flights, "
    "so lines 665-666 ('premium economy ... should be envisaged, when available') do not apply.")

scenario(
    "dune-orchard", "easy", ["dearer_option"],
    "Please book me Madrid to New York on 20 January for the transatlantic rail standards meeting, which starts the "
    "next morning. Premium economy if I'm entitled to it; otherwise economy.",
    trip(traveller_name="Ines Carvalho", traveller_title="Standards officer, safety unit",
         place_of_employment="Madrid", origin="MAD", destination="JFK", travel_date="2027-01-20",
         booking_date="2026-12-10", meeting_start_local="2027-01-21 09:00",
         purpose="Transatlantic rail standards meeting in New York", requested_cabin="PREMIUM_ECONOMY"),
    search("MAD", "JFK", "2027-01-20", {
        "iberia": {"carrier": "IB", "depart": "11:30", "minutes": [440]},
        "american": {"carrier": "AA", "depart": "15:00", "minutes": [450]},
    }, [
        offer("iberia-economy", "iberia", "ECONOMY", 54000),
        offer("iberia-premium", "iberia", "PREMIUM_ECONOMY", 109000),
        offer("iberia-business", "iberia", "BUSINESS", 365000),
        offer("american-economy", "american", "ECONOMY", 56500),
        offer("american-premium", "american", "PREMIUM_ECONOMY", 114000),
        offer("american-business", "american", "BUSINESS", 390000),
    ]),
    expected("BOOK", ["iberia-premium"], ["PREMIUM_ECONOMY"], ["PREMIUM_ECONOMY_ALLOWED"], BOOKED, ["TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [TIER_C],
    "Both nonstops fly 440-450 minutes, so premium economy may be booked (lines 707-710): the cheapest premium economy "
    "fare, Iberia at EUR 1,090.")

scenario(
    "elm-sounding", "easy", ["multi_leg", "dearer_option"],
    "Please book my flight from Paris to Copenhagen on 14 January for the Nordic rail freight forum the next morning. "
    "I don't mind which airline.",
    trip(traveller_name="Sophie Lambert", traveller_title="Policy officer, freight unit",
         place_of_employment="Paris", origin="CDG", destination="CPH", travel_date="2027-01-14",
         booking_date="2026-12-02", meeting_start_local="2027-01-15 09:00",
         purpose="Nordic rail freight forum in Copenhagen"),
    search("CDG", "CPH", "2027-01-14", {
        "amsterdam": {"carrier": "KL", "via": ["AMS"], "depart": "09:05", "minutes": [60, 75], "layovers": [70]},
        "direct": {"carrier": "AF", "depart": "10:10", "minutes": [100]},
        "frankfurt": {"carrier": "LH", "via": ["FRA"], "depart": "11:20", "minutes": [60, 80], "layovers": [75]},
    }, [
        offer("amsterdam-economy", "amsterdam", "ECONOMY", 15400),
        offer("direct-economy", "direct", "ECONOMY", 18200),
        offer("frankfurt-economy", "frankfurt", "ECONOMY", 16100),
    ]),
    expected("BOOK", ["direct-economy"], ["ECONOMY"], ["ALTERNATE_ROUTE_WITHIN_MARGIN", "DIRECT_FLIGHT_NORM", "LOWEST_FARE"], BOOKED,
             ["SMART_TRAVELLING", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [DIRECT, SHORT_AIR, TIER_A],
    "Direct flights are the norm (lines 684-687) and are favoured within reasonable cost variations (40%, lines "
    "663-664). The Air France nonstop at EUR 182 is 18% above the KLM connection at EUR 154, so on either reading of "
    "the 40% (all routes, or only up to 550 km with the norm elsewhere) the direct flight is booked.")

scenario(
    "fern-ledger", "easy", ["dearer_option"],
    "The Madrid audit may still be moved: the audited body hasn't confirmed the date. Please book me a ticket to Madrid "
    "on 16 February that I can change.",
    trip(traveller_name="Matthias Huber", traveller_title="Auditor, internal audit",
         place_of_employment="Munich", origin="MUC", destination="MAD", travel_date="2027-02-16",
         booking_date="2027-01-18", meeting_start_local="2027-02-17 09:30",
         purpose="Audit visit in Madrid, date not yet confirmed by the audited body", event_role="AUDITOR",
         wants_refundable=True, risk_of_change=True),
    munich_madrid(),
    expected("BOOK", ["morning-flex"], ["ECONOMY"], ["FLEXIBLE_FARE_JUSTIFIED", "LOWEST_FARE"], BOOKED, LOW_CLAUSES),
    [TIER_B, TIER_A],
    "The record shows the audit may be moved, so (b) applies (lines 704-706): economy at the lowest rate for flexible "
    "tickets. The cheapest changeable fare is Lufthansa 09:00 at EUR 249 (the non-refundable fares are cheaper).",
    twin_of="sorrel-gantry", twin_fact="risk_of_change true or false (the request says the audit may move or not)",
    distractors=[NONREF_RECORD])

# ===== boundary twins (8) =====

DOHA_REQUEST = ("I need to get to Doha for the Gulf railway conference, which opens the morning after I arrive. Business "
                "class if I'm entitled to it on this flight; otherwise economy is fine.")


def doha_trip(name):
    return trip(traveller_name=name, traveller_title="Adviser, international cooperation",
                place_of_employment="Rome", origin="FCO", destination="DOH", travel_date="2027-03-02",
                booking_date="2027-01-25", meeting_start_local="2027-03-03 09:00",
                purpose="Gulf railway conference in Doha", requested_cabin="BUSINESS")


scenario(
    "garnet-reach", "boundary_twin", ["dearer_option"], DOHA_REQUEST, doha_trip("Giulia Ferri"), doha(300),
    expected("BOOK", ["morning-business"], ["BUSINESS"], LONG_OK, BOOKED, ["TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [TIER_C, PREMIUM_FIRST],
    "Each nonstop is scheduled at exactly 300 minutes: 'at least five-hours of continuous flying time' is inclusive "
    "(lines 707-710), so business may be booked at the lowest rate: Qatar 09:05 at EUR 2,240. No premium economy is "
    "sold.",
    twin_of="heron-cobble", twin_fact="scheduled minutes 300 or 295")

scenario(
    "heron-cobble", "boundary_twin", ["upgrade_not_taken"], DOHA_REQUEST, doha_trip("Marco Bellini"), doha(295),
    expected("BOOK", ["afternoon-economy"], ["ECONOMY"], NOT_ELIGIBLE, BOOKED, DECLINED_CLAUSES),
    [TIER_C, TIER_A, SHORT_AIR],
    "Each nonstop is scheduled at 295 minutes, under five hours (lines 707-710), so business is not allowed and economy "
    "is the default (line 664): the lowest fare, Qatar 13:40 at EUR 498.",
    twin_of="garnet-reach", twin_fact="scheduled minutes 300 or 295")

ROME_REQUEST = ("Please book my flight from Paris to Rome on 3 February for the railway agency working party, which starts "
                "the next day at 10:00. The cheapest fare is fine, as long as it doesn't leave or land at an hour the "
                "guide says I can't be made to travel.")


def rome_trip(name):
    return trip(traveller_name=name, traveller_title="Policy officer, safety unit", place_of_employment="Paris",
                origin="CDG", destination="FCO", travel_date="2027-02-03", booking_date="2027-01-11",
                meeting_start_local="2027-02-04 10:00", purpose="Railway agency working party in Rome",
                avoids_unrequired_hours=True)


scenario(
    "iris-pennant", "boundary_twin", ["dearer_option"], ROME_REQUEST, rome_trip("Amelie Rousseau"), rome("07:55"),
    expected("BOOK", ["evening-economy"], ["ECONOMY"], ["EARLY_LATE_HOURS_PROTECTED", "LOWEST_FARE"], BOOKED,
             TIME_CLAUSES),
    [HOURS, TIER_A],
    "The cheapest flight takes off at 07:55, before 8:00, which the traveller cannot be required to do (lines 577-582) "
    "and asks not to; no line manager's reasons are on file. The cheapest flight in hours is Air France 18:20 at "
    "EUR 158.",
    twin_of="jasper-wold", twin_fact="the cheapest flight takes off at 07:55 or 08:00")

scenario(
    "jasper-wold", "boundary_twin", [], ROME_REQUEST, rome_trip("Thomas Girard"), rome("08:00"),
    expected("BOOK", ["first-economy"], ["ECONOMY"], ["EARLY_LATE_HOURS_PROTECTED", "LOWEST_FARE"], BOOKED,
             TIME_CLAUSES),
    [HOURS, TIER_A],
    "The cheapest flight takes off at 08:00, which is not 'before 8:00' (lines 577-582): book it, Air France at EUR 119.",
    twin_of="iris-pennant", twin_fact="the cheapest flight takes off at 07:55 or 08:00")

HOME_REQUEST = ("My last meeting at the Madrid workshop ends at 15:00 on 11 December. Please book my flight back to Paris "
                "that day.")


def home_trip(name):
    return trip(traveller_name=name, traveller_title="Legal officer, legal affairs", place_of_employment="Paris",
                journey="RETURN", origin="MAD", destination="CDG", travel_date="2026-12-11", booking_date="2026-11-26",
                meeting_end_local="2026-12-11 15:00", purpose="Return from the workshop in Madrid")


scenario(
    "kestrel-mallow", "boundary_twin", ["dearer_option", "date_arithmetic"], HOME_REQUEST, home_trip("Elodie Martin"),
    madrid_home("18:35"),
    expected("BOOK", ["mid-economy"], ["ECONOMY"], ["LOWEST_FARE", "RETURN_START_LIMIT"], BOOKED, TIME_CLAUSES),
    [RETURN, TIER_A],
    "The meeting ends at 15:00; a return by air starts not more than three and a half hours later (lines 583-585), so "
    "by 18:30. The cheapest flight leaves at 18:35, 215 minutes after: too late. The cheapest within the limit is "
    "Air France 17:25 at EUR 176.",
    twin_of="linden-ferrule", twin_fact="the cheapest flight leaves at 18:35 or 18:30",
    distractors=[OTHER_MEANS])

scenario(
    "linden-ferrule", "boundary_twin", ["date_arithmetic"], HOME_REQUEST, home_trip("Hugo Lefevre"),
    madrid_home("18:30"),
    expected("BOOK", ["saver-economy"], ["ECONOMY"], ["LOWEST_FARE", "RETURN_START_LIMIT"], BOOKED, TIME_CLAUSES),
    [RETURN, TIER_A],
    "The cheapest flight leaves at 18:30, exactly 210 minutes after the 15:00 end: 'not more than three-and-a-half "
    "hours' is inclusive (lines 583-585). Book Iberia at EUR 128.",
    twin_of="kestrel-mallow", twin_fact="the cheapest flight leaves at 18:35 or 18:30",
    distractors=[OTHER_MEANS])

NAIROBI_REQUEST = ("I'm going to Nairobi for the East African rail corridor review, which starts the day after I land. "
                   "Premium economy if I'm entitled to it; otherwise economy. Connections are fine.")


def nairobi_trip(name):
    return trip(traveller_name=name, traveller_title="Programme officer, international cooperation",
                place_of_employment="Paris", origin="CDG", destination="NBO", travel_date="2027-02-22",
                booking_date="2027-01-20", meeting_start_local="2027-02-23 09:00",
                purpose="East African rail corridor review in Nairobi", requested_cabin="PREMIUM_ECONOMY")


scenario(
    "maple-tern", "boundary_twin", ["multi_leg", "dearer_option"], NAIROBI_REQUEST, nairobi_trip("Nadia Okafor"),
    nairobi(300),
    expected("BOOK", ["first-premium"], ["PREMIUM_ECONOMY"], ["PREMIUM_ECONOMY_ALLOWED"], BOOKED, ["TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [TIER_C],
    "Both itineraries connect in Cairo: Paris-Cairo 260 minutes, Cairo-Nairobi 300 minutes. The journey 'includes at "
    "least one segment involving at least five-hours of continuous flying time' (lines 707-710), so premium economy may "
    "be booked: the cheapest, EgyptAir 08:15 at EUR 1,120.",
    twin_of="nutmeg-spire", twin_fact="the Cairo-Nairobi flight is scheduled at 300 or 290 minutes")

scenario(
    "nutmeg-spire", "boundary_twin", ["multi_leg", "upgrade_not_taken"], NAIROBI_REQUEST, nairobi_trip("Peter Lindqvist"),
    nairobi(290),
    expected("BOOK", ["second-economy"], ["ECONOMY"], NOT_ELIGIBLE, BOOKED, DECLINED_CLAUSES),
    [TIER_C, TIER_A, SHORT_AIR],
    "Paris-Cairo 260 and Cairo-Nairobi 290 minutes: 550 minutes of flying, but no segment reaches five hours of "
    "continuous flying (lines 707-710), and the two flights are not added together. Economy (line 664) at the lowest "
    "rate: EgyptAir 09:05 at EUR 585. No direct flight is offered.",
    twin_of="maple-tern", twin_fact="the Cairo-Nairobi flight is scheduled at 300 or 290 minutes")

# ===== multi_rule (5) =====

scenario(
    "oriel-saffron", "multi_rule", ["dearer_option"],
    "I'm accompanying the Commissioner to the Madrid ministerial meeting on 9 March. Her Cabinet has asked in writing "
    "for me to fly in the same class as her, business, so I can brief her on the way; she flies Iberia that morning. Please book that. If it isn't "
    "allowed, book what the policy allows; I have to be at the meeting.",
    trip(traveller_name="Anna Kowalska", traveller_title="Adviser to the Commissioner's Cabinet",
         place_of_employment="Paris", origin="CDG", destination="MAD", travel_date="2027-03-09",
         booking_date="2027-02-15", meeting_start_local="2027-03-09 16:00",
         purpose="Ministerial meeting in Madrid with the Commissioner", event_role="ADVISER",
         requested_cabin="BUSINESS", accompanies="MEMBER_OF_COMMISSION", accompanied_cabin="BUSINESS",
         sign_offs=[*order(), sign("CABINET", "Head of the Commissioner's Cabinet", "SAME_CLASS_REQUEST",
                                   "Written request: the adviser travels in the Commissioner's class to brief her on the "
                                   "flight; the reasons are set out in the mission order, which the authorising "
                                   "officer has signed")]),
    ministerial(),
    expected("BOOK", ["iberia-business"], ["BUSINESS"], ["SAME_CLASS_AS_MEMBER"],
             ["AUTHORISING_OFFICER", "CABINET", "LINE_MANAGER", "MEMBER_OF_COMMISSION", "NONE"], ["TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [SAME_CLASS, TIER_C, SHORT_AIR],
    "A 105-110 minute flight allows only economy (lines 664, 707-710), but lines 711-714 let staff accompanying a Member "
    "of the Commission travel in the same class, on the written request of the Member or their Cabinet, with the "
    "reasons in the mission order. Both are on file: the cheapest business fare, Iberia at EUR 598.",
    twin_of="zinnia-crest", twin_fact="the person accompanied is a Member of the Commission or a Director-General")

scenario(
    "pewter-vale", "multi_rule", ["dearer_option", "date_arithmetic"],
    "I have to be at the hearing at the French transport ministry in Paris at 09:30 on 26 January. My head of unit has "
    "put on file why I need to fly out early that morning. I'd rather not take a dawn flight, but book what the guide "
    "says.",
    trip(traveller_name="Stefan Bauer", traveller_title="Legal officer, legal affairs", place_of_employment="Munich",
         origin="MUC", destination="CDG", travel_date="2027-01-26", booking_date="2027-01-05",
         meeting_start_local="2027-01-26 09:30", purpose="Hearing at the French transport ministry in Paris",
         avoids_unrequired_hours=True,
         sign_offs=[*order(), sign(LM, "Head of unit", "TRAVEL_HOURS",
                                   "The 09:30 hearing cannot be moved and no flight the evening before suits the "
                                   "team's schedule, so the traveller flies out early that morning")]),
    search("MUC", "CDG", "2027-01-26", {
        "first": {"carrier": "LH", "depart": "06:45", "minutes": [80]},
        "second": {"carrier": "AF", "depart": "07:30", "minutes": [85]},
        "third": {"carrier": "LH", "depart": "09:10", "minutes": [80]},
    }, [
        offer("first-economy", "first", "ECONOMY", 13800),
        offer("second-economy", "second", "ECONOMY", 14900),
        offer("third-economy", "third", "ECONOMY", 12600),
    ]),
    expected("BOOK", ["first-economy"], ["ECONOMY"], ["EARLY_LATE_HOURS_JUSTIFIED"], BOOKED, TIME_CLAUSES),
    [HOURS, TIER_A],
    "The 09:10 flight is cheapest but lands at 10:30, after the 09:30 hearing (lines 689-691: taking into account the "
    "times of meetings). The 06:45 and 07:30 flights take off before 8:00, but the line manager's justifiable reasons "
    "are on file (lines 577-579), so the traveller can be required to take them: the cheaper, Lufthansa 06:45 at "
    "EUR 138. The traveller's wish is declined on the line manager's reasons, so LOWEST_FARE is not the reason.")

scenario(
    "quill-harrow", "multi_rule", ["outside_air_section"],
    "My authorisation to travel for the rail-history conference at Trinity College Dublin is signed, with the transport "
    "paid by the organisation. Please book my flight on 10 February; I speak the next morning.",
    trip(traveller_name="Ciara Walsh", traveller_title="Communication officer, communication unit",
         place_of_employment="Paris", travel_kind="AUTHORISED_TRAVEL", authorisation_pays_transport=True,
         origin="CDG", destination="DUB", travel_date="2027-02-10", booking_date="2027-01-14",
         meeting_start_local="2027-02-11 09:30", purpose="Speaking at a rail-history conference at Trinity College Dublin",
         event_role="SPEAKER",
         sign_offs=[sign(LM, "Head of unit", "AUTHORISATION_TO_TRAVEL", "Authorisation to travel signed, transport paid"),
                    sign(AO, "Authorising officer", "AUTHORISATION_TO_TRAVEL",
                         "Authorisation to travel signed for the budget: the transport")]),
    dublin(),
    expected("BOOK", ["morning-economy"], ["ECONOMY"], ["LOWEST_FARE"], BOOKED,
             ["AUTHORISATION_TO_TRAVEL", "AUTHORISED_TRAVEL_TRANSPORT", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [AUTH_ANALOGY, AUTH_SIGNED, AUTH_FINANCE, TIER_A],
    "Authorised travel follows the mission rules by analogy (lines 1147-1149), and this authorisation is signed with the "
    "transport paid (lines 1199-1203, 1085-1088). Economy at the lowest rate, all flights direct: Aer Lingus 10:40 at "
    "EUR 118.",
    twin_of="basil-ridge", twin_fact="the signed authorisation pays the transport or has no expenses")

scenario(
    "rowan-thatch", "multi_rule", ["dearer_option", "date_arithmetic"],
    "The Brenner corridor meeting in Rome runs until 18:00 on 15 January. Please book me home to Munich that evening; "
    "the cheapest is fine, but not at an hour the guide says I can't be made to travel.",
    trip(traveller_name="Katrin Vogel", traveller_title="Project officer, corridors unit", place_of_employment="Munich",
         journey="RETURN", origin="FCO", destination="MUC", travel_date="2027-01-15", booking_date="2026-12-14",
         meeting_end_local="2027-01-15 18:00", purpose="Return from the Brenner corridor meeting in Rome",
         avoids_unrequired_hours=True),
    search("FCO", "MUC", "2027-01-15", {
        "first": {"carrier": "LH", "depart": "19:10", "minutes": [80]},
        "second": {"carrier": "LH", "depart": "20:05", "minutes": [80]},
        "third": {"carrier": "LH", "depart": "20:50", "minutes": [80]},
        "fourth": {"carrier": "LH", "depart": "21:45", "minutes": [80]},
    }, [
        offer("first-economy", "first", "ECONOMY", 19600),
        offer("second-economy", "second", "ECONOMY", 17100),
        offer("third-economy", "third", "ECONOMY", 13900),
        offer("fourth-economy", "fourth", "ECONOMY", 11800),
    ]),
    expected("BOOK", ["second-economy"], ["ECONOMY"], ["EARLY_LATE_HOURS_PROTECTED", "LOWEST_FARE", "RETURN_START_LIMIT"],
             BOOKED, TIME_CLAUSES),
    [RETURN, HOURS, TIER_A],
    "Two clauses of 2.5.1: the 21:45 flight starts 225 minutes after the meeting, beyond three and a half hours (lines "
    "583-585), and lands at 23:05; the 20:50 flight starts in time but lands at 22:10, after 22:00, which the traveller "
    "cannot be required to do and asks not to (lines 577-582). The cheapest flight left is Lufthansa 20:05 at EUR 171.")

scenario(
    "sorrel-gantry", "multi_rule", [],
    "Please book my flight from Munich to Madrid on 16 February for the audit, which starts the next morning. I'd like a "
    "ticket I can change, just in case. If that isn't allowed, book what the policy allows; I have to be at the audit.",
    trip(traveller_name="Lena Hoffmann", traveller_title="Auditor, internal audit", place_of_employment="Munich",
         origin="MUC", destination="MAD", travel_date="2027-02-16", booking_date="2027-01-18",
         meeting_start_local="2027-02-17 09:30", purpose="Audit visit in Madrid, date confirmed", event_role="AUDITOR",
         wants_refundable=True),
    munich_madrid(),
    expected("BOOK", ["noon-saver"], ["ECONOMY"], ["REFUNDABLE_FARE_NOT_ALLOWED"], BOOKED, LOW_CLAUSES),
    [TIER_A, TIER_B],
    "Flexible tickets are for a mission at risk of being cancelled or amended (lines 704-706); nothing on file says so. "
    "Under (a), lines 689-691, economy including non-refundable tickets at the lowest available rate: Iberia 12:40 at "
    "EUR 159. The changeable fare is declined on (b)'s condition, so the reason is REFUNDABLE_FARE_NOT_ALLOWED.",
    twin_of="fern-ledger", twin_fact="risk_of_change true or false (the request says the audit may move or not)")

# ===== hidden clause (3) =====

scenario(
    "thistle-forge", "hidden_clause", ["multi_traveller", "upgrade_not_taken", "outside_air_section"],
    "Six of us from the interpretation DG are covering the UN meeting in New York, which starts the morning after we "
    "land. Please book my economy seat from Paris on 15 March.",
    trip(traveller_name="Elena Petrova", traveller_title="Conference interpreter, interpretation DG",
         place_of_employment="Paris", origin="CDG", destination="JFK", travel_date="2027-03-15",
         booking_date="2027-02-10", meeting_start_local="2027-03-16 09:00",
         purpose="Interpreting at a UN meeting in New York", event_role="INTERPRETER", same_dg_participants=6),
    search("CDG", "JFK", "2027-03-15", {
        "airfrance": {"carrier": "AF", "depart": "10:30", "minutes": [445]},
        "american": {"carrier": "AA", "depart": "13:15", "minutes": [450]},
    }, [
        offer("airfrance-economy", "airfrance", "ECONOMY", 48800),
        offer("airfrance-premium", "airfrance", "PREMIUM_ECONOMY", 98000),
        offer("airfrance-business", "airfrance", "BUSINESS", 320000),
        offer("american-economy", "american", "ECONOMY", 47100),
        offer("american-premium", "american", "PREMIUM_ECONOMY", 101000),
        offer("american-business", "american", "BUSINESS", 335000),
    ]),
    expected("BOOK", ["american-economy"], ["ECONOMY"], ["LOWEST_FARE"], BOOKED,
             ["SMART_ORGANISATION", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [PARTICIPANTS, INTERPRETERS, TIER_A],
    "Six staff of one DG at one meeting would need a Director-General level authorisation (lines 367-368), but "
    "footnote 25 (lines 399-400) sets that aside where specific rules fix the number of participants, as for "
    "interpreters. The flight would allow premium economy or business (lines 707-710), but the traveller asks for "
    "economy: the lowest fare, American at EUR 471.")

scenario(
    "umber-glade", "hidden_clause", ["outside_air_section"],
    "My mission order for the Madrid workshop on 25 February is signed. Please book my flight from Dublin on the 24th.",
    trip(traveller_name="Sean Murphy", traveller_title="Policy officer, Dublin liaison office",
         place_of_employment="Dublin", origin="DUB", destination="MAD", travel_date="2027-02-24",
         booking_date="2027-02-01", meeting_start_local="2027-02-25 09:00", purpose="Workshop in Madrid",
         line_manager_is_authorising_officer=True,
         sign_offs=[sign(LM, "Head of office", "MISSION_ORDER", "Mission order signed: purpose, dates, place and cost "
                         "estimate")]),
    search("DUB", "MAD", "2027-02-24", {
        "morning": {"carrier": "IB", "depart": "09:15", "minutes": [140]},
        "midday": {"carrier": "EI", "depart": "11:40", "minutes": [140]},
        "afternoon": {"carrier": "IB", "depart": "15:30", "minutes": [140]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 15600),
        offer("midday-economy", "midday", "ECONOMY", 14900),
        offer("afternoon-economy", "afternoon", "ECONOMY", 16200),
    ]),
    expected("BOOK", ["midday-economy"], ["ECONOMY"], ["LOWEST_FARE"], ["AUTHORISING_OFFICER", "LINE_MANAGER", "NONE"],
             ["AUTHORISING_OFFICER_ROLE", "MISSION_DEFINITION", "MISSION_ORDERS", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [ORDER_SIGNERS, LM_IS_AO, RESERVE, TIER_A],
    "Only the line manager has signed, but the record says the line manager is also the person who commits the budget: "
    "the authorising officer for commitments may be the same person as the line manager (lines 328 and footnote 15, "
    "lines 273-275), so the mission order is signed and tickets may be reserved (lines 426-428). The lowest fare: "
    "Aer Lingus 11:40 at EUR 149.")

scenario(
    "vesper-hollow", "hidden_clause", [],
    "Please book my flight from Paris to Amsterdam on 19 January. My mission order explains why I'm flying rather than "
    "taking the train.",
    trip(traveller_name="Julien Moreau", traveller_title="Project officer, digital rail unit", place_of_employment="Paris",
         origin="CDG", destination="AMS", travel_date="2027-01-19", booking_date="2026-12-17",
         meeting_start_local="2027-01-20 09:00", purpose="Meetings with rail operators in the Netherlands",
         rail_km=505, rail_fare_cents=10900, rail_minutes=200,
         air_justification="A particularly heavy schedule: meetings in Amsterdam, Rotterdam and Utrecht on 20 January, "
                           "set out in the signed mission order"),
    amsterdam(),
    expected("BOOK", ["evening-economy"], ["ECONOMY"], ["AIR_TRAVEL_JUSTIFIED", "LOWEST_FARE"], BOOKED,
             ["SMART_TRAVELLING", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [RAIL, SHORT_AIR, JUSTIFY, TIER_A],
    "The rail journey is 505 km and its first-class fare (EUR 109) is 20% above the lowest plane fare, so rail would be "
    "favoured (lines 630-636) and air travel up to 550 km must be appropriately justified (line 663). Footnote 40 (lines "
    "693-694) counts particularly heavy schedules with meetings in several places, which is the justification on file. "
    "The lowest fare: KLM 18:25 at EUR 91.",
    twin_of="aspen-wicket", twin_fact="a justification for flying is on file or not",
    distractors=[FLEX])

# ===== distractor (3) =====

scenario(
    "willow-tamber", "distractor", ["upgrade_not_taken", "date_arithmetic", "month_end", "overnight",
                                    "outside_air_section"],
    "I fly to Singapore on 31 January for the urban rail congress, which opens on 2 February. Economy is fine and so is "
    "the overnight flight; I'll ask for the rest day the guide allows after such a long flight.",
    trip(traveller_name="Mei Lin Tan", traveller_title="Policy officer, urban mobility", place_of_employment="Paris",
         origin="CDG", destination="SIN", travel_date="2027-01-31", booking_date="2026-12-20",
         meeting_start_local="2027-02-02 09:00", purpose="Urban rail congress in Singapore"),
    search("CDG", "SIN", "2027-01-31", {
        "airfrance": {"carrier": "AF", "depart": "11:30", "minutes": [760]},
        "singapore": {"carrier": "SQ", "depart": "12:40", "minutes": [775]},
    }, [
        offer("airfrance-economy", "airfrance", "ECONOMY", 72000),
        offer("airfrance-premium", "airfrance", "PREMIUM_ECONOMY", 164000),
        offer("airfrance-business", "airfrance", "BUSINESS", 490000),
        offer("singapore-economy", "singapore", "ECONOMY", 69500),
        offer("singapore-premium", "singapore", "PREMIUM_ECONOMY", 158000),
        offer("singapore-business", "singapore", "BUSINESS", 520000),
    ]),
    expected("BOOK", ["singapore-economy"], ["ECONOMY"], ["LOWEST_FARE"], BOOKED, LOW_CLAUSES),
    [TIER_A, SHORT_AIR],
    "Business or premium economy would be allowed (a 760-775 minute segment, lines 707-710), but the traveller asks "
    "for economy: the lowest fare, Singapore Airlines 12:40 at EUR 695, landing on 1 February. The rest period after "
    "at least 10 hours of flights (lines 815-818) is for the authorising officer to grant at the destination; it "
    "changes no ticket.",
    distractors=[REST, ALLOWANCE])

scenario(
    "yarrow-brook", "distractor", [],
    "Please book my flight from Rome to Munich on 8 February for the Brenner corridor meeting the next morning. I know "
    "there's a train, but it takes most of the day.",
    trip(traveller_name="Paolo Ricci", traveller_title="Project officer, corridors unit", place_of_employment="Rome",
         origin="FCO", destination="MUC", travel_date="2027-02-08", booking_date="2027-01-15",
         meeting_start_local="2027-02-09 09:00", purpose="Brenner corridor meeting in Munich",
         rail_km=920, rail_fare_cents=21500, rail_minutes=585),
    search("FCO", "MUC", "2027-02-08", {
        "morning": {"carrier": "LH", "depart": "10:15", "minutes": [80]},
        "afternoon": {"carrier": "LH", "depart": "15:40", "minutes": [80]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 12800),
        offer("afternoon-economy", "afternoon", "ECONOMY", 11900),
    ]),
    expected("BOOK", ["afternoon-economy"], ["ECONOMY"], ["LOWEST_FARE"], BOOKED,
             ["SMART_TRAVELLING", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"]),
    [RAIL, TIER_A],
    "The rail journey is 920 km, above 550 km, where rail is only encouraged as an efficient alternative (lines "
    "630-633); its first-class fare (EUR 215) is 81% above the plane fare and it takes 9 hours 45, so neither the 40% "
    "price test nor reasonable time favours it, and no justification is needed. The lowest fare: Lufthansa 15:40 at "
    "EUR 119.",
    distractors=[RAIL_TIME, FLEX])

scenario(
    "zinnia-crest", "distractor", [],
    "I'm accompanying our Director-General to the Madrid ministerial meeting on 9 March. He has asked in writing for me "
    "to fly in the same class as him, business, so I can brief him on the way; he flies Iberia that morning. Please book that. If it isn't allowed, "
    "book what the policy allows; I have to be at the meeting.",
    trip(traveller_name="Daniel Novak", traveller_title="Assistant to the Director-General",
         place_of_employment="Paris", origin="CDG", destination="MAD", travel_date="2027-03-09",
         booking_date="2027-02-15", meeting_start_local="2027-03-09 16:00",
         purpose="Ministerial meeting in Madrid with the Director-General", event_role="ADVISER",
         requested_cabin="BUSINESS", accompanies="DIRECTOR_GENERAL", accompanied_cabin="BUSINESS",
         sign_offs=[*order(), sign("DIRECTOR_GENERAL", "Director-General", "SAME_CLASS_REQUEST",
                                   "Written request: the assistant travels in the Director-General's class to brief him "
                                   "on the flight")]),
    ministerial(),
    expected("BOOK", ["iberia-economy"], ["ECONOMY"], NOT_ELIGIBLE, BOOKED, DECLINED_CLAUSES),
    [SAME_CLASS, TIER_C, TIER_A, SHORT_AIR],
    "The same-class derogation (lines 711-714) is for staff accompanying a Member of the Commission, on the Member's or "
    "Cabinet's written request; a Director-General's request does not qualify, so its giver is not an accepted "
    "approver. A 105-110 minute flight allows only economy (lines 664, 707-710): Iberia at EUR 139.",
    twin_of="oriel-saffron", twin_fact="the person accompanied is a Member of the Commission or a Director-General")

# ===== refusal (3) =====

scenario(
    "aspen-wicket", "refusal", [],
    "Could you book me a flight from Paris to Amsterdam on 19 January for the users' group the next morning? I simply "
    "prefer flying. If the guide says I should take the train, tell me and I'll arrange the train myself.",
    trip(traveller_name="Camille Bernard", traveller_title="Project officer, digital rail unit",
         place_of_employment="Paris", origin="CDG", destination="AMS", travel_date="2027-01-19",
         booking_date="2026-12-17", meeting_start_local="2027-01-20 09:00", purpose="Signalling users' group in Amsterdam",
         rail_km=505, rail_fare_cents=10900, rail_minutes=200),
    amsterdam(),
    expected("REFUSE", [], ["NONE"], ["DISTANCE_BELOW_MINIMUM", "NO_COMPLIANT_OFFER", "RAIL_PREFERRED"], BOOKED,
             ["SMART_TRAVELLING", "TRANSPORT_BETWEEN_PLACES"]),
    [RAIL, SHORT_AIR],
    "The rail journey is 505 km (up to 550 km) and its first-class fare (EUR 109) is 20% above the lowest plane fare "
    "(EUR 91), within 40%, so the greener alternative is favoured (lines 630-636), and air travel up to 550 km 'must be "
    "appropriately justified' (line 663). A preference for flying is no justification: no air ticket is bought.",
    twin_of="vesper-hollow", twin_fact="a justification for flying is on file or not",
    distractors=[FLEX])

scenario(
    "basil-ridge", "refusal", ["personal_travel", "outside_air_section"],
    "My authorisation to travel for the rail-history conference at Trinity College Dublin was signed without expenses: "
    "I'm paying my own way. Could you book my flight on 10 February through the organisation anyway?",
    trip(traveller_name="Aoife Byrne", traveller_title="Communication officer, communication unit",
         place_of_employment="Paris", travel_kind="AUTHORISED_TRAVEL", authorisation_pays_transport=False,
         origin="CDG", destination="DUB", travel_date="2027-02-10", booking_date="2027-01-14",
         meeting_start_local="2027-02-11 09:30", purpose="Speaking at a rail-history conference at Trinity College Dublin",
         event_role="SPEAKER",
         sign_offs=[sign(LM, "Head of unit", "AUTHORISATION_TO_TRAVEL", "Authorisation to travel signed without expenses"),
                    sign(AO, "Authorising officer", "AUTHORISATION_TO_TRAVEL",
                         "Authorisation to travel signed with a cost estimate of zero")]),
    dublin(),
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED", "TRAVEL_COSTS_NOT_COVERED"],
             BOOKED, ["AUTHORISATION_TO_TRAVEL", "AUTHORISED_TRAVEL_EXPENSES", "AUTHORISED_TRAVEL_RULES"]),
    [AUTH_FINANCE, AUTH_SIGNED, AUTH_NONE, AUTH_DEF],
    "Authorised travel may be financed in none, part or full (lines 1085-1088), and the signed authorisation allows "
    "expenses only within its limits (lines 1199-1201). This one was signed without expenses; covering a cost would need "
    "it cancelled and a new one approved (lines 1210-1213), which nobody has asked for. The organisation buys no ticket.",
    twin_of="quill-harrow", twin_fact="the signed authorisation pays the transport or has no expenses")

scenario(
    "cobalt-meadow", "refusal", ["personal_travel", "outside_air_section"],
    "I'm visiting my parents in Rome over Christmas. Could you book my flight on 22 December through the mission system? "
    "I fly so much for work anyway.",
    trip(traveller_name="Lucia Romano", traveller_title="Financial officer, budget unit", place_of_employment="Madrid",
         travel_kind="PRIVATE", origin="MAD", destination="FCO", travel_date="2026-12-22", booking_date="2026-11-30",
         purpose="Family visit in Rome over Christmas", sign_offs=[]),
    search("MAD", "FCO", "2026-12-22", {
        "morning": {"carrier": "IB", "depart": "10:30", "minutes": [125]},
        "evening": {"carrier": "IB", "depart": "17:45", "minutes": [125]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 14200),
        offer("evening-economy", "evening", "ECONOMY", 16900),
    ]),
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             ["MISSION_DEFINITION", "SCOPE"]),
    [MISSION, MISSION_BUDGET, AUTH_DEF],
    "A mission is travel solely in the interests of the service on a line manager's instruction, paid from the mission "
    "budget (lines 174-175, 323-325); authorised travel needs a link to the traveller's work (lines 191-193). A family "
    "visit is neither: the organisation buys no ticket.")

# ===== flag (4) =====

scenario(
    "dahlia-spindle", "flag", ["multi_leg", "unclear_phrase"],
    "Please book my flight from Madrid to Copenhagen on 9 February for the freight corridor meeting the next morning; "
    "I'll go however the guide says.",
    trip(traveller_name="Carmen Ortega", traveller_title="Policy officer, freight unit", place_of_employment="Madrid",
         origin="MAD", destination="CPH", travel_date="2027-02-09", booking_date="2027-01-12",
         meeting_start_local="2027-02-10 09:00", purpose="Freight corridor meeting in Copenhagen"),
    search("MAD", "CPH", "2027-02-09", {
        "amsterdam": {"carrier": "KL", "via": ["AMS"], "depart": "09:15", "minutes": [135, 75], "layovers": [65]},
        "direct": {"carrier": "IB", "depart": "10:20", "minutes": [175]},
        "frankfurt": {"carrier": "LH", "via": ["FRA"], "depart": "11:00", "minutes": [130, 80], "layovers": [70]},
    }, [
        offer("amsterdam-economy", "amsterdam", "ECONOMY", 16400),
        offer("direct-economy", "direct", "ECONOMY", 29800),
        offer("frankfurt-economy", "frankfurt", "ECONOMY", 17100),
    ]),
    expected("FLAG_FOR_APPROVAL", ["amsterdam-economy", "direct-economy"], ["ECONOMY"], UNCLEAR_REASONS, UNCLEAR_ROLES,
             ["SMART_TRAVELLING", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"], phrase="direct flights favoured when available, and within "
             "reasonable cost variations (40%)"),
    [DIRECT, SHORT_AIR, TIER_A],
    "The Iberia nonstop at EUR 298 is 82% above the KLM connection at EUR 164. Lines 684-687 make direct flights the "
    "norm, refusable only by the authorising officer as a manifestly unreasonable expense; lines 663-664 favour direct "
    "flights 'within reasonable cost variations (40%)', in a sentence about air travel up to 550 km. On a 2,058 km "
    "route the text does not say whether the 40% applies, nor what is manifestly unreasonable: hold the connection or "
    "the direct flight.",
    flag_twins=["elm-sounding", "nutmeg-spire"],
    ambiguity={"phrase": "direct flights favoured when available, and within reasonable cost variations (40%)",
               "readings": [("the 40% margin applies to every route: the direct flight is more than 40% dearer, so the "
                            "cheapest connection at the lowest available rate"),
                            ("the 40% sentence is about journeys up to 550 km; elsewhere direct flights are the norm and "
                            "only the authorising officer may refuse one as manifestly unreasonable: the direct flight")]})

scenario(
    "ember-thimble", "flag", ["dearer_option", "unclear_phrase"],
    "Business class please for the Dubai metro signalling review, which starts the morning after I land. If business "
    "isn't allowed on this flight, book what the policy allows.",
    trip(traveller_name="Florian Weber", traveller_title="Head of sector, signalling", place_of_employment="Munich",
         origin="MUC", destination="DXB", travel_date="2027-03-01", booking_date="2027-02-01",
         meeting_start_local="2027-03-02 09:00", purpose="Metro signalling review in Dubai", requested_cabin="BUSINESS"),
    search("MUC", "DXB", "2027-03-01", {
        "lufthansa": {"carrier": "LH", "depart": "10:05", "minutes": [355]},
        "emirates": {"carrier": "EK", "depart": "12:40", "minutes": [350]},
    }, [
        offer("lufthansa-economy", "lufthansa", "ECONOMY", 56000),
        offer("lufthansa-premium", "lufthansa", "PREMIUM_ECONOMY", 124000),
        offer("lufthansa-business", "lufthansa", "BUSINESS", 298000),
        offer("emirates-economy", "emirates", "ECONOMY", 54500),
        offer("emirates-business", "emirates", "BUSINESS", 315000),
    ]),
    expected("FLAG_FOR_APPROVAL", ["lufthansa-business", "lufthansa-premium"], ["BUSINESS", "PREMIUM_ECONOMY"],
             UNCLEAR_REASONS, UNCLEAR_ROLES, ["SMART_TRAVELLING", "TRANSPORT_BETWEEN_PLACES", "TRAVEL_BY_AIR"],
             phrase="This should also be the choice, for example, if the flight is not overnight or when there is no "
             "meeting immediately after arrival"),
    [TIER_C, PREMIUM_FIRST],
    "Both nonstops fly 350-355 minutes, so (c) allows 'premium economy class when suitable, or business class' (lines "
    "707-710). Lines 665-668: premium economy should be envisaged when available, and 'should also be the choice' if the "
    "flight is not overnight or no meeting follows arrival: this daytime flight lands at 19:00 and the review starts the "
    "next morning. Whether that 'should' rules out the business seat (c) allows is open: hold the cheapest premium "
    "economy or business fare.",
    flag_twins=["cedar-mosaic", "dune-orchard"],
    ambiguity={"phrase": "This should also be the choice, for example, if the flight is not overnight or when there is "
                         "no meeting immediately after arrival",
               "readings": [("'should' sets the choice: on a daytime flight with no meeting on arrival, premium economy, "
                            "the Lufthansa premium economy fare"),
                            ("(c) allows business and 'should' only advises: the business seat asked for, the Lufthansa "
                            "business fare")]})

scenario(
    "fennel-quarry", "flag", ["approval_required", "outside_air_section"],
    "My head of unit has signed my mission order for the Paris meeting on 18 February. Please book the cheapest ticket "
    "on the 17th now, before prices go up.",
    trip(traveller_name="Roberto Conti", traveller_title="Policy officer, Rome liaison office", place_of_employment="Rome",
         origin="FCO", destination="CDG", travel_date="2027-02-17", booking_date="2027-01-27",
         meeting_start_local="2027-02-18 09:30", purpose="Meeting with the French rail regulator in Paris",
         sign_offs=[sign(LM, "Head of unit", "MISSION_ORDER", "Mission order signed: purpose, dates and place")]),
    search("FCO", "CDG", "2027-02-17", {
        "morning": {"carrier": "AF", "depart": "09:40", "minutes": [125]},
        "midday": {"carrier": "AF", "depart": "13:15", "minutes": [125]},
        "evening": {"carrier": "AF", "depart": "17:50", "minutes": [125]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 13400),
        offer("midday-economy", "midday", "ECONOMY", 12800),
        offer("evening-economy", "evening", "ECONOMY", 14600),
    ]),
    expected("FLAG_FOR_APPROVAL", ["midday-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED", "MISSION_ORDER_NOT_SIGNED"],
             ["AUTHORISING_OFFICER"], ["AUTHORISING_OFFICER_ROLE", "MISSION_DEFINITION", "MISSION_ORDERS"]),
    [ORDER_SIGNERS, RESERVE, RECOVER, TIER_A],
    "Only the line manager has signed, and the record says the line manager is not the person who commits the budget. "
    "If they are not the same person the mission order must also be signed by the authorising officer for commitments "
    "(lines 328-331), and tickets are reserved only once they have signed (lines 426-428; an unrefundable ticket bought "
    "without that approval may be recovered, lines 432-437). Hold the lowest fare, Air France 13:15 at EUR 128.",
    flag_twins=["umber-glade", "alder-quay"],
    ambiguity="none: the authorising officer's signature is required and missing; the text is clear",
    distractors=[EARLY_BOOK])

scenario(
    "gorse-lattice", "flag", ["approval_required", "multi_traveller", "outside_air_section"],
    "Five of us from the DG are going to the rail safety conference in Rome on 4 March. Please book my seat on the 3rd.",
    trip(traveller_name="Pablo Navarro", traveller_title="Safety officer, safety unit", place_of_employment="Madrid",
         origin="MAD", destination="FCO", travel_date="2027-03-03", booking_date="2027-02-08",
         meeting_start_local="2027-03-04 09:00", purpose="Rail safety conference in Rome", same_dg_participants=5),
    search("MAD", "FCO", "2027-03-03", {
        "morning": {"carrier": "IB", "depart": "08:50", "minutes": [125]},
        "midday": {"carrier": "IB", "depart": "14:20", "minutes": [125]},
        "evening": {"carrier": "IB", "depart": "18:05", "minutes": [125]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 15100),
        offer("midday-economy", "midday", "ECONOMY", 13700),
        offer("evening-economy", "evening", "ECONOMY", 14900),
    ]),
    expected("FLAG_FOR_APPROVAL", ["midday-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED", "PARTICIPANTS_ABOVE_LIMIT"],
             ["DIRECTOR_GENERAL", "HR_CORRESPONDENT", "SENIOR_MANAGEMENT"], ["SMART_ORGANISATION"]),
    [PARTICIPANTS, INTERPRETERS, TIER_A],
    "Five staff of one DG at a single event is more than three, so an authorisation at Director-General level is "
    "required (lines 367-368), which the Director-General may delegate to senior management or the HR Correspondent "
    "(lines 369-371). None is on file, and these are conference participants, not interpreters (footnote 25). Hold the "
    "lowest fare, Iberia 14:20 at EUR 137.",
    flag_twins=["alder-quay", "thistle-forge"],
    ambiguity="none: an authorisation at Director-General level is required and missing; the text is clear")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios to {OUT}")


if __name__ == "__main__":
    main()
