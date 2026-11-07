"""Dependency-free lexical retrieval for the explicitly offline walkthrough."""
import math
import re
from collections import Counter
from pathlib import Path
from src.rag.load_data import load_documents

STOPWORDS = {"the", "a", "an", "is", "of", "to", "in", "and", "or", "my", "i", "should", "if"}


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


def retrieve_offline(query: str, top_k: int = 3, data_dir: Path | None = None) -> list[dict]:
    if not query.strip() or not isinstance(top_k, int) or top_k <= 0:
        raise ValueError("Query must be nonempty and top_k positive.")
    data_dir = data_dir or Path(__file__).resolve().parents[2] / "data/raw"
    docs = load_documents(data_dir)
    counts = [Counter(tokens(d["text"])) for d in docs]
    terms = set(tokens(query))
    scored = []
    for doc, counts_doc in zip(docs, counts):
        score = sum((1 + math.log(counts_doc[t])) *
                    math.log(1 + len(docs) / (1 + sum(t in c for c in counts)))
                    for t in terms if counts_doc[t])
        if score > 0:
            scored.append({
                "id": "offline:" + doc["metadata"]["source"],
                "text": doc["text"], "metadata": doc["metadata"],
                "lexical_score": score,
            })
    return sorted(scored, key=lambda d: (-d["lexical_score"], d["id"]))[:top_k]
