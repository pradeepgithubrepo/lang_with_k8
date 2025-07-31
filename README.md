# 🚀 Enterprise RAG Agent – LangGraph + FastAPI + Redis + Kubernetes

> 🧠 A production-grade, agentic AI backend that combines LangGraph, Retrieval-Augmented Generation (RAG), persistent memory via Redis, and secure FastAPI endpoints. Designed for full-scale deployment on Docker and Kubernetes with monitoring and API key security.

---

## 🎯 Objective

This project provides a **modular boilerplate** to build and deploy **end-to-end agentic AI applications** using LangGraph and RAG. It is production-ready, scalable, and extensible, enabling multi-turn conversations, external document integration, persistent memory, and comprehensive monitoring.

---

## 🧱 Architecture Overview

```
+------------------+       +-------------------+       +------------------+
|   Streamlit UI   | <---> | FastAPI Backend    | <---> |  LangGraph Agent |
+------------------+       +-------------------+       +------------------+
                                      |
                             +--------+--------+
                             |   Redis Memory   |
                             +--------+--------+
                                      |
                              +-------+--------+
                              | Vector Store    |
                              | (Chroma)  |
                              +----------------+
```

---

## 📁 Codebase Structure

```
/enterprise-rag-agent
│
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py               # App-wide config (env vars, secrets)
│   ├── tools.py                # Tool functions used in LangGraph
│   ├── graph_manager.py        # LangGraph graph and flow logic
│   ├── vector_store/
│   │   ├── loader.py           # Load PDFs, markdown, etc.
│   │   ├── embedder.py         # Embedding logic using OpenAI or others
│   │   └── vectordb.py         # Vector DB logic (FAISS/Chroma)
│   ├── node_pool/
│   │   ├── retrieve_node.py
│   │   ├── generate_node.py
│   │   └── fallback_node.py
│   ├── state_manager/
│   │   └── memory_state.py     # Redis chat history threading
│   ├── integration/
│   │   └── confluence_api.py   # Placeholder for API integrations
│   ├── security/
│   │   └── auth.py             # API key validation
│   ├── monitoring/
│   │   └── metrics.py          # Prometheus-ready metrics
│   ├── error_handler.py        # Global exception handling
│
├── streamlit_ui/
│   └── ui.py                   # Multi-tab UI for user interaction
│
├── data/
│   └── sample_docs/            # PDFs, Markdown, CSVs for ingestion
│
├── docker/
│   └── Dockerfile              # Backend Docker setup
│
├── k8/
│   ├── deployment.yaml         # Kubernetes deployment
│   └── service.yaml            # Kubernetes service
│
├── .env                        # Secrets like API keys
├── .gitignore                 # Ignored files
├── requirements.txt           # Python dependencies
└── README.md                  # You’re reading it
```

---

## ⚙️ Setup Instructions

### 1. 🧬 Clone Repo

```bash
git clone https://github.com/your-org/enterprise-rag-agent.git
cd enterprise-rag-agent
```

### 2. 🔐 Create `.env`

```env
AZURE_ENDPOINT = 
AZURE_API_KEY = 
OPENAI_API_TYPE = 
AZURE_DEPLOYMENT = 
AZURE_API_VERSION = 
AZURE_MODEL=
GEMINI_API_KEY=
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
SERPER_API_KEY=
RAG_API_KEY=
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🚀 Start Redis

```bash
docker run -d -p 6379:6379 redis
```

### 5. 🧠 Run FastAPI Backend

```bash
uvicorn app.main:app --reload
```

### 6. 🖥️ Run Streamlit UI

```bash
streamlit run streamlit_ui/ui.py
```

---

## 🔐 Security

- ✅ API key validation via `X-API-Key`
- ✅ Secure loading from `.env` using `python-dotenv`
- ✅ Centralized `auth.py` logic

---

## 🧠 Memory & Chat Threading

- 🔁 Redis-based persistent state across sessions
- 🧵 Threaded conversations
- 💾 State autosaved before/after LangGraph execution

---

## 🤖 LangGraph Agent

- Nodes:
  - 📥 Retrieve Node – RAG doc search
  - ✍️ Generate Node – LLM reasoning
  - 🧯 Fallback Node – edge case handler
- Built using LangGraph’s composable workflows

---

## 📡 API Reference

### `POST /ask`

Ask a question to the agent.

```http
POST /ask
Headers:
  X-API-Key: your_api_key

Body:
{
  "question": "What is the sales trend for Q1?"
}
```

**Response**
```json
{
  "final_answer": "The sales trend for Q1 was an upward growth of 18%."
}
```

---

## 📊 Monitoring

- 📈 `/metrics` endpoint exposes Prometheus counters
- Tracks:
  - ⚡ Request duration
  - 🔢 Total requests
  - ✅ Response status codes
  - 🔍 RAG operation metrics

---

## 🐳 Docker Support

```bash
docker network create rag-net
 docker run -d   --name redis   --network rag-network   redis:latest
docker network connect rag-net redis

 docker run -d   --name rag-backend   --network rag-net   -p 8000:8000   rag-backend:latest

docker run -d   --name rag-frontend   --network rag-net   -p 8501:8501   rag-frontend:latest<img width="902" height="189" alt="image" src="https://github.com/user-attachments/assets/66ef1b9e-081d-4c5c-9b61-93f61d7576c5" />

```

---

## ☸️ Kubernetes Deployment

```bash
kubectl apply -f deployment/
```

---

## ✅ Feature Highlights

- 🔐 Secure API layer
- 📚 Vector Search with FAISS/Chroma
- 🔄 Persistent Redis memory
- 🧠 LangGraph agent orchestration
- 🧪 Monitoring with Prometheus
- 🖥️ Multi-tab Streamlit UI
- 🐳 Docker-ready
- ☸️ Kubernetes-ready

---

## 🚧 Coming Soon

- 🚀 CI/CD via GitHub Actions  
- ☁️ Azure Blob, SharePoint, Confluence integrations  
- 💬 Slack & Teams notifications  
- 🧾 Session transcripts and summaries

---

## 👨‍💻 Maintainer

**Pradeep P.** – Software Professional | AI & Cloud Engineer

Feel free to fork, contribute, or raise issues!

---
