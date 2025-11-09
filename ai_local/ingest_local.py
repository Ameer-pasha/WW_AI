# ingest_local.py
# Chunking, embedding and storing pieces in Chroma

from .embeddings_local import embed_texts
from .vectorstore_local import add_documents
from datetime import datetime
import math

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_OVERLAP = 200

def chunk_text(text, chunk_size=DEFAULT_CHUNK_SIZE, overlap=DEFAULT_OVERLAP):
    if not text:
        return []
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= L:
            break
        start = end - overlap
    return chunks

def ingest_text(employee_id, source, text, extra_meta=None):
    """
    employee_id: int or str
    source: str e.g. "user_post", "github_readme"
    text: str
    extra_meta: dict
    Returns: number of chunks stored
    """
    extra_meta = extra_meta or {}
    chunks = chunk_text(text)
    if not chunks:
        return 0
    embeddings = embed_texts(chunks)
    # prepare metadata and ids
    now = datetime.utcnow().isoformat()
    metadatas = []
    ids = []
    for i, ch in enumerate(chunks):
        md = {"employee_id": str(employee_id), "source": source, "created_at": now}
        md.update(extra_meta)
        metadatas.append(md)
        ids.append(f"{employee_id}_{source}_{int(datetime.utcnow().timestamp())}_{i}")
    add_documents(doc_texts=chunks, embeddings=embeddings, metadatas=metadatas, ids=ids)
    return len(chunks)
