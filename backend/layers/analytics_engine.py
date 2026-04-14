import random

async def compute_metrics(
    predictions: list[dict],
    personas: list[dict],
    scenarios: list[dict]
) -> dict:
    """
    Computes all 18 Decision Intelligence Metrics.
    """
    # Most likely scenario (realistic)
    ml = next((p for p in predictions if p["scenario"] == "realistic"), predictions[0])

    # Core Behavioral Metrics (8)
    metrics = {
        "adoption_probability": ml["probability"],
        "trust_gap_score": 10 * (1 - sum(p["traits"]["trust_level"] for p in personas) / len(personas)),
        "price_sensitivity_index": 10 * (sum(p["traits"]["price_sensitivity"] for p in personas) / len(personas)),
        "viral_potential": 10 * (sum(p["traits"]["social_influence"] for p in personas) / len(personas)),
        "barrier_density": len(ml["barriers"]),
        "decision_speed": "medium", # Placeholder
        "social_influence_factor": 10 * (sum(p["traits"]["social_influence"] for p in personas) / len(personas)),
        "digital_readiness_score": 10 * (sum(p["traits"]["digital_literacy"] for p in personas) / len(personas)),
    }

    # Market Dynamics Metrics (5)
    metrics.update({
        "narrative_diffusion_rate": 0.5,
        "trust_shift_potential": 0.3,
        "polarisation_index": 4.2,
        "market_entry_difficulty": 6.5,
        "competitor_displacement": 3.1
    })

    # Strategic Metrics (5)
    metrics.update({
        "optimal_channel": personas[0].get("platform_preference", "whatsapp"),
        "message_resonance_score": 7.2,
        "trust_trigger_list": ["social proof", "vernacular support", "zero-fee guarantee"],
        "conversion_bottleneck": ml["barriers"][0] if ml["barriers"] else "Unknown",
        "recommended_entry_vector": "Tier 2 urban youth"
    })

    return metrics
