from backend.core.logger import log
from backend.layers import input_layer, persona_engine, scenario_engine, simulation_engine, output_layer
from backend.db.postgres import async_session
from backend.db.models import Simulation, Scenario, Prediction
from backend.db.redis_client import redis_client
from backend.core import config
from sqlalchemy import update
from datetime import datetime

async def run(run_id: str, input_data: dict):
    log(run_id, "orchestrator", "started")

    try:
        # 1. Input Layer
        normalized = await input_layer.process(input_data)

        async with async_session() as session:
            await session.execute(
                update(Simulation).where(Simulation.id == run_id).values(status="processing", input=normalized)
            )
            await session.commit()
        await redis_client.set_run_status(run_id, "processing")

        # 2. Persona Engine
        # For Phase 1, we use a smaller count if the request is large to save time/cost during dev
        agent_count = normalized.get("agent_count", config.DEFAULT_AGENTS_PER_RUN)
        personas = await persona_engine.get_personas(
            normalized["segment"],
            agent_count
        )

        # 3. Scenario Engine
        scenarios_data = await scenario_engine.generate_scenarios(normalized)

        # Save scenarios to DB
        async with async_session() as session:
            db_scenarios = []
            for s in scenarios_data:
                db_scenario = Scenario(run_id=run_id, name=s["name"], variables=s["variables"])
                session.add(db_scenario)
                db_scenarios.append(db_scenario)
            await session.commit()
            # Refresh to get IDs
            for s in db_scenarios:
                await session.refresh(s)

            # Map name to ID for simulation engine
            scenario_map = {s.name: str(s.id) for s in db_scenarios}
            for s in scenarios_data:
                s["id"] = scenario_map[s["name"]]

        # 4. Simulation Engine
        predictions_data = await simulation_engine.run_simulation(
            run_id, personas, scenarios_data, normalized
        )

        # 5. Output Layer
        output = await output_layer.structure_output(predictions_data)

        # 6. Persist
        async with async_session() as session:
            for p_data in predictions_data:
                prediction = Prediction(
                    run_id=run_id,
                    scenario_id=p_data["id"],
                    predicted_outcome=p_data["predicted_outcome"],
                    sentiment=p_data["sentiment"],
                    barriers=p_data["barriers"],
                    probability=p_data["probability"],
                    confidence=p_data["confidence"],
                    raw_output=p_data["raw_output"]
                )
                session.add(prediction)

            await session.execute(
                update(Simulation).where(Simulation.id == run_id).values(
                    status="complete",
                    output=output,
                    completed_at=datetime.utcnow()
                )
            )
            await session.commit()

        await redis_client.set_run_status(run_id, "complete")
        await redis_client.publish_event(run_id, {"type": "complete", "output": output})

        log(run_id, "orchestrator", "complete")
        return output

    except Exception as e:
        log(run_id, "orchestrator", f"failed: {str(e)}")
        async with async_session() as session:
            await session.execute(
                update(Simulation).where(Simulation.id == run_id).values(status="failed")
            )
            await session.commit()
        await redis_client.set_run_status(run_id, "failed")
        raise e
