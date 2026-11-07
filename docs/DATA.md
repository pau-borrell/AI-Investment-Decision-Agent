# Data inventory and provenance

| Asset | Purpose | Known limitations |
|---|---|---|
| data/raw/*.txt | Small educational knowledge corpus | Original URLs, authors, collection dates and redistribution terms are not recorded |
| data/evaluation_cases.json | Six qualitative scenario prompts | All expected_decision fields are null; not an accuracy benchmark |
| data/demo_snapshot.json | Synthetic sector fixture for offline tests and UI | Illustrative values, not actual or current asset metadata |
| data/portfolio_demo.json | Original demonstration portfolio | Inputs are proportions/amounts, not a historical performance dataset |
| Live Yahoo/yfinance | Asset types, sectors and optional adjusted prices | Availability, freshness, currency consistency and historical completeness are not guaranteed |

Files named investopedia_basics or financial_phrasebank_sample should not be assumed to be an official or complete dataset distribution. This repository does not document sufficient provenance to substantiate that claim. Verify original sources and reuse terms before expanding or redistributing the corpus.

The offline walkthrough fingerprints the exact local text files and synthetic metadata. It does not treat synthetic values as live market evidence. Unknown tickers and unclassified or unreported ETF weights remain Unknown rather than being treated as safe or diversified.

Portfolio amounts must use a common unit or base currency. There is no FX conversion. For prices, only aligned non-missing daily returns are used; missing prices are not forward-filled. No fees, taxes or corporate-event reconciliation beyond provider-adjusted prices is performed.
