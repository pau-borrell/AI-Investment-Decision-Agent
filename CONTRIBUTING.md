# Contributing

Use Python 3.10–3.12 and install requirements-dev.txt. Run python -m pytest -q and python -m src.demo before opening a pull request. CI must remain independent of network calls to model or market providers.

Inject providers in tests rather than downloading model weights. Keep offline fixtures visibly synthetic. Treat missing metadata as unknown, and document changes to financial assumptions or simulation methods.

Add a regression test for numerical or validation fixes. Include source URLs, collection dates and reuse terms for new corpus data. Do not commit portfolio data from real users, local model weights, credentials or generated outputs.

The original team retains credit for the project. There is currently no declared repository license; agree licensing with the contributors before distributing under a new license.
