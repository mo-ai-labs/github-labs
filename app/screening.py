"""Screening rules. Every name, country code and threshold here is invented."""

from difflib import SequenceMatcher

from app.models import Decision, RuleHit, TransactionIn, WatchlistEntry
from app.rules import (
    HIGH_RISK_COUNTRIES,
    LARGE_AMOUNT,
    NAME_MATCH_THRESHOLD,
    RISK_SCORE_REVIEW_THRESHOLD,
    ROUND_AMOUNT_STEP,
    RULES,
)
_SCORES = {rule.id: rule.score for rule in RULES}


def _normalise(name: str) -> str:
    return " ".join(name.lower().split())


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalise(a), _normalise(b)).ratio()


def screen(txn: TransactionIn, watchlist: list[WatchlistEntry]) -> tuple[Decision, int, list[RuleHit]]:
    hits: list[RuleHit] = []

    for party in (txn.originator_name, txn.beneficiary_name):
        for entry in watchlist:
            similarity = _similarity(party, entry.name)
            if similarity >= NAME_MATCH_THRESHOLD:
                hits.append(
                    RuleHit(
                        rule_id="WATCHLIST_NAME",
                        detail=f"'{party}' ~ '{entry.name}' ({entry.list_name}, {similarity:.2f})",
                        score=_SCORES["WATCHLIST_NAME"],
                    )
                )

    for country in {txn.originator_country.upper(), txn.beneficiary_country.upper()}:
        if country in HIGH_RISK_COUNTRIES:
            hits.append(
                RuleHit(rule_id="HIGH_RISK_COUNTRY", detail=country, score=_SCORES["HIGH_RISK_COUNTRY"])
            )

    if txn.amount >= LARGE_AMOUNT:
        hits.append(
            RuleHit(rule_id="LARGE_AMOUNT", detail=f"{txn.amount} {txn.currency}", score=_SCORES["LARGE_AMOUNT"])
        )

    if txn.amount >= ROUND_AMOUNT_STEP and txn.amount % ROUND_AMOUNT_STEP == 0:
        hits.append(
            RuleHit(rule_id="ROUND_AMOUNT", detail=f"{txn.amount} {txn.currency}", score=_SCORES["ROUND_AMOUNT"])
        )

    risk_score = min(sum(hit.score for hit in hits), 100)
    decision = Decision.REVIEW if risk_score >= RISK_SCORE_REVIEW_THRESHOLD else Decision.CLEAR
    return decision, risk_score, hits
