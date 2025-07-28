import redis
import json
from typing import Optional, Dict, Any, List

class RedisMemory:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, ttl_seconds: int = 3600):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.ttl = ttl_seconds

    # --- Existing session-level state methods ---
    def save_state(self, session_id: str, state: Dict[str, Any]) -> None:
        serialized = json.dumps(state)
        self.client.setex(session_id, self.ttl, serialized)

    def get_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        value = self.client.get(session_id)
        if value:
            return json.loads(value)
        return None

    def clear_state(self, session_id: str) -> None:
        self.client.delete(session_id)

    # --- NEW: Chat threading methods ---
    def append_turn(self, session_id: str, question: str, answer: str) -> None:
        key = f"thread:{session_id}"
        turn = {"question": question, "answer": answer}
        self.client.rpush(key, json.dumps(turn))
        self.client.expire(key, self.ttl)

    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        key = f"thread:{session_id}"
        history = self.client.lrange(key, 0, -1)
        return [json.loads(item) for item in history]

    def clear_chat_history(self, session_id: str) -> None:
        key = f"thread:{session_id}"
        self.client.delete(key)
