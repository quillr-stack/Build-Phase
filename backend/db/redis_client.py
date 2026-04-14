import redis.asyncio as redis
import json
from backend.core import config

class RedisClient:
    def __init__(self):
        self.client = redis.from_url(config.REDIS_URL, decode_responses=True)

    async def set_run_status(self, run_id, status):
        await self.client.set(f"run:{run_id}:status", status)

    async def get_run_status(self, run_id):
        return await self.client.get(f"run:{run_id}:status")

    async def publish_event(self, run_id, event_data):
        await self.client.publish(f"run:{run_id}:events", json.dumps(event_data))

redis_client = RedisClient()
