from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.db.postgres import init_db
from backend.graph.kuzu_client import kuzu_client
from backend.graph.seed_data import seed_if_empty
from backend.api.routes import simulation, personas, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await kuzu_client.init()
    await kuzu_client.init_schema()
    await seed_if_empty(kuzu_client)
    yield
    # Shutdown
    # Add any cleanup if needed

app = FastAPI(
    title="[ SATTVA ] Behavioral Intelligence Engine",
    description="""
SATTVA is India's Behavioral Intelligence Engine.
A multi-agent simulation system that models how Indian citizens think, react, and behave.

### [ CAPABILITIES ]
- Multi-agent OASIS Simulation Engine
- ReACT Agent Intelligence (Claude Sonnet 3.5)
- KuzuDB Knowledge Graph (Indian Behavioral Ontologies)
- Real-world Validation & Feedback Loop
""",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(simulation.router, prefix="/api")
app.include_router(personas.router, prefix="/api")
app.include_router(health.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to SATTVA API"}
