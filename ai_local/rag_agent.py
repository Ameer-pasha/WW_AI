# rag_agent.py
# RAG orchestration: retrieve relevant docs, form prompt, call local LLaMA

from .vectorstore_local import query
from .llama_local import call_local_llama
from .embeddings_local import embed_texts
import json

SYSTEM_PROMPT = """You are WorkWise AI. Use the evidence below and employee metadata to provide:
1) 3 short actionable recommendations (bullet list).
2) 1 concise empathetic sentence.
3) Provide short rationales and a confidence score (0-100) for each recommendation.
Return valid JSON with keys: recommendations (list of dict), emotional_support (string), citations (list).
"""

def build_prompt(employee_meta: dict, retrieved_docs: list, user_question: str):
    meta_json = json.dumps(employee_meta, indent=0)
    evidence_parts = []
    for i, (doc_text, meta) in enumerate(retrieved_docs):
        s = f"[{i}] source={meta.get('source')} employee_id={meta.get('employee_id')} created_at={meta.get('created_at')}\n{doc_text}"
        evidence_parts.append(s)
    evidence_str = "\n\n---\n\n".join(evidence_parts) if evidence_parts else "No evidence available."

    prompt = f"""{SYSTEM_PROMPT}

Employee Metadata:
{meta_json}

User Question:
{user_question}

Evidence:
{evidence_str}

Instructions:
- Use only the evidence above when citing facts.
- Provide exactly 3 recommendations.
- Output plain JSON only, no extra commentary.
"""
    return prompt


def retrieve_for_employee(employee_id, question_text, top_k=5):
    """
    Create embedding for the question, and search in Chroma for similar docs for that employee.
    """
    # Convert the question into an embedding
    query_vector = embed_texts([question_text])[0]

    # Query vector DB for matching docs of this employee
    res = query(
        query_embeddings=[query_vector],
        n_results=top_k,
        filter={"employee_id": str(employee_id)}
    )

    docs = []
    if res and "documents" in res:
        documents = res.get("documents", [[]])[0]
        metadatas = res.get("metadatas", [[]])[0]
        for d, m in zip(documents, metadatas):
            docs.append((d, m))
    return docs


def ask(employee_meta, employee_id, question, top_k=5):
    docs = retrieve_for_employee(employee_id, question, top_k=top_k)
    prompt = build_prompt(employee_meta, docs, question)
    answer = call_local_llama(prompt)
    return answer
