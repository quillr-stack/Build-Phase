from backend.core.logger import log

async def generate_scenarios(input_data: dict) -> list[dict]:
    """
    Generates optimistic, realistic, and pessimistic scenarios.
    """
    scenarios = [
        {
            "name": "optimistic",
            "variables": {**input_data.get("variables", {}), "execution_quality": "high", "market_sentiment": "positive"}
        },
        {
            "name": "realistic",
            "variables": {**input_data.get("variables", {}), "execution_quality": "medium", "market_sentiment": "neutral"}
        },
        {
            "name": "pessimistic",
            "variables": {**input_data.get("variables", {}), "execution_quality": "low", "market_sentiment": "skeptical"}
        }
    ]

    log("none", "scenario_engine", "generated", data={"count": len(scenarios)})
    return scenarios
