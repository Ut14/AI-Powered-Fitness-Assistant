# AI-Powered Fitness Assistant

## Problem Statement

Modern fitness tracking tools often lack true personalization. Users typically receive generic advice that fails to consider their specific goals, physical data, and evolving habits. This project addresses the need for a personalized AI assistant that understands the user’s fitness journey through their notes, goals, and queries, and enhances this with dynamic web knowledge when required.

Traditional fitness bots or apps do not scale well with user-specific context and lack intelligent reasoning across multiple knowledge sources. This project introduces an intelligent, multi-agent AI system that adapts, reasons, and personalizes responses.

## Why Use AI Agents?

AI agents are ideal for this task because they can independently manage subtasks like reasoning over personal data, deciding when to search the web, and formulating responses. Multi-agent collaboration adds value by:

- Separating concerns: Each agent performs a specific function (retrieval, routing, answering, etc.).
- Dynamic behavior: The system intelligently decides whether to use internal memory or external sources.
- Flexibility: Easily extensible to include future agents (e.g., scheduling, nutrition planning).

## Project Description

This project is a fitness assistant web app built using Gradio and LangChain. Users can update their fitness profile, add personal notes (e.g., workouts, meals, progress), and ask questions. The system intelligently combines personal context and online resources to generate tailored responses.

### Agent Interactions

This application uses a LangGraph-powered agent framework. Each logical component behaves as an autonomous agent and collaborates as follows:

- **Context Loader Agent**: Loads user profile and relevant notes for the question.
- **Router Agent**: Uses an LLM to decide if the internal context is enough or if web search is needed.
- **Web Search Agent**: If necessary, retrieves relevant online data using SerpAPI.
- **Answer Generation Agent**: Synthesizes all context into a concise and useful response.

**Example Flow:**

1. User asks: "What should I eat after my workout?"
2. Context Loader gathers profile + fitness notes.
3. Router decides more information is needed.
4. Web Search Agent fetches results from the web.
5. Answer Generator combines all context to give a precise answer.

## Tools, Libraries, and Frameworks Used

- **LangChain**: Core framework for agent orchestration and document processing.
- **LangGraph**: Manages stateful agent workflows in a directed graph architecture.
- **Gradio**: Used for building the user interface.
- **Cassandra + Astra DB**: Vector storage for long-term memory (fitness notes).
- **Hugging Face Transformers**: For text embeddings (MiniLM).
- **SerpAPI**: Enables access to real-time web search results.
- **dotenv**: Secure secret management.

## LLM Selection

### Ideal Choice

- **GPT-4** or **Claude 3**: For production-grade reasoning, better multi-step understanding, and high-quality summarization.

### Free-Tier Option Used

- **Groq (LLaMA 3 70B)**: For cost-effective and fast inference, especially suited for development and prototyping.
- **Hugging Face's all-MiniLM-L6-v2**: Used for local embeddings and retrieval.

### Justification

- GPT-4 or Claude 3 would provide superior coherence and reasoning for nuanced health queries.
- Groq’s LLaMA 3 model balances speed, accuracy, and cost, making it ideal for prototyping.
- Open-source embedding models suffice for context-based note retrieval.

## Folder Structure and Deployment

You should upload the following to GitHub:

- `app.py`: Main application logic (agents, Gradio UI).
- `.env`: Template for environment variables (omit secrets).
- `user_profile.json`: Optional initial profile (auto-generated if not present).
- `requirements.txt`: Dependency list.
- `README.md`: Project documentation.
- `.gitignore`: To exclude `__pycache__`, `.venv`, `.env`, etc.
- `fitness_notes/`: Optional folder if logs or additional docs are stored.

## How to Run

1. Clone the repository.
2. Set up a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Fill in your API keys.
4. Run the app:
   ```bash
   python app.py
   ```
