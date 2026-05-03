"""
AI-Assisted Audit Platform - Main Application
Audit Canvas - IBM Bob Dev Hackathon
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="Audit Canvas - AI Audit Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load EY Canvas-style CSS
def load_css():
    with open('assets/ey_canvas_style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Import utilities
from utils.auth import check_authentication, login_page
from utils.session import initialize_session_state

# Initialize session state
initialize_session_state()

# Authentication check
if not check_authentication():
    login_page()
else:
    # Import main dashboard after authentication
    from pages.dashboard import render_dashboard
    render_dashboard()

# Made with Bob
