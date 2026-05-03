"""
Coordinator Dashboard Component
For coordinators to view assigned items and submit documents
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import uuid

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_models import audit_db, Document

def generate_id(prefix: str) -> str:
    """Generate unique ID with prefix"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def render_coordinator_component():
    """Main coordinator dashboard"""
    
    st.title("📋 My Assigned Items")
    
    # Check if user is coordinator
    if st.session_state.get('user_role') != 'coordinator':
        st.error("⚠️ Access Denied: Only coordinators can access this page")
        return
    
    username = st.session_state.username
    user_group = st.session_state.get('user_group', 'N/A')
    
    # Display coordinator info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Coordinator:** {username}")
        st.markdown(f"**Group:** {user_group}")
    with col2:
        # Get assignments
        assignments = audit_db.get_assignments_by_coordinator(username)
        st.metric("Assigned Items", len(assignments))
    
    st.markdown("---")
    
    # Get all assignments for this coordinator
    assignments = audit_db.get_assignments_by_coordinator(username)
    
    if not assignments:
        st.info("📝 No items assigned to you yet. Your auditor will assign items soon.")
        return
    
    # Group items by status
    pending_items = []
    in_progress_items = []
    submitted_items = []
    returned_items = []
    completed_items = []
    
    for assignment in assignments:
        item = audit_db.get_item(assignment.item_id)
        if item:
            project = audit_db.get_project(item.project_id)
            documents = audit_db.get_documents_by_item(item.item_id)
            
            item_data = {
                'assignment': assignment,
                'item': item,
                'project': project,
                'documents': documents
            }
            
            if item.status == 'pending':
                pending_items.append(item_data)
            elif item.status == 'in_progress':
                in_progress_items.append(item_data)
            elif item.status == 'submitted':
                submitted_items.append(item_data)
            elif item.status == 'returned':
                returned_items.append(item_data)
            elif item.status in ['reviewed', 'completed']:
                completed_items.append(item_data)
    
    # Display items by status
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"⏳ Pending ({len(pending_items)})",
        f"🔄 In Progress ({len(in_progress_items)})",
        f"📤 Submitted ({len(submitted_items)})",
        f"🔙 Returned ({len(returned_items)})",
        f"✅ Completed ({len(completed_items)})"
    ])
    
    with tab1:
        render_items_list(pending_items, "pending")
    
    with tab2:
        render_items_list(in_progress_items, "in_progress")
    
    with tab3:
        render_items_list(submitted_items, "submitted")
    
    with tab4:
        render_items_list(returned_items, "returned")
    
    with tab5:
        render_items_list(completed_items, "completed")

def render_items_list(items_data: list, status: str):
    """Render list of items with given status"""
    
    if not items_data:
        st.info(f"No items with status: {status.replace('_', ' ').title()}")
        return
    
    for data in items_data:
        item = data['item']
        project = data['project']
        documents = data['documents']
        
        # Determine due date color
        due_date = datetime.fromisoformat(item.due_date)
        days_until_due = (due_date - datetime.now()).days
        
        if days_until_due < 0:
            due_color = "🔴"
            due_text = f"Overdue by {abs(days_until_due)} days"
        elif days_until_due <= 3:
            due_color = "🟡"
            due_text = f"Due in {days_until_due} days"
        else:
            due_color = "🟢"
            due_text = f"Due in {days_until_due} days"
        
        with st.expander(f"{due_color} {item.title} - {project.name if project else 'Unknown Project'}", expanded=False):
            # Item details
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Project:** {project.name if project else 'N/A'}")
                st.markdown(f"**Description:** {item.description}")
                st.markdown(f"**Status:** {item.status.replace('_', ' ').title()}")
            
            with col2:
                st.markdown(f"**Due Date:** {item.due_date}")
                st.markdown(f"**{due_text}**")
                st.markdown(f"**Documents:** {len(documents)}")
            
            # Show submitted documents with auditor feedback
            if documents:
                st.markdown("---")
                st.markdown("**📎 Submitted Documents:**")
                
                for doc in documents:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"📄 **{doc.filename}**")
                    with col2:
                        st.markdown(f"*{doc.submitted_at[:10]}*")
                    with col3:
                        status_emoji = {
                            'submitted': '📤',
                            'reviewed': '👁️',
                            'approved': '✅',
                            'rejected': '❌'
                        }.get(doc.status, '📄')
                        
                        # Color code the status
                        if doc.status == 'approved':
                            st.success(f"{status_emoji} {doc.status.title()}")
                        elif doc.status == 'rejected':
                            st.error(f"{status_emoji} {doc.status.title()}")
                        else:
                            st.info(f"{status_emoji} {doc.status.title()}")
                    
                    # Show coordinator's submission notes
                    if doc.notes:
                        st.markdown(f"*Your notes: {doc.notes}*")
                    
                    # Show auditor feedback from comments
                    comments = audit_db.get_comments_by_item(item.item_id)
                    auditor_feedback = [c for c in comments if c.user != st.session_state.username and c.comment_type == 'status_change']
                    
                    if auditor_feedback:
                        latest_feedback = auditor_feedback[-1]
                        if doc.status in ['approved', 'rejected']:
                            st.markdown(f"**🔔 Auditor Feedback:**")
                            if '[ACCEPT]' in latest_feedback.comment_text:
                                st.success(f"✅ {latest_feedback.comment_text.replace('[ACCEPT]', '').strip()}")
                            elif '[REJECT]' in latest_feedback.comment_text:
                                st.error(f"❌ {latest_feedback.comment_text.replace('[REJECT]', '').strip()}")
                            elif '[RETURN]' in latest_feedback.comment_text:
                                st.warning(f"🔄 {latest_feedback.comment_text.replace('[RETURN]', '').strip()}")
                            else:
                                st.info(f"💬 {latest_feedback.comment_text}")
                            st.markdown(f"*{latest_feedback.created_at[:16]}*")
                    
                    st.markdown("---")
            
            # Show all comments for communication
            comments = audit_db.get_comments_by_item(item.item_id)
            if comments:
                st.markdown("**💬 Communication History:**")
                for comment in comments[-3:]:  # Show last 3 comments
                    if comment.user == st.session_state.username:
                        st.markdown(f"- **You:** {comment.comment_text} *({comment.created_at[:16]})*")
                    else:
                        st.markdown(f"- **Auditor ({comment.user}):** {comment.comment_text} *({comment.created_at[:16]})*")
            
            # Action buttons
            st.markdown("---")
            
            if status in ['pending', 'in_progress', 'returned']:
                col1, col2 = st.columns(2)
                
                with col1:
                    button_text = "📤 Submit Document" if status != 'returned' else "🔄 Resubmit Document"
                    if st.button(button_text, key=f"submit_{item.item_id}", use_container_width=True):
                        st.session_state.submit_doc_item = item.item_id
                        st.rerun()
                
                with col2:
                    if status == 'pending' and st.button("▶️ Start Working", key=f"start_{item.item_id}", use_container_width=True):
                        item.status = 'in_progress'
                        item.updated_at = datetime.now().isoformat()
                        audit_db.save_item(item)
                        st.success("Status updated to In Progress!")
                        st.rerun()
                
                # Show special message for returned items
                if status == 'returned':
                    st.warning("⚠️ **Action Required:** Auditor has returned this item. Please review feedback above and resubmit.")
            
            elif status == 'submitted':
                st.info("⏳ Waiting for auditor review...")
            
            elif status == 'reviewed':
                st.success("✅ Item reviewed and approved by auditor!")
    
    # Handle document submission dialog
    if 'submit_doc_item' in st.session_state:
        render_document_submission_dialog(st.session_state.submit_doc_item)

def render_document_submission_dialog(item_id: str):
    """Dialog for submitting documents"""
    
    st.markdown("---")
    st.subheader("📤 Submit Document")
    
    item = audit_db.get_item(item_id)
    if not item:
        st.error("Item not found")
        return
    
    project = audit_db.get_project(item.project_id)
    
    st.info(f"**Item:** {item.title}\n\n**Project:** {project.name if project else 'N/A'}")
    
    with st.form("submit_document_form"):
        st.markdown("**Upload Document**")
        
        uploaded_file = st.file_uploader(
            "Choose file",
            type=['pdf', 'xlsx', 'xls', 'csv', 'docx', 'doc', 'txt'],
            help="Supported formats: PDF, Excel, CSV, Word, Text"
        )
        
        notes = st.text_area(
            "Notes (Optional)",
            placeholder="Add any notes or comments about this submission..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Submit", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if cancel:
            del st.session_state.submit_doc_item
            st.rerun()
        
        if submit:
            if not uploaded_file:
                st.error("⚠️ Please select a file to upload")
            else:
                # In production, save file to proper storage
                # For demo, we'll just store metadata
                
                # Create uploads directory
                uploads_dir = Path("data/uploads")
                uploads_dir.mkdir(parents=True, exist_ok=True)
                
                # Save file
                file_path = uploads_dir / f"{item_id}_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Create document record
                doc_id = generate_id("DOC")
                document = Document(
                    document_id=doc_id,
                    item_id=item_id,
                    filename=uploaded_file.name,
                    file_path=str(file_path),
                    submitted_by=st.session_state.username,
                    notes=notes
                )
                audit_db.save_document(document)
                
                # Update item status
                if item.status != 'submitted':
                    item.status = 'submitted'
                    item.updated_at = datetime.now().isoformat()
                    audit_db.save_item(item)
                
                st.success(f"✅ Document '{uploaded_file.name}' submitted successfully!")
                del st.session_state.submit_doc_item
                st.rerun()

def render_coordinator_stats():
    """Display coordinator statistics"""
    
    username = st.session_state.username
    assignments = audit_db.get_assignments_by_coordinator(username)
    
    if not assignments:
        return
    
    # Calculate stats
    total_items = len(assignments)
    pending = 0
    in_progress = 0
    submitted = 0
    completed = 0
    overdue = 0
    
    for assignment in assignments:
        item = audit_db.get_item(assignment.item_id)
        if item:
            if item.status == 'pending':
                pending += 1
            elif item.status == 'in_progress':
                in_progress += 1
            elif item.status == 'submitted':
                submitted += 1
            elif item.status in ['reviewed', 'completed']:
                completed += 1
            
            # Check if overdue
            due_date = datetime.fromisoformat(item.due_date)
            if due_date < datetime.now() and item.status not in ['reviewed', 'completed']:
                overdue += 1
    
    # Display stats
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Items", total_items)
    with col2:
        st.metric("Pending", pending)
    with col3:
        st.metric("In Progress", in_progress)
    with col4:
        st.metric("Submitted", submitted)
    with col5:
        st.metric("Overdue", overdue, delta=None if overdue == 0 else f"-{overdue}")

# Made with Bob
