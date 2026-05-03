# 🤝 Collaboration Features Implementation Guide

## Overview
This guide shows how to add comments/threads and real-time updates to the audit platform so auditors and coordinators can communicate.

---

## ✅ What's Already Built

### **1. Comments Component** ([`components/comments.py`](components/comments.py:1))
A complete, reusable comments system with:
- ✅ Thread-style comments
- ✅ Both auditors and coordinators can post
- ✅ Automatic status change notifications
- ✅ Activity timeline
- ✅ Delete own comments
- ✅ Styled UI (own comments vs others)

### **2. Data Models** ([`utils/data_models.py`](utils/data_models.py:1))
Already has:
- ✅ `Comment` class
- ✅ `ActivityLog` class
- ✅ Database operations for comments
- ✅ Database operations for activity logs

---

## 🔧 How to Add Comments to Existing Pages

### **Step 1: Import the Comments Component**

Add this to the top of your file:

```python
from components.comments import (
    render_comments_section,
    render_activity_timeline,
    add_status_change_comment,
    add_assignment_comment,
    add_document_comment
)
```

### **Step 2: Add Comments Section to Item Details**

In [`components/projects.py`](components/projects.py:1), when showing item details:

```python
# After displaying item information
with st.expander(f"📋 {item.title}", expanded=True):
    # ... existing item display code ...
    
    # ADD THIS: Comments section
    render_comments_section(item.item_id, item.title)
    
    # OPTIONAL: Activity timeline
    render_activity_timeline(item.item_id)
```

### **Step 3: Add Comments to Coordinator View**

In [`components/coordinator.py`](components/coordinator.py:1), when showing assigned items:

```python
def render_items_list(items, status):
    for item_data in items:
        item = item_data['item']
        
        with st.expander(f"📋 {item.title}", expanded=False):
            # ... existing item display code ...
            
            # ADD THIS: Comments section
            render_comments_section(item.item_id, item.title)
```

---

## 🔄 Auto-Comments for Status Changes

### **When Status Changes:**

```python
# In your status update code
old_status = item.status
new_status = "in_progress"  # or whatever new status

# Update the item
item.status = new_status
audit_db.save_item(item)

# ADD THIS: Auto-comment for status change
add_status_change_comment(
    item_id=item.item_id,
    old_status=old_status,
    new_status=new_status,
    username=st.session_state.username
)
```

### **When Assigning Coordinator:**

```python
# After creating assignment
assignment = Assignment(...)
audit_db.save_assignment(assignment)

# ADD THIS: Auto-comment for assignment
add_assignment_comment(
    item_id=item.item_id,
    coordinator_username=coordinator_username,
    auditor_username=st.session_state.username
)
```

### **When Document Submitted:**

```python
# After saving document
document = Document(...)
audit_db.save_document(document)

# ADD THIS: Auto-comment for document
add_document_comment(
    item_id=item.item_id,
    filename=document.filename,
    coordinator_username=st.session_state.username
)
```

---

## 🔄 Real-Time Updates

### **Option 1: Manual Refresh Button (Simplest)**

Add a refresh button at the top of pages:

```python
col1, col2 = st.columns([5, 1])
with col1:
    st.title("📋 My Projects")
with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
```

### **Option 2: Auto-Refresh with Timer**

Add this at the top of your page:

```python
import time

# Auto-refresh every 30 seconds
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

current_time = time.time()
if current_time - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = current_time
    st.rerun()

# Show countdown
time_until_refresh = 30 - int(current_time - st.session_state.last_refresh)
st.sidebar.info(f"🔄 Auto-refresh in {time_until_refresh}s")
```

### **Option 3: Refresh on Action**

After any update, just call:

```python
st.rerun()
```

This immediately refreshes the page to show changes.

---

## 📝 Complete Integration Example

### **For Auditor's Project View:**

```python
# In components/projects.py

from components.comments import render_comments_section, add_status_change_comment

def render_projects_list():
    st.subheader("My Audit Projects")
    
    # Refresh button
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("")
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    projects = audit_db.get_projects_by_auditor(st.session_state.username)
    
    for project in projects:
        items = audit_db.get_items_by_project(project.project_id)
        
        for item in items:
            with st.expander(f"📋 {item.title}", expanded=False):
                # Item details
                st.markdown(f"**Description:** {item.description}")
                st.markdown(f"**Status:** {item.status}")
                st.markdown(f"**Due Date:** {item.due_date}")
                
                # Status update
                new_status = st.selectbox(
                    "Update Status",
                    ["pending", "in_progress", "submitted", "reviewed", "completed"],
                    index=["pending", "in_progress", "submitted", "reviewed", "completed"].index(item.status),
                    key=f"status_{item.item_id}"
                )
                
                if new_status != item.status:
                    if st.button("💾 Save Status", key=f"save_{item.item_id}"):
                        old_status = item.status
                        item.status = new_status
                        audit_db.save_item(item)
                        
                        # Auto-comment
                        add_status_change_comment(
                            item.item_id,
                            old_status,
                            new_status,
                            st.session_state.username
                        )
                        
                        st.success("Status updated!")
                        st.rerun()
                
                # Comments section
                render_comments_section(item.item_id, item.title)
```

### **For Coordinator's View:**

```python
# In components/coordinator.py

from components.comments import render_comments_section, add_document_comment

def render_items_list(items, status):
    for item_data in items:
        item = item_data['item']
        project = item_data['project']
        
        with st.expander(f"📋 {item.title} - {project.name}", expanded=False):
            # Item details
            st.markdown(f"**Project:** {project.name}")
            st.markdown(f"**Description:** {item.description}")
            st.markdown(f"**Due Date:** {item.due_date}")
            st.markdown(f"**Status:** {item.status}")
            
            # Document upload
            if status in ['pending', 'in_progress', 'returned']:
                uploaded_file = st.file_uploader(
                    "Upload Document",
                    key=f"upload_{item.item_id}"
                )
                
                if uploaded_file and st.button("📤 Submit", key=f"submit_{item.item_id}"):
                    # Save document
                    document_id = generate_id("doc")
                    file_path = f"uploads/{document_id}_{uploaded_file.name}"
                    
                    document = Document(
                        document_id=document_id,
                        item_id=item.item_id,
                        filename=uploaded_file.name,
                        file_path=file_path,
                        submitted_by=st.session_state.username
                    )
                    audit_db.save_document(document)
                    
                    # Auto-comment
                    add_document_comment(
                        item.item_id,
                        uploaded_file.name,
                        st.session_state.username
                    )
                    
                    # Update item status
                    item.status = 'submitted'
                    audit_db.save_item(item)
                    
                    st.success("Document submitted!")
                    st.rerun()
            
            # Comments section
            render_comments_section(item.item_id, item.title)
```

---

## 🎨 UI Features

### **What the Comments Look Like:**

1. **Own Comments:** Light blue background
2. **Others' Comments:** Light gray background
3. **User Badge:** Shows username and "(You)" for own comments
4. **Timestamp:** Formatted date and time
5. **Delete Button:** Only for own comments or admins
6. **Auto-Comments:** System-generated for status changes, assignments, documents

### **Activity Timeline:**

- Shows all actions with icons
- Status changes: 🔄
- Documents: 📄
- Comments: 💬
- Assignments: 👥
- Sorted newest first

---

## 🚀 Quick Start Checklist

To add collaboration features:

- [ ] Import comments component in `projects.py`
- [ ] Add `render_comments_section()` to item details
- [ ] Import comments component in `coordinator.py`
- [ ] Add `render_comments_section()` to coordinator item view
- [ ] Add `add_status_change_comment()` when status changes
- [ ] Add `add_assignment_comment()` when assigning coordinators
- [ ] Add `add_document_comment()` when documents submitted
- [ ] Add refresh button or auto-refresh
- [ ] Test with both auditor and coordinator accounts

---

## 🎯 Benefits

### **For Auditors:**
- ✅ See coordinator questions/updates
- ✅ Provide clarifications
- ✅ Track all activity
- ✅ Know when documents submitted

### **For Coordinators:**
- ✅ Ask questions to auditors
- ✅ Get clarifications
- ✅ See status changes
- ✅ Know what's expected

### **For Both:**
- ✅ Clear communication history
- ✅ No need for external emails
- ✅ Everything in one place
- ✅ Audit trail of all actions

---

## 📞 Need Help?

The comments component is fully built and ready to use. Just:
1. Import it
2. Call `render_comments_section(item_id, item_title)`
3. Done!

All the database operations, styling, and logic are handled automatically.

---

**Made with Bob** 🤖