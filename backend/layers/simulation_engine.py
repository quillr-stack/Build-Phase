import asyncio
from backend.intelligence import react_agent
from backend.db.redis_client import redis_client
from backend.core.logger import log

async def run_simulation(
    run_id: str,
    personas: list[dict],
    scenarios: list[dict],
    input_data: dict
) -> list[dict]:
    """
    Runs the simulation loop for each scenario.
    """
    all_predictions = []

    total_steps = len(scenarios)
    for i, scenario in enumerate(scenarios):
        log(run_id, "simulation_engine", f"starting scenario: {scenario['name']}")

        # In Phase 1, we might use a subset of agents for speed if count is high
        # but here we use the requested count.

        results = await react_agent.run_agents_batch(
            personas,
            scenario,
            input_data["objective"],
            input_data["product_description"],
            run_id
        )

        # Aggregate results
        if not results:
            log(run_id, "simulation_engine", f"scenario {scenario['name']} failed: no results")
            continue

        adoptions = [r for r in results if r.get("decision") == "adopt"]
        shares = [r for r in results if r.get("decision") == "share"]

        sentiment_scores = {"positive": 1.0, "neutral": 0.5, "skeptical": 0.0}
        avg_sentiment_val = sum(sentiment_scores.get(r.get("sentiment", "neutral"), 0.5) for r in results) / len(results)

        sentiment = "neutral"
        if avg_sentiment_val > 0.7: sentiment = "positive"
        elif avg_sentiment_val < 0.3: sentiment = "skeptical"

        barriers = {}
        for r in results:
            for b in r.get("barriers", []):
                barriers[b] = barriers.get(b, 0) + 1

        # Sort barriers by frequency
        sorted_barriers = sorted(barriers.items(), key=lambda x: x[1], reverse=True)
        top_barriers = [b[0] for b in sorted_barriers[:5]]

        prediction = {
            "scenario": scenario["name"],
            "predicted_outcome": "high_conversion" if len(adoptions)/len(results) > 0.6 else "medium_conversion" if len(adoptions)/len(results) > 0.2 else "low_conversion",
            "sentiment": sentiment,
            "barriers": top_barriers,
            "probability": len(adoptions) / len(results),
            "confidence": 0.8, # Placeholder
            "raw_output": {"results_count": len(results), "adoptions": len(adoptions), "shares": len(shares)}
        }

        all_predictions.append(prediction)

        # Update progress in Redis
        progress = (i + 1) / total_steps
        await redis_client.publish_event(run_id, {"type": "progress", "value": progress})

    return all_predictions
