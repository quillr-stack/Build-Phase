async def structure_output(predictions: list[dict]) -> dict:
    """
    Aggregates all scenario predictions.
    """
    best_case = next((p for p in predictions if p["scenario"] == "optimistic"), predictions[0])
    worst_case = next((p for p in predictions if p["scenario"] == "pessimistic"), predictions[0])
    most_likely = next((p for p in predictions if p["scenario"] == "realistic"), predictions[0])

    # Simple extraction of key driver from top barriers across all scenarios
    all_barriers = []
    for p in predictions:
        all_barriers.extend(p["barriers"])

    key_driver = max(set(all_barriers), key=all_barriers.count) if all_barriers else "None identified"

    return {
        "best_case": best_case,
        "worst_case": worst_case,
        "most_likely": most_likely,
        "key_driver": key_driver,
        "sensitivity": "Execution quality and market sentiment",
        "summary": f"The simulation suggests a {most_likely['predicted_outcome']} outcome with a primary barrier being {key_driver}."
    }
