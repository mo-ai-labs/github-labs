"""Screening rules. Every name, country code and threshold here is invented."""

from decimal import Decimal

from app.models import Rule

# ISO 3166 user-assigned codes, so they can never collide with a real country.
HIGH_RISK_COUNTRIES = {"XQ", "XR", "ZZ"}
LARGE_AMOUNT = Decimal("7500")
ROUND_AMOUNT_STEP = Decimal("1000")
NAME_MATCH_THRESHOLD = 0.85
RISK_SCORE_REVIEW_THRESHOLD = 50

RULES = [
    Rule(id="WATCHLIST_NAME", description="Party name fuzzy-matches a watchlist entry", score=70),
    Rule(id="HIGH_RISK_COUNTRY", description="Party is in a high-risk (synthetic) jurisdiction", score=40),
    Rule(id="LARGE_AMOUNT", description=f"Amount is at least {LARGE_AMOUNT}", score=20),
    Rule(id="ROUND_AMOUNT", description=f"Amount is an exact multiple of {ROUND_AMOUNT_STEP}", score=10),
]
