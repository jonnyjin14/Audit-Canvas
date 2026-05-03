# 📋 Coordinator Workflow Guide

## Overview
This guide explains the new coordinator workflow feature that enables auditors to create projects, assign items to coordinators, and coordinators to submit required documents.

## User Roles

### 1. **Auditor** 👨‍💼
- Creates audit projects
- Adds audit items to projects
- Assigns coordinators to items (multiple coordinators per item)
- Reviews submitted documents
- Manages project lifecycle

### 2. **Coordinator** 👥
- Views assigned audit items
- Submits required documents
- Tracks item status and due dates
- Belongs to a specific group (Finance, Operations, IT, etc.)

### 3. **Admin** 🔑
- Full access to all features
- Can perform both auditor and coordinator functions

---

## Login Credentials

### Auditors
- **Username:** `auditor` | **Password:** `audit123`
- **Username:** `auditor2` | **Password:** `audit123`

### Coordinators
- **Username:** `coordinator1` | **Password:** `coord123` | **Group:** Finance
- **Username:** `coordinator2` | **Password:** `coord123` | **Group:** Operations
- **Username:** `coordinator3` | **Password:** `coord123` | **Group:** IT

### Admin
- **Username:** `admin` | **Password:** `admin123`

---

## Complete Workflow

### Phase 1: Auditor Creates Project

1. **Login as Auditor**
   - Use credentials: `auditor` / `audit123`

2. **Navigate to Projects**
   - Click "📁 Projects" in the sidebar

3. **Create New Project**
   - Go to "➕ Create Project" tab
   - Enter project name (e.g., "Q4 2026 Financial Audit")
   - Enter description
   - Click "✅ Create Project"

### Phase 2: Auditor Adds Items

1. **View Project**
   - In "📊 My Projects" tab, find your project
   - Click "➕ Add Item" button

2. **Create Audit Item**
   - Enter item title (e.g., "Revenue Recognition Analysis")
   - Enter description of what needs to be audited
   - Set due date
   - Click "✅ Add Item"

3. **Repeat** for multiple items as needed

### Phase 3: Auditor Assigns Coordinators

1. **Assign Coordinators**
   - Click "👥 Assign Coordinators" button on the project
   - For each item:
     - Select coordinator from dropdown (grouped by department)
     - Click "➕ Assign"
     - Can assign multiple coordinators to same item

2. **Verify Assignments**
   - Check that coordinators are listed under each item
   - Item status automatically changes to "in_progress"

### Phase 4: Coordinator Submits Documents

1. **Login as Coordinator**
   - Use credentials: `coordinator1` / `coord123`

2. **View Assigned Items**
   - Click "📋 My Assigned Items" in sidebar
   - See items organized by status:
     - ⏳ Pending
     - 🔄 In Progress
     - 📤 Submitted
     - ✅ Completed

3. **Submit Document**
   - Click on an item to expand
   - Click "📤 Submit Document"
   - Upload file (PDF, Excel, Word, etc.)
   - Add optional notes
   - Click "✅ Submit"

4. **Track Progress**
   - View submitted documents
   - Monitor due dates
   - Check document status

### Phase 5: Auditor Reviews

1. **Login as Auditor**
   - Return to "📁 Projects"
   - View project items
   - See submitted documents count
   - Review and approve/reject documents

---

## Key Features

### Multi-Coordinator Assignment
- ✅ Multiple coordinators can be assigned to a single item
- ✅ Coordinators from different groups can collaborate
- ✅ Each coordinator can submit documents independently

### Group Management
- 📁 Coordinators belong to groups (Finance, Operations, IT, HR, Legal)
- 📁 Easy filtering and assignment by group
- 📁 Add new coordinators in "👥 Manage Coordinators" tab

### Document Tracking
- 📄 All document submissions are tracked
- 📄 Submission timestamps recorded
- 📄 Document status (submitted, reviewed, approved, rejected)
- 📄 Optional notes for each submission

### Status Management
- **Pending:** Item created, not yet started
- **In Progress:** Coordinator assigned and working
- **Submitted:** Documents submitted, awaiting review
- **Reviewed:** Auditor has reviewed
- **Completed:** Item fully completed

### Due Date Tracking
- 🔴 Red indicator: Overdue
- 🟡 Yellow indicator: Due within 3 days
- 🟢 Green indicator: More than 3 days remaining

---

## Testing Scenarios

### Scenario 1: Single Coordinator Assignment
1. Auditor creates project with 3 items
2. Assigns coordinator1 (Finance) to all items
3. Coordinator1 logs in and submits documents for each item

### Scenario 2: Multi-Coordinator Assignment
1. Auditor creates project with 1 item
2. Assigns coordinator1 (Finance) and coordinator2 (Operations)
3. Both coordinators log in and submit their respective documents

### Scenario 3: Cross-Group Collaboration
1. Auditor creates project requiring Finance, IT, and Operations input
2. Assigns coordinators from each group to relevant items
3. Each coordinator submits group-specific documents

### Scenario 4: Overdue Items
1. Create items with past due dates
2. Coordinator logs in to see red overdue indicators
3. Submit documents to resolve overdue status

---

## Data Storage

### File Locations
- **Database:** `data/*.json` (JSON-based storage for demo)
- **Uploads:** `data/uploads/` (submitted documents)

### Data Models
- **Projects:** Project metadata and status
- **Items:** Audit items within projects
- **Assignments:** Coordinator-to-item mappings
- **Documents:** Submitted document records
- **Users:** User accounts with roles and groups

---

## Tips & Best Practices

### For Auditors
- ✅ Create clear, descriptive item titles
- ✅ Set realistic due dates
- ✅ Assign coordinators based on expertise
- ✅ Review documents promptly
- ✅ Use project status to track overall progress

### For Coordinators
- ✅ Check assigned items regularly
- ✅ Start working on items early
- ✅ Add notes when submitting documents
- ✅ Monitor due dates
- ✅ Communicate with auditor if issues arise

---

## Troubleshooting

### Issue: Can't see assigned items
**Solution:** Ensure you're logged in as a coordinator and have been assigned items by an auditor.

### Issue: Can't submit documents
**Solution:** Check that:
- You're assigned to the item
- File format is supported
- File size is reasonable
- You have proper permissions

### Issue: Assignments not showing
**Solution:** 
- Refresh the page
- Check that auditor completed the assignment
- Verify you're looking at the correct project

---

## Future Enhancements

- 🔮 Email notifications for assignments
- 🔮 Document version control
- 🔮 Bulk document upload
- 🔮 Advanced search and filtering
- 🔮 Audit trail and activity logs
- 🔮 Integration with external storage (SharePoint, Google Drive)
- 🔮 Mobile app support

---

## Support

For questions or issues:
1. Check this guide first
2. Review the main README.md
3. Check QUICK_START.md for basic setup
4. Contact your system administrator

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-03  
**Status:** ✅ Production Ready