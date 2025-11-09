# embeddings_local.py
# Provides local embedding creation using sentence-transformers

from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Model selection: all-MiniLM-L6-v2 is small and fast
EMBED_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model

def embed_texts(texts):
    """
    texts: list[str]
    returns: list[list[float]] embeddings
    """
    model = get_model()
    embs = model.encode(texts, normalize_embeddings=True)
    # convert to python lists
    return [list(map(float, e)) for e in embs]
