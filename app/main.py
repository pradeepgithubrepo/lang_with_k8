# app/main.py

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from app.graph_manager import build_graph, GraphState
from app.security.auth import verify_api_key
app = FastAPI(title="Enterprise RAG Agent")

# Build the LangGraph graph once during app startup
graph = build_graph()

# Request body schema
class QueryRequest(BaseModel):
    question: str

# Response schema
class QueryResponse(BaseModel):
    final_answer: str

@app.post("/ask",dependencies=[Depends(verify_api_key)], response_model=QueryResponse)
async def ask_question(query: QueryRequest, request: Request):
    # Construct the state with the question
    state: GraphState = {
        "question": query.question
    }

    try:
        result = graph.invoke(state)
        final_answer = result.get("final_answer", "No answer generated.")
        return QueryResponse(final_answer=final_answer)
    except Exception as e:
        return QueryResponse(final_answer=f"Error: {str(e)}")
