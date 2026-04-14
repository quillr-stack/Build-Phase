import anthropic
import json
from backend.core import config

client = anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)

async def call_agent(
    persona: dict,
    scenario: dict,
    objective: str,
    product_description: str
) -> dict:
    """
    Single agent ReACT call.
    Returns structured prediction dict.
    Max tokens: 300 (config.CLAUDE_MAX_TOKENS_PER_AGENT)
    """
    system_prompt = f"""
    You are a representative of the following Indian persona:
    Persona ID: {persona.get('persona_id')}
    Segment: {persona.get('segment')}
    State: {persona.get('state')}
    Traits: {json.dumps(persona.get('traits'))}

    Objective: {objective}
    Product: {product_description}
    Scenario Variables: {json.dumps(scenario.get('variables'))}

    You must respond ONLY in valid JSON.
    Format: {{"action": "...", "reasoning": "...", "decision": "...", "sentiment": "...", "barriers": []}}

    Decisions can be: "adopt", "reject", "ignore", "share".
    Sentiments can be: "skeptical", "neutral", "positive".
    Barriers should be a list of strings explaining what stops you.
    """

    try:
        response = await client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=config.CLAUDE_MAX_TOKENS_PER_AGENT,
            system=system_prompt,
            messages=[
                {"role": "user", "content": "Analyze the product and scenario and make a decision."}
            ]
        )

        # Parse JSON from response
        text = response.content[0].text
        # Basic JSON extraction in case there's preamble
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(text[start:end])
        else:
            return {"error": "Invalid JSON response", "raw": text}

    except Exception as e:
        return {"error": str(e)}
