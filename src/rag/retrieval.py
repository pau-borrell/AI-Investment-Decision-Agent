from pathlib import Path

import chromadb

from src.rag.embeddings import load_embedding_model


CHROMA_PATH = Path("data/chroma_db")
COLLECTION_NAME = "financial_knowledge"
TOP_K = 5


def get_collection(path: Path = CHROMA_PATH, collection_name: str = COLLECTION_NAME):
    client = chromadb.PersistentClient(path=str(path))
    collection = client.get_collection(name=collection_name)
    return collection


def retrieve_relevant_chunks(query: str, top_k: int = TOP_K) -> list[dict]:
    model = load_embedding_model()
    query_embedding = model.encode([query], convert_to_numpy=True)[0].tolist()

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
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