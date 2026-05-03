"""
Document Review Component
For auditors to review submitted documents and provide feedback
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import uuid

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_models import audit_db, Comment, ActivityLog

def generate_id(prefix: str) -> str:
    """Generate unique ID with prefix"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def render_document_review_component():
    """Main document review interface for auditors"""
    
    st.title("📄 Document Review")
    
    # Check if user is auditor
    if st.session_state.get('user_role') not in ['auditor', 'admin']:
        st.error("⚠️ Access Denied: Only auditors can access this page")
        return
    
    username = st.session_state.username
    
    # Get all projects by this auditor
    projects = audit_db.get_projects_by_auditor(username)
    
    if not projects:
        st.info("📝 No projects yet. Create a project first!")
        return
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs([
        "📥 Pending Review",
        "✅ Reviewed",
        "📊 All Submissions"
    ])
    
    with tab1:
        render_pending_documents(projects)
    
    with tab2:
        render_reviewed_documents(projects)
    
    with tab3:
        render_all_submissions(projects)

def render_pending_documents(projects):
    """Display documents pending review"""
    
    st.subheader("Documents Pending Review")
    
    pending_count = 0
    
    for project in projects:
        items = audit_db.get_items_by_project(project.project_id)
        
        for item in items:
            documents = audit_db.get_documents_by_item(item.item_id)
            pending_docs = [d for d in documents if d.status == 'submitted']
            
            if pending_docs:
                pending_count += len(pending_docs)
                
                with st.expander(f"📋 {item.title} ({project.name}) - {len(pending_docs)} pending", expanded=True):
                    st.markdown(f"**Item Description:** {item.description}")
                    st.markdown(f"**Due Date:** {item.due_date}")
                    st.markdown("---")
                    
                    for doc in pending_docs:
                        render_document_review_card(doc, item, project)
    
    if pending_count == 0:
        st.info("✅ No documents pending review. Great job!")

def render_reviewed_documents(projects):
    """Display reviewed documents"""
    
    st.subheader("Recently Reviewed Documents")
    
    reviewed_count = 0
    
    for project in projects:
        items = audit_db.get_items_by_project(project.project_id)
        
        for item in items:
            documents = audit_db.get_documents_by_item(item.item_id)
            reviewed_docs = [d for d in documents if d.status in ['approved', 'rejected']]
            
            if reviewed_docs:
                reviewed_count += len(reviewed_docs)
                
                with st.expander(f"📋 {item.title} ({project.name}) - {len(reviewed_docs)} reviewed"):
                    for doc in reviewed_docs:
                        render_reviewed_document_card(doc, item)
    
    if reviewed_count == 0:
        st.info("No reviewed documents yet.")

def render_all_submissions(projects):
    """Display all document submissions"""
    
    st.subheader("All Document Submissions")
    
    all_docs = []
    
    for project in projects:
        items = audit_db.get_items_by_project(project.project_id)
        
        for item in items:
            documents = audit_db.get_documents_by_item(item.item_id)
            
            for doc in documents:
                all_docs.append({
                    'Project': project.name,
                    'Item': item.title,
                    'Document': doc.filename,
                    'Submitted By': doc.submitted_by,
                    'Submitted At': doc.submitted_at[:10],
                    'Status': doc.status.title()
                })
    
    if all_docs:
        df = pd.DataFrame(all_docs)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No documents submitted yet.")

def render_document_review_card(doc, item, project):
    """Render a document review card with actions"""
    
    st.markdown(f"### 📄 {doc.filename}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Submitted by:** {doc.submitted_by}")
        st.markdown(f"**Submitted at:** {doc.submitted_at}")
        if doc.notes:
            st.markdown(f"**Coordinator Notes:** {doc.notes}")
    
    with col2:
        st.markdown(f"**Status:** {doc.status.title()}")
        
        # Download button (simulated)
        if st.button("📥 Download", key=f"download_{doc.document_id}"):
            st.info(f"File location: {doc.file_path}")
    
    # Get existing comments for this item
    comments = audit_db.get_comments_by_item(item.item_id)
    
    if comments:
        st.markdown("**💬 Comments & History:**")
        for comment in comments[-3:]:  # Show last 3 comments
            user_role = "Auditor" if comment.user == st.session_state.username else "Coordinator"
            st.markdown(f"- **{comment.user}** ({user_role}): {comment.comment_text} *({comment.created_at[:16]})*")
    
    # Review actions
    st.markdown("---")
    st.markdown("**Review Actions:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Accept", key=f"accept_{doc.document_id}", use_container_width=True):
            st.session_state[f'action_{doc.document_id}'] = 'accept'
            st.rerun()
    
    with col2:
        if st.button("🔄 Return (Need More)", key=f"return_{doc.document_id}", use_container_width=True):
            st.session_state[f'action_{doc.document_id}'] = 'return'
            st.rerun()
    
    with col3:
        if st.button("❌ Reject", key=f"reject_{doc.document_id}", use_container_width=True):
            st.session_state[f'action_{doc.document_id}'] = 'reject'
            st.rerun()
    
    # Handle actions with feedback
    action_key = f'action_{doc.document_id}'
    if action_key in st.session_state:
        render_feedback_form(doc, item, project, st.session_state[action_key])

def render_feedback_form(doc, item, project, action):
    """Render feedback form for document review"""
    
    st.markdown("---")
    
    if action == 'accept':
        st.success("✅ Accepting Document")
        action_text = "Accept"
        new_status = "approved"
        new_item_status = "reviewed"
    elif action == 'return':
        st.warning("🔄 Returning Document for More Information")
        action_text = "Return"
        new_status = "submitted"  # Keep as submitted
        new_item_status = "returned"
    else:  # reject
        st.error("❌ Rejecting Document")
        action_text = "Reject"
        new_status = "rejected"
        new_item_status = "returned"
    
    with st.form(f"feedback_form_{doc.document_id}"):
        feedback = st.text_area(
            "Feedback / Comments*",
            placeholder=f"Provide feedback for the coordinator...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button(f"✅ Confirm {action_text}", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if cancel:
            del st.session_state[f'action_{doc.document_id}']
            st.rerun()
        
        if submit:
            if not feedback:
                st.error("⚠️ Please provide feedback")
            else:
                # Update document status
                doc.status = new_status
                audit_db.save_document(doc)
                
                # Update item status
                old_status = item.status
                item.status = new_item_status
                item.updated_at = datetime.now().isoformat()
                audit_db.save_item(item)
                
                # Add comment
                comment_id = generate_id("CMT")
                comment = Comment(
                    comment_id=comment_id,
                    item_id=item.item_id,
                    user=st.session_state.username,
                    comment_text=f"[{action_text.upper()}] {feedback}",
                    comment_type='status_change'
                )
                audit_db.save_comment(comment)
                
                # Add activity log
                log_id = generate_id("LOG")
                activity_log = ActivityLog(
                    log_id=log_id,
                    item_id=item.item_id,
                    user=st.session_state.username,
                    action=f'document_{action}',
                    details=f"Document '{doc.filename}' {action}ed. Feedback: {feedback}",
                    old_value=old_status,
                    new_value=new_item_status
                )
                audit_db.save_activity_log(activity_log)
                
                st.success(f"✅ Document {action}ed successfully! Coordinator will be notified.")
                del st.session_state[f'action_{doc.document_id}']
                st.rerun()

def render_reviewed_document_card(doc, item):
    """Render a reviewed document card"""
    
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        st.markdown(f"**📄 {doc.filename}**")
        st.markdown(f"*Submitted by: {doc.submitted_by}*")
    
    with col2:
        st.markdown(f"*Submitted: {doc.submitted_at[:10]}*")
    
    with col3:
        if doc.status == 'approved':
            st.success("✅ Approved")
        elif doc.status == 'rejected':
            st.error("❌ Rejected")
    
    # Show last comment
    comments = audit_db.get_comments_by_item(item.item_id)
    if comments:
        last_comment = comments[-1]
        if last_comment.user == st.session_state.username:
            st.markdown(f"*Your feedback: {last_comment.comment_text}*")
    
    st.markdown("---")

def render_item_detail_window(item_id: str):
    """Render detailed item window with all information"""
    
    item = audit_db.get_item(item_id)
    if not item:
        st.error("Item not found")
        return
    
    project = audit_db.get_project(item.project_id)
    
    st.title(f"📋 {item.title}")
    
    # Item information
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Project:** {project.name if project else 'N/A'}")
        st.markdown(f"**Description:** {item.description}")
        st.markdown(f"**Status:** {item.status.replace('_', ' ').title()}")
    
    with col2:
        st.markdown(f"**Due Date:** {item.due_date}")
        st.markdown(f"**Created:** {item.created_at[:10]}")
        st.markdown(f"**Updated:** {item.updated_at[:10]}")
    
    st.markdown("---")
    
    # Assigned coordinators
    st.subheader("👥 Assigned Coordinators")
    assignments = audit_db.get_assignments_by_item(item_id)
    if assignments:
        for assignment in assignments:
            user = audit_db.get_user(assignment.coordinator_username)
            group_info = f" ({user.group})" if user and user.group else ""
            st.markdown(f"- {assignment.coordinator_username}{group_info}")
    else:
        st.info("No coordinators assigned yet")
    
    st.markdown("---")
    
    # Documents
    st.subheader("📄 Submitted Documents")
    documents = audit_db.get_documents_by_item(item_id)
    if documents:
        for doc in documents:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{doc.filename}**")
            with col2:
                st.markdown(f"*by {doc.submitted_by}*")
            with col3:
                st.markdown(f"*{doc.status}*")
    else:
        st.info("No documents submitted yet")
    
    st.markdown("---")
    
    # Comments
    st.subheader("💬 Comments & Communication")
    comments = audit_db.get_comments_by_item(item_id)
    if comments:
        for comment in comments:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{comment.user}:** {comment.comment_text}")
                with col2:
                    st.markdown(f"*{comment.created_at[:16]}*")
                st.markdown("---")
    else:
        st.info("No comments yet")
    
    # Add comment
    with st.form("add_comment_form"):
        new_comment = st.text_area("Add Comment", placeholder="Type your comment here...")
        if st.form_submit_button("💬 Post Comment"):
            if new_comment:
                comment_id = generate_id("CMT")
                comment = Comment(
                    comment_id=comment_id,
                    item_id=item_id,
                    user=st.session_state.username,
                    comment_text=new_comment,
                    comment_type='comment'
                )
                audit_db.save_comment(comment)
                
                # Log activity
                log_id = generate_id("LOG")
                activity_log = ActivityLog(
                    log_id=log_id,
                    item_id=item_id,
                    user=st.session_state.username,
                    action='comment_added',
                    details=new_comment
                )
                audit_db.save_activity_log(activity_log)
                
                st.success("Comment added!")
                st.rerun()
    
    st.markdown("---")
    
    # Activity Log
    st.subheader("📊 Activity Log")
    logs = audit_db.get_activity_logs_by_item(item_id)
    if logs:
        for log in logs[:10]:  # Show last 10 activities
            icon = {
                'document_accept': '✅',
                'document_return': '🔄',
                'document_reject': '❌',
                'document_submitted': '📤',
                'comment_added': '💬',
                'status_change': '🔄'
            }.get(log.action, '📝')
            
            st.markdown(f"{icon} **{log.user}** - {log.action.replace('_', ' ').title()}")
            st.markdown(f"*{log.timestamp[:16]}* - {log.details}")
            if log.old_value and log.new_value:
                st.markdown(f"*Status: {log.old_value} → {log.new_value}*")
            st.markdown("---")
    else:
        st.info("No activity yet")

# Made with Bob
