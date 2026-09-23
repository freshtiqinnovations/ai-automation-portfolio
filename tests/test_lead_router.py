from src.lead_router import Lead, score_lead
from src.resilient_worker import RetryPolicy, run_with_retry

def test_high_intent_lead_is_prioritized():
    lead = Lead(
        name="Client",
        company="Example Co",
        budget=1200,
        message="We need an AI automation bot with API integration and webhook routing.",
    )
    decision = score_lead(lead)
    assert decision.route == "priority_sales"
    assert decision.score >= 60

def test_empty_message_needs_details():
    decision = score_lead(Lead(name="Client", message=""))
    assert decision.route == "needs_details"

def test_retry_recovers_after_transient_errors():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("temporary")
        return "ok"

    result = run_with_retry(
        flaky,
        policy=RetryPolicy(attempts=3, base_delay_seconds=0),
        sleep=lambda _: None,
    )
    assert result == "ok"
    assert calls["n"] == 3
