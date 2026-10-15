from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class TransactionIn(BaseModel):
    reference: str = Field(min_length=1, max_length=64, pattern=r"\S", examples=["TXN-0001"])
    amount: Decimal = Field(gt=0, decimal_places=2, examples=[8200])
    currency: str = Field(pattern=r"^[A-Z]{3}$", examples=["EUR"])
    purpose_code: str | None = Field(default=None, pattern=r"^[A-Z]{4}$", examples=["SALA"])
    originator_name: str = Field(min_length=1, pattern=r"\S", examples=["Jane Example"])
    originator_country: str = Field(pattern=r"^[A-Z]{2}$", examples=["NL"])
    beneficiary_name: str = Field(min_length=1, pattern=r"\S", examples=["Globex Front LLC"])
    beneficiary_country: str = Field(pattern=r"^[A-Z]{2}$", examples=["XQ"])


class BulkTransactionIn(BaseModel):
    transactions: list[TransactionIn] = Field(min_length=1, max_length=100)


class RuleHit(BaseModel):
    rule_id: str
    detail: str
    score: int


class Decision(StrEnum):
    CLEAR = "clear"
    REVIEW = "review"


class ScreeningResult(BaseModel):
    transaction_id: str
    transaction: TransactionIn
    decision: Decision
    risk_score: int
    hits: list[RuleHit]
    alert_id: str | None
    screened_at: datetime


class AlertStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


class Disposition(StrEnum):
    FALSE_POSITIVE = "false_positive"
    TRUE_POSITIVE = "true_positive"


class AlertEventType(StrEnum):
    CREATED = "created"
    ASSIGNED = "assigned"
    NOTE_ADDED = "note_added"
    CLOSED = "closed"
    DISPOSITION_CHANGED = "disposition_changed"


class AlertHistoryEvent(BaseModel):
    type: AlertEventType
    actor: str | None = None
    from_disposition: Disposition | None = None
    to_disposition: Disposition | None = None
    timestamp: datetime


class Note(BaseModel):
    id: str
    author: str
    text: str
    created_at: datetime


class Alert(BaseModel):
    id: str
    transaction_id: str
    status: AlertStatus
    risk_score: int
    hits: list[RuleHit]
    assignee: str | None = None
    disposition: Disposition | None = None
    close_reason: str | None = None
    notes: list[Note] = []
    created_at: datetime
    closed_at: datetime | None = None


class NoteIn(BaseModel):
    author: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=2000)


class AssignIn(BaseModel):
    assignee: str = Field(min_length=1)


class CloseAlertIn(BaseModel):
    disposition: Disposition
    reason: str = Field(min_length=1, max_length=500)


class DispositionChangeIn(BaseModel):
    disposition: Disposition
    reviewer: str = Field(min_length=1)
    reason: str = Field(min_length=1, max_length=500)


class WatchlistEntryIn(BaseModel):
    name: str = Field(min_length=1)
    list_name: str = Field(default="SYNTH-SANCTIONS", min_length=1)


class WatchlistEntry(WatchlistEntryIn):
    id: str


class Rule(BaseModel):
    id: str
    description: str
    score: int
