"""
Authentication Module
Handles user authentication and login functionality
"""

import streamlit as st
from datetime import datetime
import hashlib

# Demo credentials with roles (In production, use proper database and hashing)
DEMO_USERS = {
    'admin': {
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
        'role': 'admin',
        'group': None
    },
    'auditor': {
        'password': hashlib.sha256('audit123'.encode()).hexdigest(),
        'role': 'auditor',
        'group': None
    },
    'auditor2': {
        'password': hashlib.sha256('audit123'.encode()).hexdigest(),
        'role': 'auditor',
        'group': None
    },
    'coordinator1': {
        'password': hashlib.sha256('coord123'.encode()).hexdigest(),
        'role': 'coordinator',
        'group': 'Finance'
    },
    'coordinator2': {
        'password': hashlib.sha256('coord123'.encode()).hexdigest(),
        'role': 'coordinator',
        'group': 'Operations'
    },
    'coordinator3': {
        'password': hashlib.sha256('coord123'.encode()).hexdigest(),
        'role': 'coordinator',
        'group': 'IT'
    },
    'demo': {
        'password': hashlib.sha256('demo123'.encode()).hexdigest(),
        'role': 'admin',
        'group': None
    }
}

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username: str, password: str) -> tuple:
    """Verify user credentials and return (success, role, group)"""
    if username in DEMO_USERS:
        user_data = DEMO_USERS[username]
        if user_data['password'] == hash_password(password):
            return True, user_data['role'], user_data.get('group')
    return False, None, None

def check_authentication() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def login_user(username: str, role: str, group: str | None = None):
    """Log in user and set session state"""
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.user_role = role
    st.session_state.user_group = group
    st.session_state.login_time = datetime.now()

def logout_user():
    """Log out user and clear session"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.user_group = None
    st.session_state.login_time = None
    st.session_state.current_page = 'dashboard'

def login_page():
    """Render login page"""
    
    # Custom CSS for login page
    st.markdown("""
        <style>
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            font-size: 1.2rem;
            color: #666;
        }
        .demo-credentials {
            background-color: #f0f8ff;
            border-left: 4px solid #1f77b4;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }
        .demo-credentials h4 {
            margin-top: 0;
            color: #1f77b4;
        }
        .demo-credentials code {
            background-color: #e8f4f8;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="login-header">
            <div class="login-title">📊 Audit Canvas</div>
            <div class="login-subtitle">AI-Assisted Audit Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Demo credentials info
    st.markdown("""
        <div class="demo-credentials">
            <h4>🔑 Demo Credentials</h4>
            <p><strong>Admin:</strong> <code>admin</code> / <code>admin123</code></p>
            <p><strong>Auditor:</strong> <code>auditor</code> / <code>audit123</code></p>
            <p><strong>Coordinator (Finance):</strong> <code>coordinator1</code> / <code>coord123</code></p>
            <p><strong>Coordinator (Operations):</strong> <code>coordinator2</code> / <code>coord123</code></p>
            <p><strong>Coordinator (IT):</strong> <code>coordinator3</code> / <code>coord123</code></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        st.subheader("🔐 Login")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("⚠️ Please enter both username and password")
            else:
                success, role, group = verify_credentials(username, password)
                if success:
                    login_user(username, role, group)
                    role_display = f"{role.title()}" + (f" ({group})" if group else "")
                    st.success(f"✅ Welcome back, {username}! Role: {role_display}")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            <p>🏆 IBM Bob Dev Hackathon Project</p>
            <p>Powered by AI • Streamlit • Python</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Made with Bob
