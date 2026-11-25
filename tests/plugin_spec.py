"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "eu-rail-missions" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 32-scenario row).
MIX = {"easy": 6, "boundary_twin": 8, "multi_rule": 5, "hidden_clause": 3, "distractor": 3, "refusal": 3, "flag": 4}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has. It has no rule on overnight stops
# within a journey (the rest period of lines 815-820 is time at the destination, not a stop), so no overnight-stop
# case is required; one overnight flight is tagged anyway.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1, "multi_traveller": 1,
    "dearer_option": 2, "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "rail", "train", "direct", "nonstop", "connection", "segment", "mission", "order", "authorised", "authorising",
    "officer", "manager", "director", "general", "cabinet", "commissioner", "member", "interpreter", "participants",
    "staff", "refundable", "flexible", "changeable", "miles", "airmiles", "early", "late", "dawn", "night", "return",
    "meeting", "leave", "private", "personal", "family", "justified", "justification", "premium", "business",
    "economy", "class", "rest", "delegate", "agency", "norm", "lowest", "rate", "risk",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.TravelKind, contract.Journey, contract.EventRole, contract.Accompanied,
                     contract.SignOffSubject]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section).
MAX_PASS_ALWAYS_FLAG = 2
MAX_PASS_ALWAYS_LOWEST = 10

# Hand-built duration cases beyond the automatic both-sides tests: (rule, outbound scheduled minutes per
# flight, layovers, expected True / False / None for unclear).
DURATION_CASES = [
    ("long-segment", [300], [], True),  # inclusive: "at least five-hours"
    ("long-segment", [295], [], False),
    ("long-segment", [260, 300], [95], True),  # one qualifying segment qualifies the journey
    ("long-segment", [260, 290], [95], False),  # 550 minutes of flying, but no segment of five hours
    ("long-segment", [250, 250, 250], [60, 60], False),  # never added together
    ("rest-period", [600], [], True),  # inclusive: "at least 10 hours", the flights added together
    ("rest-period", [599], [], False),
    ("rest-period", [300, 300], [120], True),  # ground time left out, flights added
    ("rest-period", [300, 290], [400], False),
]
