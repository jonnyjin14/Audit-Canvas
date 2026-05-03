"""
Seed Data Script
Populates the database with sample projects, items, and assignments for demo purposes
"""

import sys
import io
from datetime import datetime, timedelta
from data_models import (
    audit_db, Project, AuditItem, Assignment, User, Document
)
import uuid

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate_id(prefix: str) -> str:
    """Generate unique ID with prefix"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def seed_users():
    """Create sample users"""
    print("Creating sample users...")
    
    # Create coordinators if they don't exist
    coordinators = [
        ('coordinator1', 'coordinator', 'Finance'),
        ('coordinator2', 'coordinator', 'Operations'),
        ('coordinator3', 'coordinator', 'IT'),
    ]
    
    for username, role, group in coordinators:
        if not audit_db.get_user(username):
            user = User(username, role, group)
            audit_db.save_user(user)
            print(f"  ✓ Created user: {username} ({group})")

def seed_projects():
    """Create sample projects with items and assignments"""
    print("\nCreating sample projects...")
    
    # Project 1: Q4 2026 Financial Audit
    project1_id = generate_id("PRJ")
    project1 = Project(
        project_id=project1_id,
        name="Q4 2026 Financial Audit",
        description="Comprehensive financial audit for Q4 2026 including revenue recognition, expense validation, and balance sheet reconciliation.",
        created_by="auditor",
        status="active"
    )
    audit_db.save_project(project1)
    print(f"  ✓ Created project: {project1.name}")
    
    # Items for Project 1
    items1 = [
        {
            'title': 'Revenue Recognition Analysis',
            'description': 'Review revenue recognition policies and validate Q4 revenue transactions. Ensure compliance with ASC 606 standards.',
            'due_date': (datetime.now() + timedelta(days=7)).date().isoformat(),
            'status': 'in_progress',
            'coordinators': ['coordinator1']
        },
        {
            'title': 'Expense Validation',
            'description': 'Validate all Q4 operating expenses, verify proper authorization and documentation for expenses over $10,000.',
            'due_date': (datetime.now() + timedelta(days=10)).date().isoformat(),
            'status': 'in_progress',
            'coordinators': ['coordinator1', 'coordinator2']
        },
        {
            'title': 'IT Systems Access Review',
            'description': 'Review user access rights to financial systems, identify and remove unnecessary privileges, document all administrative accounts.',
            'due_date': (datetime.now() + timedelta(days=5)).date().isoformat(),
            'status': 'pending',
            'coordinators': ['coordinator3']
        },
        {
            'title': 'Accounts Receivable Aging',
            'description': 'Analyze AR aging report, identify overdue accounts, verify collection procedures are being followed.',
            'due_date': (datetime.now() + timedelta(days=14)).date().isoformat(),
            'status': 'pending',
            'coordinators': ['coordinator1']
        }
    ]
    
    for item_data in items1:
        item_id = generate_id("ITEM")
        item = AuditItem(
            item_id=item_id,
            project_id=project1_id,
            title=item_data['title'],
            description=item_data['description'],
            due_date=item_data['due_date'],
            status=item_data['status']
        )
        audit_db.save_item(item)
        print(f"    ✓ Created item: {item.title}")
        
        # Create assignments
        for coordinator in item_data['coordinators']:
            assignment_id = generate_id("ASGN")
            assignment = Assignment(
                assignment_id=assignment_id,
                item_id=item_id,
                coordinator_username=coordinator,
                assigned_by="auditor"
            )
            audit_db.save_assignment(assignment)
            print(f"      → Assigned to: {coordinator}")
    
    # Project 2: Operational Efficiency Review
    project2_id = generate_id("PRJ")
    project2 = Project(
        project_id=project2_id,
        name="Operational Efficiency Review",
        description="Assessment of operational processes, workflow optimization opportunities, and resource utilization across departments.",
        created_by="auditor",
        status="active"
    )
    audit_db.save_project(project2)
    print(f"  ✓ Created project: {project2.name}")
    
    # Items for Project 2
    items2 = [
        {
            'title': 'Supply Chain Process Documentation',
            'description': 'Document current supply chain processes, identify bottlenecks, and recommend improvements for efficiency.',
            'due_date': (datetime.now() + timedelta(days=12)).date().isoformat(),
            'status': 'in_progress',
            'coordinators': ['coordinator2']
        },
        {
            'title': 'Inventory Management Review',
            'description': 'Review inventory levels, turnover rates, and storage costs. Identify slow-moving items and optimization opportunities.',
            'due_date': (datetime.now() + timedelta(days=8)).date().isoformat(),
            'status': 'pending',
            'coordinators': ['coordinator2']
        },
        {
            'title': 'IT Infrastructure Assessment',
            'description': 'Assess current IT infrastructure capacity, identify upgrade needs, and evaluate cloud migration opportunities.',
            'due_date': (datetime.now() + timedelta(days=15)).date().isoformat(),
            'status': 'pending',
            'coordinators': ['coordinator3']
        }
    ]
    
    for item_data in items2:
        item_id = generate_id("ITEM")
        item = AuditItem(
            item_id=item_id,
            project_id=project2_id,
            title=item_data['title'],
            description=item_data['description'],
            due_date=item_data['due_date'],
            status=item_data['status']
        )
        audit_db.save_item(item)
        print(f"    ✓ Created item: {item.title}")
        
        # Create assignments
        for coordinator in item_data['coordinators']:
            assignment_id = generate_id("ASGN")
            assignment = Assignment(
                assignment_id=assignment_id,
                item_id=item_id,
                coordinator_username=coordinator,
                assigned_by="auditor"
            )
            audit_db.save_assignment(assignment)
            print(f"      → Assigned to: {coordinator}")
    
    # Project 3: Compliance Audit (with overdue item)
    project3_id = generate_id("PRJ")
    project3 = Project(
        project_id=project3_id,
        name="Annual Compliance Audit",
        description="Annual review of regulatory compliance including SOX controls, data privacy regulations, and industry-specific requirements.",
        created_by="auditor2",
        status="active"
    )
    audit_db.save_project(project3)
    print(f"  ✓ Created project: {project3.name}")
    
    # Items for Project 3 (including overdue)
    items3 = [
        {
            'title': 'SOX Controls Testing',
            'description': 'Test key SOX controls for financial reporting, document results, and identify any control deficiencies.',
            'due_date': (datetime.now() - timedelta(days=2)).date().isoformat(),  # OVERDUE
            'status': 'in_progress',
            'coordinators': ['coordinator1', 'coordinator3']
        },
        {
            'title': 'Data Privacy Compliance Check',
            'description': 'Verify GDPR and CCPA compliance, review data handling procedures, and assess privacy policy adequacy.',
            'due_date': (datetime.now() + timedelta(days=6)).date().isoformat(),
            'status': 'pending',
            'coordinators': ['coordinator3']
        },
        {
            'title': 'Vendor Compliance Review',
            'description': 'Review vendor contracts for compliance clauses, verify vendor certifications, and assess third-party risk.',
            'due_date': (datetime.now() + timedelta(days=20)).date().isoformat(),
            'status': 'pending',
            'coordinators': ['coordinator2']
        }
    ]
    
    for item_data in items3:
        item_id = generate_id("ITEM")
        item = AuditItem(
            item_id=item_id,
            project_id=project3_id,
            title=item_data['title'],
            description=item_data['description'],
            due_date=item_data['due_date'],
            status=item_data['status']
        )
        audit_db.save_item(item)
        print(f"    ✓ Created item: {item.title}")
        
        # Create assignments
        for coordinator in item_data['coordinators']:
            assignment_id = generate_id("ASGN")
            assignment = Assignment(
                assignment_id=assignment_id,
                item_id=item_id,
                coordinator_username=coordinator,
                assigned_by="auditor2"
            )
            audit_db.save_assignment(assignment)
            print(f"      → Assigned to: {coordinator}")

def seed_all():
    """Seed all sample data"""
    print("=" * 60)
    print("SEEDING SAMPLE DATA")
    print("=" * 60)
    
    seed_users()
    seed_projects()
    
    print("\n" + "=" * 60)
    print("✅ SAMPLE DATA CREATED SUCCESSFULLY!")
    print("=" * 60)
    print("\nSummary:")
    print("  • 3 Projects created")
    print("  • 10 Audit items created")
    print("  • Multiple coordinator assignments")
    print("  • 1 Overdue item for testing")
    print("\nYou can now:")
    print("  1. Login as 'auditor' to see projects")
    print("  2. Login as 'coordinator1', 'coordinator2', or 'coordinator3'")
    print("     to see assigned items")
    print("\n")

if __name__ == "__main__":
    seed_all()

# Made with Bob
