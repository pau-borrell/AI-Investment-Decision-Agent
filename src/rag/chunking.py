from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.load_data import load_documents


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def chunk_documents(documents: list[dict], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    for doc_index, doc in enumerate(documents):
        text = doc["text"]
        metadata = doc["metadata"]

        split_texts = splitter.split_text(text)

        for chunk_index, chunk_text in enumerate(split_texts):
            chunks.append(
                {
                    "id": f"doc_{doc_index}_chunk_{chunk_index}",
                    "text": chunk_text,
                    "metadata": {
                        "source": metadata["source"],
                        "type": metadata["type"],
                        "doc_index": doc_index,
                        "chunk_index": chunk_index
                    }
                }
            )

    return chunks


def main():
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.\n")

    for i, chunk in enumerate(chunks[:10], start=1):
        print(f"Chunk {i}")
        print(f"ID: {chunk['id']}")
        print(f"Source: {chunk['metadata']['source']}")
        print(f"Chunk index: {chunk['metadata']['chunk_index']}")
        print(f"Characters: {len(chunk['text'])}")
        print("Text:")
        print(chunk["text"])
        print("-" * 60)


if __name__ == "__main__":
    main()