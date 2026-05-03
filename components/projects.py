"""
Project Management Component
For auditors to create and manage audit projects and items
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_models import (
    audit_db, Project, AuditItem, Assignment, User, ActivityLog
)

def generate_id(prefix: str) -> str:
    """Generate unique ID with prefix"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def render_projects_component():
    """Main project management interface for auditors"""
    
    st.title("📋 Project Management")
    
    # Check if user is auditor
    if st.session_state.get('user_role') not in ['auditor', 'admin']:
        st.error("⚠️ Access Denied: Only auditors can access this page")
        return
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 My Projects", "➕ Create Project", "👥 Manage Coordinators"])
    
    with tab1:
        render_projects_list()
    
    with tab2:
        render_create_project()
    
    with tab3:
        render_coordinator_management()

def render_projects_list():
    """Display list of projects created by the auditor"""
    
    st.subheader("My Audit Projects")
    
    # Get projects for current auditor
    username = st.session_state.username
    projects = audit_db.get_projects_by_auditor(username)
    
    if not projects:
        st.info("📝 No projects yet. Create your first project in the 'Create Project' tab!")
        return
    
    # Display projects
    for project in projects:
        with st.expander(f"📁 {project.name} ({project.status.upper()})", expanded=False):
            st.markdown(f"**Description:** {project.description}")
            st.markdown(f"**Created:** {project.created_at[:10]}")
            st.markdown(f"**Status:** {project.status}")
            
            # Show items for this project
            items = audit_db.get_items_by_project(project.project_id)
            
            if items:
                st.markdown("---")
                st.markdown("**📋 Audit Items:**")
                
                for item in items:
                    # Get assignments
                    assignments = audit_db.get_assignments_by_item(item.item_id)
                    coordinators = [a.coordinator_username for a in assignments]
                    
                    # Get documents
                    documents = audit_db.get_documents_by_item(item.item_id)
                    
                    with st.container():
                        col1, col2, col3 = st.columns([3, 2, 1])
                        
                        with col1:
                            st.markdown(f"**{item.title}**")
                            st.markdown(f"*{item.description[:100]}...*" if len(item.description) > 100 else f"*{item.description}*")
                        
                        with col2:
                            st.markdown(f"**Due:** {item.due_date}")
                            st.markdown(f"**Status:** {item.status.replace('_', ' ').title()}")
                            st.markdown(f"**Assigned:** {', '.join(coordinators) if coordinators else 'Unassigned'}")
                        
                        with col3:
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                if st.button("✏️", key=f"edit_{item.item_id}", help="Edit item"):
                                    st.session_state.edit_item = item.item_id
                                    st.rerun()
                            with btn_col2:
                                if st.button("🗑️", key=f"delete_{item.item_id}", help="Delete item"):
                                    st.session_state.delete_item = item.item_id
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No items in this project yet.")
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("➕ Add Item", key=f"add_item_{project.project_id}", use_container_width=True):
                    st.session_state.add_item_to_project = project.project_id
                    st.rerun()
            
            with col2:
                if project.status == 'active':
                    if st.button("✅ Complete", key=f"complete_{project.project_id}", use_container_width=True):
                        project.status = 'completed'
                        project.updated_at = datetime.now().isoformat()
                        audit_db.save_project(project)
                        st.success("Project marked as completed!")
                        st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_proj_{project.project_id}", use_container_width=True):
                    st.session_state.delete_project = project.project_id
                    st.rerun()
    
    # Handle add item dialog
    if 'add_item_to_project' in st.session_state:
        render_add_item_dialog(st.session_state.add_item_to_project)
    
    # Handle edit item dialog
    if 'edit_item' in st.session_state:
        edit_item_modal(st.session_state.edit_item)
    
    # Handle delete item confirmation
    if 'delete_item' in st.session_state:
        delete_item_confirmation(st.session_state.delete_item)
    
    # Handle delete project confirmation
    if 'delete_project' in st.session_state:
        delete_project_confirmation(st.session_state.delete_project)

def render_create_project():
    """Form to create a new project"""
    
    st.subheader("Create New Audit Project")
    
    with st.form("create_project_form"):
        project_name = st.text_input("Project Name*", placeholder="e.g., Q4 2026 Financial Audit")
        project_desc = st.text_area("Description*", placeholder="Describe the audit scope and objectives...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Create Project", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            if not project_name or not project_desc:
                st.error("⚠️ Please fill in all required fields")
            else:
                # Create project
                project_id = generate_id("PRJ")
                project = Project(
                    project_id=project_id,
                    name=project_name,
                    description=project_desc,
                    created_by=st.session_state.username
                )
                audit_db.save_project(project)
                st.success(f"✅ Project '{project_name}' created successfully!")
                st.rerun()

def render_add_item_dialog(project_id: str):
    """Dialog to add an item to a project"""
    
    st.markdown("---")
    st.subheader("➕ Add Audit Item")
    
    project = audit_db.get_project(project_id)
    if not project:
        st.error("Project not found")
        return
    st.info(f"Adding item to: **{project.name}**")
    
    # Get all coordinators for assignment
    coordinators = audit_db.get_all_coordinators()
    coord_options = {}
    for coord in coordinators:
        group = coord.group or "No Group"
        display = f"{coord.username} ({group})"
        coord_options[display] = coord.username
    
    with st.form("add_item_form"):
        item_title = st.text_input("Item Title*", placeholder="e.g., Revenue Recognition Analysis")
        item_desc = st.text_area("Description*", placeholder="Describe what needs to be audited...")
        due_date = st.date_input("Due Date*", value=datetime.now() + timedelta(days=14))
        
        # Coordinator assignment dropdown
        st.markdown("**Assign Coordinators:**")
        if coord_options:
            selected_coords = st.multiselect(
                "Select Coordinators",
                options=list(coord_options.keys()),
                help="You can select multiple coordinators"
            )
        else:
            st.warning("No coordinators available. Add coordinators in the 'Manage Coordinators' tab.")
            selected_coords = []
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Add Item", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if cancel:
            del st.session_state.add_item_to_project
            st.rerun()
        
        if submit:
            if not item_title or not item_desc:
                st.error("⚠️ Please fill in all required fields")
            else:
                # Create item
                item_id = generate_id("ITEM")
                item = AuditItem(
                    item_id=item_id,
                    project_id=project_id,
                    title=item_title,
                    description=item_desc,
                    due_date=due_date.isoformat(),
                    status='in_progress' if selected_coords else 'pending'
                )
                audit_db.save_item(item)
                
                # Create assignments for selected coordinators
                for coord_display in selected_coords:
                    coord_username = coord_options[coord_display]
                    assignment_id = generate_id("ASGN")
                    assignment = Assignment(
                        assignment_id=assignment_id,
                        item_id=item_id,
                        coordinator_username=coord_username,
                        assigned_by=st.session_state.username
                    )
                    audit_db.save_assignment(assignment)
                
                success_msg = f"✅ Item '{item_title}' added successfully!"
                if selected_coords:
                    success_msg += f" Assigned to {len(selected_coords)} coordinator(s)."
                st.success(success_msg)

@st.dialog("✏️ Edit Audit Item", width="large")
def edit_item_modal(item_id: str):
    """Modal dialog to edit an existing item"""
    
    item = audit_db.get_item(item_id)
    if not item:
        st.error("Item not found")
        return
    
    project = audit_db.get_project(item.project_id)
    st.markdown(f"**Project:** {project.name if project else 'Unknown Project'}")
    st.markdown("---")
    
    # Get current assignments
    current_assignments = audit_db.get_assignments_by_item(item_id)
    current_coord_usernames = [a.coordinator_username for a in current_assignments]
    
    # Get all coordinators and groups
    all_coordinators = audit_db.get_all_coordinators()
    
    # Create options for individual coordinators
    coord_options = {}
    for coord in all_coordinators:
        group = coord.group or "No Group"
        display = f"{coord.username} ({group})"
        coord_options[display] = coord.username
    
    # Create options for groups
    groups = set(coord.group for coord in all_coordinators if coord.group)
    group_options = {f"📁 All in {group} Group": group for group in groups}
    
    with st.form("edit_item_form"):
        item_title = st.text_input("Item Title*", value=item.title)
        item_desc = st.text_area("Description*", value=item.description)
        
        # Parse current due date
        try:
            current_due = datetime.fromisoformat(item.due_date).date()
        except:
            current_due = datetime.now().date()
        
        due_date = st.date_input("Due Date*", value=current_due)
        
        st.markdown("**Assign Coordinators:**")
        
        # Option to assign by group or individual
        assignment_type = st.radio(
            "Assignment Type",
            ["Individual Coordinators", "Entire Group"],
            horizontal=True
        )
        
        if assignment_type == "Individual Coordinators":
            # Multi-select for individual coordinators
            # Pre-select currently assigned coordinators
            current_displays = []
            for u in current_coord_usernames:
                user = audit_db.get_user(u)
                if user:
                    group = user.group or 'No Group'
                    current_displays.append(f"{u} ({group})")
            
            selected_coords = st.multiselect(
                "Select Coordinators",
                options=list(coord_options.keys()),
                default=[d for d in current_displays if d in coord_options.keys()],
                help="Select one or more coordinators"
            )
            selected_group = None
        else:
            # Select entire group
            selected_coords = []
            selected_group = st.selectbox(
                "Select Group",
                options=list(group_options.keys()) if group_options else ["No groups available"]
            )
        
        submit = st.form_submit_button("✅ Save Changes", use_container_width=True)
        
        if submit:
            if not item_title or not item_desc:
                st.error("⚠️ Please fill in all required fields")
            else:
                # Update item
                item.title = item_title
                item.description = item_desc
                item.due_date = due_date.isoformat()
                item.updated_at = datetime.now().isoformat()
                audit_db.save_item(item)
                
                # Remove all current assignments
                for assignment in current_assignments:
                    audit_db.delete_assignment(assignment.assignment_id)
                
                # Add new assignments
                if assignment_type == "Individual Coordinators" and selected_coords:
                    for coord_display in selected_coords:
                        coord_username = coord_options[coord_display]
                        assignment_id = generate_id("ASGN")
                        assignment = Assignment(
                            assignment_id=assignment_id,
                            item_id=item_id,
                            coordinator_username=coord_username,
                            assigned_by=st.session_state.username
                        )
                        audit_db.save_assignment(assignment)
                
                elif assignment_type == "Entire Group" and selected_group and selected_group in group_options.values():
                    # Assign all coordinators in the selected group
                    group_name = selected_group
                    group_coordinators = [c for c in all_coordinators if c.group == group_name]
                    
                    for coord in group_coordinators:
                        assignment_id = generate_id("ASGN")
                        assignment = Assignment(
                            assignment_id=assignment_id,
                            item_id=item_id,
                            coordinator_username=coord.username,
                            assigned_by=st.session_state.username
                        )
                        audit_db.save_assignment(assignment)
                
                # Log the change
                log_id = generate_id("LOG")
                details = f"Item updated: {item_title}"
                if assignment_type == "Entire Group":
                    details += f" | Assigned to entire {selected_group} group"
                else:
                    details += f" | Assigned to {len(selected_coords)} coordinator(s)"
                
                activity_log = ActivityLog(
                    log_id=log_id,
                    item_id=item_id,
                    user=st.session_state.username,
                    action='item_updated',
                    details=details
                )
                audit_db.save_activity_log(activity_log)
                
                st.success(f"✅ Item '{item_title}' updated successfully!")
                del st.session_state.edit_item
                st.rerun()
                del st.session_state.add_item_to_project
                st.rerun()

@st.dialog("🗑️ Delete Item", width="large")
def delete_item_confirmation(item_id: str):
    """Confirmation dialog to delete an item"""
    
    item = audit_db.get_item(item_id)
    if not item:
        st.error("Item not found")
        return
    
    st.warning(f"⚠️ Are you sure you want to delete the item **'{item.title}'**?")
    st.markdown("This action will also delete:")
    st.markdown("- All coordinator assignments")
    st.markdown("- All submitted documents")
    st.markdown("- All comments and activity logs")
    st.markdown("---")
    st.error("**This action cannot be undone!**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
            # Delete all related data
            assignments = audit_db.get_assignments_by_item(item_id)
            for assignment in assignments:
                audit_db.delete_assignment(assignment.assignment_id)
            
            documents = audit_db.get_documents_by_item(item_id)
            for doc in documents:
                audit_db.delete_document(doc.document_id)
            
            comments = audit_db.get_comments_by_item(item_id)
            for comment in comments:
                audit_db.delete_comment(comment.comment_id)
            
            logs = audit_db.get_activity_logs_by_item(item_id)
            for log in logs:
                audit_db.delete_activity_log(log.log_id)
            
            # Delete the item itself
            audit_db.delete_item(item_id)
            
            st.success(f"✅ Item '{item.title}' deleted successfully!")
            del st.session_state.delete_item
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            del st.session_state.delete_item
            st.rerun()

@st.dialog("🗑️ Delete Project", width="large")
def delete_project_confirmation(project_id: str):
    """Confirmation dialog to delete a project"""
    
    project = audit_db.get_project(project_id)
    if not project:
        st.error("Project not found")
        return
    
    items = audit_db.get_items_by_project(project_id)
    item_count = len(items)
    
    st.warning(f"⚠️ Are you sure you want to delete the project **'{project.name}'**?")
    st.markdown(f"This project contains **{item_count} item(s)**.")
    st.markdown("This action will also delete:")
    st.markdown("- All audit items in this project")
    st.markdown("- All coordinator assignments")
    st.markdown("- All submitted documents")
    st.markdown("- All comments and activity logs")
    st.markdown("---")
    st.error("**This action cannot be undone!**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, Delete Everything", use_container_width=True, type="primary"):
            # Delete all items and their related data
            for item in items:
                # Delete assignments
                assignments = audit_db.get_assignments_by_item(item.item_id)
                for assignment in assignments:
                    audit_db.delete_assignment(assignment.assignment_id)
                
                # Delete documents
                documents = audit_db.get_documents_by_item(item.item_id)
                for doc in documents:
                    audit_db.delete_document(doc.document_id)
                
                # Delete comments
                comments = audit_db.get_comments_by_item(item.item_id)
                for comment in comments:
                    audit_db.delete_comment(comment.comment_id)
                
                # Delete activity logs
                logs = audit_db.get_activity_logs_by_item(item.item_id)
                for log in logs:
                    audit_db.delete_activity_log(log.log_id)
                
                # Delete the item
                audit_db.delete_item(item.item_id)
            
            # Delete the project itself
            audit_db.delete_project(project_id)
            
            st.success(f"✅ Project '{project.name}' and all its items deleted successfully!")
            del st.session_state.delete_project
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            del st.session_state.delete_project
            st.rerun()


def render_coordinator_management():
    """Manage coordinators and groups"""
    
    st.subheader("👥 Coordinator Management")
    
    # Display existing coordinators
    coordinators = audit_db.get_all_coordinators()
    
    if coordinators:
        st.markdown("### Current Coordinators")
        
        # Group by group
        groups = {}
        for coord in coordinators:
            group = coord.group or "No Group"
            if group not in groups:
                groups[group] = []
            groups[group].append(coord)
        
        for group, coords in groups.items():
            with st.expander(f"📁 {group} ({len(coords)} coordinators)"):
                for coord in coords:
                    st.markdown(f"- **{coord.username}**")
    else:
        st.info("No coordinators registered yet.")
    
    # Add new coordinator (simplified - in production, use proper user management)
    st.markdown("---")
    st.markdown("### Add New Coordinator")
    st.info("💡 In production, coordinators would register through a proper user management system. This is a demo interface.")
    
    with st.form("add_coordinator_form"):
        new_username = st.text_input("Username*", placeholder="e.g., john.doe")
        new_group = st.selectbox("Group*", ["Finance", "Operations", "IT", "HR", "Legal", "Other"])
        
        if st.form_submit_button("➕ Add Coordinator"):
            if not new_username:
                st.error("⚠️ Please enter a username")
            elif audit_db.get_user(new_username):
                st.error("⚠️ Username already exists")
            else:
                # Create coordinator user
                user = User(new_username, 'coordinator', new_group)
                audit_db.save_user(user)
                st.success(f"✅ Coordinator '{new_username}' added to group '{new_group}'!")
                st.rerun()

# Made with Bob
