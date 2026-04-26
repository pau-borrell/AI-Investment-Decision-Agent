# AI Investment Decision Agent

## Team Name
Erasmus

## Team Members
Natalia Patallo Suarez  
Pau Borrell Bullich  
Guilherme Chagas Silva  
Norbert Bara  
Ilayda Tiryaki  

## Project Description

This project develops an AI agent that assists investors in deciding whether to buy a particular stock or fund based on their existing investment portfolio.

Traditional financial assistants usually provide general market summaries or sentiment analysis but do not personalize recommendations according to the investor’s portfolio composition. Because of this, the same investment recommendation may not be appropriate for different investors.

The goal of this project is to build a portfolio-aware AI decision agent that combines financial knowledge retrieval, quantitative portfolio analysis tools, and reasoning capabilities from a fine-tuned Small Language Model (SLM).

The system will integrate several components including Retrieval-Augmented Generation (RAG), portfolio analysis tools, and an agent architecture capable of selecting tools and combining their outputs. Financial knowledge will be stored in a vector database and retrieved during inference to ground the model’s reasoning and reduce hallucinations.

The agent will produce structured recommendations including:
- A final decision (Buy / Do Not Buy / Neutral)
- Key reasoning
- Portfolio diversification analysis
- Concentration risk evaluation
- Possible alternative investments

## Architecture Overview

The system follows an agent-based architecture composed of several components:

User Query  
↓  
LLM Agent Controller  
↓  
Tool Selection  
↓  
Portfolio Memory + Analytical Tools  
↓  
Financial Knowledge Retrieval (RAG)  
↓  
Final Structured Recommendation  

## Technologies

Python  
Mistral 7B (fine-tuned SLM)  
LangChain / LlamaIndex  
ChromaDB (vector database)  
Sentence Transformers (embeddings)  
HuggingFace Transformers  
PEFT / LoRA fine-tuning  
yfinance (market data)

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/pau-borrell/AI-Investment-Decision-Agent
cd AI-Investment-Decision-Agent
```

Create a virtual environment (recommended):

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```


## Running the Project

### 1. Build the RAG Vector Database

This step processes the financial knowledge files, creates embeddings, and stores them in ChromaDB.

```bash
python -m src.rag.build_index
```

You should see output indicating:

* documents loaded
* chunks created
* embeddings generated
* database stored successfully


### 2. Start the Language Model (Ollama)

Make sure Ollama is installed and running locally.

Start the model:

```bash
ollama run mistral
```

Leave this running in the background.


### 3. Run the Investment Agent

```bash
python -m src.agent.run_agent
```

## Example Usage

Enter your portfolio:

```text
Holding: AAPL 3000
Holding: SPY 5000
Holding: done
```

Then enter your question:

```text
Question: Should I buy Nvidia if I already own a lot of technology stocks?
```

## Expected Output

The agent will return:

* Recommendation (Buy / Do Not Buy / Neutral)
* Justification based on retrieved knowledge
* Portfolio impact analysis
* Uncertainty explanation

It will also display:

* Retrieved knowledge sources
* Portfolio analysis results


## Repository

GitHub Repository:
https://github.com/pau-borrell/AI-Investement-Decision-Agent
