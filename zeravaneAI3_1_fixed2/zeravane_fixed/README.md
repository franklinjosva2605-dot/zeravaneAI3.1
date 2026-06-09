# ⚡ ZeravaneAI v3.1

> **Enterprise AI Coding Assistant** — 4-Tier LLM · 3-Tier Scraping · Persistent RAG · Conversation Memory

---

## 🚀 What's New in v3.1

| Feature | v2.0 | v3.1 |
|---------|-------|-------|
| Vector DB | In-memory (resets on restart) | **Persistent ChromaDB** |
| LLM Tiers | 3 (Gemini → Groq → AI/ML API) | **4 (+ Ollama local fallback)** |
| Scraping Tiers | 2 (ScraperAPI → Requests) | **3 (Crawl4AI → ScraperAPI → Requests)** |
| Conversation Memory | ❌ | **✅ Multi-turn memory** |
| Free scraping | ❌ | **✅ Crawl4AI (unlimited)** |
| Local LLM fallback | ❌ | **✅ Ollama (RTX 3060 ready)** |
| API endpoints | 3 | **9 full REST endpoints** |

---

## 🧠 LLM Fallback Architecture

```
Request
  ↓
Tier 1 — Gemini 2.5 Flash     (Google AI Studio — 1M tokens/day free)
  ↓ (if rate limited)
Tier 2 — Groq llama-3.3-70b   (ultra-fast — 30 req/min free)
  ↓ (if exhausted)
Tier 3 — AI/ML API gpt-4o-mini (free tier)
  ↓ (if all cloud APIs fail)
Tier 4 — Ollama local          (qwen2.5-coder:7b — always-on, zero cost)
```

## 🕷️ Scraping Architecture

```
URL
  ↓
Tier 1 — Crawl4AI              (free, unlimited, LLM-optimised markdown)
  ↓ (if fails)
Tier 2 — ScraperAPI            (JS rendering, rotating proxies — optional)
  ↓ (if fails)
Tier 3 — Standard requests     (plain HTML — always works)
```

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/zeravaneAI
cd zeravaneAI
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env with your keys
```

At minimum you need: `GEMINI_API_KEY` (free at [aistudio.google.com](https://aistudio.google.com))

### 3. (Optional) Set up Ollama for local fallback

```bash
# Install Ollama: https://ollama.com/download
ollama pull qwen2.5-coder:7b    # ~4GB, runs well on RTX 3060 6GB
```

### 4. Run

```bash
# Streamlit UI
streamlit run streamlit_app.py

# FastAPI backend (separate terminal)
uvicorn zeravaneai.backend.api:app --reload --port 8000
```

---

## 🐳 Docker

```bash
docker build -t zeravaneai .
docker run -p 8501:8501 --env-file .env zeravaneai
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System status + all tier states |
| POST | `/query` | Full RAG pipeline with memory |
| POST | `/scrape` | Pre-warm cache for a URL |
| POST | `/multi-scrape` | Scrape multiple URLs + query |
| POST | `/github` | GitHub repo analysis |
| POST | `/tech-stack` | Tech stack detection |
| POST | `/codegen` | Code generation from live docs |
| GET | `/memory` | View conversation history |
| DELETE | `/memory` | Clear conversation memory |

---

## 🛠️ Tech Stack

```
Frontend     → Streamlit (React migration in progress)
Backend      → FastAPI + Python 3.11
LLMs         → Gemini 2.5 Flash → Groq → AI/ML API → Ollama
Scraping     → Crawl4AI → ScraperAPI → requests
Vector DB    → ChromaDB (persistent)
Deployment   → Docker + Streamlit Cloud + Railway
```

---

## 📁 Project Structure

```
zeravaneAI/
├── streamlit_app.py          # Entry point
├── requirements.txt
├── Dockerfile
├── .env.example
└── zeravaneai/
    ├── backend/
    │   ├── engine.py         # Core engine (LLM, RAG, scraping)
    │   └── api.py            # FastAPI REST API
    ├── frontend/
    │   └── app.py            # Streamlit UI
    └── data/
        └── zeravane_db/      # Persistent ChromaDB storage
```

---

Built by **Franklin Josva** · ZeravaneAI · 2025
