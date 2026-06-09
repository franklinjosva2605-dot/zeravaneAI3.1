# ZeravaneAI v3.1 — Deployment Guide

## 🚀 Streamlit Cloud Deployment

### Fix Applied (v3.1)

The repository structure had nested directories with spaces/parentheses that broke dependency resolution:

```
❌ Old (broken):
  zeravaneAI3_1_fixed3 (1)/zeravane_fixed/requirements.txt  ← Package manager can't parse this path

✅ New (fixed):
  requirements.txt  ← Top level, clean path
  streamlit_app.py  ← Entry point with flexible path handling
```

### Deployment Steps

1. **Ensure these files are at repo root:**
   - `requirements.txt` ✅
   - `streamlit_app.py` ✅
   - `.streamlit/config.toml` ✅

2. **In Streamlit Cloud dashboard:**
   - Set **Main file path** to: `streamlit_app.py`
   - Set **Python version** to: `3.11+`

3. **Environment variables** (Streamlit Cloud Secrets):
   ```
   GEMINI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   AIML_API_KEY=your_key_here
   SCRAPER_API_KEY=your_key_here
   GITHUB_TOKEN=your_token_here
   ```

### Directory Structure

```
zeravaneAI3.1/
├── requirements.txt              ← ✅ Top level (dependency resolution)
├── streamlit_app.py              ← ✅ Entry point with path flexibility
├── .streamlit/
│   └── config.toml               ← ✅ Streamlit settings
├── zeravaneai/                   ← App code (production flatten)
│   ├── backend/
│   │   ├── engine.py
│   │   └── api.py
│   ├── frontend/
│   │   └── app.py
│   └── data/
│       └── zeravane_db/
└── zeravaneAI3_1_fixed3 (1)/     ← Legacy nested (still works for backwards compat)
    └── zeravane_fixed/
        ├── requirements.txt
        ├── streamlit_app.py
        └── zeravaneai/
```

### Local Development

```bash
# Clone repo
git clone https://github.com/yourusername/zeravaneAI3.1
cd zeravaneAI3.1

# Create env
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install deps
pip install -r requirements.txt

# Optional: Crawl4AI (local only)
pip install crawl4ai
crawl4ai-setup

# Run Streamlit
streamlit run streamlit_app.py
```

### Docker Deployment

```bash
docker build -t zeravaneai .
docker run -p 8501:8501 --env-file .env zeravaneai
```

### Troubleshooting

| Error | Solution |
|-------|----------|
| `Invalid requirement: '(1)/zeravane_fixed/requirements.txt'` | ✅ Fixed — use top-level `requirements.txt` |
| `ModuleNotFoundError: zeravaneai` | ✅ Fixed — `streamlit_app.py` handles nested/flat paths |
| `protobuf` version mismatch | Use `protobuf>=5.29.0` (Python 3.14 compatible) |
| `chromadb` import errors | Pin `chromadb<0.7.0` (avoid protobuf 4.x conflict) |

### Key Changes in v3.1

- ✅ Top-level `requirements.txt` with clean path resolution
- ✅ Flexible entry point `streamlit_app.py` (supports both directory structures)
- ✅ `.streamlit/config.toml` for deployment settings
- ✅ Memory consistency fix across all 4-tier LLM fallbacks
- ✅ Groq & AI/ML API now use proper `get_memory_context(exclude_last_n=1)`

### Support

For deployment issues:
1. Check `.streamlit/config.toml` exists
2. Verify `requirements.txt` at root level
3. Test locally: `streamlit run streamlit_app.py`
4. Check Streamlit Cloud logs for exact error
