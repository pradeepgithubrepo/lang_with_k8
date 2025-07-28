# app/graph_executor.py

from app.graph_manager import build_graph
from app.state_manager.memory_state import RedisMemory
from typing import Dict, Any

class GraphWithMemory:
    def __init__(self):
        self.graph = build_graph()
        self.memory = RedisMemory()

    def run(self, session_id: str, input_state: Dict[str, Any]) -> Dict[str, Any]:
        previous_state = self.memory.get_state(session_id) or {}
        full_state = {**previous_state, **input_state}

        self.memory.save_state(session_id, full_state)
        result_state = self.graph.invoke(full_state)
        self.memory.save_state(session_id, result_state)

        return result_state
