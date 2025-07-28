from typing import Dict, Any

def fallback_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["final_answer"] = (
        "I couldn’t find the answer in my current knowledge base. "
        "I’ll now try to fetch it from the internet using a tool."
    )
    state["trigger_tool_node"] = True  # Used to branch in the graph
    return state
