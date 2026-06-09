# ZeravaneAI v3.0 — Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies for Crawl4AI (Playwright) and ChromaDB
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers for Crawl4AI
RUN playwright install chromium --with-deps || true

# Copy project
COPY . .

# Create persistent data directory
RUN mkdir -p zeravaneai/data/zeravane_db

# Expose ports
EXPOSE 8501 8000

# Default: run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
