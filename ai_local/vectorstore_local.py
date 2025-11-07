# vectorstore_local.py
# Compatible with new Chroma client API (2024+)

import os
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

_client = None
_collection = None

def get_client():
    """Create or return the Chroma persistent client."""
    global _client
    if _client is None:
        # New API: PersistentClient replaces chromadb.Client(Settings(...))
        from chromadb import PersistentClient
        _client = PersistentClient(path=CHROMA_DIR)
    return _client

def get_collection(name="workwise_docs"):
    """Return or create the main document collection."""
    global _collection
    client = get_client()
    try:
        _collection = client.get_collection(name)
    except Exception:
        _collection = client.create_collection(name)
    return _collection

def add_documents(doc_texts, embeddings, metadatas, ids=None):
    """Add documents to collection."""
    coll = get_collection()
    if ids is None:
        ids = [f"doc_{i}" for i in range(len(doc_texts))]
    coll.add(
        documents=doc_texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    # Persist to disk
    client = get_client()
    if hasattr(client, "persist"):
        client.persist()

def query(query_embeddings, n_results=5, filter=None):
    """Query the collection for similar documents."""
    coll = get_collection()
    res = coll.query(
        query_embeddings=query_embeddings,
        n_results=n_results,
        where=filter
    )
    return res
