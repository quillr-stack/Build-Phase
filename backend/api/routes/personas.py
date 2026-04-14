from fastapi import APIRouter
from backend.graph.seed_data import SEED_PERSONAS

router = APIRouter()

@router.get("/personas")
async def get_personas():
    return SEED_PERSONAS
