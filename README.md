
# AI-Powered Fitness Assistant

An intelligent fitness companion powered by LLM agents and vector search that helps users track goals, manage notes, and receive personalized advice through a simple Gradio interface.

---

## Problem Statement

Staying consistent with fitness goals requires:
- Tracking personal health metrics
- Managing scattered notes and logs
- Getting timely, relevant, and personalized advice

Most fitness tools either rely heavily on static data or generic content. There's a need for a dynamic system that leverages personal context while also accessing up-to-date public knowledge when necessary.

---

## Why AI Agents?

AI agents are ideal because they:
- Personalize answers based on user profile and logs
- Reason over notes stored as vector embeddings
- Decide if additional context is required from the web
- Automate multi-step processes like retrieval and synthesis

### Why Multi-Agent Architecture?

Multi-agent collaboration enables:
- Clear role delegation (retriever, router, responder, searcher)
- Independent task execution and intelligent decision routing
- Context-aware responses with optional web enhancement

---

## Application Overview

**Tech Stack:**
- **UI:** Gradio
- **Core AI Logic:** LangChain + LangGraph
- **Embedding & Vector Storage:** HuggingFace + CassandraDB (Astra)
- **LLM:** Groq's LLaMA3-70B
- **Web Search:** SerpAPI
- **Prompt Orchestration:** LangChain PromptTemplate

**Features:**
- Profile Setup (Age, Height, Weight, Goal)
- Note Logging with Timestamps
- Chat Q&A with Smart Context Usage
- Web Search Fallback for Real-Time Queries
- View & Delete Stored Notes

---

## Agent Workflow

This application uses LangGraph to define a multi-agent state machine:

### Agents Involved:

| Agent               | Responsibility                                  |
|--------------------|--------------------------------------------------|
| Context Loader     | Loads profile and relevant notes                 |
| Router Agent       | Determines if web search is required             |
| Web Search Agent   | Queries SerpAPI and returns top 3 results        |
| Answer Agent       | Generates final output using all available info  |

### Flow Logic

```
[User Question]
     ↓
[Load Profile + Notes]
     ↓
[Routing Agent]
 ┌────────────┬────────────┐
 ↓                         ↓
NO_WEB                 USE_WEB
 ↓                         ↓
[Answer Agent]       [Search Web]
     ↓                   ↓
     └───> [Answer Agent] ────> Final Answer
```

---

## Tools & Libraries

- LangChain: Agent logic, LLM abstraction, vector store support
- LangGraph: Multi-agent conditional workflow execution
- Gradio: Interactive user interface
- HuggingFace Embeddings: Semantic vectorization of notes
- Astra DB (Cassandra): Vector storage backend
- SerpAPI: Web search tool
- ChatGroq: Fast and free-tier LLM backend using LLaMA3

---

## LLMs Used

### Ideal LLM:
- GPT-4 or Claude 3 Opus
  - Better contextual reasoning
  - Handles long context windows (notes and web)
  - Ideal for production-grade deployment

### Free-Tier Used:
- LLaMA3-70B-8192 via Groq
  - Fast response
  - Free via API
  - Suitable for local and experimental setups

### Justification:
- LLaMA3 is sufficient for multi-agent routing, summarization, and question answering.
- In production, GPT-4 could enhance personalization, tone, and edge-case handling.

---

## Future Scope

- Add health tracking APIs (Fitbit, Google Fit)
- Enable workout and diet recommendation agents
- Incorporate memory and feedback agents
- Use CrewAI or AutoGen for higher-level task delegation

---

## Getting Started

### 1. Install dependencies

```bash
pip install gradio langchain langgraph langchain_huggingface langchain_community cassio cassandra-driver chromadb transformers accelerate tiktoken langchain_groq google-search-results
```

### 2. Set environment variables (or use `userdata.get()` in Colab)

```python
import os
os.environ["SERPAPI_API_KEY"] = "<your-serpapi-key>"
os.environ["GROQ_API_KEY"] = "<your-groq-key>"
```

### 3. Launch the app

```bash
python your_gradio_app.py
```

---

## License

This project is under the MIT License.

---

## Acknowledgements

- LangChain (https://github.com/langchain-ai/langchain)
- Groq (https://console.groq.com/)
- HuggingFace (https://huggingface.co/)
- Astra DB (https://www.datastax.com/astra)
- Gradio (https://gradio.app/)
- SerpAPI (https://serpapi.com/)
