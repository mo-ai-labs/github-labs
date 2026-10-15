import pytest
from fastapi.testclient import TestClient

from app.store import Store
from tests.conftest import make_txn


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_screen_clean_transaction_creates_no_alert(client, store):
    response = client.post("/transactions/screen", json=make_txn())
    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "clear"
    assert body["alert_id"] is None
    assert body["transaction"]["purpose_code"] is None
    assert store.alerts == {}


def test_screen_accepts_purpose_code(client):
    response = client.post("/transactions/screen", json=make_txn(purpose_code="SALA"))
    assert response.status_code == 201
    assert response.json()["transaction"]["purpose_code"] == "SALA"


@pytest.mark.parametrize("purpose_code", ["salA", "SAL", "SALAA", "SA1A"])
def test_screen_rejects_malformed_purpose_code(client, purpose_code):
    response = client.post("/transactions/screen", json=make_txn(purpose_code=purpose_code))
    assert response.status_code == 422


def test_screen_suspicious_transaction_opens_alert(client):
    response = client.post(
        "/transactions/screen",
        json=make_txn(beneficiary_name="Acme Shell Holdings"),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "review"
    assert body["risk_score"] == 70

    alert = client.get(f"/alerts/{body['alert_id']}").json()
    assert alert["status"] == "open"
    assert alert["transaction_id"] == body["transaction_id"]


def test_get_screening_result(client):
    screened = client.post("/transactions/screen", json=make_txn()).json()
    response = client.get(f"/transactions/{screened['transaction_id']}")
    assert response.status_code == 200
    assert response.json() == screened


def test_get_unknown_transaction_returns_404(client):
    assert client.get("/transactions/txn_missing").status_code == 404


def test_screen_rejects_invalid_payload(client):
    response = client.post("/transactions/screen", json=make_txn(amount=-5, currency="EURO"))
    assert response.status_code == 422


def test_screen_rejects_zero_amount(client):
    response = client.post("/transactions/screen", json=make_txn(amount=0))
    assert response.status_code == 422


def test_screen_rejects_negative_amount(client):
    response = client.post("/transactions/screen", json=make_txn(amount=-0.01))
    assert response.status_code == 422


def test_screen_rejects_lowercase_currency(client):
    response = client.post("/transactions/screen", json=make_txn(currency="eur"))
    assert response.status_code == 422


def test_screen_rejects_numeric_currency(client):
    response = client.post("/transactions/screen", json=make_txn(currency="123"))
    assert response.status_code == 422


def test_screen_rejects_lowercase_originator_country(client):
    response = client.post("/transactions/screen", json=make_txn(originator_country="de"))
    assert response.status_code == 422


def test_screen_rejects_numeric_originator_country(client):
    response = client.post("/transactions/screen", json=make_txn(originator_country="12"))
    assert response.status_code == 422


def test_screen_rejects_three_letter_originator_country(client):
    response = client.post("/transactions/screen", json=make_txn(originator_country="XQZ"))
    assert response.status_code == 422


def test_screen_rejects_lowercase_beneficiary_country(client):
    response = client.post("/transactions/screen", json=make_txn(beneficiary_country="de"))
    assert response.status_code == 422


def test_screen_rejects_three_letter_beneficiary_country(client):
    response = client.post("/transactions/screen", json=make_txn(beneficiary_country="XQZ"))
    assert response.status_code == 422


def test_screen_rejects_numeric_beneficiary_country(client):
    response = client.post("/transactions/screen", json=make_txn(beneficiary_country="12"))
    assert response.status_code == 422


def test_screen_rejects_whitespace_reference(client):
    response = client.post("/transactions/screen", json=make_txn(reference="   "))
    assert response.status_code == 422


def test_screen_rejects_whitespace_originator_name(client):
    response = client.post("/transactions/screen", json=make_txn(originator_name="   "))
    assert response.status_code == 422


def test_screen_rejects_whitespace_beneficiary_name(client):
    response = client.post("/transactions/screen", json=make_txn(beneficiary_name="   "))
    assert response.status_code == 422


def test_screen_rejects_amount_with_more_than_two_decimal_places(client):
    response = client.post("/transactions/screen", json=make_txn(amount=10.123))
    assert response.status_code == 422


def test_rules_are_listed(client):
    ids = {rule["id"] for rule in client.get("/rules").json()}
    assert ids == {"WATCHLIST_NAME", "HIGH_RISK_COUNTRY", "LARGE_AMOUNT", "ROUND_AMOUNT"}


def test_screen_bulk_preserves_order_and_creates_alert_for_review(
    client: TestClient, store: Store
) -> None:
    transactions = [
        make_txn(reference="TXN-BULK-1"),
        make_txn(reference="TXN-BULK-2", beneficiary_name="Acme Shell Holdings"),
        make_txn(reference="TXN-BULK-3"),
    ]
    response = client.post("/transactions/screen/bulk", json={"transactions": transactions})

    assert response.status_code == 201
    results = response.json()
    assert [result["transaction"]["reference"] for result in results] == [
        txn["reference"] for txn in transactions
    ]
    assert [result["decision"] for result in results] == ["clear", "review", "clear"]
    assert [result["risk_score"] for result in results] == [0, 70, 0]
    assert results[0]["alert_id"] is None
    assert results[2]["alert_id"] is None
    assert len(store.results) == 3
    assert len(store.alerts) == 1
    alert_response = client.get(f"/alerts/{results[1]['alert_id']}")
    assert alert_response.status_code == 200
    alert = alert_response.json()
    assert alert["transaction_id"] == results[1]["transaction_id"]
    assert alert["status"] == "open"
    assert alert["risk_score"] == results[1]["risk_score"]
    assert alert["hits"] == results[1]["hits"]
    assert alert["created_at"] == results[1]["screened_at"]


def test_screen_bulk_rejects_empty_transactions(client: TestClient) -> None:
    response = client.post("/transactions/screen/bulk", json={"transactions": []})
    assert response.status_code == 422


def test_screen_bulk_rejects_more_than_100_transactions(client: TestClient) -> None:
    transactions = [make_txn(reference=f"TXN-BULK-{index}") for index in range(101)]
    response = client.post("/transactions/screen/bulk", json={"transactions": transactions})
    assert response.status_code == 422


def test_screen_bulk_accepts_100_transactions(client: TestClient, store: Store) -> None:
    transactions = [make_txn(reference=f"TXN-BULK-{index}") for index in range(100)]
    response = client.post("/transactions/screen/bulk", json={"transactions": transactions})
    assert response.status_code == 201
    assert len(response.json()) == 100
    assert len({result["transaction_id"] for result in response.json()}) == 100
    assert len(store.results) == 100


def test_screen_bulk_rejects_invalid_item_without_storing_results(
    client: TestClient, store: Store
) -> None:
    existing = client.post(
        "/transactions/screen", json=make_txn(beneficiary_name="Acme Shell Holdings")
    )
    assert existing.status_code == 201
    results_before = store.results.copy()
    alerts_before = store.alerts.copy()
    transactions = [
        make_txn(reference="TXN-BULK-1", beneficiary_name="Acme Shell Holdings"),
        make_txn(reference="TXN-BULK-2", amount=-5),
        make_txn(reference="TXN-BULK-3"),
    ]
    response = client.post("/transactions/screen/bulk", json={"transactions": transactions})
    assert response.status_code == 422
    assert store.results == results_before
    assert store.alerts == alerts_before


def test_get_screening_result_for_each_bulk_transaction(client: TestClient) -> None:
    transactions = [
        make_txn(reference="TXN-BULK-1"),
        make_txn(reference="TXN-BULK-2", beneficiary_name="Acme Shell Holdings"),
        make_txn(reference="TXN-BULK-3"),
    ]
    screened = client.post("/transactions/screen/bulk", json={"transactions": transactions})
    assert screened.status_code == 201
    for result in screened.json():
        response = client.get(f"/transactions/{result['transaction_id']}")
        assert response.status_code == 200
        assert response.json() == result
