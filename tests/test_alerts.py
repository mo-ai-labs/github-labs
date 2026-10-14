from datetime import UTC, datetime

from tests.conftest import make_txn


CLOSE_BODY = {"disposition": "false_positive", "reason": "Name-only match, different entity"}


def test_list_alerts(client, alert_id):
    response = client.get("/alerts")
    assert response.status_code == 200
    assert [alert["id"] for alert in response.json()] == [alert_id]


def test_list_alerts_filters_by_status(client, alert_id):
    client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY)
    assert client.get("/alerts", params={"alert_status": "open"}).json() == []
    assert len(client.get("/alerts", params={"alert_status": "closed"}).json()) == 1


def test_list_alerts_filters_by_assignee(client, alert_id):
    client.post(f"/alerts/{alert_id}/assign", json={"assignee": "analyst-1"})
    assert len(client.get("/alerts", params={"assignee": "analyst-1"}).json()) == 1
    assert client.get("/alerts", params={"assignee": "analyst-2"}).json() == []


def test_list_alerts_filters_by_min_risk_score(client, alert_id):
    lower_score = client.post(
        "/transactions/screen",
        json=make_txn(reference="TXN-LOWER-SCORE", beneficiary_name="Acme Shell Holdings"),
    ).json()
    assert lower_score["risk_score"] == 70

    response = client.get("/alerts", params={"min_risk_score": 100})
    assert [alert["id"] for alert in response.json()] == [alert_id]


def test_list_alerts_filters_by_transaction_id(client, alert_id):
    transaction_id = client.get(f"/alerts/{alert_id}").json()["transaction_id"]

    response = client.get("/alerts", params={"transaction_id": transaction_id})

    assert [alert["id"] for alert in response.json()] == [alert_id]


def test_list_alerts_includes_alert_at_min_risk_score(client, alert_id):
    lower_score = client.post(
        "/transactions/screen",
        json=make_txn(reference="TXN-THRESHOLD", beneficiary_name="Acme Shell Holdings"),
    ).json()

    response = client.get("/alerts", params={"min_risk_score": 70})
    assert {alert["id"] for alert in response.json()} == {alert_id, lower_score["alert_id"]}


def test_list_alerts_rejects_min_risk_score_above_100(client):
    assert client.get("/alerts", params={"min_risk_score": 101}).status_code == 422


def test_list_alerts_rejects_min_risk_score_below_0(client):
    assert client.get("/alerts", params={"min_risk_score": -1}).status_code == 422


def test_list_alerts_combines_min_risk_score_with_status_and_assignee(client, alert_id):
    client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY)
    lower_score = client.post(
        "/transactions/screen",
        json=make_txn(reference="TXN-ASSIGNED", beneficiary_name="Acme Shell Holdings"),
    ).json()
    client.post(f"/alerts/{lower_score['alert_id']}/assign", json={"assignee": "analyst-1"})

    response = client.get(
        "/alerts",
        params={"min_risk_score": 70, "alert_status": "open", "assignee": "analyst-1"},
    )
    assert [alert["id"] for alert in response.json()] == [lower_score["alert_id"]]


def test_list_alerts_combines_transaction_id_with_existing_filters(client, alert_id):
    client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY)
    screened = client.post(
        "/transactions/screen",
        json=make_txn(reference="TXN-COMBINED", beneficiary_name="Acme Shell Holdings"),
    ).json()
    client.post(f"/alerts/{screened['alert_id']}/assign", json={"assignee": "analyst-1"})

    response = client.get(
        "/alerts",
        params={
            "transaction_id": screened["transaction_id"],
            "alert_status": "open",
            "assignee": "analyst-1",
            "min_risk_score": 70,
        },
    )

    assert [alert["id"] for alert in response.json()] == [screened["alert_id"]]


def test_list_alerts_returns_empty_list_for_unknown_transaction_id(client):
    response = client.get("/alerts", params={"transaction_id": "txn_missing"})

    assert response.json() == []


def test_get_alert(client, alert_id):
    response = client.get(f"/alerts/{alert_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == alert_id
    assert body["status"] == "open"
    assert {hit["rule_id"] for hit in body["hits"]} == {"WATCHLIST_NAME", "HIGH_RISK_COUNTRY"}


def test_get_unknown_alert_returns_404(client):
    assert client.get("/alerts/alt_missing").status_code == 404


def test_get_alert_history_returns_all_events_chronologically(client, alert_id):
    client.post(f"/alerts/{alert_id}/assign", json={"assignee": "analyst-1"})
    client.post(f"/alerts/{alert_id}/notes", json={"author": "analyst-1", "text": "Reviewing"})
    client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY)

    response = client.get(f"/alerts/{alert_id}/history")

    assert response.status_code == 200
    events = response.json()
    assert [event["type"] for event in events] == ["created", "assigned", "note_added", "closed"]
    assert [event["actor"] for event in events] == [None, None, "analyst-1", None]
    assert all(event["timestamp"] for event in events)
    assert [event["timestamp"] for event in events] == sorted(event["timestamp"] for event in events)


def test_get_alert_history_returns_404_for_unknown_alert(client):
    response = client.get("/alerts/alt_missing/history")

    assert response.status_code == 404


def test_assign_alert(client, alert_id):
    response = client.post(f"/alerts/{alert_id}/assign", json={"assignee": "analyst-1"})
    assert response.status_code == 200
    assert response.json()["assignee"] == "analyst-1"


def test_add_note(client, alert_id):
    response = client.post(f"/alerts/{alert_id}/notes", json={"author": "analyst-1", "text": "Looking into it"})
    assert response.status_code == 201
    assert response.json()["text"] == "Looking into it"

    notes = client.get(f"/alerts/{alert_id}").json()["notes"]
    assert [note["text"] for note in notes] == ["Looking into it"]


def test_list_alert_notes_returns_empty_list(client, alert_id):
    response = client.get(f"/alerts/{alert_id}/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_list_alert_notes_returns_404_for_unknown_alert(client):
    response = client.get("/alerts/alt_missing/notes")

    assert response.status_code == 404


def test_list_alert_notes_returns_newest_first(client, store, alert_id):
    for text in ("First note", "Second note"):
        client.post(f"/alerts/{alert_id}/notes", json={"author": "analyst-1", "text": text})
    notes = store.alerts[alert_id].notes
    notes[0].created_at = datetime(2026, 1, 1, tzinfo=UTC)
    notes[1].created_at = datetime(2026, 1, 2, tzinfo=UTC)

    response = client.get(f"/alerts/{alert_id}/notes")

    assert response.status_code == 200
    assert [note["text"] for note in response.json()] == ["Second note", "First note"]


def test_list_alert_notes_for_closed_alert(client, alert_id):
    client.post(f"/alerts/{alert_id}/notes", json={"author": "analyst-1", "text": "Review complete"})
    client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY)

    response = client.get(f"/alerts/{alert_id}/notes")

    assert response.status_code == 200
    assert [note["text"] for note in response.json()] == ["Review complete"]


def test_close_alert(client, alert_id):
    response = client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "closed"
    assert body["disposition"] == "false_positive"
    assert body["close_reason"] == CLOSE_BODY["reason"]
    assert body["closed_at"] is not None


def test_closed_alert_cannot_be_closed_or_assigned(client, alert_id):
    client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY)
    assert client.post(f"/alerts/{alert_id}/close", json=CLOSE_BODY).status_code == 409
    assert client.post(f"/alerts/{alert_id}/assign", json={"assignee": "analyst-1"}).status_code == 409


def test_close_rejects_unknown_disposition(client, alert_id):
    response = client.post(f"/alerts/{alert_id}/close", json={"disposition": "maybe", "reason": "x"})
    assert response.status_code == 422
