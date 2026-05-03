# 📊 Sample Data Guide

## Overview
The database has been populated with realistic sample data to demonstrate the coordinator workflow feature.

## Sample Data Summary

### 🎯 3 Projects Created

#### 1. **Q4 2026 Financial Audit** (by auditor)
**Status:** Active  
**Description:** Comprehensive financial audit for Q4 2026

**Items:**
- ✅ Revenue Recognition Analysis (Due in 7 days)
  - Assigned to: coordinator1 (Finance)
  - Status: In Progress
  
- ✅ Expense Validation (Due in 10 days)
  - Assigned to: coordinator1 (Finance), coordinator2 (Operations)
  - Status: In Progress
  
- ⏳ IT Systems Access Review (Due in 5 days)
  - Assigned to: coordinator3 (IT)
  - Status: Pending
  
- ⏳ Accounts Receivable Aging (Due in 14 days)
  - Assigned to: coordinator1 (Finance)
  - Status: Pending

#### 2. **Operational Efficiency Review** (by auditor)
**Status:** Active  
**Description:** Assessment of operational processes and workflow optimization

**Items:**
- ✅ Supply Chain Process Documentation (Due in 12 days)
  - Assigned to: coordinator2 (Operations)
  - Status: In Progress
  
- ⏳ Inventory Management Review (Due in 8 days)
  - Assigned to: coordinator2 (Operations)
  - Status: Pending
  
- ⏳ IT Infrastructure Assessment (Due in 15 days)
  - Assigned to: coordinator3 (IT)
  - Status: Pending

#### 3. **Annual Compliance Audit** (by auditor2)
**Status:** Active  
**Description:** Annual review of regulatory compliance

**Items:**
- 🔴 SOX Controls Testing (OVERDUE by 2 days!)
  - Assigned to: coordinator1 (Finance), coordinator3 (IT)
  - Status: In Progress
  
- ⏳ Data Privacy Compliance Check (Due in 6 days)
  - Assigned to: coordinator3 (IT)
  - Status: Pending
  
- ⏳ Vendor Compliance Review (Due in 20 days)
  - Assigned to: coordinator2 (Operations)
  - Status: Pending

---

## Coordinator Assignments

### 👤 coordinator1 (Finance Group)
**Total Assigned Items:** 4

1. Revenue Recognition Analysis (Q4 2026 Financial Audit)
2. Expense Validation (Q4 2026 Financial Audit) - *Shared with coordinator2*
3. Accounts Receivable Aging (Q4 2026 Financial Audit)
4. SOX Controls Testing (Annual Compliance Audit) - *Shared with coordinator3* - **OVERDUE**

### 👤 coordinator2 (Operations Group)
**Total Assigned Items:** 4

1. Expense Validation (Q4 2026 Financial Audit) - *Shared with coordinator1*
2. Supply Chain Process Documentation (Operational Efficiency Review)
3. Inventory Management Review (Operational Efficiency Review)
4. Vendor Compliance Review (Annual Compliance Audit)

### 👤 coordinator3 (IT Group)
**Total Assigned Items:** 4

1. IT Systems Access Review (Q4 2026 Financial Audit)
2. IT Infrastructure Assessment (Operational Efficiency Review)
3. SOX Controls Testing (Annual Compliance Audit) - *Shared with coordinator1* - **OVERDUE**
4. Data Privacy Compliance Check (Annual Compliance Audit)

---

## Testing Scenarios

### Scenario 1: View Assigned Items
1. Login as `coordinator1` / `coord123`
2. Click "📋 My Assigned Items"
3. See 4 items organized by status
4. Notice the overdue SOX Controls Testing item (red indicator)

### Scenario 2: Submit Document
1. Login as `coordinator2` / `coord123`
2. Go to "📋 My Assigned Items"
3. Click on "Supply Chain Process Documentation"
4. Click "📤 Submit Document"
5. Upload a file and add notes
6. Submit and see status update

### Scenario 3: Multi-Coordinator Item
1. Login as `coordinator1` / `coord123`
2. View "Expense Validation" item
3. Submit a document
4. Logout and login as `coordinator2` / `coord123`
5. View same "Expense Validation" item
6. Submit a different document
7. Both submissions are tracked separately

### Scenario 4: Auditor Review
1. Login as `auditor` / `audit123`
2. Go to "📁 Projects"
3. View "Q4 2026 Financial Audit"
4. See document submission counts
5. Review submitted documents

### Scenario 5: Overdue Item
1. Login as `coordinator1` or `coordinator3`
2. See red indicator on "SOX Controls Testing"
3. Item shows "Overdue by 2 days"
4. Submit document to resolve

---

## Key Features Demonstrated

✅ **Multiple Projects** - 3 different audit projects  
✅ **Various Item Types** - Financial, operational, and compliance items  
✅ **Multi-Coordinator Assignment** - Some items assigned to multiple coordinators  
✅ **Cross-Group Collaboration** - Finance, Operations, and IT working together  
✅ **Status Workflow** - Pending, In Progress, Submitted, Completed  
✅ **Due Date Tracking** - Items with different due dates  
✅ **Overdue Alerts** - One item is overdue for testing  
✅ **Realistic Descriptions** - Professional audit item descriptions

---

## Resetting Sample Data

To reset and recreate the sample data:

```bash
# Delete existing data
rm -rf data/*.json

# Run seed script again
python utils/seed_data.py
```

Or on Windows:
```powershell
# Delete existing data
Remove-Item data\*.json

# Run seed script again
python utils/seed_data.py
```

---

## Next Steps

1. **Explore as Auditor:**
   - Login as `auditor` / `audit123`
   - View all 3 projects
   - See item assignments
   - Add new items or projects

2. **Explore as Coordinator:**
   - Login as any coordinator (coordinator1, coordinator2, coordinator3)
   - View assigned items
   - Submit documents
   - Track progress

3. **Test Workflows:**
   - Complete the overdue item
   - Submit documents for pending items
   - Create new projects and assignments
   - Test multi-coordinator collaboration

---

**Tip:** The sample data provides a realistic starting point. Feel free to add more projects, items, and assignments to fully test the system!