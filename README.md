# AI-Powered Fitness Assistant

An intelligent, personalized fitness assistant that leverages multi-agent collaboration, vector search, and LLM reasoning to help users manage their fitness journey through note-taking, contextual Q&A, and live web integration.

---

## Problem Statement

Staying on track with fitness goals is difficult without tailored advice and a centralized place to store personal insights. Users often maintain notes in scattered places and struggle to get answers that consider their unique profile and history.

This project solves that by building a personal fitness agent that:
- Understands your goals, body metrics, and history
- Provides personalized answers to your fitness questions
- Decides intelligently when to bring in web data for enhanced context

AI agents are ideal here because they can:
- Manage user context dynamically
- Make autonomous decisions about resource use (internal data vs web)
- Deliver accurate, concise, and personal recommendations

Multi-agent collaboration enables modular, scalable task handling—where each agent independently contributes to the final response based on its specialization.

---

## Project Description

The application is a Gradio-based AI assistant for fitness enthusiasts.

It includes:

- Profile Management: Age, height, weight, and fitness goals
- Note Storage & Retrieval: Store fitness logs, training notes, etc., in a vector DB
- Personalized Q&A: Ask fitness questions and get tailored answers
- Web-enhanced Reasoning: When personal data isn’t enough, the app fetches real-time info using search

### Agent Workflow (LangGraph)

1. Context Loader Agent  
   Loads user profile and retrieves relevant notes from AstraDB.

2. Routing Agent  
   Uses an LLM to decide if the system has enough context to answer or needs a web search.

3. Web Search Agent  
   Queries SERP API for additional context when needed.

4. Answer Generator Agent  
   Synthesizes a final answer using profile, notes, and web results.

---

## Tools, Libraries & Frameworks

| Tool | Purpose |
|------|---------|
| LangChain | Core agent orchestration |
| LangGraph | Multi-agent workflow engine |
| Gradio | Frontend UI |
| Cassandra (AstraDB) | Vector storage for user notes |
| Cassio | LangChain-AstraDB integration |
| HuggingFace Embeddings | Embedding model for notes |
| SERP API | Web search results |
| Groq + LLaMA3-70B | Fast and powerful LLM backend |
| dotenv | Secret key management |

---

## LLM Selection

### Ideal LLM

- GPT-4 Turbo or Claude 3 Opus  
  Chosen for:
  - Strong contextual memory
  - Precise and health-safe reasoning
  - Adaptability to user-specific queries

### Current LLM

- LLaMA3-70B via Groq  
  - High-speed, low-latency generation
  - Strong reasoning capabilities
  - Ideal for real-time apps

### Free / Open Source Alternatives

| Model | Platform | Notes |
|-------|----------|-------|
| GPT-3.5 | OpenAI | Good fallback with lower cost |
| Gemini Pro | Google Cloud | Useful for broader expansion |
| Mistral / Mixtral | HuggingFace | Great for local or private deployments |

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Ut14/AI-Powered-Fitness-Assistant.git
   cd fitness-agent-app
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your .env file with:
   ```env
   ASTRA_DB_ID=your_db_id
   ASTRA_DB_APPLICATION_TOKEN=your_token
   SERPAPI_API_KEY=your_serpapi_key
   GROQ_API_KEY=your_groq_key
   ```

4. Run the app:
   ```bash
   python app.py
   ```

---

## License

MIT License © 2025 Your Name
