import asyncio
from backend.intelligence import llm_client

async def run_agent_loop(
    persona: dict,
    scenario: dict,
    objective: str,
    product_description: str,
    run_id: str
) -> dict:
    """
    Implements the ReACT loop for a single agent.
    For Phase 1, we simplify to a single call that encapsulates the ReACT reasoning.
    """
    # In a full ReACT loop, we'd have multiple steps: Observe, Reason, Act, Reflect.
    # To keep token usage low as per CLAUDE.md, we do it in one structured call.

    result = await llm_client.call_agent(
        persona, scenario, objective, product_description
    )

    return result

async def run_agents_batch(
    personas: list[dict],
    scenario: dict,
    objective: str,
    product_description: str,
    run_id: str,
    batch_size: int = 50
) -> list[dict]:
    results = []
    for i in range(0, len(personas), batch_size):
        batch = personas[i:i+batch_size]
        tasks = [
            run_agent_loop(p, scenario, objective, product_description, run_id)
            for p in batch
        ]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        # Optional: Sleep to respect rate limits if not handled by client
        # await asyncio.sleep(0.1)
    return results
