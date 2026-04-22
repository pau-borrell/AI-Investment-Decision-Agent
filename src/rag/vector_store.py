from pathlib import Path

import chromadb

from src.rag.load_data import load_documents
from src.rag.chunking import chunk_documents
from src.rag.embeddings import load_embedding_model, embed_chunks


CHROMA_PATH = Path("data/chroma_db")
COLLECTION_NAME = "financial_knowledge"


def get_chroma_client(path: Path = CHROMA_PATH):
    path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(path))
    return client


def create_collection(client, collection_name: str = COLLECTION_NAME):
    existing_collections = [c.name for c in client.list_collections()]
    if collection_name in existing_collections:
        client.delete_collection(collection_name)
    collection = client.create_collection(name=collection_name)
    return collection


def store_chunks(collection, chunks: list[dict], embeddings: list[list[float]]):
    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def main():
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.")

    model = load_embedding_model()
    embeddings = embed_chunks(chunks, model)

    print(f"Generated {len(embeddings)} embeddings.")

    client = get_chroma_client()
    collection = create_collection(client)

    store_chunks(collection, chunks, embeddings)

    print(f"Stored {collection.count()} chunks in ChromaDB.")
    print(f"Database path: {CHROMA_PATH}")
    print(f"Collection name: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()