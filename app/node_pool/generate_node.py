from typing import Dict, Any
from app.utility import Helperclass
from langchain_core.messages import HumanMessage

helper = Helperclass()
llm = helper.openai_client()

def generate_node(state: Dict[str, Any]) -> Dict[str, Any]:
    question = state.get("question")
    retrieved_docs = state.get("retrieved_docs", [])

    context = "\n\n".join(retrieved_docs)
    prompt = f"""
    Answer the user's question based only on the context below.
    
    Context:
    \"\"\"
    {context}
    \"\"\"

    Question: {question}
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])

    state["final_answer"] = response.content.strip()
    return state
