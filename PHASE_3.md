# SATTVA — PHASE 2: INTELLIGENCE LAYER
# Read CLAUDE.md first. Always.
# Prerequisite: Phase 1 checklist 100% complete.
# Goal: SATTVA learns. Predictions improve over time. The moat begins.

---

## PHASE 2 OBJECTIVE

Phase 1 SATTVA predicts. Phase 2 SATTVA learns.

By end of Phase 2:
1. Real-world outcomes can be fed back into the system
2. Validation engine scores every prediction against reality
3. Persona traits and scenario weights auto-adjust
4. Prediction accuracy improves measurably run-over-run

This is not a nice-to-have. This is the entire business defensibility.
Every day this loop runs = competitive moat grows.

---

## STEP 1: VALIDATION ENGINE

### 1.1 validation_engine.py

The most important file in the codebase.

```python
async def validate(
    prediction_id: str,
    actual_outcome: str,
    actual_metrics: dict  # whatever real data the client provides
) -> dict:
    """
    Compares prediction vs reality.
    Computes:
    - directional_accuracy: bool (did we get the direction right?)
    - error_margin: float (how far off was the probability?)
    - behavior_match_score: float 0-1 (how well did barriers match?)
    - barrier_accuracy: dict (which barriers were correct?)

    Stores result in outcomes table.
    Triggers feedback_loop.process() automatically.
    Returns: validation_record dict
    """
```

### Scoring Logic

**Directional Accuracy** (binary):
- Predicted "low_conversion" (probability < 0.4) AND actual conversion was low → True
- Any directional mismatch → False

**Error Margin** (float):
- `abs(predicted_probability - actual_probability)`
- If actual probability unknown, estimate from client metrics
  (e.g., 50 signups from 1000 impressions = 0.05 actual probability)

**Behavior Match Score** (float 0–1):
- Client confirms which barriers were real
- Score = confirmed_barriers / predicted_barriers
- Weight trust/price barriers 1.5x (more impactful in India)

**Overall Accuracy Score**:
```
score = (directional_accuracy * 0.5) +
        ((1 - error_margin) * 0.3) +
        (behavior_match_score * 0.2)
```

---

## STEP 2: FEEDBACK LOOP ENGINE

### 2.1 intelligence/feedback_loop.py

```python
async def process(validation_record: dict) -> dict:
    """
    Takes validation output.
    Updates persona traits and scenario weights.
    Returns: summary of what was updated.
    """
```

### Persona Trait Adjustment Logic

If directional_accuracy = False:
- Get all personas used in that run
- Identify which traits most influenced the wrong prediction
  (stored in raw_output from Phase 1)
- Adjust those traits by ±0.05 (small, incremental, never drastic)
- Cap all traits between 0.0 and 1.0

Examples:
```
Predicted: trust would not be a barrier → actually WAS a barrier
Action: increase trust_level weight for that segment by 0.05

Predicted: price_sensitivity low → actually HIGH barrier
Action: increase price_sensitivity for that segment by 0.05
```

### Scenario Weight Recalibration

Each scenario (optimistic/realistic/pessimistic) has a weight.
Initial: optimistic=0.25, realistic=0.50, pessimistic=0.25

After each validation:
- Whichever scenario was CLOSEST to actual → increase its weight by 0.05
- Whichever was furthest → decrease by 0.05
- Normalize weights to sum to 1.0

Store per-industry, per-segment. Not global.

### Update Storage

After each feedback cycle, save to `persona_updates` table:
```json
{
  "persona_id": "T2_M_25_34_UP",
  "trait_updates": {
    "trust_level": {"old": 0.30, "new": 0.35, "reason": "validation_id_xyz"}
  },
  "triggered_by": "validation_id"
}
```

Also update KuzuDB agent nodes with new trait values.

---

## STEP 3: OUTCOME INPUT API

### 3.1 New Route: POST /api/outcomes

This is how clients feed reality back in.

```json
Request:
{
  "run_id": "uuid",
  "actual_outcome": "conversion_rate_0.08",
  "actual_metrics": {
    "impressions": 10000,
    "conversions": 800,
    "drop_off_stage": "trust_verification",
    "confirmed_barriers": ["trust", "kyc_complexity"]
  },
  "notes": "Campaign ran for 2 weeks in UP and Bihar"
}

Response:
{
  "validation_id": "uuid",
  "accuracy_score": 0.74,
  "directional_accuracy": true,
  "error_margin": 0.04,
  "behavior_match_score": 0.81,
  "what_was_updated": {
    "persona_traits_adjusted": 3,
    "scenario_weights_recalibrated": true
  }
}
```

### 3.2 GET /api/runs/{run_id}/accuracy

Returns accuracy history for a run's predictions.
```json
{
  "run_id": "uuid",
  "validation": {
    "status": "validated|pending",
    "accuracy_score": 0.74,
    "validated_at": "iso8601"
  }
}
```

---

## STEP 4: INTELLIGENCE METRICS

These 18 metrics are SATTVA's signature output.
Reference: slide deck says "18 Decision Intelligence Metrics."

Compute these in `output_layer.py` for every run.

### Core Behavioral Metrics (8)
```
1.  adoption_probability      — % of agents who would adopt
2.  trust_gap_score           — how much trust deficit exists (0-10)
3.  price_sensitivity_index   — how price-driven the decision is (0-10)
4.  viral_potential           — likelihood of organic sharing (0-10)
5.  barrier_density           — count of distinct barriers encountered
6.  decision_speed            — how fast agents decide (fast/medium/slow)
7.  social_influence_factor   — how much peer opinion matters (0-10)
8.  digital_readiness_score   — segment's tech comfort level (0-10)
```

### Market Dynamics Metrics (5)
```
9.  narrative_diffusion_rate  — how fast info spreads in this segment
10. trust_shift_potential     — how much trust could improve with intervention
11. polarisation_index        — how divided the segment is on this product
12. market_entry_difficulty   — composite score (0-10)
13. competitor_displacement   — how easily segment would switch away
```

### Strategic Metrics (5)
```
14. optimal_channel           — WhatsApp|Facebook|YouTube|offline|word-of-mouth
15. message_resonance_score   — how well current framing lands (0-10)
16. trust_trigger_list        — top 3 things that would increase trust
17. conversion_bottleneck     — single biggest conversion killer
18. recommended_entry_vector  — which sub-segment to target first
```

Store all 18 as structured JSON in the predictions output.
Display all 18 in the frontend (Phase 3).

---

## STEP 5: ANALYTICS ENGINE

### 5.1 New module: layers/analytics_engine.py

```python
async def compute_metrics(
    predictions: list[dict],
    personas: list[dict],
    scenarios: list[dict]
) -> dict:
    """
    Computes all 18 Decision Intelligence Metrics.
    Called by output_layer after predictions are assembled.
    Returns: metrics dict with all 18 values.
    """
```

Rules for metric computation:
- All scores 0-10 must be normalized from raw agent data
- `optimal_channel` is plurality vote from agent platform_preference + decision pathway
- `trust_trigger_list` = top 3 most common barrier reversals across agents
- `conversion_bottleneck` = highest-frequency barrier in pessimistic scenario

---

## STEP 6: SYSTEM ACCURACY TRACKING

### 6.1 New Route: GET /api/system/accuracy

Returns aggregate accuracy across ALL validated runs.

```json
{
  "total_runs": 47,
  "validated_runs": 23,
  "overall_accuracy": 0.71,
  "directional_accuracy": 0.83,
  "by_segment": {
    "tier2_male_25_34": { "accuracy": 0.74, "runs": 8 },
    "tier1_metro": { "accuracy": 0.69, "runs": 6 }
  },
  "by_industry": {
    "fintech": { "accuracy": 0.78, "runs": 12 }
  },
  "trend": "improving",
  "accuracy_delta_last_10_runs": "+0.06"
}
```

This endpoint powers the live accuracy dashboard in Phase 3 UI.
This is what an investor sees. This is what makes SATTVA credible.

### 6.2 New DB View: v_accuracy_summary

Create a PostgreSQL view that joins simulations + predictions + outcomes
to power the accuracy API without slow queries.

---

## STEP 7: PERSONA VERSIONING

Every time a persona's traits are updated by the feedback loop,
create a new version. Never overwrite history.

```sql
CREATE TABLE persona_versions (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  persona_id      VARCHAR(100) NOT NULL,
  version         INTEGER NOT NULL,
  traits          JSONB NOT NULL,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  source          VARCHAR(50),  -- 'seed' | 'feedback_loop' | 'manual'
  validation_id   UUID REFERENCES outcomes(id)
);
```

`persona_engine.py` always fetches the latest version.
Old versions preserved for audit and rollback.

---

## STEP 8: ENHANCED SIMULATION ENGINE

Upgrade `simulation_engine.py` for Phase 2:

### Multi-Round Simulation

Phase 1 had single ReACT round. Phase 2 adds social propagation.

After initial agent decisions:
- Round 2: High social_influence agents see their network's decisions
  (query KuzuDB INFLUENCES edges)
- Round 3: Mid-influence agents optionally update based on Round 2
- Final: Re-aggregate outcomes

This is what makes SATTVA "emergent" — decisions change based on
social network effects. Not just individual agent reasoning.

Implementation:
```
Round 1: Individual decision (existing ReACT loop)
Round 2: Network propagation (KuzuDB query neighbors → update if influenced)
Round 3: Final decision lock
```

Only 3 rounds for Phase 2. More rounds = diminishing returns + cost.

### WhatsApp/Facebook Graph Simulation

Replace OASIS's Reddit propagation model with India-specific channels:

**WhatsApp Groups (70% of agents):**
- Group size: 50-200 members
- Propagation: High-trust, high-velocity within family/community groups
- Forwarding probability: Depends on agent's `wa_forwarder` trait

**Facebook Community Pages (20% of agents):**
- Reach: Wider but lower trust
- Propagation: Likes/shares model

**Offline Word-of-Mouth (10% of agents):**
- Tier 3/rural agents
- Slow propagation, very high trust

When seeding the KuzuDB graph for a run:
- Create WhatsApp group clusters based on segment geography
- Create INFLUENCES edges with `channel: "whatsapp"` or `channel: "facebook"`
- Weight edges: WhatsApp edges get trust_multiplier = 1.5

---

## PHASE 2 COMPLETION CHECKLIST

- [ ] POST /api/outcomes accepts real-world data and stores validation record
- [ ] Validation engine computes accuracy_score for every outcome submitted
- [ ] Feedback loop updates persona traits after each validation
- [ ] Persona trait updates saved to persona_versions table
- [ ] GET /api/system/accuracy returns aggregate accuracy data
- [ ] All 18 Decision Intelligence Metrics computed in every run output
- [ ] Multi-round simulation runs (3 rounds: individual → network → final)
- [ ] WhatsApp/Facebook graph propagation working in simulation
- [ ] System accuracy demonstrably improves after 3+ validated runs
- [ ] Run 5 simulations, submit outcomes, verify traits updated in DB
- [ ] KuzuDB agent nodes reflect updated traits post-feedback
- [ ] No performance regression: 1000-agent run still completes < 5 minutes

---

## VALIDATION TEST SEQUENCE

After Phase 2 is built, run this exact sequence:

```bash
# Run 1: Fintech, Tier-2 UP
POST /api/simulate → run_id_1

# Submit outcome for Run 1
POST /api/outcomes {
  "run_id": "run_id_1",
  "actual_outcome": "conversion_rate_0.05",
  "actual_metrics": {
    "impressions": 5000,
    "conversions": 250,
    "confirmed_barriers": ["trust", "kyc_complexity"]
  }
}

# Run 2: Same segment, same industry
POST /api/simulate (same params)

# Compare Run 1 vs Run 2 predictions
# Run 2 should show higher trust_gap_score and lower adoption_probability
# This proves the feedback loop worked
GET /api/system/accuracy → should show improvement
```

---

## WHEN PHASE 2 IS COMPLETE

The system is now a learning system, not just a prediction tool.
That sentence is the pitch. Investors buy that sentence.

Open PHASE_3.md.
