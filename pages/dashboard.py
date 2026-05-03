"""
Main Dashboard Page
Central hub for the Audit Canvas platform
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import logout_user
from utils.data_models import audit_db

def render_sidebar():
    """Render sidebar navigation with role-based menu"""
    with st.sidebar:
        st.title("📊 Audit Canvas")
        
        # User info
        username = st.session_state.username
        user_role = st.session_state.get('user_role', 'user')
        user_group = st.session_state.get('user_group')
        
        st.markdown(f"**User:** {username}")
        role_display = user_role.title()
        if user_group:
            role_display += f" ({user_group})"
        st.markdown(f"**Role:** {role_display}")
        st.markdown("---")
        
        # Navigation menu - role-based
        st.subheader("📋 Navigation")
        
        # Define menu items based on role
        if user_role == 'coordinator':
            menu_items = {
                'dashboard': '🏠 Dashboard',
                'my_items': '📋 My Assigned Items',
                'settings': '⚙️ Settings'
            }
        elif user_role == 'auditor':
            menu_items = {
                'dashboard': '🏠 Dashboard',
                'projects': '📁 Projects',
                'document_review': '📄 Document Review',
                'upload': '📤 Upload Data',
                'profiling': '🔍 Data Profiling',
                'quality': '✅ Quality Checks',
                'reconciliation': '🔄 Reconciliation',
                'reports': '📊 Reports',
                'settings': '⚙️ Settings'
            }
        else:  # admin or other roles
            menu_items = {
                'dashboard': '🏠 Dashboard',
                'projects': '📁 Projects',
                'document_review': '📄 Document Review',
                'upload': '📤 Upload Data',
                'profiling': '🔍 Data Profiling',
                'quality': '✅ Quality Checks',
                'reconciliation': '🔄 Reconciliation',
                'reports': '📊 Reports',
                'settings': '⚙️ Settings'
            }
        
        for key, label in menu_items.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats - role-based
        st.subheader("📈 Quick Stats")
        
        if user_role == 'coordinator':
            # Show coordinator stats
            assignments = audit_db.get_assignments_by_coordinator(username)
            pending = 0
            for a in assignments:
                item = audit_db.get_item(a.item_id)
                if item and item.status == 'pending':
                    pending += 1
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Assigned Items", len(assignments))
            with col2:
                st.metric("Pending", pending)
        
        elif user_role == 'auditor':
            # Show auditor stats
            projects = audit_db.get_projects_by_auditor(username)
            active_projects = sum(1 for p in projects if p.status == 'active')
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Projects", len(projects))
            with col2:
                st.metric("Active", active_projects)
        
        else:
            # Show general stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Files Uploaded", len(st.session_state.uploaded_files))
            with col2:
                st.metric("Active Tasks", 0)
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()

def render_dashboard_home():
    """Render main dashboard home page"""
    st.title("🏠 Dashboard")
    st.markdown(f"Welcome back, **{st.session_state.username}**!")
    
    # Key metrics
    st.subheader("📊 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📁 Total Files",
            value=len(st.session_state.uploaded_files),
            delta="0 new"
        )
    
    with col2:
        st.metric(
            label="✅ Quality Checks",
            value="0",
            delta="0 passed"
        )
    
    with col3:
        st.metric(
            label="🔄 Reconciliations",
            value="0",
            delta="0 completed"
        )
    
    with col4:
        st.metric(
            label="📊 Reports",
            value="0",
            delta="0 generated"
        )
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Upload New Data", use_container_width=True):
            st.session_state.current_page = 'upload'
            st.rerun()
    
    with col2:
        if st.button("🔍 Run Profiling", use_container_width=True):
            st.session_state.current_page = 'profiling'
            st.rerun()
    
    with col3:
        if st.button("🔄 Start Reconciliation", use_container_width=True):
            st.session_state.current_page = 'reconciliation'
            st.rerun()
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    st.info("No recent activity. Upload data to get started!")
    
    # Platform features
    st.markdown("---")
    st.subheader("🎯 Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Data Quality & Profiling**
        - 📊 Automated data profiling
        - 🔍 Missing values detection
        - 📈 Statistical analysis
        - 🎯 Outlier identification
        - ✅ Data type validation
        """)
        
        st.markdown("""
        **Reconciliation Engine**
        - 🔄 Record count comparison
        - 🔎 Missing records detection
        - 🗺️ Column mapping validation
        - ⚖️ Data consistency checks
        """)
    
    with col2:
        st.markdown("""
        **AI-Powered Insights**
        - 🤖 Anomaly explanations
        - 💡 Smart suggestions
        - 📝 Auto-documentation
        - 🎨 Column mapping AI
        """)
        
        st.markdown("""
        **Report Generation**
        - 📊 Excel workpapers
        - 📄 HTML audit reports
        - 📈 Interactive visualizations
        - 💾 Export capabilities
        """)

def render_projects_page():
    """Render projects management page"""
    from components.projects import render_projects_component
    render_projects_component()

def render_document_review_page():
    """Render document review page"""
    from components.document_review import render_document_review_component
    render_document_review_component()

def render_my_items_page():
    """Render coordinator's assigned items page"""
    from components.coordinator import render_coordinator_component
    render_coordinator_component()

def render_upload_page():
    """Render data upload page"""
    from components.upload import render_upload_component
    render_upload_component()

def render_profiling_page():
    """Render data profiling page"""
    from components.profiling import render_profiling_component
    render_profiling_component()

def render_quality_page():
    """Render quality checks page"""
    from components.quality import render_quality_component
    render_quality_component()

def render_reconciliation_page():
    """Render reconciliation page"""
    from components.reconciliation import render_reconciliation_component
    render_reconciliation_component()

def render_reports_page():
    """Render reports page"""
    from components.reports import render_reports_component
    render_reports_component()

def render_settings_page():
    """Render settings page"""
    st.title("⚙️ Settings")
    st.subheader("User Preferences")
    
    # Theme selection
    theme = st.selectbox("Theme", ["Light", "Dark"], index=0)
    
    # Notification settings
    st.checkbox("Enable notifications", value=True)
    st.checkbox("Email reports", value=False)
    
    # Data retention
    st.subheader("Data Management")
    retention_days = st.slider("Data retention (days)", 7, 90, 30)
    
    if st.button("Save Settings"):
        st.success("✅ Settings saved successfully!")

def render_dashboard():
    """Main dashboard render function"""
    
    # Render sidebar
    render_sidebar()
    
    # Render current page
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard':
        render_dashboard_home()
    elif current_page == 'projects':
        render_projects_page()
    elif current_page == 'document_review':
        render_document_review_page()
    elif current_page == 'my_items':
        render_my_items_page()
    elif current_page == 'upload':
        render_upload_page()
    elif current_page == 'profiling':
        render_profiling_page()
    elif current_page == 'quality':
        render_quality_page()
    elif current_page == 'reconciliation':
        render_reconciliation_page()
    elif current_page == 'reports':
        render_reports_page()
    elif current_page == 'settings':
        render_settings_page()
    else:
        render_dashboard_home()

# Made with Bob
