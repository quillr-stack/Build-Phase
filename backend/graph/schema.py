NODE_TABLES = [
    """
    CREATE NODE TABLE Agent (
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
    CREATE NODE TABLE Concept (
        concept_id STRING,
        name STRING,
        category STRING,
        PRIMARY KEY (concept_id)
    )
    """
]

REL_TABLES = [
    """
    CREATE REL TABLE INFLUENCES (
        FROM Agent TO Agent,
        weight DOUBLE,
        channel STRING
    )
    """,
    """
    CREATE REL TABLE HOLDS_BELIEF (
        FROM Agent TO Concept,
        strength DOUBLE
    )
    """
]
