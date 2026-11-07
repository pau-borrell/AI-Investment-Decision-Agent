"""One-pass retrieval/tool orchestration with injectable dependencies."""
import time
from src.agent.agent_controller import decide_tools
from src.agent.agent_prompt import build_agent_prompt
from src.agent.response import validate_answer
from src.tools.portfolio_input import validate_portfolio


def run_investment_agent(query: str, portfolio: dict | None = None, *,
                         retriever=None, analyzer=None, generator=None,
                         run_simulation: bool = False) -> dict:
    if not isinstance(query, str) or not query.strip() or len(query) > 10000:
        raise ValueError("Question must contain 1–10000 characters.")
    if portfolio is not None:
        portfolio = validate_portfolio(portfolio)
    if retriever is None:
        from src.rag.retrieval import retrieve_relevant_chunks
        retriever = retrieve_relevant_chunks
    if analyzer is None:
        from src.tools.analyze_portfolio import analyze_portfolio
        analyzer = analyze_portfolio
    if generator is None:
        from src.rag.slm import generate_answer
        generator = generate_answer
    start = time.perf_counter()
    decisions = decide_tools(query)
    # An explicit portfolio must be analyzed even without a routing keyword.
    decisions["use_portfolio_tools"] = portfolio is not None
    warnings = []
    try:
        retrieved = retriever(query) if decisions["use_rag"] else []
    except Exception as exc:
        retrieved = []
        warnings.append(f"Retrieval unavailable ({type(exc).__name__}).")
    analysis = None
    if portfolio is not None:
        analysis = analyzer(portfolio, run_simulation=run_simulation)
        warnings.extend(analysis.get("warnings", []))
    prompt = build_agent_prompt(query, retrieved, analysis)
    answer = generator(prompt)
    validation = validate_answer(answer, {c["id"] for c in retrieved})
    return {
        "query": query, "decisions": decisions, "retrieved_chunks": retrieved,
        "portfolio_analysis": analysis, "prompt": prompt, "answer": answer,
        "validation": validation, "warnings": warnings,
        "elapsed_ms": (time.perf_counter() - start) * 1000,
    }
