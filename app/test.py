# import asyncio
# from app.components.loader import load_documents_parallel
# from app.components.embedder import split_docs, embed_documents_parallel
# from app.components.vectordb import build_vector_db, search_vector_db

# async def test_parallel_load_and_embed():
#     docs = await load_documents_parallel("data/")
#     print(f"\nLoaded {len(docs)} documents.")

#     chunks = split_docs(docs)
#     print(f"\nSplit into {len(chunks)} chunks.")

#     embeddings = await embed_documents_parallel(chunks)
#     print(f"\nGenerated {len([e for e in embeddings if e is not None])} embeddings.")

#     vstore = build_vector_db(chunks)
#     print("\nVector DB created and persisted.")

#     results = search_vector_db("Where did the americans land?")
#     for idx, doc in enumerate(results):
#         print(f"\nResult {idx + 1}:\n{doc.page_content[:300]}...")

# asyncio.run(test_parallel_load_and_embed())

# from app.node_pool.retrieve_node import retriever_node

# state = {"question": "What is LangGraph?"}
# updated_state = retriever_node(state)

# print("\n--- Retrieved Chunks ---")
# for idx, chunk in enumerate(updated_state["retrieved_docs"]):
#     print(f"\nChunk {idx+1}:\n{chunk[:300]}...")

# from app.graph_manager import build_graph
# from typing import TypedDict, List, Optional

# # Define the GraphState TypedDict (must match what's in graph_manager.py)
# class GraphState(TypedDict, total=False):
#     question: str
#     retrieved_docs: List[str]
#     final_answer: str
#     trigger_tool_node: bool

# # Build the graph
# graph = build_graph()

# # Define the initial state
# state: GraphState = {
#     "question": "Who won the 2024 Nobel Prize in Literature?"
# }

# # Invoke the graph
# result = graph.invoke(state)

# # Print final output
# print("Final Answer:\n", result.get("final_answer", "No answer found."))

from app.state_manager.memory_state import RedisMemory

# Initialize Redis memory store
memory = RedisMemory()

# Define session and sample state
session_id = "session-001"
test_state = {
    "question": "Who invented penicillin?",
    "answer": "Alexander Fleming",
    "retrieved_docs": ["Some doc text...", "Another one..."]
}

# Save state
memory.save_state(session_id, test_state)
print("✅ State saved.")

# Retrieve state
retrieved = memory.get_state(session_id)
print("📦 Retrieved state:")
print(retrieved)

# Clear state (optional test)
# memory.clear_state(session_id)
# print("🧹 State cleared.")



