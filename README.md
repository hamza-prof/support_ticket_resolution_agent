
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
```
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

```

- **Classifier:** Determines ticket type  
- **Retriever:** Fetches documents from FAISS index  
- **LLM Node:** Generates response using OpenRouter  
- **Reviewer:** Validates response quality  
- **Retry Logic:** Retries failed generations  
- **Escalation:** Sends ticket to human after 2 failures  


## ⚙️ Setup

### Prerequisites

- **Python Version**: Python 3.11+ (3.11, 3.12, or 3.13 recommended)
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Memory**: Minimum 4GB RAM (8GB+ recommended for optimal performance)
- **Storage**: At least 2GB free disk space

### 1. Clone the repo


git clone https://github.com/hamza-prof/support-agent-langgraph.git
cd support-agent-langgraph

### 2. Create virtual environment and activate

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
# Install the package in development mode
pip install -e ".[dev]"

# Alternative: Install from requirements.txt
pip install -r requirements.txt
```


## 🚀 Running the App

### System Requirements Check

Before running, ensure your system meets the requirements:

```bash
# Check Python version (should be 3.11+)
python --version

# Check available memory (should be 4GB+)
# On Windows: Check Task Manager
# On macOS/Linux: free -h

# Check available disk space (should be 2GB+)
# On Windows: Check File Explorer
# On macOS/Linux: df -h
```

### Starting the Application

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


## 🚨 Troubleshooting

### Common Issues & Solutions

#### Python Version Issues
```bash
# If you get "Python version not supported" error
# Install Python 3.11+ from python.org or use pyenv

# Check if multiple Python versions are installed
python --version
python3 --version
py --version  # Windows
```

#### Virtual Environment Issues
```bash
# If venv creation fails
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv

# If activation fails on Windows
# Make sure you're running PowerShell or Command Prompt as Administrator
```

#### Dependency Installation Issues
```bash
# If pip install fails
pip install --upgrade pip setuptools wheel

# If you get SSL errors
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -e ".[dev]"

# Alternative installation method
pip install -r requirements.txt
```

#### Memory/Performance Issues
- **Slow startup**: Ensure you have at least 4GB RAM available
- **Model loading errors**: Check available disk space (2GB+ required)
- **Timeout errors**: Increase system timeout settings or check network connectivity

### Getting Help

If you encounter issues not covered here:
1. Check the [Issues](https://github.com/hamza-prof/support-agent-langgraph/issues) page
2. Search existing discussions
3. Create a new issue with detailed error information

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


## 🛠️ Development & Contributing

### Development Setup

```bash
# Clone the repository
git clone https://github.com/hamza-prof/support-agent-langgraph.git
cd support-agent-langgraph

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
ruff format .
```

### Project Structure for Developers

```
src/agent/
├── __init__.py          # Package initialization and exports
├── config.py            # Configuration management
├── graph.py             # Main LangGraph agent definition
└── nodes/               # Individual processing nodes
    ├── classifier.py    # Ticket classification logic
    ├── retriever.py     # Context retrieval using FAISS
    ├── drafter.py       # Response generation with LLM
    ├── reviewer.py      # Response quality validation
    └── escalation.py    # Human escalation handling
```

### Contributing Guidelines

1. **Fork the repository** and create a feature branch
2. **Follow the coding standards** (use ruff for formatting)
3. **Write tests** for new functionality
4. **Update documentation** for any API changes
5. **Submit a pull request** with clear description

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit_tests/test_classifier.py

# Run with coverage
pytest --cov=src/agent

# Run integration tests
pytest tests/integration_tests/
```

## 📈 Future Improvements

### 🚀 **Phase 1: Enhanced Integration & Automation**
- **Ticketing System Integration**: Webhook integration with Zendesk, Freshdesk, Jira Service Desk
- **Multi-Channel Support**: Slack, Microsoft Teams, Discord bot integration
- **Email Automation**: SMTP integration for automated email responses and escalations
- **API Gateway**: RESTful API endpoints for external system integration

### 🎨 **Phase 2: User Experience & Interface**
- **Web Dashboard**: React/Vue.js frontend for ticket monitoring and management
- **Real-time Analytics**: Live dashboard showing response times, success rates, and escalation metrics
- **Mobile App**: iOS/Android app for support agents on-the-go
- **Customizable Templates**: Drag-and-drop interface for response template creation

### 🧠 **Phase 3: AI & Machine Learning Enhancements**
- **Fine-tuned Models**: Custom training on company-specific support data
- **Sentiment Analysis**: Automatic detection of customer satisfaction and urgency
- **Predictive Escalation**: ML-based prediction of when tickets need human intervention
- **Multi-language Support**: Automatic translation and localization for global support
- **Voice Integration**: Speech-to-text and text-to-speech for phone support

### 🔒 **Phase 4: Security & Compliance**
- **Advanced Authentication**: OAuth 2.0, SAML, and multi-factor authentication
- **Audit Logging**: Comprehensive logging for compliance (SOC 2, ISO 27001)
- **Data Encryption**: End-to-end encryption for sensitive customer data
- **Role-based Access Control**: Granular permissions for different support levels
- **GDPR Compliance**: Automated data deletion and privacy controls

### 📊 **Phase 5: Analytics & Intelligence**
- **Business Intelligence**: Advanced reporting and KPI dashboards
- **Performance Optimization**: AI-driven suggestions for improving response quality
- **Customer Insights**: Behavioral analysis and customer journey mapping
- **A/B Testing**: Framework for testing different response strategies
- **Predictive Maintenance**: Proactive identification of system issues

### 🔧 **Phase 6: Infrastructure & Scalability**
- **Microservices Architecture**: Containerized deployment with Docker and Kubernetes
- **Cloud Deployment**: Multi-cloud support (AWS, Azure, GCP)
- **Auto-scaling**: Dynamic resource allocation based on ticket volume
- **High Availability**: Multi-region deployment with failover capabilities
- **Performance Monitoring**: APM integration and real-time performance metrics

### 🌐 **Phase 7: Ecosystem & Extensions**
- **Plugin System**: Third-party integrations and custom extensions
- **Marketplace**: Community-driven add-ons and integrations
- **API Ecosystem**: Developer portal and SDK for custom implementations
- **Webhook Marketplace**: Pre-built integrations with popular business tools
- **Community Support**: Open-source contributions and community-driven development



