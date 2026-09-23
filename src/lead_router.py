from dataclasses import dataclass
from typing import Literal

Route = Literal["priority_sales", "standard_followup", "needs_details"]

@dataclass(frozen=True)
class Lead:
    name: str
    message: str
    budget: float | None = None
    company: str | None = None

@dataclass(frozen=True)
class LeadDecision:
    score: int
    route: Route
    reasons: tuple[str, ...]

HIGH_INTENT_TERMS = {
    "automation", "bot", "api", "integration", "telegram",
    "whatsapp", "crm", "webhook", "python", "ai agent",
}

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

def score_lead(lead: Lead) -> LeadDecision:
    text = normalize(lead.message)
    score = 0
    reasons: list[str] = []

    matches = sorted(term for term in HIGH_INTENT_TERMS if term in text)
    if matches:
        score += min(50, len(matches) * 10)
        reasons.append("relevant service keywords: " + ", ".join(matches))

    if lead.budget is not None and lead.budget > 0:
        score += 25
        reasons.append("budget supplied")

    if lead.company and lead.company.strip():
        score += 15
        reasons.append("company supplied")

    if len(text) >= 40:
        score += 10
        reasons.append("detailed inquiry")

    score = min(score, 100)

    if not text:
        route: Route = "needs_details"
    elif score >= 60:
        route = "priority_sales"
    else:
        route = "standard_followup"

    return LeadDecision(score=score, route=route, reasons=tuple(reasons))
