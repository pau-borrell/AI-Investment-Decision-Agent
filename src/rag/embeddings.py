from sentence_transformers import SentenceTransformer

from src.rag.load_data import load_documents
from src.rag.chunking import chunk_documents


MODEL_NAME = "BAAI/bge-base-en"


def load_embedding_model(model_name: str = MODEL_NAME):
    model = SentenceTransformer(model_name)
    return model


def embed_chunks(chunks: list[dict], model) -> list[list[float]]:
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    return embeddings.tolist()


def main():
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.")

    model = load_embedding_model()
    embeddings = embed_chunks(chunks, model)

    print(f"Generated {len(embeddings)} embeddings.")
    print(f"Embedding dimension: {len(embeddings[0])}")

    print("\nFirst chunk preview:")
    print(chunks[0]["text"])

    print("\nFirst embedding preview (first 10 values):")
    print(embeddings[0][:10])


if __name__ == "__main__":
    main()