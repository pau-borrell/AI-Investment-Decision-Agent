from src.rag.retrieval import retrieve_relevant_chunks
from src.rag.prompt_builder import build_rag_prompt


def generate_answer_without_llm(query: str, retrieved_chunks: list[dict]) -> str:
    if not retrieved_chunks:
        return "Insufficient data."

    context_summary = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks[:3]
    )

    answer = f"""
Based on the retrieved financial knowledge, the main relevant points are:

{context_summary}

This suggests that ETFs can help improve diversification because they provide exposure to a broad range of assets. However, diversification does not eliminate overall market risk, and the final decision depends on the user's existing portfolio, risk tolerance, and concentration exposure.
""".strip()

    return answer


def run_rag_pipeline(query: str) -> dict:
    retrieved_chunks = retrieve_relevant_chunks(query)
    prompt = build_rag_prompt(query, retrieved_chunks)
    answer = generate_answer_without_llm(query, retrieved_chunks)

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

    print("\nGENERATED PROMPT")
    print(result["prompt"])

    print("=" * 60)

    print("\nANSWER")
    print(result["answer"])


if __name__ == "__main__":
    main()