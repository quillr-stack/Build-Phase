from backend.core.logger import log

VALID_SEGMENTS = ["tier1_metro", "tier2_urban", "tier3_rural", "mixed_india"]
VALID_INDUSTRIES = ["fintech", "fmcg", "edtech", "healthtech", "ecommerce", "government"]

async def process(raw_input: dict) -> dict:
    """
    Validates and normalizes input.
    """
    segment = raw_input.get("segment")
    industry = raw_input.get("industry")
    objective = raw_input.get("objective")
    product_description = raw_input.get("product_description")

    if not all([segment, industry, objective, product_description]):
        raise ValueError("Missing required fields: segment, industry, objective, product_description")

    segment = segment.lower().strip()
    industry = industry.lower().strip()

    if segment not in VALID_SEGMENTS:
        # Fallback or error
        pass

    if industry not in VALID_INDUSTRIES:
        pass

    normalized = {
        "segment": segment,
        "industry": industry,
        "objective": objective,
        "product_description": product_description,
        "agent_count": raw_input.get("agent_count", 1000),
        "variables": raw_input.get("variables", {})
    }

    log("none", "input_layer", "processed", data=normalized)
    return normalized
