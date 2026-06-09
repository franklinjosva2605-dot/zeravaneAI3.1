"""
ZeravaneAI v3.1 — Streamlit entry point
Run: streamlit run streamlit_app.py
"""
import os
import sys
import runpy

# Force protobuf to use its pure-Python implementation.
# The C extension in protobuf <5 crashes on Python 3.14 (Streamlit Cloud)
# because _message.so was compiled against an older ABI.
# Must be set BEFORE any import that transitively loads protobuf
# (chromadb → opentelemetry → google.protobuf).
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

# Set working directory to zeravaneai package
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "zeravaneai"))
sys.path.insert(0, os.getcwd())

runpy.run_path("frontend/app.py", run_name="__main__")
