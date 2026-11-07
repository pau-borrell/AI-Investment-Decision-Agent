# Evaluation methodology and status

## Reproducible automated coverage

CI runs the dependency-free core suite plus NumPy/Pandas scenarios, mocked Ollama and retrieval boundaries, and Streamlit AppTest checks on Python 3.10 and 3.12.

The tests check duplicate aggregation, invalid holdings, scale invariance, sector alias merging, incomplete ETF coverage, unknown-data warnings, cash handling, ticker-aligned returns, single-ticker download shapes, no implicit forward fill, bootstrap repeatability, exact response structure, citation IDs, injected orchestration, lexical retrieval, offline determinism and UI error handling.

These are software checks. They do not prove that an LLM recommendation is financially correct.

## Offline artifact

Run:

```bash
python -m src.demo --out outputs/offline_demo.json
```

The result contains synthetic analytics, retrieved passages and SHA-256 fingerprints. It declares that it uses no LLM and supplies no recommendation. CI uploads this artifact for inspection.

## Live ablations

After installing requirements-rag.txt, building the index and starting local Ollama:

```bash
python -m src.evaluation.evaluate --cases data/evaluation_cases.json --out outputs
```

| Mode | Inputs to generation |
|---|---|
| model_only | Question plus general financial-education instructions; no retrieval/tools |
| rag_only | Question and retrieved knowledge |
| rag_tools | Question, retrieved knowledge and computed portfolio analysis |

Outputs: timestamped per-case JSONL and summary JSON with backend/model configuration. Runs with retrieval, analytics or generation errors exit nonzero after saving diagnostics.

The evaluator reports exact structure validity, individual headings, keyword mentions, retrieved count, errors and optional expected-decision matches. The reference-labeled denominator is explicit. All six bundled cases currently have expected_decision=null: decision accuracy is therefore **not measured**.

## Historical notes

The previous report recorded a 2026-05-12 run with six structured outputs per mode, but committed raw generations, model digests and complete run metadata were absent. Those notes cannot serve as a reproduced benchmark for this revision. No new live-model results are claimed.

## Limits and next experiments

Heading and keyword counts can be gamed and should never be interpreted as quality scores. Source-ID membership is weaker than claim-level citation support. The tiny corpus and six cases cannot establish generalization or investment performance.

A stronger study would fix model digests and data snapshots, label retrieval relevance and factual claims, measure numerical consistency and abstention, review adversarial documents, and compare models on a larger held-out set. Proposed trade parameters and historical outcome ground truth are needed for claims about decision utility.
