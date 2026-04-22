from pathlib import Path

import chromadb

from src.rag.load_data import load_documents
from src.rag.chunking import chunk_documents
from src.rag.embeddings import load_embedding_model, embed_chunks
from src.rag.vector_store import get_chroma_client, create_collection, store_chunks


CHROMA_PATH = Path("data/chroma_db")
COLLECTION_NAME = "financial_knowledge"


def query_collection(collection, query_text: str, model, top_k: int = 3):
    query_embedding = model.encode([query_text], convert_to_numpy=True)[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


def main():
    print("STEP 1: Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.\n")

    print("STEP 2: Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks.\n")

    print("STEP 3: Loading embedding model...")
    model = load_embedding_model()
    print("Embedding model loaded.\n")

    print("STEP 4: Generating embeddings...")
    embeddings = embed_chunks(chunks, model)
    print(f"Generated {len(embeddings)} embeddings.\n")

    print("STEP 5: Storing in ChromaDB...")
    client = get_chroma_client(CHROMA_PATH)
    collection = create_collection(client, COLLECTION_NAME)
    store_chunks(collection, chunks, embeddings)
    print(f"Stored {collection.count()} chunks in collection '{COLLECTION_NAME}'.\n")

    print("STEP 6: Testing retrieval...")
    test_query = "Should I buy an ETF to improve diversification in my portfolio?"
    results = query_collection(collection, test_query, model, top_k=3)

    print(f"Test query: {test_query}\n")

    retrieved_docs = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]
    retrieved_ids = results["ids"][0]

    for i, (doc_id, metadata, text) in enumerate(zip(retrieved_ids, retrieved_metadatas, retrieved_docs), start=1):
        print(f"Result {i}")
        print(f"ID: {doc_id}")
        print(f"Source: {metadata['source']}")
        print(f"Chunk index: {metadata['chunk_index']}")
        print("Text:")
        print(text)
        print("-" * 60)


if __name__ == "__main__":
    main()