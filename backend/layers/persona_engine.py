import random
from backend.graph.seed_data import SEED_PERSONAS
from backend.core.logger import log

async def get_personas(segment: str, count: int) -> list[dict]:
    """
    Loads relevant personas. For Phase 1, we use seed data and variation.
    """
    relevant_seeds = [p for p in SEED_PERSONAS if p["segment"] == segment]
    if not relevant_seeds:
        # Fallback to all seeds if segment not found
        relevant_seeds = SEED_PERSONAS

    personas = []
    for i in range(count):
        base = random.choice(relevant_seeds)
        # Create variation
        persona = {
            "persona_id": f"{base['persona_id']}_{i}",
            "segment": base["segment"],
            "state": base["state"],
            "traits": {
                k: min(1.0, max(0.0, v + random.uniform(-0.1, 0.1)))
                for k, v in base["traits"].items() if isinstance(v, (int, float))
            },
            "platform_preference": base["traits"].get("platform_preference", "whatsapp")
        }
        personas.append(persona)

    log("none", "persona_engine", "loaded", data={"count": len(personas)})
    return personas
