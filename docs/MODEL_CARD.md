# Model and system card

## Intended use

A local educational prototype for inspectable portfolio analytics and retrieval-grounded language generation. It is useful for demonstrating orchestration, uncertainty reporting, data quality and evaluation engineering.

## Models

Default local generation: Ollama mistral. Optional generation: a user-supplied Hugging Face base model and LoRA adapter. Semantic embeddings: BAAI/bge-base-en. The original Kaggle guide describes synthetic fine-tuning; CI neither trains nor validates an adapter. Model and dataset licenses remain those of the original providers.

No fine-tuned weights are committed. A community Ollama model mentioned in older setup instructions is not equivalent to a verified training artifact or a pinned model digest.

## Output and abstention

Requested sections: Recommendation, Justification, Portfolio impact, Uncertainty. Allowed labels: Buy, Do Not Buy, Neutral. Missing evidence should produce Neutral with an insufficient-data explanation. Proposed trade size, asset valuation and investor objectives are generally absent, so current portfolio risk alone cannot substantiate a candidate's marginal diversification benefit.

Validation checks exact section order, nonempty content, an allowed single decision and citation-ID membership. It does not establish that the recommendation is correct, suitable, safe or supported by the cited passage.

## Known failure modes

- Financial or numerical hallucinations despite a valid response format.
- Prompt injection through the user query or retrieved text.
- Tiny corpus coverage and lexical/semantic retrieval mismatches.
- Stale or missing ETF metadata and unmeasured constituent overlap.
- Bias inherited from base models or synthetic training examples.
- Context truncation, generation latency and hardware-specific failures.
- Heuristic thresholds that have not been optimized or validated for investor outcomes.

## Evaluation status

Offline numerical invariants and orchestration behaviors have reproducible tests. CI smoke-tests the UI and mocked model/provider boundaries. Live six-case ablations remain formatting diagnostics, with no reference decisions and no financial-performance ground truth. Fresh live generation, adapter quality, retrieval relevance and claim-level grounding require separate evaluation.

Useful follow-up experiments: expert-labeled factual claims, adversarial retrieval cases, numeric consistency checks, retrieved-passage relevance labels, abstention precision/recall, and repeat runs with pinned model digests. None are represented as completed benchmarks.
