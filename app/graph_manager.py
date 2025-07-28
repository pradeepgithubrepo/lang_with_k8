from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from typing import Dict, Any , Optional,TypedDict,List

from app.node_pool.retrieve_node import retriever_node
from app.node_pool.generate_node import generate_node
from app.node_pool.fallback_node import fallback_node
from app.node_pool.tools import tool_node

# Shared state structure
class GraphState(TypedDict, total=False):
    question: str
    retrieved_docs: List[str]
    final_answer: str
    trigger_tool_node: bool

class NodeWrapper(Runnable):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def invoke(self, input: GraphState, config: Optional[dict] = None, **kwargs) -> GraphState:
        print(f"Node `{self.func.__name__}` received input:\n{input}")
        return self.func(input)
    
# Define the graph
def build_graph() -> Runnable:
    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node("retrieve", NodeWrapper(retriever_node))
    graph.add_node("generate", NodeWrapper(generate_node))
    graph.add_node("fallback", NodeWrapper(fallback_node))
    graph.add_node("tool", NodeWrapper(tool_node))

    # Edges
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")

    # Conditional route after generation
    def decide_next_node(state: GraphState) -> str:
        answer = state.get("final_answer", "").lower()
        
        if not answer.strip():
            return "fallback"

        fallback_signals = [
            "sorry", 
            "i can't", 
            "based on the given context", 
            "i don't know", 
            "insufficient context"
        ]
        
        if any(signal in answer for signal in fallback_signals):
            return "fallback"

        return END


    graph.add_conditional_edges("generate", decide_next_node)

    # Fallback route (if RAG fails)
    def check_tool_needed(state: GraphState) -> str:
        return "tool" if state.get("trigger_tool_node") else END

    graph.add_conditional_edges("fallback", check_tool_needed)
    graph.add_edge("tool", END)

    return graph.compile()
