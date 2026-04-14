import os
from dotenv import load_dotenv

load_dotenv()

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
MAX_AGENTS_PER_RUN = int(os.getenv("MAX_AGENTS_PER_RUN", "10000"))
DEFAULT_AGENTS_PER_RUN = int(os.getenv("DEFAULT_AGENTS_PER_RUN", "1000"))
CLAUDE_MAX_TOKENS_PER_AGENT = int(os.getenv("CLAUDE_MAX_TOKENS_PER_AGENT", "300"))

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
KUZU_DB_PATH = os.getenv("KUZU_DB_PATH", "./data/kuzu_graph")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
