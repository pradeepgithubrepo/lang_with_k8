import redis
import json
from typing import Optional, Dict, Any

class RedisMemory:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, ttl_seconds: int = 3600):
        """
        Initialize Redis client with given host, port, and database.
        TTL (Time to Live) sets the expiration time (in seconds) for each stored state.
        """
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.ttl = ttl_seconds

    def save_state(self, session_id: str, state: Dict[str, Any]) -> None:
        """
        Serialize and store the state in Redis with a TTL.
        - session_id: Unique identifier for the session (used as Redis key)
        - state: Dictionary containing the session state
        """
        serialized = json.dumps(state)
        self.client.setex(session_id, self.ttl, serialized)

    def get_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve and deserialize the session state from Redis.
        Returns None if no data is found.
        """
        value = self.client.get(session_id)
        if value:
            return json.loads(value)
        return None

    def clear_state(self, session_id: str) -> None:
        """
        Remove the state from Redis for the given session_id.
        """
        self.client.delete(session_id)
