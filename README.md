
# AI-Powered Fitness Assistant (Colab Notebook)

An AI-enabled fitness assistant built entirely in a Google Colab Notebook using LLM agents and vector search to help users manage health profiles, store notes, and receive personalized answers to fitness-related questions.

---

## Problem Statement

Users often struggle to consistently track their fitness data, organize logs, and receive relevant guidance tailored to their goals. Existing solutions either lack personalization or fail to leverage external context like live search results. This project bridges that gap by integrating retrieval-augmented generation and intelligent decision routing in an interactive notebook environment.

---

## Why AI Agents?

This solution utilizes AI agents to:
- Contextually respond to user queries using profile data and stored notes
- Detect when information is insufficient and trigger a live web search
- Seamlessly orchestrate multi-step reasoning using LangGraph

### Why Multi-Agent Architecture?

Multi-agent design enables:
- Modular role-specific agents (retriever, router, responder, searcher)
- Conditional decision-making on whether to include web search
- Greater control over flow, context management, and debugging

---

## Application Overview

**Environment**: Google Colab  
**Interface**: Gradio (launched inside Colab)  
**Workflow Engine**: LangGraph  
**LLM**: LLaMA3-70B via Groq API  
**Vector Store**: Astra DB (CassandraDB)  
**Embedding Model**: all-MiniLM-L6-v2 (via HuggingFace)  
**Web Search**: SerpAPI  

---

## Features

- User profile setup (age, height, weight, fitness goal)
- Note submission with timestamp and vector embedding
- Intelligent question answering using LLM + retrieved context
- Dynamic web search fallback when profile data is insufficient
- Notes view and deletion via interactive interface

---

## Agent Workflow

| Agent              | Responsibility                               |
|-------------------|-----------------------------------------------|
| Context Loader     | Fetches user profile and relevant notes      |
| Routing Agent      | Determines if web search is needed           |
| Web Search Agent   | Gathers latest information using SerpAPI     |
| Answer Agent       | Synthesizes final response from all inputs   |

### Flow Structure

[User Question]  
↓  
[Load Context (Profile + Notes)]  
↓  
[Routing Agent]  
┌────────────┬────────────┐  
↓            ↓  
NO_WEB     USE_WEB  
↓            ↓  
[Answer Agent]     [Search Web]  
↓                    ↓  
└──────> [Answer Agent] ────> Final Answer

---

## Tools and Libraries

- LangChain: Agent logic and vector database integrations
- LangGraph: Agent orchestration and conditional workflow
- Gradio: UI elements in Colab
- Cassio + Astra DB: Vector store backend
- HuggingFace: Embedding model provider
- SerpAPI: Live search functionality
- ChatGroq: LLaMA3-based LLM provider

---

## LLM Justification

**Ideal LLMs for Production:**
- GPT-4, Claude 3 Opus — excellent for multi-turn reasoning, reliability, and longer contexts

**Free Tier Used in Development:**
- LLaMA3-70B-8192 via Groq — good speed, cost-effective, handles large contexts reasonably well

**Reason for Choice:**
LLaMA3 via Groq provides a balance of performance and accessibility for iterative development inside Colab.

---

## How to Run

### 1. Open the Notebook

> [Colab Notebook Link](https://colab.research.google.com/drive/1_vHt2x6pDxB7Eoog-yUQ9-LK4tfumkjk)

### 2. Install Required Libraries

```python
!pip install gradio langchain langgraph langchain_huggingface \
langchain_community cassio cassandra-driver \
chromadb transformers accelerate tiktoken \
langchain_groq google-search-results
```

### 3. Set API Keys (Groq & SerpAPI)

```python
from google.colab import userdata
groq_api_key = userdata.get("groq_api_key")
serp_api_key = userdata.get("serp_api_key")
```

### 4. Run the Notebook Cells in Order

The Gradio interface will launch within the notebook.

---

## Future Enhancements

- Integration with health trackers (Fitbit, Apple Health, etc.)
- Recommendation agents for diet and workout routines
- Adding feedback loop using memory agents
- Higher-order planning via CrewAI or AutoGen

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- LangChain
- LangGraph
- HuggingFace
- Astra DB by DataStax
- Gradio
- Groq
- SerpAPI
