from fastapi import FastAPI
from pydantic import BaseModel, Field

from .lead_router import Lead, score_lead

app = FastAPI(
    title="Freshtiq AI Automation Demo",
    version="1.0.0",
    description="Portfolio API showing lead intake, scoring, and routing.",
)

class LeadPayload(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=4000)
    budget: float | None = Field(default=None, ge=0)
    company: str | None = Field(default=None, max_length=200)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/lead")
def intake_lead(payload: LeadPayload) -> dict[str, object]:
    decision = score_lead(
        Lead(
            name=payload.name,
            message=payload.message,
            budget=payload.budget,
            company=payload.company,
        )
    )
    return {
        "accepted": True,
        "score": decision.score,
        "route": decision.route,
        "reasons": list(decision.reasons),
    }
