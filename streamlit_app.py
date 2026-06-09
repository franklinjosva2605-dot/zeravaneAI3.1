"""
ZeravaneAI v3.1 — Streamlit entry point (production-safe)
Run: streamlit run streamlit_app.py

This entry point handles multiple directory structures:
  1. Nested (development): zeravaneAI3_1_fixed3 (1)/zeravane_fixed/zeravaneai/
  2. Flat (production/Streamlit Cloud): ./zeravaneai/
"""
import os
import sys

# Get the absolute path of this file's directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Strategy 1: Try nested development structure
nested_path = os.path.join(base_dir, "zeravaneAI3_1_fixed3 (1)", "zeravane_fixed", "zeravaneai")
if os.path.isdir(nested_path):
    os.chdir(nested_path)
    sys.path.insert(0, os.getcwd())
    exec(open(os.path.join(nested_path, "frontend", "app.py")).read())
else:
    # Strategy 2: Try flat production structure
    flat_path = os.path.join(base_dir, "zeravaneai")
    if os.path.isdir(flat_path):
        os.chdir(flat_path)
        sys.path.insert(0, os.getcwd())
        exec(open(os.path.join(flat_path, "frontend", "app.py")).read())
    else:
        # Strategy 3: Direct import (if zeravaneai package is available)
        sys.path.insert(0, base_dir)
        import streamlit as st
        st.error(
            "❌ Failed to locate ZeravaneAI module. Expected either:\n"
            f"  - {nested_path}\n"
            f"  - {flat_path}"
        )
        st.stop()
