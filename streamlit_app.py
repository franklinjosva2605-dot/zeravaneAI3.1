"""
ZeravaneAI v3.1 — Streamlit entry point (production-ready)
Run: streamlit run streamlit_app.py

⚠️ CRITICAL: This MUST be the entry point for Streamlit Cloud.
Set "Main file path" to: streamlit_app.py (not nested paths)
"""
import os
import sys

# [CRITICAL] Set protobuf implementation BEFORE any imports
# chromadb's opentelemetry integration breaks with protobuf 7.x in Python 3.14
# unless we use the pure-Python implementation
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import importlib.util

# Get base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Try nested development structure first
nested_app_path = os.path.join(base_dir, "zeravaneAI3_1_fixed3 (1)", "zeravane_fixed", "zeravaneai", "frontend", "app.py")

# Try flat production structure second
flat_app_path = os.path.join(base_dir, "zeravaneai", "frontend", "app.py")

# Determine which path exists
if os.path.isfile(nested_app_path):
    app_path = nested_app_path
    os.chdir(os.path.dirname(os.path.dirname(app_path)))  # Navigate to zeravaneai directory
elif os.path.isfile(flat_app_path):
    app_path = flat_app_path
    os.chdir(os.path.dirname(os.path.dirname(app_path)))  # Navigate to zeravaneai directory
else:
    import streamlit as st
    st.error(
        "❌ **Critical Error**: ZeravaneAI module not found!\n\n"
        f"Expected either:\n"
        f"  • `{nested_app_path}`\n"
        f"  • `{flat_app_path}`\n\n"
        "Please ensure the repository structure is correct."
    )
    st.stop()

# Load and execute the frontend app
spec = importlib.util.spec_from_file_location("frontend_app", app_path)
frontend_app = importlib.util.module_from_spec(spec)
sys.modules["frontend_app"] = frontend_app
spec.loader.exec_module(frontend_app)
