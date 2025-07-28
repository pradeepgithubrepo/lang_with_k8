# app/main.py

from fastapi import FastAPI, Request, Depends,Query
from pydantic import BaseModel
from app.graph_manager import build_graph, GraphState
from app.security.auth import verify_api_key
from app.state_manager.memory_state import RedisMemory
from app.error_handler import add_exception_handlers

from app.monitoring.metrics import router as metrics_router
from app.monitoring.middleware import MetricsMiddleware

app = FastAPI(title="Enterprise RAG Agent")

# Register monitoring middleware and endpoint
app.add_middleware(MetricsMiddleware)
app.include_router(metrics_router)
add_exception_handlers(app)


# Initialize the Redis-based memory manager
memory = RedisMemory()

# Initialize the LangGraph at startup
graph = build_graph()

# Request schema
class QueryRequest(BaseModel):
    question: str

# Response schema
class QueryResponse(BaseModel):
    final_answer: str

@app.post("/ask", dependencies=[Depends(verify_api_key)], response_model=QueryResponse)
async def ask_question(query: QueryRequest, request: Request):
    session_id = "user123-session"  # This can later come from auth/user context

    # 1. Load prior turns (chat history) from Redis
    prior_turns = memory.get_chat_history(session_id)

    # 2. Create the LangGraph state with question and prior turns
    state: GraphState = {
        "question": query.question,
        "chat_history": prior_turns or []   # Default to empty if none
    }
    try:
        # 3. Run the graph with memory context
        result = graph.invoke(state)
        final_answer = result.get("final_answer", "No answer generated.")

        # 4. Append this new interaction back to Redis
        memory.append_turn(session_id, query.question, final_answer)

        return QueryResponse(final_answer=final_answer)

    except Exception as e:
        return QueryResponse(final_answer=f"Error: {str(e)}")



@app.get("/history")
async def get_chat_history(session_id: str = Query(...), api_key: str = Depends(verify_api_key)):
    """
    Retrieve the chat history for a given session_id.
    """
    try:
        history = memory.get_chat_history(session_id)
        return {"session_id": session_id, "chat_history": history}
    except Exception as e:
        return {"error": str(e)}
