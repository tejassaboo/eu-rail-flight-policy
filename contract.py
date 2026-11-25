"""Each tool's and task's typed input and output (see nanoagent.plugin.v0001.contract): declarations only.

The first part is the original-handbook template's shared contract and is the same in every plugin made from
it. The HANDBOOK-SPECIFIC part in the middle is filled per handbook: the scenario ids, the closed lists of
approvers and sections, and the trip record; the shared inputs and outputs after it refer to those names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output

# ---------------------------------------------------------------------------------------------------------
# SHARED (template): keep identical across plugins, except the agent task's id in Task.BOOK_FLIGHT.
# ---------------------------------------------------------------------------------------------------------


class Tool(Enum):
    BOOKING_REQUIREMENTS = "booking_requirements"
    GET_TRIP = "get_trip"
    SEARCH_FLIGHTS = "search_flights"
    SOLVE_BOOKING = "solve_booking"


class Task(Enum):
    BOOKING_REQUIREMENTS = "booking-requirements"
    SEARCH_FLIGHTS = "search-flights"
    BOOK_FLIGHT = "book-eu-rail-flight"


class Decision(Enum):
    BOOK = "BOOK"
    REFUSE = "REFUSE"
    FLAG_FOR_APPROVAL = "FLAG_FOR_APPROVAL"


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"
    NONE = "NONE"


class ReasonCode(Enum):
    """Why the decision was made. The list is shared by every handbook plugin, so it also holds reasons
    that a given handbook never uses."""

    LOWEST_FARE = "LOWEST_FARE"
    UPGRADE_NOT_ELIGIBLE = "UPGRADE_NOT_ELIGIBLE"
    CLIENT_REIMBURSABLE = "CLIENT_REIMBURSABLE"
    UPGRADE_WITHIN_FARE_MARGIN = "UPGRADE_WITHIN_FARE_MARGIN"
    MEDICAL_NEED = "MEDICAL_NEED"
    COST_SAVINGS = "COST_SAVINGS"
    NO_ECONOMY_SEATS_URGENT = "NO_ECONOMY_SEATS_URGENT"
    TRAVELER_PAYS_UPGRADE = "TRAVELER_PAYS_UPGRADE"
    LONG_FLIGHT_APPROVED = "LONG_FLIGHT_APPROVED"
    LONG_FLIGHT_CONDITION_NOT_MET = "LONG_FLIGHT_CONDITION_NOT_MET"
    PREMIUM_ECONOMY_ALLOWED = "PREMIUM_ECONOMY_ALLOWED"
    UPGRADE_COST_NOT_NOMINAL = "UPGRADE_COST_NOT_NOMINAL"
    ALTERNATE_ROUTE_WITHIN_MARGIN = "ALTERNATE_ROUTE_WITHIN_MARGIN"
    ALTERNATE_ROUTE_TOO_EXPENSIVE = "ALTERNATE_ROUTE_TOO_EXPENSIVE"
    LOYALTY_PROGRAM_PREFERENCE = "LOYALTY_PROGRAM_PREFERENCE"
    COMPANION_NOT_COVERED = "COMPANION_NOT_COVERED"
    PERSONAL_TRAVEL_NOT_COVERED = "PERSONAL_TRAVEL_NOT_COVERED"
    OUTSIDE_POLICY_SCOPE = "OUTSIDE_POLICY_SCOPE"
    NO_COMPLIANT_OFFER = "NO_COMPLIANT_OFFER"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNCLEAR_POLICY_TEXT = "UNCLEAR_POLICY_TEXT"
    ADVANCE_PURCHASE_TOO_LATE = "ADVANCE_PURCHASE_TOO_LATE"
    DISTANCE_BELOW_MINIMUM = "DISTANCE_BELOW_MINIMUM"
    DRIVING_EXPECTED = "DRIVING_EXPECTED"
    RAIL_PREFERRED = "RAIL_PREFERRED"
    REFUNDABLE_FARE_NOT_ALLOWED = "REFUNDABLE_FARE_NOT_ALLOWED"
    PREFERRED_CARRIER_REQUIRED = "PREFERRED_CARRIER_REQUIRED"
    CONNECTION_TOO_LONG = "CONNECTION_TOO_LONG"
    OVERNIGHT_STOP_REQUIRED = "OVERNIGHT_STOP_REQUIRED"
    NATIONAL_CARRIER_REQUIRED = "NATIONAL_CARRIER_REQUIRED"
    SENIOR_ROLE_ENTITLEMENT = "SENIOR_ROLE_ENTITLEMENT"
    INTERNATIONAL_LONG_FLIGHT = "INTERNATIONAL_LONG_FLIGHT"
    TRAVELLER_LIMIT_PER_FLIGHT = "TRAVELLER_LIMIT_PER_FLIGHT"
    # HANDBOOK-SPECIFIC reason codes go below this line; keep every shared one above.
    DIRECT_FLIGHT_NORM = "DIRECT_FLIGHT_NORM"
    FLEXIBLE_FARE_JUSTIFIED = "FLEXIBLE_FARE_JUSTIFIED"
    SAME_CLASS_AS_MEMBER = "SAME_CLASS_AS_MEMBER"
    AIR_TRAVEL_JUSTIFIED = "AIR_TRAVEL_JUSTIFIED"
    EARLY_LATE_HOURS_PROTECTED = "EARLY_LATE_HOURS_PROTECTED"
    EARLY_LATE_HOURS_JUSTIFIED = "EARLY_LATE_HOURS_JUSTIFIED"
    RETURN_START_LIMIT = "RETURN_START_LIMIT"
    TRAVEL_COSTS_NOT_COVERED = "TRAVEL_COSTS_NOT_COVERED"
    MISSION_ORDER_NOT_SIGNED = "MISSION_ORDER_NOT_SIGNED"
    PARTICIPANTS_ABOVE_LIMIT = "PARTICIPANTS_ABOVE_LIMIT"
    # Decoys: codes for rules of other handbooks that this one lacks, so the list hints at none of its own rules.
    WEEKEND_TRAVEL_HOME = "WEEKEND_TRAVEL_HOME"
    WEEKEND_TRIP_NOT_EARNED = "WEEKEND_TRIP_NOT_EARNED"
    NEXT_OF_KIN_TRAVEL = "NEXT_OF_KIN_TRAVEL"
    FLY_AMERICA_US_CARRIER_REQUIRED = "FLY_AMERICA_US_CARRIER_REQUIRED"
    OPEN_SKIES_AGREEMENT = "OPEN_SKIES_AGREEMENT"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    CHANCELLOR_WRITTEN_AUTHORIZATION = "CHANCELLOR_WRITTEN_AUTHORIZATION"
    DOUBLE_BOOKING_PROHIBITED = "DOUBLE_BOOKING_PROHIBITED"
    PRIVATE_AIRCRAFT_NOT_APPROVED = "PRIVATE_AIRCRAFT_NOT_APPROVED"
    CANDIDATE_TRIP_NOT_COVERED = "CANDIDATE_TRIP_NOT_COVERED"
    TRAVEL_PACKAGE_NOT_ITEMIZED = "TRAVEL_PACKAGE_NOT_ITEMIZED"


class TripType(Enum):
    ONE_WAY = "ONE_WAY"
    ROUND_TRIP = "ROUND_TRIP"


class Topic(Enum):
    ALL = "ALL"
    FIELDS = "FIELDS"
    AIRPORTS = "AIRPORTS"


CODE = "An IATA airport code, e.g. JFK"


@dataclass
class Airport(Output):
    code: Annotated[str, CODE]
    name: Annotated[str, "The airport's name"]
    city: Annotated[str, "The city it serves"]
    country: Annotated[str, "Its country, as an ISO code"]


@dataclass
class Segment(Output):
    flight_number: Annotated[str, "The airline's flight number, e.g. BA 117"]
    origin: Annotated[str, CODE]
    destination: Annotated[str, CODE]
    depart_local: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, local time at that airport"]
    arrive_local: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, local time at that airport"]
    depart_utc: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, UTC"]
    arrive_utc: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, UTC"]
    scheduled_minutes: Annotated[int, "Its scheduled time from departure to arrival, in minutes"]


@dataclass
class Offer(Output):
    offer_id: Annotated[str, "The offer's id, to submit when booking or holding it"]
    carrier: Annotated[str, "The airline"]
    trip_type: Annotated[TripType, "ONE_WAY, or ROUND_TRIP when the fare covers the flights out and back"]
    cabin: Annotated[Cabin, "The cabin sold on every flight of the offer"]
    fare_cents: Annotated[int, "The whole fare for one passenger, in cents of the search's currency"]
    seats_available: Annotated[bool, "False when this cabin is sold out on these flights: it is listed but cannot be bought"]
    refundable: Annotated[bool, "Whether the fare can be refunded or changed without a fee"]
    stops: Annotated[int, "Connections on the way out; zero for a nonstop"]
    segments: Annotated[list[Segment], "The flights out, in order"]
    layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights out"]
    stopover_nights: Annotated[list[bool], "Per connection out: true when it is a ticketed stopover with a hotel night booked"]
    flying_minutes: Annotated[int, "The flights' scheduled minutes out added together, ground time left out"]
    elapsed_minutes: Annotated[int, "Minutes from the first departure out to the last arrival, ground time included"]
    return_segments: Annotated[list[Segment], "For a round trip, the flights back, in order; empty otherwise"]
    return_layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights back"]
    return_stopover_nights: Annotated[list[bool], "Per connection back: true for a ticketed stopover with a hotel night"]
    return_flying_minutes: Annotated[int, "The flights' scheduled minutes back added together; zero one way"]
    return_elapsed_minutes: Annotated[int, "Minutes from the first departure back to the last arrival; zero one way"]


# ---------------------------------------------------------------------------------------------------------
# HANDBOOK-SPECIFIC: Europe's Rail Joint Undertaking, Governing Board Decision 11/2025 applying the Commission's
# Guide to Missions and Authorised Travel, C(2025) 2495.
# ---------------------------------------------------------------------------------------------------------


class Scenario(Enum):
    ALDER_QUAY = "alder-quay"
    ASPEN_WICKET = "aspen-wicket"
    BASIL_RIDGE = "basil-ridge"
    BIRCH_LANTERN = "birch-lantern"
    CEDAR_MOSAIC = "cedar-mosaic"
    COBALT_MEADOW = "cobalt-meadow"
    DAHLIA_SPINDLE = "dahlia-spindle"
    DUNE_ORCHARD = "dune-orchard"
    ELM_SOUNDING = "elm-sounding"
    EMBER_THIMBLE = "ember-thimble"
    FENNEL_QUARRY = "fennel-quarry"
    FERN_LEDGER = "fern-ledger"
    GARNET_REACH = "garnet-reach"
    GORSE_LATTICE = "gorse-lattice"
    HERON_COBBLE = "heron-cobble"
    IRIS_PENNANT = "iris-pennant"
    JASPER_WOLD = "jasper-wold"
    KESTREL_MALLOW = "kestrel-mallow"
    LINDEN_FERRULE = "linden-ferrule"
    MAPLE_TERN = "maple-tern"
    NUTMEG_SPIRE = "nutmeg-spire"
    ORIEL_SAFFRON = "oriel-saffron"
    PEWTER_VALE = "pewter-vale"
    QUILL_HARROW = "quill-harrow"
    ROWAN_THATCH = "rowan-thatch"
    SORREL_GANTRY = "sorrel-gantry"
    THISTLE_FORGE = "thistle-forge"
    UMBER_GLADE = "umber-glade"
    VESPER_HOLLOW = "vesper-hollow"
    WILLOW_TAMBER = "willow-tamber"
    YARROW_BROOK = "yarrow-brook"
    ZINNIA_CREST = "zinnia-crest"


class Approver(Enum):
    """Roles that may sign off. NONE: the decision relies on no one's sign-off, given or awaited (one for
    something else may be on file). NOT_NAMED: one is needed, but the handbook names no role."""

    NONE = "NONE"
    NOT_NAMED = "NOT_NAMED"
    LINE_MANAGER = "LINE_MANAGER"
    AUTHORISING_OFFICER = "AUTHORISING_OFFICER"
    DIRECTOR_GENERAL = "DIRECTOR_GENERAL"
    SENIOR_MANAGEMENT = "SENIOR_MANAGEMENT"
    HR_CORRESPONDENT = "HR_CORRESPONDENT"
    MEMBER_OF_COMMISSION = "MEMBER_OF_COMMISSION"
    CABINET = "CABINET"
    HEAD_OF_CABINET = "HEAD_OF_CABINET"
    PMO = "PMO"
    DG_HR = "DG_HR"
    CHIEF_FINANCIAL_OFFICER = "CHIEF_FINANCIAL_OFFICER"
    CHIEF_EXECUTIVE = "CHIEF_EXECUTIVE"
    VICE_PRESIDENT = "VICE_PRESIDENT"


class Clause(Enum):
    """The handbook's sections, by heading."""

    SCOPE = "SCOPE"
    PRINCIPLES_AND_ROLES = "PRINCIPLES_AND_ROLES"
    LINE_MANAGER_ROLE = "LINE_MANAGER_ROLE"
    AUTHORISING_OFFICER_ROLE = "AUTHORISING_OFFICER_ROLE"
    MISSION_DEFINITION = "MISSION_DEFINITION"
    SMART_ORGANISATION = "SMART_ORGANISATION"
    ORGANISATION_OF_MISSIONS = "ORGANISATION_OF_MISSIONS"
    BOOKING_METHODS = "BOOKING_METHODS"
    MISSION_ORDERS = "MISSION_ORDERS"
    PERSONAL_CHANGES = "PERSONAL_CHANGES"
    RECALL_FROM_LEAVE = "RECALL_FROM_LEAVE"
    CANCELLATION = "CANCELLATION"
    DEPARTURE_RETURN = "DEPARTURE_RETURN"
    TRANSPORT_BETWEEN_PLACES = "TRANSPORT_BETWEEN_PLACES"
    SMART_TRAVELLING = "SMART_TRAVELLING"
    TRAVEL_BY_RAIL = "TRAVEL_BY_RAIL"
    TRAVEL_BY_AIR = "TRAVEL_BY_AIR"
    AIR_PASSENGER_RIGHTS = "AIR_PASSENGER_RIGHTS"
    ACCOMMODATION = "ACCOMMODATION"
    MISSION_DURATION = "MISSION_DURATION"
    DAILY_ALLOWANCE = "DAILY_ALLOWANCE"
    LONG_STAY = "LONG_STAY"
    THIRD_PARTY_EXPENSES = "THIRD_PARTY_EXPENSES"
    SECONDED_EXPERTS = "SECONDED_EXPERTS"
    STATEMENT_OF_EXPENSES = "STATEMENT_OF_EXPENSES"
    AUTHORISED_TRAVEL = "AUTHORISED_TRAVEL"
    AUTHORISED_TRAVEL_RULES = "AUTHORISED_TRAVEL_RULES"
    AUTHORISED_TRAVEL_TRANSPORT = "AUTHORISED_TRAVEL_TRANSPORT"
    AUTHORISATION_TO_TRAVEL = "AUTHORISATION_TO_TRAVEL"
    AUTHORISED_TRAVEL_EXPENSES = "AUTHORISED_TRAVEL_EXPENSES"
    GENERAL_PROVISIONS = "GENERAL_PROVISIONS"
    SAFETY_AND_SECURITY = "SAFETY_AND_SECURITY"


class TravelKind(Enum):
    MISSION = "MISSION"
    AUTHORISED_TRAVEL = "AUTHORISED_TRAVEL"
    PRIVATE = "PRIVATE"


class Journey(Enum):
    OUTWARD = "OUTWARD"
    RETURN = "RETURN"


class EventRole(Enum):
    PARTICIPANT = "PARTICIPANT"
    SPEAKER = "SPEAKER"
    INTERPRETER = "INTERPRETER"
    AUDITOR = "AUDITOR"
    ADVISER = "ADVISER"


class Accompanied(Enum):
    NOBODY = "NOBODY"
    MEMBER_OF_COMMISSION = "MEMBER_OF_COMMISSION"
    DIRECTOR_GENERAL = "DIRECTOR_GENERAL"


class SignOffSubject(Enum):
    MISSION_ORDER = "MISSION_ORDER"
    AUTHORISATION_TO_TRAVEL = "AUTHORISATION_TO_TRAVEL"
    SAME_CLASS_REQUEST = "SAME_CLASS_REQUEST"
    PARTICIPATION = "PARTICIPATION"
    TRAVEL_HOURS = "TRAVEL_HOURS"


@dataclass
class SignOff(Output):
    role: Annotated[Approver, "The signer's role"]
    name: Annotated[str, "Their name"]
    subject: Annotated[
        SignOffSubject,
        "What the sign-off covers: the trip's mission order (its purpose, dates and place; the ticket is chosen "
        "when booking), the travel authorisation of AUTHORISED_TRAVEL, a written request about the class of "
        "travel, an approval for this many staff to take part, or the reasons the traveller must fly at a given hour",
    ]
    note: Annotated[str, "What the sign-off says, in brief"]


@dataclass
class Trip(Output):
    traveller_name: Annotated[str, "Who flies"]
    traveller_title: Annotated[str, "Their job title and service"]
    place_of_employment: Annotated[str, "The city where the traveller works, which their trips start from and end at"]
    travel_kind: Annotated[
        TravelKind,
        "MISSION: work travel the traveller's head of unit sent them on; AUTHORISED_TRAVEL: an outside event the "
        "traveller asked to attend, linked to their work; PRIVATE: a trip of their own",
    ]
    authorisation_pays_transport: Annotated[
        bool, "For AUTHORISED_TRAVEL, whether the signed authorisation has the organisation pay the transport; false otherwise"
    ]
    journey: Annotated[Journey, "OUTWARD: to where the work or event is; RETURN: back to the traveller's own city"]
    origin: Annotated[Airport, "Where the flight leaves from"]
    destination: Annotated[Airport, "Where it goes"]
    travel_date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport"]
    booking_date: Annotated[str, "Today in this world, the day the ticket is bought, YYYY-MM-DD"]
    meeting_start_local: Annotated[
        str, "For an OUTWARD flight, when the first meeting or session starts, YYYY-MM-DD HH:MM local at the destination; empty otherwise"
    ]
    meeting_end_local: Annotated[
        str, "For a RETURN flight, when the last meeting ends, YYYY-MM-DD HH:MM local at the origin; empty otherwise"
    ]
    purpose: Annotated[str, "Why the trip is made, in plain words"]
    event_role: Annotated[EventRole, "What the traveller does at the meeting or event"]
    same_dg_participants: Annotated[
        int, "How many staff of the traveller's Directorate-General take part in this meeting or event in person, the traveller included"
    ]
    requested_cabin: Annotated[Cabin, "The cabin the traveller asks for"]
    wants_refundable: Annotated[bool, "Whether the traveller asks for a fare that can be refunded or changed without a fee"]
    risk_of_change: Annotated[bool, "Whether the trip is known to be at risk of being called off or moved"]
    chosen_airline: Annotated[str, "The airline the traveller asks to fly, as search_flights names airlines; empty when none"]
    avoids_unrequired_hours: Annotated[
        bool, "Whether the traveller asks not to be booked at hours they cannot be made to travel at; false when any time suits"
    ]
    accompanies: Annotated[Accompanied, "The senior person the traveller goes with on this trip, if any"]
    accompanied_cabin: Annotated[Cabin, "The cabin that person flies in; NONE when the traveller goes with nobody"]
    rail_km: Annotated[int, "The rail alternative on file for this journey: its distance in km; zero when none is on file"]
    rail_fare_cents: Annotated[int, "That rail journey's first-class fare, in euro cents; zero when none"]
    rail_minutes: Annotated[int, "That rail journey's time from station to station, in minutes; zero when none"]
    air_justification: Annotated[str, "The reason given on file for flying rather than taking the train; empty when none"]
    line_manager_is_authorising_officer: Annotated[
        bool, "Whether the traveller's line manager is also the person who commits the budget for this trip"
    ]
    sign_offs: Annotated[list[SignOff], "Sign-offs already on file for this trip, each given before today"]


# ---------------------------------------------------------------------------------------------------------
# SHARED (template), continued: the tools' and tasks' inputs and outputs.
# ---------------------------------------------------------------------------------------------------------


@dataclass
class TaskInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    request: Annotated[str, "The traveller's request, in their own words"]


@dataclass
class TripInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id, as the task input gives it"]


@dataclass
class TripOutput(Output):
    scenario: Annotated[Scenario, "The case id"]
    request: Annotated[str, "The traveller's request, in their own words"]
    trip: Annotated[Trip, "The trip record behind the request"]


@dataclass
class SearchInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    origin: Annotated[str, "The airport to leave from: An IATA airport code, e.g. JFK"]
    destination: Annotated[str, "The airport to fly to: An IATA airport code, e.g. JFK"]
    date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport, on or after the booking date"]
    return_date: Annotated[str, "For round-trip fares, the day to fly back, YYYY-MM-DD, local at the destination; empty for one way"]


@dataclass
class SearchOutput(Output):
    note: Annotated[str, "Where the offers come from, and a word when this case lists none for the search"]
    currency: Annotated[str, "The currency of every fare, as an ISO code"]
    offers: Annotated[list[Offer], "Every offer leaving on that local date, in departure order"]


@dataclass
class BookingOutput(Output):
    decision: Annotated[
        Decision,
        "BOOK: buy offer_id now. REFUSE: buy nothing, because the organisation buys no ticket at all for this request. "
        "FLAG_FOR_APPROVAL: hold offer_id and buy nothing yet, because someone must approve it first or "
        "the handbook's words leave the answer open",
    ]
    offer_id: Annotated[str, "The offer bought or held, exactly as search_flights listed it; empty when refusing"]
    cabin: Annotated[Cabin, "That offer's cabin; NONE when refusing"]
    reason_code: Annotated[ReasonCode, "Why, from the closed list"]
    approver: Annotated[
        Approver,
        "The role whose sign-off this decision relies on, whether already on file or still awaited; NONE when "
        "this decision relies on no one's sign-off, even if a sign-off for something else is on file; NOT_NAMED "
        "when a sign-off is needed but the handbook names no role",
    ]
    clause: Annotated[Clause, "The handbook section the decision rests on"]


@dataclass
class SolveOutput(Output):
    trip: Annotated[Trip, "The trip record"]
    offers: Annotated[list[Offer], "Every offer on the trip's route and date"]
    decision: Annotated[Decision, "The correct decision"]
    offer_ids: Annotated[list[str], "Every offer id that is a correct choice; empty when refusing"]
    cabins: Annotated[list[Cabin], "Every correct cabin"]
    reason_codes: Annotated[list[ReasonCode], "Every accepted reason"]
    approvers: Annotated[list[Approver], "Every accepted approver"]
    clauses: Annotated[list[Clause], "Every accepted section"]
    unclear_phrase: Annotated[str, "For a hold over unclear words, those words; empty otherwise"]
    explanation: Annotated[str, "How the answer key reached the answer"]


@dataclass
class FieldHelp(Output):
    name: Annotated[str, "The trip record field's name"]
    kind: Annotated[str, "Its type"]
    description: Annotated[str, "What it means"]


@dataclass
class RequirementsInput(Output):
    topic: Annotated[Topic, "ALL for everything, FIELDS for the trip record's fields, AIRPORTS for the airport list"]


@dataclass
class RequirementsOutput(Output):
    fields: Annotated[list[FieldHelp], "The trip record's fields; empty for AIRPORTS"]
    conventions: Annotated[list[str], "How times, dates, fares and seats work in this world; empty for AIRPORTS"]
    airports: Annotated[list[Airport], "The airports the simulated world knows; empty for FIELDS"]


TOOLS = {
    Tool.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Tool.GET_TRIP: (TripInput, TripOutput),
    Tool.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Tool.SOLVE_BOOKING: (TaskInput, SolveOutput),
}
TASKS = {
    Task.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Task.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Task.BOOK_FLIGHT: (TaskInput, BookingOutput),
}
