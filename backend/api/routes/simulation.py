from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
import uuid
from backend.core import orchestrator
from backend.db.postgres import async_session
from backend.db.models import Simulation
from backend.db.redis_client import redis_client
from sqlalchemy import select

router = APIRouter()

class SimulationRequest(BaseModel):
    segment: Literal["tier1_metro", "tier2_urban", "tier3_rural", "mixed_india"] = Field(
        ...,
        description="The target Indian citizen segment for the simulation"
    )
    industry: Literal["fintech", "fmcg", "edtech", "healthtech", "ecommerce", "government"] = Field(
        ...,
        description="The industry vertical of the product or campaign"
    )
    objective: str = Field(
        ...,
        description="The primary goal (e.g., 'signup', 'brand_awareness', 'purchase')"
    )
    product_description: str = Field(
        ...,
        description="Detailed description of the product or campaign to be tested"
    )
    agent_count: Optional[int] = Field(
        1000,
        ge=1,
        le=10000,
        description="Number of autonomous agents to involve in the simulation"
    )
    variables: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Custom scenario variables and execution parameters"
    )

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
