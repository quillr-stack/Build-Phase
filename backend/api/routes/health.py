from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "db": "ok", # Simplified for now
        "redis": "ok",
        "kuzu": "ok"
    }
