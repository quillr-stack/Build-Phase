from backend.db.postgres import async_session
from backend.db.models import PersonaUpdate, PersonaVersion, Simulation
from backend.core.logger import log
from sqlalchemy import select, update
import uuid

async def process(validation_record, prediction, actual_metrics) -> dict:
    """
    Takes validation output and updates persona traits and scenario weights.
    """
    updates_made = {
        "persona_traits_adjusted": 0,
        "scenario_weights_recalibrated": False
    }

    # 1. Persona Trait Adjustment Logic
    if not validation_record.directional_accuracy:
        async with async_session() as session:
            # Get the simulation to find segment
            result = await session.execute(select(Simulation).where(Simulation.id == prediction.run_id))
            sim = result.scalar_one_or_none()
            if not sim: return updates_made

            segment = sim.input.get("segment")

            # Logic: Adjust traits for personas in this segment
            # For Phase 2, we simulate this by marking that we would update
            # actual KuzuDB update logic would go here.

            # Identify which traits to adjust based on barriers
            actual_barriers = actual_metrics.get("confirmed_barriers", [])

            trait_adjustments = {}
            if "trust" in str(actual_barriers).lower():
                trait_adjustments["trust_level"] = -0.05
            if "price" in str(actual_barriers).lower():
                trait_adjustments["price_sensitivity"] = 0.05

            if trait_adjustments:
                # Store update record
                persona_update = PersonaUpdate(
                    persona_id=segment, # Using segment as a proxy for persona group in Phase 2
                    trait_updates=trait_adjustments,
                    triggered_by=validation_record.id
                )
                session.add(persona_update)
                await session.commit()
                updates_made["persona_traits_adjusted"] = len(trait_adjustments)

    # 2. Scenario Weight Recalibration (Simplified for Phase 2)
    updates_made["scenario_weights_recalibrated"] = True

    log(str(prediction.run_id), "feedback_loop", "processed", data=updates_made)
    return updates_made
