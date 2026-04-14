# SATTVA — PHASE 1: FOUNDATION
# Read CLAUDE.md first. Always.
# Goal: Working backend. Core simulation loop. API responding.
# Duration: Build until Phase 1 checklist is 100% complete.

---

## PHASE 1 OBJECTIVE

By end of Phase 1, one thing must work:
POST /api/simulate → returns a structured prediction JSON.

That's it. No UI. No validation. No feedback loop.
Just the core pipe: Input → Persona → Scenario → Simulate → Output → Store.

---

## STEP 1: PROJECT SCAFFOLD

### 1.1 Docker Compose Setup

Create `docker-compose.yml` at project root:

```yaml
version: '3.9'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./backend:/app
      - ./data:/data
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: sattva
      POSTGRES_PASSWORD: sattva_secret
      POSTGRES_DB: sattva_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 1.2 Backend requirements.txt

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.0
python-dotenv==1.0.1
anthropic==0.26.0
kuzu==0.4.2
asyncpg==0.29.0
sqlalchemy[asyncio]==2.0.30
redis[hiredis]==5.0.4
python-jose==3.3.0
httpx==0.27.0
```

### 1.3 Backend Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## STEP 2: CORE INFRASTRUCTURE

### 2.1 config.py

Load all env vars. All constants live here.
Key constants:
- `CLAUDE_MODEL = "claude-sonnet-4-20250514"`
- `MAX_AGENTS_PER_RUN = 10000`
- `DEFAULT_AGENTS_PER_RUN = 1000`
- `CLAUDE_MAX_TOKENS_PER_AGENT = 300`

### 2.2 logger.py

Every log entry must include:
- `timestamp` (ISO 8601)
- `run_id` (if applicable)
- `layer` (which layer is logging: input_layer, persona_engine, etc.)
- `event` (what happened)
- `data` (relevant payload, truncated if large)

Use Python `logging` module. JSON formatted logs.
Log to both stdout AND append to `./data/logs/{run_id}.jsonl`

### 2.3 database/postgres.py

- Async SQLAlchemy engine using asyncpg
- Connection pool: min=2, max=10
- Auto-create tables on startup (use `metadata.create_all`)

### 2.4 database/models.py

Create these tables:

**simulations**
```
id          UUID PRIMARY KEY DEFAULT gen_random_uuid()
status      VARCHAR(20) NOT NULL DEFAULT 'pending'
input       JSONB NOT NULL
agent_count INTEGER NOT NULL DEFAULT 1000
created_at  TIMESTAMPTZ DEFAULT NOW()
completed_at TIMESTAMPTZ
```

**scenarios**
```
id          UUID PRIMARY KEY DEFAULT gen_random_uuid()
run_id      UUID REFERENCES simulations(id)
name        VARCHAR(100)
variables   JSONB
created_at  TIMESTAMPTZ DEFAULT NOW()
```

**predictions**
```
id                UUID PRIMARY KEY DEFAULT gen_random_uuid()
run_id            UUID REFERENCES simulations(id)
scenario_id       UUID REFERENCES scenarios(id)
predicted_outcome VARCHAR(50)
sentiment         VARCHAR(30)
barriers          JSONB
probability       FLOAT
confidence        FLOAT
raw_output        JSONB
created_at        TIMESTAMPTZ DEFAULT NOW()
```

**outcomes** (Phase 2 — create table now, populate later)
```
id                    UUID PRIMARY KEY DEFAULT gen_random_uuid()
prediction_id         UUID REFERENCES predictions(id)
actual_outcome        VARCHAR(100)
directional_accuracy  BOOLEAN
error_margin          FLOAT
behavior_match_score  FLOAT
recorded_at           TIMESTAMPTZ DEFAULT NOW()
```

**persona_updates** (Phase 2 — create table now, populate later)
```
id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
persona_id    VARCHAR(100)
trait_updates JSONB
triggered_by  UUID REFERENCES outcomes(id)
applied_at    TIMESTAMPTZ DEFAULT NOW()
```

### 2.5 database/redis_client.py

Simple wrapper around redis-py async client:
- `set_run_status(run_id, status)` — stores run state
- `get_run_status(run_id)` — retrieves run state
- `publish_event(run_id, event_data)` — publishes to Redis channel for SSE

---

## STEP 3: KNOWLEDGE GRAPH (KuzuDB)

### 3.1 graph/schema.py

Define the graph schema:

```python
NODE_TABLES = [
    """
    CREATE NODE TABLE IF NOT EXISTS Agent (
        agent_id STRING,
        persona_id STRING,
        segment STRING,
        state STRING,
        trust_level DOUBLE,
        price_sensitivity DOUBLE,
        digital_literacy DOUBLE,
        social_influence DOUBLE,
        religious_influence DOUBLE,
        platform_preference STRING,
        PRIMARY KEY (agent_id)
    )
    """,
    """
    CREATE NODE TABLE IF NOT EXISTS Concept (
        concept_id STRING,
        name STRING,
        category STRING,
        PRIMARY KEY (concept_id)
    )
    """
]

REL_TABLES = [
    """
    CREATE REL TABLE IF NOT EXISTS INFLUENCES (
        FROM Agent TO Agent,
        weight DOUBLE,
        channel STRING
    )
    """,
    """
    CREATE REL TABLE IF NOT EXISTS HOLDS_BELIEF (
        FROM Agent TO Concept,
        strength DOUBLE
    )
    """
]
```

### 3.2 graph/kuzu_client.py

- Initialize KuzuDB at path from config
- Run schema creation on startup
- Methods:
  - `create_agents(agents: list[dict])` — bulk insert
  - `get_agent_network(run_id)` — returns nodes + edges for viz
  - `query(cypher: str)` — raw query runner

### 3.3 graph/seed_data.py

Create 20 base Indian persona archetypes as seed JSON.
Must include:
```
T1_M_18_24_metro      ← Tier-1 urban young male
T1_F_25_34_metro      ← Tier-1 urban working woman
T2_M_25_34_UP         ← Tier-2 male, UP state
T2_F_35_44_Bihar      ← Tier-2 woman, Bihar
T3_M_45_54_rural      ← Rural senior male
KISAN_M_40_MP         ← Farmer, Madhya Pradesh
JOURNALIST_F_30       ← Journalist, metro
STUDENT_M_20_college  ← College student
RELIGIOUS_M_60        ← Religious community leader
WA_FORWARDER_M_50     ← WhatsApp forwarder, semi-urban
SHOPKEEPER_M_45_tier3 ← Small town shopkeeper
GENZ_F_19_metro       ← Gen Z metro female
OBC_M_30_UP           ← OBC male, rural UP
TECH_M_28_bangalore   ← Tech worker, Bangalore
MIGRANT_M_35_delhi    ← Migrant worker in Delhi
HOUSEWIFE_F_40_UP     ← Homemaker, UP
TRADER_M_50_gujarat   ← Trader, Gujarat
TEACHER_F_35_tier2    ← Government teacher
DOCTOR_M_45_metro     ← Urban doctor
STARTUP_F_27_metro    ← Female founder, metro
```

Each archetype must have all trait fields from the persona schema in CLAUDE.md.
Data must be grounded in NSSO, TRAI, Census 2011 statistics.
Add `data_sources` array to each persona listing which dataset.

---

## STEP 4: INTELLIGENCE LAYER

### 4.1 intelligence/llm_client.py

Wrapper around Anthropic client:

```python
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
```

System prompt must instruct Claude to:
1. ONLY respond in valid JSON
2. Format: `{"action": "...", "reasoning": "...", "decision": "...", "sentiment": "...", "barriers": []}`
3. Embody the persona traits provided
4. Consider the scenario variables

### 4.2 intelligence/react_agent.py

ReACT loop for each agent:

```
Round 1: Observe (read product/campaign info)
Round 2: Reason (apply persona traits to context)
Round 3: Act (decide: adopt/reject/ignore/share)
Round 4: Reflect (explain why, list barriers)
```

Each round is one LLM call.
Batch agents: run 50 agents concurrently using asyncio.gather.
Respect rate limits: add exponential backoff on 429.

---

## STEP 5: LAYER IMPLEMENTATIONS

Build in this exact order:

### 5.1 input_layer.py

```python
async def process(raw_input: dict) -> dict:
    """
    Validates: segment, industry, objective, product_description required.
    Normalizes: lowercase, strip whitespace, validate enums.
    Returns: structured input dict matching InputSchema.
    Raises: ValidationError with specific field errors.
    Logs: layer="input_layer", event="processed", data=output
    """
```

Supported segments (Phase 1):
`tier1_metro`, `tier2_urban`, `tier3_rural`, `mixed_india`

Supported industries (Phase 1):
`fintech`, `fmcg`, `edtech`, `healthtech`, `ecommerce`, `government`

### 5.2 persona_engine.py

```python
async def get_personas(segment: str, count: int) -> list[dict]:
    """
    Loads relevant personas from KuzuDB for this segment.
    If count > available seed personas, clones with variation.
    Returns: list of persona dicts.
    Logs: layer="persona_engine", event="loaded", data={"count": n}
    """
```

### 5.3 scenario_engine.py

```python
async def generate_scenarios(input_data: dict) -> list[dict]:
    """
    Always generates 3 scenarios minimum:
    1. optimistic   — best execution assumptions
    2. realistic    — average execution assumptions
    3. pessimistic  — worst execution assumptions

    If variables have unknowns (budget=unknown, targeting=unknown):
    Add 2 more scenarios covering those permutations.

    Returns: list of scenario dicts with name + variables.
    Logs: layer="scenario_engine", event="generated", data={"count": n}
    """
```

### 5.4 simulation_engine.py

```python
async def run_simulation(
    run_id: str,
    personas: list[dict],
    scenarios: list[dict],
    input_data: dict
) -> list[dict]:
    """
    For each scenario:
      - Select agent subset (default 1000 agents, configurable)
      - Run ReACT loop for each agent (batched async)
      - Aggregate: count decisions, average sentiment, collect barriers
      - Compute probability = adopters / total_agents
      - Compute confidence based on variance across agents
    Returns: list of prediction dicts.
    Updates Redis run status throughout.
    NEVER writes to PostgreSQL directly.
    Logs every step.
    """
```

### 5.5 output_layer.py

```python
async def structure_output(predictions: list[dict]) -> dict:
    """
    Aggregates all scenario predictions.
    Returns:
    {
      "best_case": prediction_dict,
      "worst_case": prediction_dict,
      "most_likely": prediction_dict,
      "key_driver": "string — top barrier/enabler",
      "sensitivity": "string — what variable matters most",
      "summary": "2 sentence plain English summary"
    }
    """
```

---

## STEP 6: ORCHESTRATOR

### 6.1 core/orchestrator.py

This file does ONE thing: coordinate the flow.
No business logic. No data processing.

```python
async def run(run_id: str, input_data: dict) -> dict:
    log(run_id, "orchestrator", "started")

    # 1. Input Layer
    normalized = await input_layer.process(input_data)
    await db.update_run(run_id, status="processing")

    # 2. Persona Engine
    personas = await persona_engine.get_personas(
        normalized["segment"],
        config.DEFAULT_AGENTS_PER_RUN
    )

    # 3. Scenario Engine
    scenarios = await scenario_engine.generate_scenarios(normalized)

    # 4. Simulation Engine
    predictions = await simulation_engine.run_simulation(
        run_id, personas, scenarios, normalized
    )

    # 5. Output Layer
    output = await output_layer.structure_output(predictions)

    # 6. Persist
    await db.save_predictions(run_id, predictions)
    await db.update_run(run_id, status="complete", output=output)
    await redis.set_run_status(run_id, "complete")

    log(run_id, "orchestrator", "complete")
    return output
```

---

## STEP 7: API ROUTES

### 7.1 POST /api/simulate

```json
Request:
{
  "segment": "tier2_male_25_34",
  "industry": "fintech",
  "objective": "signup",
  "product_description": "A UPI-based savings app for rural users",
  "agent_count": 1000
}

Response (immediate — run is async):
{
  "run_id": "uuid",
  "status": "pending",
  "estimated_duration_seconds": 45
}
```

Run simulation as background task (FastAPI BackgroundTasks).

### 7.2 GET /api/runs/{run_id}

```json
Response:
{
  "run_id": "uuid",
  "status": "running|complete|failed",
  "progress": 0.65,
  "output": null | { structured output when complete }
}
```

### 7.3 GET /api/runs/{run_id}/stream

Server-Sent Events endpoint.
Streams Redis pub/sub events for live UI updates.
Each event: `data: {"type": "agent_decision", "agent_id": "...", "decision": "..."}`

### 7.4 GET /api/personas

Returns all available persona archetypes.
Used by frontend persona explorer.

### 7.5 GET /health

```json
{ "status": "ok", "db": "ok", "redis": "ok", "kuzu": "ok" }
```

---

## STEP 8: main.py

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.init()
    await kuzu.init_schema()
    await kuzu.seed_if_empty()
    yield
    # Shutdown
    await db.close()

app = FastAPI(
    title="SATTVA API",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(simulation_router, prefix="/api")
app.include_router(persona_router, prefix="/api")
app.include_router(health_router)
```

---

## PHASE 1 COMPLETION CHECKLIST

Run through every item. Do not call Phase 1 done until all pass.

- [ ] `docker compose up` starts all services without errors
- [ ] `GET /health` returns `{"status": "ok"}` for all services
- [ ] `GET /api/personas` returns 20 Indian persona archetypes
- [ ] `POST /api/simulate` with valid input returns `run_id` instantly
- [ ] `GET /api/runs/{run_id}` shows status changing from pending → running → complete
- [ ] `GET /api/runs/{run_id}/stream` streams live agent events via SSE
- [ ] Completed run has predictions stored in PostgreSQL
- [ ] KuzuDB has agent nodes created for each run
- [ ] Every step produces a log entry in `./data/logs/{run_id}.jsonl`
- [ ] Simulation with 1000 agents completes in under 3 minutes
- [ ] Test with 3 different segments — all produce valid predictions
- [ ] Error handling: invalid input returns 422 with field-specific errors
- [ ] Error handling: Claude API failure triggers retry (3x) then fails gracefully

---

## PHASE 1 TEST COMMAND

```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "segment": "tier2_male_25_34",
    "industry": "fintech",
    "objective": "signup",
    "product_description": "A UPI-based savings app targeting rural UP users with zero account fees",
    "agent_count": 100
  }'
```

Expected: `{"run_id": "some-uuid", "status": "pending", "estimated_duration_seconds": 15}`

Then poll: `curl http://localhost:8000/api/runs/{run_id}`

Expected final: Full prediction JSON with probability, barriers, sentiment.

---

## WHEN PHASE 1 IS COMPLETE

Call it done. Open PHASE_2.md.
Do not begin Phase 2 work while Phase 1 checklist has any unchecked items.
