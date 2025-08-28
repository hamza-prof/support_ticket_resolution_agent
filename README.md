
# 🛠️ Support Agent AI – LangGraph Project

This project is an intelligent support ticket classifier and responder built using **LangGraph**, a powerful framework for building stateful, multi-agent AI systems. It classifies incoming support tickets, retrieves contextual data using RAG, generates appropriate replies using OpenRouter models, and supports retry + escalation logic.


## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Setup](#-setup)
- [Running the App](#-running-the-app)
- [Environment Variables](#-environment-variables)
- [Example Usage](#-example-usage)
- [Project Structure](#-project-structure)
- [Future Improvements](#-future-improvements)


## 🔍 Overview

This LangGraph-based agent automates customer support by processing incoming tickets. It:

- Classifies tickets (e.g., billing or technical)
- Retrieves relevant context from a FAISS vector store
- Uses an LLM to generate a helpful response
- Reviews the LLM output
- Retries on failure up to a limit
- Escalates to a human if the model cannot produce a good response


## ✨ Features

✅ LangGraph agent with retry and fallback logic  
✅ Local LangGraph server with Studio UI  
✅ OpenRouter LLM integration  
✅ Retrieval-Augmented Generation (RAG) using FAISS  
✅ Dynamic routing and stateful decision-making  
✅ Environment-based configuration  
✅ Human-readable ticket outputs with escalation logging  


## 🧠 Architecture

graph TD
    Start --> Classifier
    Classifier -->|Billing| Retriever
    Classifier -->|Technical| Retriever
    Retriever --> LLM
    LLM --> Reviewer
    Reviewer -->|Pass| FinalResponse
    Reviewer -->|Fail| Retry[Retry Counter]
    Retry -->|< 2 attempts| LLM
    Retry -->|>= 2 attempts| Escalation

- **Classifier:** Determines ticket type  
- **Retriever:** Fetches documents from FAISS index  
- **LLM Node:** Generates response using OpenRouter  
- **Reviewer:** Validates response quality  
- **Retry Logic:** Retries failed generations  
- **Escalation:** Sends ticket to human after 2 failures  


## ⚙️ Setup

### 1. Clone the repo


git clone https://github.com/yourusername/support-agent-langgraph.git
cd support-agent-langgraph

### 2. Create virtual environment and activate

python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -e ".[dev]"


## 🚀 Running the App

Make sure your `.env` file is configured (see next section), then run:


langgraph dev


You’ll see:

- 🎨 LangGraph Studio: [http://localhost:2024](http://localhost:2024)
- 📚 API Docs: [http://localhost:2024/docs](http://localhost:2024/docs)

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:


OPENROUTER_API_KEY=your-openrouter-api-key
LANGSMITH_API_KEY=your-langsmith-api-key

These are automatically loaded via `python-dotenv`.


## 🧪 Example Usage

### ✅ Success Example


{
  "subject": "Billing Issue",
  "description": "I was charged twice for the same invoice."
}


➡️ Agent classifies it, retrieves context, generates valid response.

### ❌ Failure Example (Escalated)

{
  "subject": "Hello",
  "description": "Hi"
}

➡️ Fails classification and generation → retries twice → escalates to human.


## 📁 Project Structure
```
├── src/
│   └── agent/
│       ├── __init__.py        # Exports the graph
│       ├── graph.py           # LangGraph agent graph definition
│       └── nodes/
│           ├── classifier.py
│           ├── retriever.py
│           ├── reviewer.py
│           └── escalation.py
│
├── graph_router.py            # (Optional) Multi-graph router
├── langgraph.json             # LangGraph CLI config
├── .env.example               # Example environment config
├── pyproject.toml             # Project + dependency config
├── requirements.txt           # Populated for compatibility
└── README.md                  # You are here!
```


## 📈 Future Improvements

- Webhook integration with a ticketing system (e.g., Zendesk, Freshdesk)  
- UI interface for input and monitoring  
- Fine-tuning classifier on internal data  
- Slack or email escalation notification  
- Persistent vector store using SQLite or Qdrant



