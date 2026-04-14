# SATTVA — Master Project DNA
# This file is the single source of truth for Claude Code.
# Read this entire file before writing a single line of code.

---

## WHAT IS SATTVA

SATTVA is India's Behavioral Intelligence Engine.
NOT a survey tool. NOT a chatbot. NOT another AI demo.

It is a multi-agent simulation system that models how Indian citizens
think, react, and behave — before a brand, policy, or product ever
reaches them. One simulation run replaces a ₹40 Lakh McKinsey report.

End state: Every org that needs Indian consumer intelligence calls
SATTVA's API. It becomes infrastructure — not a product.

---

## ABSOLUTE RULES (Never Break These)

1. Do NOT mix business logic into the Orchestrator. It routes only.
2. Simulation Engine NEVER writes directly to DB. Always via Orchestrator.
3. Every execution step MUST be logged. No silent operations.
4. Validation Engine is NOT optional. It runs on every simulation that
   has real-world outcome data attached.
5. All inter-module communication uses structured JSON only.
6. No cross-layer logic. Input Layer handles input. Persona Engine handles
   personas. Never bleed one into another.
7. The feedback loop is sacred. Every prediction must eventually be
   compared to reality. This is the moat.

---

## CONFIRMED TECH STACK (Locked — Do Not Substitute)

### Backend
- **FastAPI** (Python) — async, clean, production-ready
- **Python 3.11+**

### Simulation Core
- **OASIS Engine** — forked from MiroFish, modified for India context
  - Replace Reddit propagation with WhatsApp/Facebook community graphs
  - Agent count target: 10,000 per run
  - Multi-round emergent behavior (not single-pass LLM)

### Knowledge Graph
- **KuzuDB** — embedded graph DB, no external server needed
  - Stores: persona relationships, behavioral ontologies, social networks
  - Primary schema: nodes(agents) ↔ edges(relationships/influence)

### Agent Intelligence
- **ReACT pattern** — Reason + Act loop for each agent
- **Claude API** (claude-sonnet-4-20250514) — LLM backbone
  - Max tokens per agent call: 300 (keep costs lean)
  - Batch agent calls where possible

### Storage
- **PostgreSQL** — structured data (simulations, predictions, outcomes)
- **Redis** — session cache, run status, real-time updates
- **Local filesystem / S3-compatible** — raw logs, report artifacts

### Frontend
- **Next.js 14** (App Router)
- **Three.js** — 3D particle visualization of agent network
- **D3.js** — knowledge graph visualization, behavioral charts
- **Tailwind CSS** — utility classes only, no component libraries

### Infrastructure
- **Docker + Docker Compose** — all services containerized
- **Single machine deployable** — no Kubernetes for Phase 1-2

---

## VISUAL IDENTITY (Non-Negotiable)

SATTVA is exclusive. The UI must feel like a Bloomberg Terminal
crossed with a classified intelligence dashboard. Not a startup SaaS.

### Color Palette (Exact Hex)
```
--sattva-cream:     #F2EDE3   /* Primary background — warm parchment */
--sattva-navy:      #0D2240   /* Primary text, heavy elements */
--sattva-navy-mid:  #1B3A6B   /* Cards, borders, map elements */
--sattva-navy-light:#4A7AB5   /* Hover states, secondary elements */
--sattva-green:     #2D7A4F   /* Success, positive metrics, SATTVA accent */
--sattva-amber:     #C8961A   /* Warning, analytics metrics, highlights */
--sattva-grid:      #C8BFB0   /* Blueprint grid lines */
--sattva-white:     #FFFFFF   /* Text on dark backgrounds */
--sattva-muted:     #8A8070   /* Secondary text, labels */
```

### Typography
```
Font Stack:
- Display/Headers:  'Space Grotesk', sans-serif (bold 700/800)
- Body:             'Inter', sans-serif (400/500)
- Monospace/Labels: 'JetBrains Mono', monospace (labels, stats, code)
  → ALL [ BRACKET ] labels use JetBrains Mono
  → ALL metrics/numbers use JetBrains Mono
```

### Design Language
- Background: cream parchment (`#F2EDE3`) with subtle topographic grid
- Labels ALWAYS formatted as: `[ COMPONENT NAME ]` — brackets, monospace, uppercase
- Corner crosshair markers on panels: `+` in each corner
- Thin rule lines (0.5px) for borders and dividers
- No rounded corners > 4px on data panels (sharp, technical)
- Cards: slight navy border + cream bg. No shadows — flat technical.
- 3D visualization: dark navy canvas (`#060D1A`) with navy-blue particles

### Page Philosophy (Critical)
- Google-product style: ONE primary action per page
- No long scroll pages. Dense, informative, above the fold.
- Status always visible: run state, agent count, progress
- Every number is live. Nothing static that should be dynamic.

---

## PROJECT FOLDER STRUCTURE

```
sattva/
├── CLAUDE.md                    ← This file
├── docker-compose.yml
├── .env.example
│
├── backend/
│   ├── main.py                  ← FastAPI entry point
│   ├── requirements.txt
│   │
│   ├── core/
│   │   ├── orchestrator.py      ← Routes only. No logic.
│   │   ├── logger.py            ← Logs every step
│   │   └── config.py            ← Env vars, constants
│   │
│   ├── layers/
│   │   ├── input_layer.py       ← Normalize + validate input
│   │   ├── persona_engine.py    ← Persona profiles + traits
│   │   ├── scenario_engine.py   ← Multi-scenario generation
│   │   ├── simulation_engine.py ← OASIS + ReACT agents
│   │   ├── output_layer.py      ← Aggregate + structure results
│   │   └── validation_engine.py ← Prediction vs reality scoring
│   │
│   ├── intelligence/
│   │   ├── react_agent.py       ← ReACT loop implementation
│   │   ├── llm_client.py        ← Claude API wrapper
│   │   └── feedback_loop.py     ← Model improvement logic
│   │
│   ├── graph/
│   │   ├── kuzu_client.py       ← KuzuDB connection + queries
│   │   ├── schema.py            ← Graph schema definitions
│   │   └── seed_data.py         ← Indian persona seed data
│   │
│   ├── db/
│   │   ├── postgres.py          ← PostgreSQL connection
│   │   ├── redis_client.py      ← Redis operations
│   │   └── models.py            ← SQLAlchemy models
│   │
│   └── api/
│       ├── routes/
│       │   ├── simulation.py    ← POST /simulate, GET /runs
│       │   ├── personas.py      ← GET /personas
│       │   ├── outcomes.py      ← POST /outcomes (validation input)
│       │   └── health.py        ← GET /health
│       └── schemas.py           ← Pydantic request/response models
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx             ← Dashboard / run launcher
│   │   ├── run/[id]/page.tsx    ← Live simulation view
│   │   ├── results/[id]/page.tsx← Results + report
│   │   └── personas/page.tsx    ← Persona explorer
│   │
│   ├── components/
│   │   ├── ui/                  ← Reusable SATTVA design system
│   │   │   ├── Panel.tsx        ← [ BRACKET ] labeled panel
│   │   │   ├── MetricCard.tsx   ← Stat display
│   │   │   ├── StatusBadge.tsx  ← Run status indicator
│   │   │   └── BracketLabel.tsx ← [ LABEL ] component
│   │   │
│   │   ├── viz/
│   │   │   ├── AgentGraph3D.tsx ← Three.js particle network
│   │   │   ├── KnowledgeGraph.tsx ← D3 graph viz
│   │   │   └── BehaviorChart.tsx  ← D3 outcome charts
│   │   │
│   │   └── simulation/
│   │       ├── RunLauncher.tsx  ← Input form + launch
│   │       ├── LiveFeed.tsx     ← Real-time agent activity
│   │       └── ResultsPanel.tsx ← Final output display
│   │
│   ├── lib/
│   │   ├── api.ts               ← Backend API client
│   │   └── colors.ts            ← SATTVA color constants
│   │
│   └── styles/
│       └── globals.css          ← CSS variables + base styles
│
└── data/
    ├── personas/                ← Indian persona JSON seeds
    └── ontologies/              ← Behavioral ontology files
```

---

## DATA MODELS (Core)

### Simulation Run
```json
{
  "run_id": "uuid",
  "input": {
    "segment": "tier2_male_25_34",
    "industry": "fintech",
    "objective": "signup",
    "product_description": "string",
    "variables": {}
  },
  "status": "pending|running|complete|failed",
  "agent_count": 1000,
  "scenarios": [],
  "predictions": [],
  "created_at": "iso8601",
  "completed_at": "iso8601"
}
```

### Persona Profile
```json
{
  "persona_id": "T2_M_25_34_UP_001",
  "segment": "tier2_male_25_34",
  "state": "uttar_pradesh",
  "traits": {
    "trust_level": 0.3,
    "price_sensitivity": 0.85,
    "digital_literacy": 0.55,
    "social_influence": 0.6,
    "religious_influence": 0.7,
    "platform_preference": "whatsapp"
  },
  "data_sources": ["NSSO", "TRAI", "Census2011"]
}
```

### Prediction (Output)
```json
{
  "prediction_id": "uuid",
  "run_id": "uuid",
  "scenario": "string",
  "predicted_outcome": "low_conversion|medium_conversion|high_conversion",
  "sentiment": "skeptical|neutral|positive",
  "barriers": ["trust", "complexity", "price"],
  "probability": 0.28,
  "confidence": 0.72
}
```

### Validation Record (THE MOAT)
```json
{
  "validation_id": "uuid",
  "prediction_id": "uuid",
  "actual_outcome": "string",
  "directional_accuracy": true,
  "error_margin": 0.12,
  "behavior_match_score": 0.81,
  "recorded_at": "iso8601"
}
```

---

## ENV VARIABLES (.env.example)

```
# API Keys
ANTHROPIC_API_KEY=

# PostgreSQL
DATABASE_URL=postgresql://sattva:password@localhost:5432/sattva_db

# Redis
REDIS_URL=redis://localhost:6379

# KuzuDB
KUZU_DB_PATH=./data/kuzu_graph

# App
ENVIRONMENT=development
LOG_LEVEL=INFO
MAX_AGENTS_PER_RUN=10000
DEFAULT_AGENTS_PER_RUN=1000
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS_PER_AGENT=300

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## BUILD ORDER (Strict)

Phase 1 → Phase 2 → Phase 3.
Never skip. Never work ahead.
Each phase produces a working system. Not a partial one.

PHASE_1.md = Backend foundation + core simulation loop
PHASE_2.md = Intelligence layer + validation + feedback loop
PHASE_3.md = UI/UX + 3D visualization + API hardening

---

## WHAT SUCCESS LOOKS LIKE

Phase 1 done: You can POST a simulation request and get a prediction JSON back.
Phase 2 done: Predictions improve over time as validation data flows in.
Phase 3 done: You can demo SATTVA live to an investor in under 3 minutes.
