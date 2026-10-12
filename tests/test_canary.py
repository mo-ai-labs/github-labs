import os


def test_canary():
    """Fails only when the nightly workflow is dispatched with simulate_failure=true."""
    assert os.environ.get("SIMULATE_FAILURE") != "true", (
        "simulated nightly failure (Day 12 drill)"
    )
