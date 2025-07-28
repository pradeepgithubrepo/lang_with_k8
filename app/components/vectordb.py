import os
from typing import List
from langchain_core.documents import Document
from langchain.vectorstores import FAISS
from app.utility import Helperclass

helper = Helperclass()
embedding_model = helper.gemini_client()

DB_PATH = "local_db"

def build_vector_db(chunks: List[Document]) -> FAISS:
    vstore = FAISS.from_documents(chunks, embedding_model)
    vstore.save_local(DB_PATH)
    return vstore

def load_vector_db() -> FAISS:
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Vector DB directory not found.")
    return FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)


def search_vector_db(query: str, k: int = 3) -> List[Document]:
    vstore = load_vector_db()
    return vstore.similarity_search(query, k=k)
