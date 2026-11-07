# Portfolio-aware AI Investment Agent

A local-language-model project combining financial document retrieval with quantitative portfolio tools. It makes the evidence behind an answer inspectable: retrieved passages, normalized weights, concentration flags, sector coverage and response validation travel with every result.

Built by **Team Erasmus**: Natalia Patallo Suarez, Pau Borrell Bullich, Guilherme Chagas Silva, Norbert Bara and Ilayda Tiryaki.

## Explore in two minutes

Python 3.10–3.12. From the repository root, run the dependency-free offline walkthrough:

```bash
python -m src.demo --out outputs/offline_demo.json
```

This computes real analytics over **synthetic fixture metadata** and retrieves local educational snippets using lexical matching. It makes no network calls, downloads no model, and produces no AI recommendation.

For the interactive walkthrough:

```bash
python -m venv .venv
# Activate on macOS/Linux: source .venv/bin/activate
# Activate on Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-demo.txt
streamlit run app.py
```

Edit holdings, inspect weights and sector look-through, review coverage warnings and retrieved snippets, then download the analysis as JSON. This interface demonstrates the analytics and retrieval workflow; the live LLM pipeline runs separately below.

## What is implemented

| Component | Implementation |
|---|---|
| Orchestration | One-pass Python controller: retrieve, analyze, build prompt, generate, validate |
| Local generation | Ollama/Mistral or Hugging Face base model + LoRA adapter |
| Semantic RAG | Local text corpus, BGE embeddings, ChromaDB and source IDs |
| Portfolio tools | Validated weights, position HHI, concentration and ETF sector look-through |
| Scenarios | Seeded historical bootstrap with ticker-aligned returns; optional |
| Offline demonstration | Dependency-free lexical retrieval and synthetic metadata, with fingerprints |
| Evaluation | Model-only / RAG-only / RAG + tools format diagnostics |
| Quality checks | Unit tests, mocked orchestration/provider checks, Streamlit smoke tests and CI |

The controller is a bounded one-pass workflow, not an autonomous trading agent. LangChain text splitting is used for indexing; an LLM does not dynamically select or execute arbitrary tools. No order execution is implemented.

## Run the live local-model pipeline

Install the semantic retrieval dependencies:

```bash
python -m pip install -r requirements-rag.txt
python -m src.rag.build_index
ollama pull mistral
ollama serve
```

Run the agent in a separate terminal:

```bash
python scripts/demo.py --query "What concentration risks are present?" --portfolio "AAPL=45,MSFT=35,SPY=20" --save-output outputs/live_demo.jsonl
```

Or use interactive portfolio entry:

```bash
python -m src.agent.run_agent
```

The first semantic-index build downloads the embedding model. Ollama must be installed separately; model size and hardware affect latency. No OpenAI account or API key is required. The offline walkthrough does not validate local model availability.

Index creation refuses to replace an existing collection accidentally. Use `python -m src.rag.build_index --rebuild` to deliberately replace it.

Configuration is read from environment variables; [.env.example](.env.example) documents them but is not automatically loaded. For example:

| Variable | Default / purpose |
|---|---|
| SLM_BACKEND | ollama; alternatively hf |
| OLLAMA_MODEL | mistral; set explicitly for an adapter-derived model |
| OLLAMA_URL | http://localhost:11434/api/generate |
| HF_BASE_MODEL_PATH | Local base-model directory, required for hf |
| HF_LORA_ADAPTER_PATH | models/mistral7b-lora |
| HF_MAX_NEW_TOKENS | 256 |

For Hugging Face/LoRA training and merging, install `requirements-finetune.txt` and follow the original [Kaggle training guide](docs/kaggle_finetune_notebook.md). Those GPU workflows and community model weights are optional and are not trained or downloaded by CI. Training dependencies are bounded rather than a hardware-specific lockfile.

## Analytics and data contracts

Portfolio values are amounts or weights in **one consistent currency/unit**. Duplicate tickers are aggregated, names normalized and values renormalized. Negative, non-finite, boolean, empty and zero-total inputs are rejected; this is a long-only model.

Position HHI is the sum of squared position weights; effective positions is its reciprocal. HHI across ETF positions does **not** measure constituent overlap or full economic diversification. Concentration thresholds are illustrative heuristics.

Stock and ETF sector names share a canonical vocabulary. Missing metadata and incomplete ETF coverage remain **Unknown**, with coverage warnings; cash is represented separately. Live Yahoo metadata may fail or be stale, and current metadata cannot establish historical exposure.

Optional `--simulate` scenarios use aligned adjusted-price returns and a seeded historical bootstrap. They assume daily rebalancing and zero cash yield, omit currency conversion, taxes and transaction costs, and do not model serial dependence or future regime changes. Outcomes are labeled by the requested horizon, not always one year.

## Reproducible example

The synthetic offline fixture uses AAPL 45%, MSFT 35%, SPY 20%, with deliberately incomplete illustrative ETF metadata:

| Check | Expected |
|---|---:|
| Position HHI | 0.365 |
| Effective positions | 2.740 |
| Technology exposure | 86.0% |
| Known sector/cash weight | 96.0% |

These are software reference values for synthetic inputs, **not measured current fund composition**. The exported JSON includes snapshot and corpus SHA-256 fingerprints. No investment-performance result is claimed.

## Tests and evaluation

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
# Dependency-free core checks:
python -m unittest discover -s tests -p test_core.py -v
```

The automated suite contains **35 passing tests**. CI tests Python 3.10 and 3.12, exercises the local UI without a model, and uploads offline JSON artifacts. It does not call Yahoo, start Ollama or download embeddings.

For live ablations after building the index and starting Ollama:

```bash
python -m src.evaluation.evaluate --cases data/evaluation_cases.json --out outputs
```

See [evaluation methodology](docs/evaluation_report.md). Heading/keyword compliance does not measure correctness, grounding or investment returns. The six existing cases have no reference decisions; the evaluator reports the labeled denominator explicitly. No fresh live-model benchmark is claimed.

## Architecture, provenance and limitations

- [Architecture and execution boundaries](docs/architecture.md)
- [Model behavior and limitations](docs/MODEL_CARD.md)
- [Data sources and missing provenance](docs/DATA.md)
- [Development and contribution guide](CONTRIBUTING.md)

Generated model responses remain untrusted. Format and source-ID checks can flag malformed answers and fabricated IDs, but cannot prove claim-level support or resist every prompt injection. The prompt requests abstention when trade details or evidence are missing; no runtime decision-quality guarantee is implied.

This is a financial education and software demonstration, not a validated investment advisory or trading system. The project has no declared repository license; no new license is imposed on the original team contributions or third-party materials.
