"""
Session State Management
Handles session state initialization and management
"""

import streamlit as st
from datetime import datetime

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Authentication state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None
    
    # Navigation state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    # Data state
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    
    if 'source_data' not in st.session_state:
        st.session_state.source_data = None
    
    if 'target_data' not in st.session_state:
        st.session_state.target_data = None
    
    # Analysis results
    if 'profiling_results' not in st.session_state:
        st.session_state.profiling_results = None
    
    if 'quality_results' not in st.session_state:
        st.session_state.quality_results = None
    
    if 'reconciliation_results' not in st.session_state:
        st.session_state.reconciliation_results = None
    
    # UI state
    if 'show_sidebar' not in st.session_state:
        st.session_state.show_sidebar = True
    
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def reset_session():
    """Reset all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()

def get_session_info():
    """Get current session information"""
    return {
        'authenticated': st.session_state.get('authenticated', False),
        'username': st.session_state.get('username', None),
        'login_time': st.session_state.get('login_time', None),
        'current_page': st.session_state.get('current_page', 'dashboard')
    }

# Made with Bob
