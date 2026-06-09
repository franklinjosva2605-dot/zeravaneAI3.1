# =============================================================================
# ZeravaneAI — Streamlit Frontend v3.0
# =============================================================================
import os
import sys

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import re
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.engine import ZeravaneEngine

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="ZeravaneAI v3.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    :root {
        --neon-cyan:   #00D9FF;
        --neon-green:  #00FF41;
        --neon-orange: #FF6B35;
        --neon-purple: #A855F7;
        --neon-yellow: #FFD700;
        --dark-bg:     #0A0E27;
        --card-bg:     rgba(10, 20, 40, 0.85);
        --text-primary: #E0E6FF;
        --text-muted:   #7A8AB5;
    }

    /* Global background */
    .stApp { background: linear-gradient(135deg, #060B1A 0%, #0A1628 50%, #060B1A 100%); }
    .main  { background: transparent; color: var(--text-primary); }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea  > div > div > textarea {
        border: 1.5px solid rgba(0,217,255,0.4) !important;
        background: rgba(0,15,35,0.9) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 6px rgba(0,217,255,0.15) !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea  > div > div > textarea:focus {
        border-color: var(--neon-cyan) !important;
        box-shadow: 0 0 16px rgba(0,217,255,0.35) !important;
    }

    /* Buttons */
    .stButton > button {
        border: 1.5px solid var(--neon-cyan) !important;
        background: linear-gradient(135deg, rgba(0,30,60,0.9), rgba(0,50,90,0.9)) !important;
        color: var(--neon-cyan) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 0 8px rgba(0,217,255,0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 0 24px rgba(0,217,255,0.55) !important;
        border-color: #fff !important;
        color: #fff !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(0,15,35,0.9) !important;
        border: 1.5px solid rgba(0,217,255,0.3) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0,10,25,0.8);
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0,40,80,0.95), rgba(0,60,120,0.95)) !important;
        color: var(--neon-cyan) !important;
        box-shadow: 0 0 12px rgba(0,217,255,0.3) !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: var(--card-bg) !important;
        border: 1px solid rgba(0,217,255,0.2) !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(0,15,35,0.8) !important;
        border: 1px solid rgba(0,217,255,0.15) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    /* Animations */
    @keyframes pulse-green  { 0%,100%{box-shadow:0 0 8px rgba(0,255,65,.4);} 50%{box-shadow:0 0 20px rgba(0,255,65,.8);} }
    @keyframes pulse-cyan   { 0%,100%{box-shadow:0 0 8px rgba(0,217,255,.4);} 50%{box-shadow:0 0 20px rgba(0,217,255,.8);} }
    @keyframes pulse-orange { 0%,100%{box-shadow:0 0 8px rgba(255,107,53,.4);} 50%{box-shadow:0 0 20px rgba(255,107,53,.8);} }
    @keyframes pulse-purple { 0%,100%{box-shadow:0 0 8px rgba(168,85,247,.4);} 50%{box-shadow:0 0 20px rgba(168,85,247,.8);} }
    @keyframes glow-text    { 0%,100%{text-shadow:0 0 8px rgba(0,217,255,.6);} 50%{text-shadow:0 0 24px rgba(0,217,255,1);} }

    /* Badges */
    .badge { display:inline-block; padding:6px 14px; border-radius:6px; font-weight:700; font-size:13px; margin:4px; }
    .badge-green  { border:1.5px solid rgba(0,255,65,.6);  background:rgba(0,40,20,.8);  color:#00FF41; animation:pulse-green  2s ease-in-out infinite; }
    .badge-cyan   { border:1.5px solid rgba(0,217,255,.6); background:rgba(0,25,50,.8);  color:#00D9FF; animation:pulse-cyan   2s ease-in-out infinite; }
    .badge-orange { border:1.5px solid rgba(255,107,53,.6);background:rgba(50,15,0,.8);  color:#FF6B35; animation:pulse-orange 2s ease-in-out infinite; }
    .badge-purple { border:1.5px solid rgba(168,85,247,.6);background:rgba(35,0,50,.8);  color:#A855F7; animation:pulse-purple 2s ease-in-out infinite; }

    /* Chat bubbles */
    .chat-user {
        background: linear-gradient(135deg, rgba(0,30,70,.9), rgba(0,50,100,.9));
        border: 1px solid rgba(0,217,255,.3);
        border-radius: 12px 12px 4px 12px;
        padding: 12px 16px; margin: 8px 0;
        color: var(--text-primary); font-size:14px;
    }
    .chat-ai {
        background: linear-gradient(135deg, rgba(20,0,50,.9), rgba(40,0,80,.9));
        border: 1px solid rgba(168,85,247,.3);
        border-radius: 12px 12px 12px 4px;
        padding: 12px 16px; margin: 8px 0;
        color: var(--text-primary); font-size:14px;
    }
    .chat-meta { font-size:11px; color:var(--text-muted); margin-top:6px; }

    /* Status banner */
    .banner {
        background: linear-gradient(135deg, rgba(0,15,40,.95), rgba(0,30,70,.95));
        border: 1px solid rgba(0,217,255,.25);
        border-radius: 12px; padding: 14px 20px; margin: 10px 0; text-align:center;
    }
    .model-tag {
        display:inline-block; padding:2px 10px; border-radius:4px;
        background:rgba(168,85,247,.15); border:1px solid rgba(168,85,247,.4);
        color:#A855F7; font-size:11px; font-weight:700; margin-left:6px;
    }
    .memory-tag {
        display:inline-block; padding:2px 10px; border-radius:4px;
        background:rgba(0,255,65,.1); border:1px solid rgba(0,255,65,.35);
        color:#00FF41; font-size:11px; font-weight:700; margin-left:6px;
    }

    /* Scrollable chat history */
    .chat-scroll {
        max-height: 500px; overflow-y: auto;
        padding-right: 8px;
        scrollbar-width: thin;
        scrollbar-color: rgba(0,217,255,.3) transparent;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<h1 style='text-align:center; color:#00D9FF; letter-spacing:3px; margin-bottom:4px;
           animation:glow-text 3s ease-in-out infinite;'>
⚡ ZeravaneAI <span style='font-size:18px; opacity:0.7;'>v3.0</span>
</h1>
<p style='text-align:center; color:#7A8AB5; font-size:12px; letter-spacing:2px; margin:0;'>
ENTERPRISE AI CODING ASSISTANT · 4-TIER LLM · 3-TIER SCRAPING · PERSISTENT RAG · MEMORY
</p>
""", unsafe_allow_html=True)

# =============================================================================
# ENGINE + SESSION STATE
# =============================================================================

@st.cache_resource(show_spinner="⚡ Initialising ZeravaneAI engine...")
def load_engine():
    return ZeravaneEngine()

engine = load_engine()

# Session state defaults
for key, val in {
    "chat_history": [],
    "last_url": "",
    "memory_enabled": True,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0;'>
        <span style='font-size:28px;'>⚡</span>
        <div style='color:#00D9FF; font-weight:700; letter-spacing:2px; font-size:14px;'>ZERAVANE AI</div>
        <div style='color:#7A8AB5; font-size:10px;'>v3.0 · Enterprise Edition</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # LLM Status
    st.markdown("**🧠 LLM Tiers**")
    tiers = [
        ("⚡ Gemini 2.5 Flash",   engine.gemini_enabled,  "badge-green"),
        ("🟣 Groq llama-3.3-70b", engine.groq_enabled,    "badge-cyan"),
        ("🔶 AI/ML API",          engine.aiml_enabled,    "badge-orange"),
        (f"🖥️ Ollama ({engine.ollama_model})", engine.ollama_enabled, "badge-purple"),
    ]
    for label, active, cls in tiers:
        state = "● ACTIVE" if active else "○ INACTIVE"
        color = "#00FF41" if active else "#555"
        st.markdown(
            f"<div style='font-size:12px; padding:3px 0; color:{color};'>{label} — {state}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Scraping Status
    st.markdown("**🕷️ Scraping Tiers**")
    scrape_tiers = [
        ("🟢 Crawl4AI (Free · Unlimited)", True),
        ("🔵 ScraperAPI (JS Rendering)", engine.scraper_enabled),
        ("⚪ Standard Requests", True),
    ]
    for label, active in scrape_tiers:
        color = "#00FF41" if active else "#555"
        st.markdown(f"<div style='font-size:12px; padding:2px 0; color:{color};'>{label}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Memory toggle
    st.markdown("**💬 Conversation Memory**")
    st.session_state.memory_enabled = st.toggle(
        "Enable memory",
        value=st.session_state.memory_enabled,
        help="When on, ZeravaneAI remembers previous turns in this session",
    )
    turns = len(engine.conversation_memory) // 2
    st.markdown(
        f"<div style='font-size:12px; color:#7A8AB5;'>Active turns: <b style='color:#00FF41;'>{turns}</b></div>",
        unsafe_allow_html=True,
    )

    if st.button("🗑️ Clear Memory", use_container_width=True):
        engine.clear_memory()
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    # Vector DB status
    db_type = "Persistent ChromaDB" if hasattr(engine.chroma_client, "list_collections") else "In-Memory Store"
    st.markdown(f"**🗄️ Vector DB:** {db_type}")
    if engine._cached_url:
        short_url = engine._cached_url[:40] + "..." if len(engine._cached_url) > 40 else engine._cached_url
        st.markdown(
            f"<div style='font-size:11px; color:#00FF41; word-break:break-all;'>✅ Cached: {short_url}</div>",
            unsafe_allow_html=True,
        )

    if st.button("🗑️ Clear Cache", use_container_width=True):
        try:
            engine.chroma_client.delete_collection(name=engine._cached_collection)
        except Exception:
            pass
        engine._cached_url = None
        st.session_state.last_url = ""
        st.rerun()

    st.markdown("---")

    # Debug
    with st.expander("🔍 Debug"):
        keys_status = {
            "GEMINI_API_KEY":  bool(engine.gemini_api_key),
            "GROQ_API_KEY":    bool(engine.groq_api_key),
            "AIML_API_KEY":    bool(engine.aiml_api_key),
            "SCRAPER_API_KEY": bool(engine.scraper_api_key),
            "GITHUB_TOKEN":    bool(engine.github_token),
            "OLLAMA":          engine.ollama_enabled,
        }
        for k, v in keys_status.items():
            icon = "✅" if v else "❌"
            st.markdown(f"<div style='font-size:11px;'>{icon} {k}</div>", unsafe_allow_html=True)

# =============================================================================
# MAIN TABS
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat Agent",
    "🔗 Multi-URL RAG",
    "🐙 GitHub Analyzer",
    "🔍 Tech Stack Detector",
    "⚙️ Code Generator",
])

# =============================================================================
# TAB 1 — CHAT AGENT (with memory)
# =============================================================================
with tab1:
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown("#### 🌐 Target URL *(optional)*")
        target_url = st.text_input(
            "URL to scrape for context",
            placeholder="https://docs.fastapi.tiangolo.com  (leave blank for base knowledge)",
            value=st.session_state.last_url,
            key="tab1_url",
            label_visibility="collapsed",
        )

    with col_right:
        st.markdown("#### Options")
        force_rescrape = st.checkbox("🔄 Force re-scrape", value=False, key="tab1_force")

    # Status banner
    if not target_url.strip():
        st.markdown(
            "<div class='banner'><span class='badge badge-cyan'>🧠 Core Mode — Base Model Knowledge</span></div>",
            unsafe_allow_html=True,
        )
    elif engine.scraper_enabled:
        st.markdown(
            "<div class='banner'><span class='badge badge-green'>🌐 Web Intelligence Mode — Multi-Tier Scraping Active</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='banner'><span class='badge badge-orange'>🌐 Web Mode — Crawl4AI + Standard Requests</span></div>",
            unsafe_allow_html=True,
        )

    # Chat history display
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown(f"**💬 Conversation** ({len(st.session_state.chat_history)} turns)")
        st.markdown("<div class='chat-scroll'>", unsafe_allow_html=True)
        for entry in st.session_state.chat_history:
            st.markdown(f"<div class='chat-user'>👤 {entry['query']}</div>", unsafe_allow_html=True)
            response_preview = entry["response"]
            st.markdown(f"<div class='chat-ai'>🤖 {response_preview}</div>", unsafe_allow_html=True)
            meta = f"Model: {entry['model_used']} · Scrape: {entry['scrape_method']}"
            if entry.get("url"):
                meta += f" · URL: {entry['url'][:50]}"
            st.markdown(f"<div class='chat-meta'>{meta}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Input area
    st.markdown("---")
    user_query = st.text_area(
        "💬 Your query",
        placeholder="Ask anything about code, APIs, frameworks, architectures...",
        height=100,
        key="tab1_query",
    )

    col_btn1, col_btn2 = st.columns([4, 1])
    with col_btn1:
        execute_btn = st.button("🚀 Execute Agent Query", use_container_width=True, key="tab1_execute")
    with col_btn2:
        if st.button("🗑️ Clear Chat", use_container_width=True, key="tab1_clear"):
            st.session_state.chat_history = []
            engine.clear_memory()
            st.rerun()

    if execute_btn:
        if not user_query.strip():
            st.error("Please enter a query.")
        else:
            url_to_use = target_url.strip() if target_url.strip() else None
            spinner_msg = (
                "🌐 Scraping live web data · Indexing vectors · Querying LLM..."
                if url_to_use else
                "🧠 Processing with ZeravaneAI base engine..."
            )
            with st.spinner(spinner_msg):
                response_text, context_payload, scrape_method, model_used = engine.execute_live_agent_query(
                    user_query=user_query,
                    target_url=url_to_use,
                    force_rescrape=force_rescrape,
                    use_memory=st.session_state.memory_enabled,
                )

            if url_to_use:
                st.session_state.last_url = url_to_use

            st.session_state.chat_history.append({
                "query":        user_query,
                "response":     response_text,
                "scrape_method": scrape_method,
                "model_used":   model_used,
                "url":          url_to_use,
            })

            st.markdown("### 🤖 ZeravaneAI Response")
            meta_parts = [f"<b style='color:#00D9FF;'>{scrape_method}</b>"]
            meta_parts.append(f"<span class='model-tag'>{model_used}</span>")
            if st.session_state.memory_enabled:
                turns = len(engine.conversation_memory) // 2
                meta_parts.append(f"<span class='memory-tag'>🧠 Memory: {turns} turns</span>")
            st.markdown(
                f"<small style='color:#555;'>{' · '.join(meta_parts)}</small>",
                unsafe_allow_html=True,
            )
            st.markdown(response_text)

            with st.expander("🔍 Inspect Vector Context"):
                st.text_area(
                    "Retrieved context injected into LLM:",
                    value=context_payload or "[No context retrieved — running on base weights]",
                    disabled=True,
                    height=180,
                )

            st.rerun()

# =============================================================================
# TAB 2 — MULTI-URL RAG
# =============================================================================
with tab2:
    st.subheader("🔗 Multi-URL RAG Engine")
    st.caption("Scrape multiple URLs and build a unified knowledge base to query across all of them.")

    st.markdown("""
    <div class='banner'>
        <span style='color:#00D9FF; font-weight:700;'>📡 Multi-Source Intelligence</span>
        <span style='color:#7A8AB5; font-size:12px; margin-left:12px;'>
            Each URL scraped via 3-tier fallback · Merged into unified ChromaDB index
        </span>
    </div>
    """, unsafe_allow_html=True)

    multi_urls_input = st.text_area(
        "Enter URLs (one per line)",
        placeholder="https://docs.fastapi.tiangolo.com\nhttps://docs.pydantic.dev\nhttps://www.uvicorn.org",
        height=130,
        key="multi_urls",
    )
    multi_query = st.text_area(
        "💬 Query across all sources",
        placeholder="Compare authentication approaches across these frameworks...",
        height=80,
        key="multi_query",
    )

    if st.button("🚀 Scrape All + Query", use_container_width=True, key="multi_execute"):
        urls = [u.strip() for u in multi_urls_input.strip().splitlines() if u.strip()]
        if not urls:
            st.error("Enter at least one URL.")
        elif not multi_query.strip():
            st.error("Enter a query.")
        else:
            with st.spinner(f"🌐 Scraping {len(urls)} URLs..."):
                chunks, summary = engine.scrape_multiple_urls(urls)

            st.markdown("#### 📊 Scrape Results")
            for line in summary.splitlines():
                st.success(line) if line.startswith("✅") else st.error(line)

            if chunks:
                with st.spinner("🧠 Querying merged knowledge base..."):
                    context_payload = engine.query_vector_context(
                        collection_name="zeravane_multi_url",
                        query=multi_query,
                        n_results=5,
                    )
                    system = (
                        "You are ZeravaneAI, a multi-source web intelligence agent. "
                        "Answer using merged content from all provided URLs. Cite sources."
                    )
                    prompt = (
                        f"Sources: {', '.join(urls)}\n\n"
                        f"=== MERGED CONTENT ===\n{context_payload}\n\n"
                        f"=== QUESTION ===\n{multi_query}"
                    )
                    response_text, model_used = engine._infer(system, prompt)

                st.markdown("### 🤖 Response")
                st.markdown(
                    f"<small style='color:#555;'>Sources: {len(urls)} URLs merged · "
                    f"<span class='model-tag'>{model_used}</span></small>",
                    unsafe_allow_html=True,
                )
                st.markdown(response_text)
            else:
                st.warning("No URLs scraped successfully.")

# =============================================================================
# TAB 3 — GITHUB ANALYZER
# =============================================================================
with tab3:
    st.subheader("🐙 GitHub Repo Analyzer")
    st.caption("Deep-dive any public GitHub repo — README, file tree, metadata, topics — then ask anything about it.")

    st.markdown("""
    <div class='banner'>
        <span style='color:#00D9FF; font-weight:700;'>🐙 GitHub API + RAG</span>
        <span style='color:#7A8AB5; font-size:12px; margin-left:12px;'>
            README · File tree · Metadata · Stars · License · Topics
        </span>
    </div>
    """, unsafe_allow_html=True)

    github_url_input = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/tiangolo/fastapi",
        key="github_url",
    )
    github_query = st.text_area(
        "💬 Ask about this repo",
        placeholder="How do I get started? What does this project do? What's the architecture?",
        height=80,
        key="github_query",
    )

    if st.button("🚀 Analyze Repository", use_container_width=True, key="github_execute"):
        if not github_url_input.strip():
            st.error("Enter a GitHub URL.")
        elif not github_query.strip():
            st.error("Enter a question.")
        else:
            with st.spinner("🐙 Fetching repository via GitHub API..."):
                repo_content, metadata = engine.analyze_github_repo(github_url_input.strip())

            if metadata:
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("⭐ Stars",    f"{metadata.get('stars', 0):,}")
                m2.metric("🍴 Forks",    f"{metadata.get('forks', 0):,}")
                m3.metric("🐛 Issues",   f"{metadata.get('open_issues', 0):,}")
                m4.metric("💻 Language", metadata.get("language", "N/A"))
                m5.metric("📄 License",  metadata.get("license", "N/A"))

                if metadata.get("description"):
                    st.info(f"📝 {metadata['description']}")
                if metadata.get("topics"):
                    tags = " ".join([f"<span class='badge badge-purple'>{t}</span>" for t in metadata["topics"][:10]])
                    st.markdown(tags, unsafe_allow_html=True)

            if not repo_content.startswith(("GitHub_Error", "Invalid")):
                with st.spinner("🧠 Analysing + answering..."):
                    context_payload = engine.query_vector_context(
                        collection_name="zeravane_github",
                        query=github_query,
                        n_results=4,
                    ) or repo_content[:7000]
                    system = (
                        "You are ZeravaneAI, a GitHub repository analyst. "
                        "Answer the user's question from the repository data provided. "
                        "Be specific, cite file names, README sections, or metadata."
                    )
                    prompt = (
                        f"Repository: {github_url_input.strip()}\n\n"
                        f"=== REPO DATA ===\n{context_payload}\n\n"
                        f"=== QUESTION ===\n{github_query}"
                    )
                    response_text, model_used = engine._infer(system, prompt)

                st.markdown("### 🤖 Response")
                st.markdown(
                    f"<small style='color:#555;'>GitHub API · <span class='model-tag'>{model_used}</span></small>",
                    unsafe_allow_html=True,
                )
                st.markdown(response_text)

                with st.expander("📁 Raw Repository Data"):
                    st.text_area("", value=repo_content[:4000], disabled=True, height=250)
            else:
                st.error(f"Failed: {repo_content}")

# =============================================================================
# TAB 4 — TECH STACK DETECTOR
# =============================================================================
with tab4:
    st.subheader("🔍 Tech Stack Detector")
    st.caption("Scrape any website live and detect its full technology stack using AI analysis.")

    st.markdown("""
    <div class='banner'>
        <span style='color:#00D9FF; font-weight:700;'>🔬 AI-Powered Stack Analysis</span>
        <span style='color:#7A8AB5; font-size:12px; margin-left:12px;'>
            Live scrape · Pattern recognition · Confidence-rated results
        </span>
    </div>
    """, unsafe_allow_html=True)

    stack_url = st.text_input(
        "Website URL",
        placeholder="https://vercel.com  or  https://github.com/tiangolo/fastapi",
        key="stack_url",
    )

    if st.button("🔍 Detect Tech Stack", use_container_width=True, key="stack_execute"):
        if not stack_url.strip():
            st.error("Enter a URL.")
        else:
            with st.spinner("🌐 Scraping + analysing tech stack..."):
                raw_content, scrape_method = engine.scrape_live_url(stack_url.strip())
                stack_report = engine.detect_tech_stack(raw_content, stack_url.strip())

            st.markdown(
                f"<small style='color:#555;'>Scrape: <b style='color:#00D9FF;'>{scrape_method}</b></small>",
                unsafe_allow_html=True,
            )
            st.markdown("### 🛠️ Detected Stack")
            st.markdown(stack_report)

            with st.expander("🔍 Raw Scraped Content (first 2500 chars)"):
                st.text_area("", value=raw_content[:2500], disabled=True, height=160)

# =============================================================================
# TAB 5 — CODE GENERATOR
# =============================================================================
with tab5:
    st.subheader("⚙️ Code Generator from Live Docs")
    st.caption("Paste any documentation URL — ZeravaneAI scrapes it and generates production-ready code from it.")

    st.markdown("""
    <div class='banner'>
        <span style='color:#00D9FF; font-weight:700;'>🤖 Live Docs → Production Code</span>
        <span style='color:#7A8AB5; font-size:12px; margin-left:12px;'>
            Crawl4AI fetches docs · RAG indexes content · LLM generates boilerplate
        </span>
    </div>
    """, unsafe_allow_html=True)

    codegen_url = st.text_input(
        "Documentation URL",
        placeholder="https://docs.stripe.com/api  or  https://docs.fastapi.tiangolo.com",
        key="codegen_url",
    )
    codegen_request = st.text_area(
        "💬 What code should be generated?",
        placeholder="Create a complete REST API with CRUD operations and JWT authentication...",
        height=80,
        key="codegen_request",
    )
    codegen_language = st.selectbox(
        "Target Language",
        ["Python", "TypeScript", "JavaScript", "Go", "Rust", "Java", "C#", "PHP", "Ruby", "Kotlin"],
        key="codegen_lang",
    )

    if st.button("⚙️ Generate Code from Live Docs", use_container_width=True, key="codegen_execute"):
        if not codegen_url.strip():
            st.error("Enter a documentation URL.")
        elif not codegen_request.strip():
            st.error("Describe what code you want generated.")
        else:
            with st.spinner(f"🌐 Scraping docs · Generating {codegen_language} code..."):
                generated_code, scrape_method, model_used = engine.generate_code_from_docs(
                    docs_url=codegen_url.strip(),
                    generation_request=codegen_request.strip(),
                    language=codegen_language,
                )

            st.markdown(
                f"<small style='color:#555;'>Docs: <b style='color:#00D9FF;'>{scrape_method}</b> · "
                f"<span class='model-tag'>{model_used}</span></small>",
                unsafe_allow_html=True,
            )
            st.markdown(f"### ⚙️ Generated {codegen_language} Code")
            st.markdown(generated_code)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<p style='text-align:center; font-size:11px; color:#333; letter-spacing:1px;'>
ZeravaneAI v3.0 · Built by Franklin Josva ·
⚡ Gemini 2.5 Flash · 🟣 Groq · 🔶 AI/ML API · 🖥️ Ollama · 🟢 Crawl4AI
</p>
""", unsafe_allow_html=True)
