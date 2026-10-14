from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models import (
    Alert,
    AlertEventType,
    AlertHistoryEvent,
    AlertStatus,
    BulkTransactionIn,
    Decision,
    ScreeningResult,
    TransactionIn,
)
from app.screening import screen
from app.store import Store, get_store, new_id

router = APIRouter(prefix="/transactions", tags=["transactions"])
StoreDep = Annotated[Store, Depends(get_store)]


@router.post("/screen", response_model=ScreeningResult, status_code=status.HTTP_201_CREATED)
def screen_transaction(txn: TransactionIn, store: StoreDep) -> ScreeningResult:
    now = datetime.now(UTC)
    with store.lock:
        decision, risk_score, hits = screen(txn, list(store.watchlist.values()))
        txn_id = new_id("txn")
        alert_id = None
        if decision is Decision.REVIEW:
            alert = Alert(
                id=new_id("alt"),
                transaction_id=txn_id,
                status=AlertStatus.OPEN,
                risk_score=risk_score,
                hits=hits,
                created_at=now,
            )
            store.alerts[alert.id] = alert
            store.alert_history[alert.id] = [
                AlertHistoryEvent(type=AlertEventType.CREATED, timestamp=now)
            ]
            alert_id = alert.id
        result = ScreeningResult(
            transaction_id=txn_id,
            transaction=txn,
            decision=decision,
            risk_score=risk_score,
            hits=hits,
            alert_id=alert_id,
            screened_at=now,
        )
        store.results[txn_id] = result
    return result


@router.post("/screen/bulk", response_model=list[ScreeningResult], status_code=status.HTTP_201_CREATED)
def screen_transactions(batch: BulkTransactionIn, store: StoreDep) -> list[ScreeningResult]:
    results: list[ScreeningResult] = []
    with store.lock:
        watchlist = list(store.watchlist.values())
        for txn in batch.transactions:
            now = datetime.now(UTC)
            decision, risk_score, hits = screen(txn, watchlist)
            txn_id = new_id("txn")
            alert_id = None
            if decision is Decision.REVIEW:
                alert = Alert(
                    id=new_id("alt"),
                    transaction_id=txn_id,
                    status=AlertStatus.OPEN,
                    risk_score=risk_score,
                    hits=hits,
                    created_at=now,
                )
                store.alerts[alert.id] = alert
                store.alert_history[alert.id] = [
                    AlertHistoryEvent(type=AlertEventType.CREATED, timestamp=now)
                ]
                alert_id = alert.id
            result = ScreeningResult(
                transaction_id=txn_id,
                transaction=txn,
                decision=decision,
                risk_score=risk_score,
                hits=hits,
                alert_id=alert_id,
                screened_at=now,
            )
            store.results[txn_id] = result
            results.append(result)
    return results


@router.get("/{transaction_id}", response_model=ScreeningResult)
def get_screening_result(transaction_id: str, store: StoreDep) -> ScreeningResult:
    result = store.results.get(transaction_id)
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Transaction not found")
    return result
