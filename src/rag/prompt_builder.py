def build_rag_prompt(query: str, retrieved_chunks: list[dict]) -> str:
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk["metadata"]["source"]
        text = chunk["text"]

        context_parts.append(
            f"Source {i}: {source}\n{text}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a financial education assistant.

Answer the user's question using only the retrieved context below.
If the context does not contain enough information, say "insufficient data".

Do not invent facts.
Do not give personalized financial advice.
Explain the answer clearly and mention uncertainty when relevant.

Retrieved context:
{context}

User question:
{query}

Answer:
""".strip()

    return prompt


def main():
    sample_chunks = [
        {
            "text": "ETFs can improve diversification because they provide exposure to many assets.",
            "metadata": {"source": "sample.txt"}
        }
    ]

    query = "Should I buy an ETF?"
    prompt = build_rag_prompt(query, sample_chunks)

    print(prompt)


if __name__ == "__main__":
    main()