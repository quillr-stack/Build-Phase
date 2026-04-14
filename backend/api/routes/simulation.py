from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from backend.core import orchestrator
from backend.db.postgres import async_session
from backend.db.models import Simulation
from backend.db.redis_client import redis_client
from sqlalchemy import select

router = APIRouter()

class SimulationRequest(BaseModel):
    segment: str
    industry: str
    objective: str
    product_description: str
    agent_count: Optional[int] = 1000
    variables: Optional[Dict[str, Any]] = {}

@router.post("/simulate")
async def simulate(request: SimulationRequest, background_tasks: BackgroundTasks):
    run_id = str(uuid.uuid4())

    # Create initial record in DB
    async with async_session() as session:
        new_sim = Simulation(
            id=run_id,
            status="pending",
            input=request.model_dump(),
            agent_count=request.agent_count
        )
        session.add(new_sim)
        await session.commit()

    await redis_client.set_run_status(run_id, "pending")

    # Start orchestrator in background
    background_tasks.add_task(orchestrator.run, run_id, request.model_dump())

    return {
        "run_id": run_id,
        "status": "pending",
        "estimated_duration_seconds": 45 # Rough estimate for Phase 1
    }

@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    async with async_session() as session:
        result = await session.execute(select(Simulation).where(Simulation.id == run_id))
        simulation = result.scalar_one_or_none()

        if not simulation:
            raise HTTPException(status_code=404, detail="Run not found")

        return {
            "run_id": str(simulation.id),
            "status": simulation.status,
            "input": simulation.input,
            "output": simulation.output,
            "created_at": simulation.created_at,
            "completed_at": simulation.completed_at
        }
