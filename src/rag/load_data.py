from pathlib import Path

DATA_DIR = Path("data/raw")


def load_txt_file(file_path: Path) -> dict:
    text = file_path.read_text(encoding="utf-8").strip()
    return {
        "text": text,
        "metadata": {
            "source": file_path.name,
            "type": "txt"
        }
    }


def load_documents(data_dir: Path = DATA_DIR) -> list[dict]:
    documents = []

    if not data_dir.exists():
        raise FileNotFoundError(f"Folder not found: {data_dir}")

    txt_files = sorted(data_dir.glob("*.txt"))

    if not txt_files:
        raise ValueError(f"No .txt files found in {data_dir}")

    for file_path in txt_files:
        doc = load_txt_file(file_path)
        if doc["text"]:
            documents.append(doc)

    return documents


def main():
    documents = load_documents()

    print(f"Loaded {len(documents)} documents.\n")

    for i, doc in enumerate(documents, start=1):
        print(f"Document {i}")
        print(f"Source: {doc['metadata']['source']}")
        print(f"Type: {doc['metadata']['type']}")
        print(f"Characters: {len(doc['text'])}")
        print("Preview:")
        print(doc["text"][:250])
        print("-" * 50)


if __name__ == "__main__":
    main()