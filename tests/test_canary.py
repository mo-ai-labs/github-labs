import os

import pytest


@pytest.mark.xfail(
    os.environ.get("SIMULATE_FAILURE") == "true",
    reason="simulated nightly failure (Day 12 drill)",
    raises=AssertionError,
    strict=True,
)
def test_canary() -> None:
    """Expects a failure only when the nightly simulation is explicitly enabled."""
    assert os.environ.get("SIMULATE_FAILURE") != "true", (
        "simulated nightly failure (Day 12 drill)"
    )


@pytest.mark.parametrize("value", [None, "", "false", "TRUE"])
def test_canary_without_simulation_passes(
    monkeypatch: pytest.MonkeyPatch, value: str | None
) -> None:
    if value is None:
        monkeypatch.delenv("SIMULATE_FAILURE", raising=False)
    else:
        monkeypatch.setenv("SIMULATE_FAILURE", value)
    test_canary()


def test_canary_with_simulation_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SIMULATE_FAILURE", "true")
    with pytest.raises(AssertionError, match="simulated nightly failure"):
        test_canary()
