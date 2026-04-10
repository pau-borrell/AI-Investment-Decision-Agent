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

## Repository Structure

data/ datasets and financial knowledge base
src/ project source code
src/agent/ LLM agent implementation
src/rag/ retrieval pipeline
src/tools/ portfolio analysis tools
src/evaluation/ evaluation scripts
notebooks/ experiments and exploration
docs/ project documentation

## Repository

GitHub Repository:
https://github.com/pau-borrell/AI-Investement-Decision-Agent
