from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
visits = pd.read_csv(DATA / "patient_visits.csv")
audits: list[dict] = []
app = FastAPI(title="ALZERA API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])

def latest(patient_id: str) -> dict:
    records = visits.loc[visits.patient_id.eq(patient_id)].sort_values("months_from_baseline")
    if records.empty: raise HTTPException(404, "Patient not found")
    return records.iloc[-1].where(pd.notna(records.iloc[-1]), None).to_dict()

def explanation(row: dict) -> dict:
    return {"risk_score": row["risk_score"], "priority": row["priority"], "trajectory": row["trajectory_signal"], "evidence_confidence": row["evidence_confidence"], "factors": str(row["top_contributing_factors"]).split("; "), "safety": "Clinical decision support only. Clinician review required."}

class Decision(BaseModel): action: str
class Override(BaseModel): suggested_next_stage: str; reason: str

@app.get("/health")
def health(): return {"status": "ok", "data": "synthetic", "patients": int(visits.patient_id.nunique())}

@app.get("/dashboard")
def dashboard():
    latest_rows = visits.sort_values("months_from_baseline").groupby("patient_id", as_index=False).tail(1)
    ordered = latest_rows.sort_values("risk_score", ascending=False)
    return {"disclaimer": "Synthetic demonstration data only; not clinical advice.", "patients": ordered.to_dict(orient="records")}

@app.get("/patients")
def get_patients(): return dashboard()

@app.get("/patients/{patient_id}")
def patient(patient_id: str): return {"patient": latest(patient_id), "trajectory": visits.loc[visits.patient_id.eq(patient_id)].sort_values("months_from_baseline").to_dict(orient="records")}

@app.get("/patients/{patient_id}/priority")
def priority(patient_id: str): return explanation(latest(patient_id))

@app.get("/patients/{patient_id}/explanation")
def get_explanation(patient_id: str): return explanation(latest(patient_id))

@app.get("/patients/{patient_id}/recommendation")
def recommendation(patient_id: str):
    row = latest(patient_id)
    return {"current_stage": row["current_diagnostic_stage"], "suggested_next_stage": row["suggested_next_stage"], "reason": row["reason_for_suggested_next_stage"], "clinician_review_required": True}

@app.post("/patients/{patient_id}/accept")
def accept(patient_id: str, decision: Decision):
    row = latest(patient_id); audits.append({"patient_id":patient_id,"action":"accepted","detail":decision.action,"timestamp":datetime.now(timezone.utc).isoformat()})
    return {"status":"recorded", "recommendation": row["suggested_next_stage"]}

@app.post("/patients/{patient_id}/override")
def override(patient_id: str, decision: Override):
    latest(patient_id); audits.append({"patient_id":patient_id,"action":"overridden","detail":decision.model_dump(),"timestamp":datetime.now(timezone.utc).isoformat()})
    return {"status":"recorded", "clinician_review_required":True}

@app.get("/audit")
def audit(): return {"events": audits}

# Compatibility aliases for a previously configured frontend client.
# Keep these alongside the product endpoints during the PoC transition.
@app.get("/api/v1/dashboard/stats")
def dashboard_stats():
    latest_rows = visits.sort_values("months_from_baseline").groupby("patient_id", as_index=False).tail(1)
    return {
        "total_patients": int(len(latest_rows)),
        "high_priority": int((latest_rows.priority == "High").sum()),
        "medium_priority": int((latest_rows.priority == "Medium").sum()),
        "low_priority": int((latest_rows.priority == "Low").sum()),
        "worsening_trajectory": int((latest_rows.trajectory_signal == "Worsening").sum()),
        "clinical_decision_support_only": True,
    }

@app.get("/api/v1/transactions")
def transactions(skip: int = 0, limit: int = 8):
    # “Transactions” is retained only as a legacy client alias for audit events.
    events = list(reversed(audits))[skip:skip + limit]
    return {"items": events, "total": len(audits), "skip": skip, "limit": limit}

@app.get("/api/v1/audit")
def audit_v1(): return audit()
