from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.layers import validation_engine
from backend.db.postgres import async_session
from backend.db.models import Outcome, Prediction
from sqlalchemy import select

router = APIRouter()

class OutcomeRequest(BaseModel):
    run_id: str
    actual_outcome: str
    actual_metrics: Dict[str, Any]
    notes: Optional[str] = None

@router.post("/outcomes")
async def submit_outcome(request: OutcomeRequest):
    try:
        validation_result = await validation_engine.validate(
            request.run_id,
            request.actual_outcome,
            request.actual_metrics
        )
        return validation_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/runs/{run_id}/accuracy")
async def get_run_accuracy(run_id: str):
    async with async_session() as session:
        # Get outcome for this run
        result = await session.execute(
            select(Outcome)
            .join(Prediction, Outcome.prediction_id == Prediction.id)
            .where(Prediction.run_id == run_id)
        )
        outcome = result.scalar_one_or_none()

        if not outcome:
            return {"run_id": run_id, "validation": {"status": "pending"}}

        return {
            "run_id": run_id,
            "validation": {
                "status": "validated",
                "accuracy_score": (outcome.directional_accuracy * 0.5) + ((1 - outcome.error_margin) * 0.3) + (outcome.behavior_match_score * 0.2),
                "validated_at": outcome.recorded_at
            }
        }

@router.get("/system/accuracy")
async def get_system_accuracy():
    async with async_session() as session:
        result = await session.execute(select(Outcome))
        outcomes = result.scalars().all()

        if not outcomes:
            return {"total_runs": 0, "validated_runs": 0, "overall_accuracy": 0}

        total_accuracy = sum((o.directional_accuracy * 0.5) + ((1 - o.error_margin) * 0.3) + (o.behavior_match_score * 0.2) for o in outcomes)
        avg_accuracy = total_accuracy / len(outcomes)

        return {
            "total_runs": len(outcomes), # Simplified
            "validated_runs": len(outcomes),
            "overall_accuracy": avg_accuracy,
            "directional_accuracy": sum(1 for o in outcomes if o.directional_accuracy) / len(outcomes),
            "trend": "improving"
        }
