from src.rag.rag_pipeline import run_rag_pipeline


def main():
    query = input("Enter your financial question: ")

    result = run_rag_pipeline(query)

    print("\nANSWER")
    print(result["answer"])

    print("\nRETRIEVED SOURCES")
    for i, chunk in enumerate(result["retrieved_chunks"], start=1):
        print(f"{i}. {chunk['metadata']['source']} - {chunk['id']}")


if __name__ == "__main__":
    main()