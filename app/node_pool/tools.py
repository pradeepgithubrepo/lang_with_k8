from typing import Dict, Any
from duckduckgo_search import DDGS


def duckduckgo_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            if results:
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
            else:
                return "No web results found."
    except Exception as e:
        return f"Web search failed due to: {str(e)}"


def tool_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("[tool_node] Invoking DuckDuckGo search...")
    query = state.get("question")
    if not query:
        raise ValueError("Missing 'question' for tool node.")

    print(f"[tool_node] Triggered for query: {query}")
    search_result = duckduckgo_search(query)

    # Add final answer from web
    state["final_answer"] = f"(From DuckDuckGo Search)\n{search_result}"
    return state
