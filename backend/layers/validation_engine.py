from backend.db.postgres import async_session
from backend.db.models import Outcome, Prediction
from backend.intelligence import feedback_loop
from sqlalchemy import select
import uuid
from datetime import datetime

async def validate(
    run_id: str,
    actual_outcome: str,
    actual_metrics: dict
) -> dict:
    """
    Compares prediction vs reality.
    """
    async with async_session() as session:
        # Get most likely prediction for this run
        result = await session.execute(
            select(Prediction).where(Prediction.run_id == run_id).limit(1)
        )
        prediction = result.scalar_one_or_none()

        if not prediction:
            raise ValueError(f"No prediction found for run_id: {run_id}")

        # Scoring Logic
        # 1. Directional Accuracy
        # Predicted "low_conversion" (probability < 0.4) AND actual conversion was low -> True
        actual_prob = actual_metrics.get("conversions", 0) / actual_metrics.get("impressions", 1)

        predicted_direction = "low" if prediction.probability < 0.4 else "high"
        actual_direction = "low" if actual_prob < 0.4 else "high"
        directional_accuracy = (predicted_direction == actual_direction)

        # 2. Error Margin
        error_margin = abs(prediction.probability - actual_prob)

        # 3. Behavior Match Score
        predicted_barriers = set(prediction.barriers or [])
        confirmed_barriers = set(actual_metrics.get("confirmed_barriers", []))

        if not predicted_barriers:
            behavior_match_score = 1.0 if not confirmed_barriers else 0.0
        else:
            matches = predicted_barriers.intersection(confirmed_barriers)
            behavior_match_score = len(matches) / len(predicted_barriers)

        # Overall Accuracy Score
        accuracy_score = (directional_accuracy * 0.5) + \
                        ((1 - error_margin) * 0.3) + \
                        (behavior_match_score * 0.2)

        # Store result
        outcome = Outcome(
            prediction_id=prediction.id,
            actual_outcome=actual_outcome,
            directional_accuracy=directional_accuracy,
            error_margin=error_margin,
            behavior_match_score=behavior_match_score
        )
        session.add(outcome)
        await session.commit()
        await session.refresh(outcome)

        # Trigger feedback loop
        feedback_summary = await feedback_loop.process(outcome, prediction, actual_metrics)

        return {
            "validation_id": str(outcome.id),
            "accuracy_score": accuracy_score,
            "directional_accuracy": directional_accuracy,
            "error_margin": error_margin,
            "behavior_match_score": behavior_match_score,
            "feedback_summary": feedback_summary
        }
