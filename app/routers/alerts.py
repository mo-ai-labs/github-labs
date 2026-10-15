from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models import (
    Alert,
    AlertEventType,
    AlertHistoryEvent,
    AlertStatus,
    AssignIn,
    CloseAlertIn,
    DispositionChangeIn,
    Note,
    NoteIn,
)
from app.store import Store, get_store, new_id

router = APIRouter(prefix="/alerts", tags=["alerts"])
StoreDep = Annotated[Store, Depends(get_store)]


def _get_alert(store: Store, alert_id: str) -> Alert:
    alert = store.alerts.get(alert_id)
    if alert is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alert not found")
    return alert


def _require_open(alert: Alert) -> None:
    if alert.status is AlertStatus.CLOSED:
        raise HTTPException(status.HTTP_409_CONFLICT, "Alert is already closed")


@router.get("", response_model=list[Alert])
def list_alerts(
    store: StoreDep,
    alert_status: AlertStatus | None = None,
    assignee: str | None = None,
    min_risk_score: int | None = Query(default=None, ge=0, le=100),
    transaction_id: str | None = None,
) -> list[Alert]:
    alerts = sorted(store.alerts.values(), key=lambda a: a.created_at, reverse=True)
    if alert_status is not None:
        alerts = [a for a in alerts if a.status is alert_status]
    if assignee is not None:
        alerts = [a for a in alerts if a.assignee == assignee]
    if min_risk_score is not None:
        alerts = [a for a in alerts if a.risk_score >= min_risk_score]
    if transaction_id is not None:
        alerts = [a for a in alerts if a.transaction_id == transaction_id]
    return alerts


@router.get("/{alert_id}", response_model=Alert)
def get_alert(alert_id: str, store: StoreDep) -> Alert:
    return _get_alert(store, alert_id)


@router.get("/{alert_id}/notes", response_model=list[Note])
def list_alert_notes(alert_id: str, store: StoreDep) -> list[Note]:
    with store.lock:
        alert = _get_alert(store, alert_id)
        return sorted(alert.notes, key=lambda note: note.created_at, reverse=True)


@router.get("/{alert_id}/history", response_model=list[AlertHistoryEvent])
def get_alert_history(alert_id: str, store: StoreDep) -> list[AlertHistoryEvent]:
    with store.lock:
        _get_alert(store, alert_id)
        return sorted(store.alert_history.get(alert_id, []), key=lambda event: event.timestamp)


@router.post("/{alert_id}/assign", response_model=Alert)
def assign_alert(alert_id: str, body: AssignIn, store: StoreDep) -> Alert:
    with store.lock:
        alert = _get_alert(store, alert_id)
        _require_open(alert)
        alert.assignee = body.assignee
        store.alert_history[alert_id].append(
            AlertHistoryEvent(type=AlertEventType.ASSIGNED, timestamp=datetime.now(UTC))
        )
    return alert


@router.post("/{alert_id}/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def add_note(alert_id: str, body: NoteIn, store: StoreDep) -> Note:
    with store.lock:
        alert = _get_alert(store, alert_id)
        note = Note(id=new_id("note"), author=body.author, text=body.text, created_at=datetime.now(UTC))
        alert.notes.append(note)
        store.alert_history[alert_id].append(
            AlertHistoryEvent(type=AlertEventType.NOTE_ADDED, actor=body.author, timestamp=note.created_at)
        )
    return note


@router.post("/{alert_id}/close", response_model=Alert)
def close_alert(alert_id: str, body: CloseAlertIn, store: StoreDep) -> Alert:
    with store.lock:
        alert = _get_alert(store, alert_id)
        _require_open(alert)
        alert.status = AlertStatus.CLOSED
        alert.disposition = body.disposition
        alert.close_reason = body.reason
        alert.closed_at = datetime.now(UTC)
        store.alert_history[alert_id].append(
            AlertHistoryEvent(type=AlertEventType.CLOSED, timestamp=alert.closed_at)
        )
    return alert


@router.patch("/{alert_id}/disposition", response_model=Alert)
def change_disposition(alert_id: str, body: DispositionChangeIn, store: StoreDep) -> Alert:
    with store.lock:
        alert = _get_alert(store, alert_id)
        if alert.status is not AlertStatus.CLOSED:
            raise HTTPException(status.HTTP_409_CONFLICT, "Only closed alerts can change disposition")
        if alert.disposition is body.disposition:
            raise HTTPException(status.HTTP_409_CONFLICT, "Alert already has this disposition")
        alert.disposition = body.disposition
    return alert
