from pathlib import Path


from src.rag.embeddings import load_embedding_model
from src.rag.embeddings import embed_texts


CHROMA_PATH = Path("data/chroma_db")
COLLECTION_NAME = "financial_knowledge"
TOP_K = 5


def get_collection(path: Path = CHROMA_PATH, collection_name: str = COLLECTION_NAME):
    import chromadb
    client = chromadb.PersistentClient(path=str(path))
    collection = client.get_collection(name=collection_name)
    return collection


def retrieve_relevant_chunks(query: str, top_k: int = TOP_K) -> list[dict]:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Retrieval query cannot be empty.")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k <= 0:
        raise ValueError("top_k must be a positive integer.")
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return []
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, count)
    )

    retrieved_chunks = []

    for doc_id, text, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved_chunks.append(
            {
                "id": doc_id,
                "text": text,
                "metadata": metadata,
                "distance": distance
            }
        )

    return retrieved_chunks


def main():
    query = "Should I buy an ETF to improve diversification?"
    chunks = retrieve_relevant_chunks(query)

    print(f"Query: {query}")
    print(f"Retrieved {len(chunks)} chunks.\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"Result {i}")
        print(f"ID: {chunk['id']}")
        print(f"Source: {chunk['metadata']['source']}")
        print(f"Distance: {chunk['distance']}")
        print(chunk["text"])
        print("-" * 60)


if __name__ == "__main__":
    main()