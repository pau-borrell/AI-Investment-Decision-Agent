from src.rag.retrieval import retrieve_relevant_chunks
from src.rag.prompt_builder import build_rag_prompt
from src.rag.slm import generate_answer


def run_rag_pipeline(query: str) -> dict:
    retrieved_chunks = retrieve_relevant_chunks(query)
    prompt = build_rag_prompt(query, retrieved_chunks)
    answer = generate_answer(prompt)

    return {
        "query": query,
        "retrieved_chunks": retrieved_chunks,
        "prompt": prompt,
        "answer": answer
    }


def main():
    query = "Should I buy an ETF to improve diversification in my portfolio?"
    result = run_rag_pipeline(query)

    print("QUERY")
    print(result["query"])
    print("=" * 60)

    print("\nRETRIEVED SOURCES")
    for i, chunk in enumerate(result["retrieved_chunks"], start=1):
        print(f"{i}. {chunk['metadata']['source']} - {chunk['id']}")

    print("=" * 60)

    print("\nANSWER")
    print(result["answer"])


if __name__ == "__main__":
    main()