"""In-memory storage. Data is lost on restart, which is fine for this service."""

from threading import Lock
from uuid import uuid4

from app.models import Alert, AlertHistoryEvent, ScreeningResult, WatchlistEntry

# Obviously fictional names; see the "synthetic data only" rule in the README.
SEED_WATCHLIST = [
    ("Ivan Placeholder", "SYNTH-SANCTIONS"),
    ("Globex Front LLC", "SYNTH-SANCTIONS"),
    ("Acme Shell Holdings", "SYNTH-PEP"),
    ("Dr. Evil Example", "SYNTH-PEP"),
]


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class Store:
    def __init__(self) -> None:
        self.lock = Lock()
        self.results: dict[str, ScreeningResult] = {}
        self.alerts: dict[str, Alert] = {}
        self.alert_history: dict[str, list[AlertHistoryEvent]] = {}
        self.watchlist: dict[str, WatchlistEntry] = {}
        for name, list_name in SEED_WATCHLIST:
            entry = WatchlistEntry(id=new_id("wl"), name=name, list_name=list_name)
            self.watchlist[entry.id] = entry


_store = Store()


def get_store() -> Store:
    """FastAPI dependency; override it in tests to get a fresh store."""
    return _store
