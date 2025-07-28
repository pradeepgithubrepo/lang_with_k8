from typing import Dict, Any
from app.components.vectordb import search_vector_db

def retriever_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Inside retriever_node: state =", state)
    query = state.get("question")
    if not query:
        raise ValueError("Missing 'question' in state for retrieval.")
    
    relevant_docs = search_vector_db(query)
    retrieved_chunks = [doc.page_content for doc in relevant_docs]
    
    # Add retrieved chunks to the state
    state["retrieved_docs"] = retrieved_chunks
    return state
