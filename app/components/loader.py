import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import List
import logging

from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SUPPORTED_TYPES = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
}

def get_loader(file_path: str):
    ext = Path(file_path).suffix.lower()
    loader_cls = SUPPORTED_TYPES.get(ext)
    return loader_cls(file_path) if loader_cls else None

async def load_file(file_path: str) -> List[Document]:
    loop = asyncio.get_event_loop()
    loader = get_loader(file_path)
    if not loader:
        logger.warning(f"Unsupported file type for: {file_path}")
        return []

    return await loop.run_in_executor(None, loader.load)

async def load_documents_parallel(source_dir: str) -> List[Document]:
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Directory '{source_dir}' does not exist.")

    all_files = [
        str(p) for p in Path(source_dir).rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_TYPES
    ]

    logger.info(f"Found {len(all_files)} files to load.")
    tasks = [load_file(fp) for fp in all_files]
    results = await asyncio.gather(*tasks)

    docs = [doc for result in results for doc in result]  # flatten
    logger.info(f"Loaded {len(docs)} documents from {source_dir}")
    return docs
