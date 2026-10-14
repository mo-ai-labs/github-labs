from decimal import Decimal

from app.models import Decision, TransactionIn
from app.rules import (
    HIGH_RISK_COUNTRIES,
    LARGE_AMOUNT,
    NAME_MATCH_THRESHOLD,
    RISK_SCORE_REVIEW_THRESHOLD,
    ROUND_AMOUNT_STEP,
    RULES,
)
from app.screening import screen
from app.store import Store
from tests.conftest import make_txn


def run(**overrides):
    return screen(TransactionIn(**make_txn(**overrides)), list(Store().watchlist.values()))


def rule_ids(hits):
    return sorted(hit.rule_id for hit in hits)


def test_rules_constants_unchanged():
    assert HIGH_RISK_COUNTRIES == {"XQ", "XR", "ZZ"}
    assert LARGE_AMOUNT == Decimal("7500")
    assert ROUND_AMOUNT_STEP == Decimal("1000")
    assert NAME_MATCH_THRESHOLD == 0.85
    assert RISK_SCORE_REVIEW_THRESHOLD == 50
    assert [(rule.id, rule.description, rule.score) for rule in RULES] == [
        ("WATCHLIST_NAME", "Party name fuzzy-matches a watchlist entry", 70),
        ("HIGH_RISK_COUNTRY", "Party is in a high-risk (synthetic) jurisdiction", 40),
        ("LARGE_AMOUNT", f"Amount is at least {LARGE_AMOUNT}", 20),
        ("ROUND_AMOUNT", f"Amount is an exact multiple of {ROUND_AMOUNT_STEP}", 10),
    ]


def test_clean_transaction_is_cleared():
    decision, score, hits = run()
    assert decision is Decision.CLEAR
    assert score == 0
    assert hits == []


def test_watchlist_name_fuzzy_match_triggers_review():
    decision, score, hits = run(originator_name="ivan  PLACEHOLDR")
    assert decision is Decision.REVIEW
    assert score == 70
    assert rule_ids(hits) == ["WATCHLIST_NAME"]


def test_dissimilar_name_does_not_match():
    _, _, hits = run(beneficiary_name="Ivy Holder")
    assert hits == []


def test_high_risk_country_alone_is_below_threshold():
    decision, score, hits = run(beneficiary_country="ZZ")
    assert decision is Decision.CLEAR
    assert score == 40
    assert rule_ids(hits) == ["HIGH_RISK_COUNTRY"]


def test_same_high_risk_country_on_both_sides_counts_once():
    _, score, _ = run(originator_country="XQ", beneficiary_country="XQ")
    assert score == 40


def test_amount_below_large_amount_does_not_trigger_large_amount():
    _, _, hits = run(amount=Decimal("7499.99"))
    assert "LARGE_AMOUNT" not in rule_ids(hits)


def test_amount_at_large_amount_triggers_large_amount():
    _, _, hits = run(amount=Decimal("7500.00"))
    assert rule_ids(hits) == ["LARGE_AMOUNT"]


def test_round_amount_triggers_round_amount():
    _, _, hits = run(amount=Decimal("1000"))
    assert rule_ids(hits) == ["ROUND_AMOUNT"]


def test_amount_below_round_amount_does_not_trigger_round_amount():
    _, _, hits = run(amount=Decimal("999.99"))
    assert rule_ids(hits) == []


def test_large_amount_plus_high_risk_country_triggers_review():
    decision, score, hits = run(amount=Decimal("7600.10"), beneficiary_country="XR")
    assert decision is Decision.REVIEW
    assert score == 60
    assert rule_ids(hits) == ["HIGH_RISK_COUNTRY", "LARGE_AMOUNT"]


def test_round_large_amount_stays_clear():
    decision, score, hits = run(amount=Decimal("8000"))
    assert decision is Decision.CLEAR
    assert score == 30
    assert rule_ids(hits) == ["LARGE_AMOUNT", "ROUND_AMOUNT"]


def test_score_is_capped_at_100():
    _, score, _ = run(
        amount=Decimal("9000"),
        beneficiary_name="Globex Front LLC",
        beneficiary_country="XQ",
    )
    assert score == 100
