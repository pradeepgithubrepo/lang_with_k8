import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.utility import Helperclass
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

helper = Helperclass()
embed_model = helper.gemini_client()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def split_docs(documents):
    return text_splitter.split_documents(documents)

def embed_single_chunk(chunk):
    try:
        return embed_model.embed_query(chunk.page_content)
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        return None

async def embed_documents_parallel(chunks: list) -> list:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=10) as executor:
        embeddings = await asyncio.gather(*[
            loop.run_in_executor(executor, embed_single_chunk, chunk)
            for chunk in chunks
        ])
    return embeddings
