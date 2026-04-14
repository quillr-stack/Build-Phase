import kuzu
import os
from backend.core import config
from backend.graph import schema

class KuzuClient:
    def __init__(self):
        self.db = None
        self.conn = None

    async def init(self):
        os.makedirs(config.KUZU_DB_PATH, exist_ok=True)
        self.db = kuzu.Database(config.KUZU_DB_PATH)
        self.conn = kuzu.Connection(self.db)

    async def init_schema(self):
        # Check if tables exist by trying to query them or using a try-except block
        # For simplicity in Phase 1, we attempt to create and ignore errors if they exist
        for statement in schema.NODE_TABLES:
            try:
                self.conn.execute(statement)
            except Exception:
                pass

        for statement in schema.REL_TABLES:
            try:
                self.conn.execute(statement)
            except Exception:
                pass

    async def create_agents(self, agents: list[dict]):
        for agent in agents:
            # Prepare query
            query = """
            CREATE (a:Agent {
                agent_id: $agent_id,
                persona_id: $persona_id,
                segment: $segment,
                state: $state,
                trust_level: $trust_level,
                price_sensitivity: $price_sensitivity,
                digital_literacy: $digital_literacy,
                social_influence: $social_influence,
                religious_influence: $religious_influence,
                platform_preference: $platform_preference
            })
            """
            self.conn.execute(query, agent)

    async def get_agent_network(self, run_id):
        # In Phase 1, we just return nodes. Edges are Phase 2.
        query = "MATCH (a:Agent) RETURN a.*"
        result = self.conn.execute(query)
        nodes = []
        while result.has_next():
            nodes.append(result.get_next())
        return {"nodes": nodes, "edges": []}

    async def query(self, cypher: str, params: dict = None):
        if params:
            return self.conn.execute(cypher, params)
        return self.conn.execute(cypher)

kuzu_client = KuzuClient()
