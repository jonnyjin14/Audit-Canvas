"""
Comments Component
Thread-style comments for auditors and coordinators to communicate
"""

import streamlit as st
from datetime import datetime
import uuid
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_models import audit_db, Comment, ActivityLog

def generate_id(prefix: str) -> str:
    """Generate unique ID with prefix"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def render_comments_section(item_id: str, item_title: str):
    """
    Render comments section for an audit item
    Both auditors and coordinators can view and post comments
    
    Args:
        item_id: The audit item ID
        item_title: The audit item title for context
    """
    
    st.markdown("---")
    st.subheader("💬 Comments & Discussion")
    
    # Get current user info
    username = st.session_state.get('username', 'Unknown')
    user_role = st.session_state.get('user_role', 'unknown')
    
    # Get all comments for this item
    comments = audit_db.get_comments_by_item(item_id)
    
    # Display existing comments
    if comments:
        st.markdown(f"**{len(comments)} comment(s)**")
        
        for comment in comments:
            render_comment(comment, username, user_role)
    else:
        st.info("💭 No comments yet. Start the conversation!")
    
    # Add new comment form
    st.markdown("---")
    st.markdown("**Add Comment:**")
    
    with st.form(key=f"comment_form_{item_id}", clear_on_submit=True):
        comment_text = st.text_area(
            "Your comment",
            placeholder="Type your message here...",
            height=100,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submit_button = st.form_submit_button("💬 Post", use_container_width=True)
        
        if submit_button and comment_text.strip():
            # Create new comment
            comment_id = generate_id("comment")
            new_comment = Comment(
                comment_id=comment_id,
                item_id=item_id,
                user=username,
                comment_text=comment_text.strip(),
                comment_type='comment'
            )
            
            # Save comment
            audit_db.save_comment(new_comment)
            
            # Log activity
            log_id = generate_id("log")
            activity_log = ActivityLog(
                log_id=log_id,
                item_id=item_id,
                user=username,
                action='comment_added',
                details=f"Added comment: {comment_text[:50]}..."
            )
            audit_db.save_activity_log(activity_log)
            
            st.success("✅ Comment posted!")
            st.rerun()

def render_comment(comment: Comment, current_user: str, current_role: str):
    """
    Render a single comment with styling
    
    Args:
        comment: Comment object
        current_user: Current logged-in username
        current_role: Current user's role
    """
    
    # Determine if this is the current user's comment
    is_own_comment = comment.user == current_user
    
    # Format timestamp
    try:
        timestamp = datetime.fromisoformat(comment.created_at)
        time_str = timestamp.strftime("%b %d, %Y at %I:%M %p")
    except:
        time_str = comment.created_at
    
    # Create comment container with styling
    with st.container():
        # Header with user and timestamp
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            # Show user with role badge
            if is_own_comment:
                st.markdown(f"**👤 {comment.user}** (You)")
            else:
                st.markdown(f"**👤 {comment.user}**")
        
        with col2:
            st.markdown(f"*{time_str}*")
        
        with col3:
            # Delete button (only for own comments or admins)
            if is_own_comment or current_role == 'admin':
                if st.button("🗑️", key=f"delete_{comment.comment_id}", help="Delete comment"):
                    audit_db.delete_comment(comment.comment_id)
                    st.success("Comment deleted")
                    st.rerun()
        
        # Comment text with background
        if is_own_comment:
            # Own comments - light blue background
            st.markdown(
                f"""
                <div style="background-color: #E3F2FD; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    {comment.comment_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Others' comments - light gray background
            st.markdown(
                f"""
                <div style="background-color: #F5F5F5; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    {comment.comment_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("")  # Add spacing

def render_activity_timeline(item_id: str):
    """
    Render activity timeline for an item
    Shows all status changes, document submissions, etc.
    
    Args:
        item_id: The audit item ID
    """
    
    st.markdown("---")
    st.subheader("📊 Activity Timeline")
    
    # Get activity logs
    logs = audit_db.get_activity_logs_by_item(item_id)
    
    if not logs:
        st.info("No activity yet")
        return
    
    # Display timeline
    for log in logs:
        render_activity_log(log)

def render_activity_log(log: ActivityLog):
    """
    Render a single activity log entry
    
    Args:
        log: ActivityLog object
    """
    
    # Format timestamp
    try:
        timestamp = datetime.fromisoformat(log.timestamp)
        time_str = timestamp.strftime("%b %d, %Y at %I:%M %p")
    except:
        time_str = log.timestamp
    
    # Determine icon based on action
    action_icons = {
        'status_change': '🔄',
        'document_submitted': '📄',
        'comment_added': '💬',
        'item_created': '➕',
        'item_updated': '✏️',
        'assignment_added': '👥',
        'due_date_changed': '📅'
    }
    
    icon = action_icons.get(log.action, '📌')
    
    # Create activity entry
    with st.container():
        col1, col2 = st.columns([1, 5])
        
        with col1:
            st.markdown(f"### {icon}")
        
        with col2:
            st.markdown(f"**{log.user}** {log.action.replace('_', ' ')}")
            if log.details:
                st.markdown(f"*{log.details}*")
            if log.old_value and log.new_value:
                st.markdown(f"Changed from `{log.old_value}` to `{log.new_value}`")
            st.markdown(f"<small>{time_str}</small>", unsafe_allow_html=True)
        
        st.markdown("")  # Spacing

def add_status_change_comment(item_id: str, old_status: str, new_status: str, username: str):
    """
    Automatically add a comment when status changes
    
    Args:
        item_id: The audit item ID
        old_status: Previous status
        new_status: New status
        username: User who made the change
    """
    
    comment_id = generate_id("comment")
    comment_text = f"Status changed from '{old_status}' to '{new_status}'"
    
    comment = Comment(
        comment_id=comment_id,
        item_id=item_id,
        user=username,
        comment_text=comment_text,
        comment_type='status_change'
    )
    
    audit_db.save_comment(comment)
    
    # Also log activity
    log_id = generate_id("log")
    activity_log = ActivityLog(
        log_id=log_id,
        item_id=item_id,
        user=username,
        action='status_change',
        details=comment_text,
        old_value=old_status,
        new_value=new_status
    )
    audit_db.save_activity_log(activity_log)

def add_assignment_comment(item_id: str, coordinator_username: str, auditor_username: str):
    """
    Automatically add a comment when coordinator is assigned
    
    Args:
        item_id: The audit item ID
        coordinator_username: Coordinator being assigned
        auditor_username: Auditor making the assignment
    """
    
    comment_id = generate_id("comment")
    comment_text = f"Assigned to {coordinator_username}"
    
    comment = Comment(
        comment_id=comment_id,
        item_id=item_id,
        user=auditor_username,
        comment_text=comment_text,
        comment_type='assignment'
    )
    
    audit_db.save_comment(comment)
    
    # Also log activity
    log_id = generate_id("log")
    activity_log = ActivityLog(
        log_id=log_id,
        item_id=item_id,
        user=auditor_username,
        action='assignment_added',
        details=comment_text
    )
    audit_db.save_activity_log(activity_log)

def add_document_comment(item_id: str, filename: str, coordinator_username: str):
    """
    Automatically add a comment when document is submitted
    
    Args:
        item_id: The audit item ID
        filename: Name of submitted document
        coordinator_username: Coordinator who submitted
    """
    
    comment_id = generate_id("comment")
    comment_text = f"Submitted document: {filename}"
    
    comment = Comment(
        comment_id=comment_id,
        item_id=item_id,
        user=coordinator_username,
        comment_text=comment_text,
        comment_type='document_submission'
    )
    
    audit_db.save_comment(comment)
    
    # Also log activity
    log_id = generate_id("log")
    activity_log = ActivityLog(
        log_id=log_id,
        item_id=item_id,
        user=coordinator_username,
        action='document_submitted',
        details=comment_text
    )
    audit_db.save_activity_log(activity_log)

# Made with Bob