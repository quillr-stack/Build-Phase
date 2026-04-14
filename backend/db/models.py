from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from backend.db.postgres import Base

class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    status = Column(String(20), nullable=False, default="pending")
    input = Column(JSONB, nullable=False)
    agent_count = Column(Integer, nullable=False, default=1000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    output = Column(JSONB)

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    run_id = Column(UUID(as_uuid=True), ForeignKey("simulations.id"))
    name = Column(String(100))
    variables = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    run_id = Column(UUID(as_uuid=True), ForeignKey("simulations.id"))
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenarios.id"))
    predicted_outcome = Column(String(50))
    sentiment = Column(String(30))
    barriers = Column(JSONB)
    probability = Column(Float)
    confidence = Column(Float)
    raw_output = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id"))
    actual_outcome = Column(String(100))
    directional_accuracy = Column(Boolean)
    error_margin = Column(Float)
    behavior_match_score = Column(Float)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

class PersonaUpdate(Base):
    __tablename__ = "persona_updates"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    persona_id = Column(String(100))
    trait_updates = Column(JSONB)
    triggered_by = Column(UUID(as_uuid=True), ForeignKey("outcomes.id"))
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
