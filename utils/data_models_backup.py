"""
Data Models for Audit Workflow
Manages projects, items, coordinators, and assignments
"""

from datetime import datetime
from typing import List, Dict, Optional
import json
from pathlib import Path

class DataStore:
    """Simple JSON-based data store for demo purposes"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
    def _load_file(self, filename: str) -> dict:
        """Load data from JSON file"""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_file(self, filename: str, data: dict):
        """Save data to JSON file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# Initialize global data store
data_store = DataStore()

class User:
    """User model with role support"""
    
    ROLES = ['admin', 'auditor', 'coordinator']
    
    def __init__(self, username: str, role: str, group: Optional[str] = None):
        self.username = username
        self.role = role
        self.group = group  # For coordinators
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'role': self.role,
            'group': self.group,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'User':
        user = User(data['username'], data['role'], data.get('group'))
        user.created_at = data.get('created_at', datetime.now().isoformat())
        return user

class Project:
    """Audit project model"""
    
    def __init__(self, project_id: str, name: str, description: str, 
                 created_by: str, status: str = 'active'):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.created_by = created_by  # Auditor username
        self.status = status  # active, completed, archived
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Project':
        project = Project(
            data['project_id'],
            data['name'],
            data['description'],
            data['created_by'],
            data.get('status', 'active')
        )
        project.created_at = data.get('created_at', datetime.now().isoformat())
        project.updated_at = data.get('updated_at', datetime.now().isoformat())
        return project

class AuditItem:
    """Audit item within a project"""
    
    def __init__(self, item_id: str, project_id: str, title: str, 
                 description: str, due_date: str, status: str = 'pending'):
        self.item_id = item_id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status  # pending, in_progress, submitted, reviewed, completed
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'item_id': self.item_id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'AuditItem':
        item = AuditItem(
            data['item_id'],
            data['project_id'],
            data['title'],
            data['description'],
            data['due_date'],
            data.get('status', 'pending')
        )
        item.created_at = data.get('created_at', datetime.now().isoformat())
        item.updated_at = data.get('updated_at', datetime.now().isoformat())
        return item

class Assignment:
    """Assignment of coordinators to audit items"""
    
    def __init__(self, assignment_id: str, item_id: str, 
                 coordinator_username: str, assigned_by: str):
        self.assignment_id = assignment_id
        self.item_id = item_id
        self.coordinator_username = coordinator_username
        self.assigned_by = assigned_by  # Auditor username
        self.assigned_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'assignment_id': self.assignment_id,
            'item_id': self.item_id,
            'coordinator_username': self.coordinator_username,
            'assigned_by': self.assigned_by,
            'assigned_at': self.assigned_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Assignment':
        assignment = Assignment(
            data['assignment_id'],
            data['item_id'],
            data['coordinator_username'],
            data['assigned_by']
        )
        assignment.assigned_at = data.get('assigned_at', datetime.now().isoformat())
        return assignment

class Document:
    """Document submission by coordinator"""
    
    def __init__(self, document_id: str, item_id: str, filename: str,
                 file_path: str, submitted_by: str, notes: str = ''):
        self.document_id = document_id
        self.item_id = item_id
        self.filename = filename
        self.file_path = file_path
        self.submitted_by = submitted_by  # Coordinator username
        self.notes = notes
        self.submitted_at = datetime.now().isoformat()
        self.status = 'submitted'  # submitted, reviewed, approved, rejected
    
    def to_dict(self) -> dict:
        return {
            'document_id': self.document_id,
            'item_id': self.item_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'submitted_by': self.submitted_by,
            'notes': self.notes,
            'submitted_at': self.submitted_at,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Document':
        doc = Document(
            data['document_id'],
            data['item_id'],
            data['filename'],
            data['file_path'],
            data['submitted_by'],
            data.get('notes', '')
        )
        doc.submitted_at = data.get('submitted_at', datetime.now().isoformat())
        doc.status = data.get('status', 'submitted')

class Comment:
    """Comment on an audit item"""
    
    def __init__(self, comment_id: str, item_id: str, user: str, 
                 comment_text: str, comment_type: str = 'comment'):
        self.comment_id = comment_id
        self.item_id = item_id
        self.user = user
        self.comment_text = comment_text
        self.comment_type = comment_type  # comment, status_change, document_request
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'comment_id': self.comment_id,
            'item_id': self.item_id,
            'user': self.user,
            'comment_text': self.comment_text,
            'comment_type': self.comment_type,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Comment':
        comment = Comment(
            data['comment_id'],
            data['item_id'],
            data['user'],
            data['comment_text'],
            data.get('comment_type', 'comment')
        )
        comment.created_at = data.get('created_at', datetime.now().isoformat())
        return comment

class ActivityLog:
    """Activity log entry for tracking all actions"""
    
    def __init__(self, log_id: str, item_id: str, user: str, 
                 action: str, details: str = ''):
        self.log_id = log_id
        self.item_id = item_id
        self.user = user
        self.action = action  # status_change, document_submitted, comment_added, etc.
        self.details = details
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'log_id': self.log_id,
            'item_id': self.item_id,
            'user': self.user,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'ActivityLog':
        log = ActivityLog(
            data['log_id'],
            data['item_id'],
            data['user'],
            data['action'],
            data.get('details', '')
        )
        log.timestamp = data.get('timestamp', datetime.now().isoformat())
        return log
        return doc

# Database operations
class AuditDatabase:
    """Database operations for audit workflow"""
    
    def __init__(self):
        self.store = data_store
        self.users_file = 'users.json'
        self.projects_file = 'projects.json'
        self.items_file = 'items.json'
        self.assignments_file = 'assignments.json'
        self.comments_file = 'comments.json'
        self.activity_logs_file = 'activity_logs.json'
        self.documents_file = 'documents.json'
    
    # User operations
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        users = self.store._load_file(self.users_file)
        if username in users:
            return User.from_dict(users[username])
        return None
    
    def save_user(self, user: User):
        """Save or update user"""
        users = self.store._load_file(self.users_file)
        users[user.username] = user.to_dict()
        self.store._save_file(self.users_file, users)
    
    def get_coordinators_by_group(self, group: str) -> List[User]:
        """Get all coordinators in a group"""
        users = self.store._load_file(self.users_file)
        return [User.from_dict(u) for u in users.values() 
                if u['role'] == 'coordinator' and u.get('group') == group]
    
    def get_all_coordinators(self) -> List[User]:
        """Get all coordinators"""
        users = self.store._load_file(self.users_file)
        return [User.from_dict(u) for u in users.values() 
                if u['role'] == 'coordinator']
    
    # Project operations
    def save_project(self, project: Project):
        """Save or update project"""
        projects = self.store._load_file(self.projects_file)
        projects[project.project_id] = project.to_dict()
        self.store._save_file(self.projects_file, projects)
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        projects = self.store._load_file(self.projects_file)
        if project_id in projects:
            return Project.from_dict(projects[project_id])
        return None
    
    def get_projects_by_auditor(self, auditor_username: str) -> List[Project]:
        """Get all projects created by an auditor"""
        projects = self.store._load_file(self.projects_file)
        return [Project.from_dict(p) for p in projects.values() 
                if p['created_by'] == auditor_username]
    
    def get_all_projects(self) -> List[Project]:
        """Get all projects"""
        projects = self.store._load_file(self.projects_file)
        return [Project.from_dict(p) for p in projects.values()]
    
    # Item operations
    def save_item(self, item: AuditItem):
        """Save or update audit item"""
        items = self.store._load_file(self.items_file)
        items[item.item_id] = item.to_dict()
        self.store._save_file(self.items_file, items)
    
    def get_item(self, item_id: str) -> Optional[AuditItem]:
        """Get item by ID"""
        items = self.store._load_file(self.items_file)
        if item_id in items:
            return AuditItem.from_dict(items[item_id])
        return None
    
    def get_items_by_project(self, project_id: str) -> List[AuditItem]:
        """Get all items in a project"""
        items = self.store._load_file(self.items_file)
        return [AuditItem.from_dict(i) for i in items.values() 
                if i['project_id'] == project_id]
    
    # Assignment operations
    def save_assignment(self, assignment: Assignment):
        """Save assignment"""
        assignments = self.store._load_file(self.assignments_file)
        assignments[assignment.assignment_id] = assignment.to_dict()
        self.store._save_file(self.assignments_file, assignments)
    
    def get_assignments_by_item(self, item_id: str) -> List[Assignment]:
        """Get all assignments for an item"""
        assignments = self.store._load_file(self.assignments_file)
        return [Assignment.from_dict(a) for a in assignments.values() 
                if a['item_id'] == item_id]
    
    def get_assignments_by_coordinator(self, coordinator_username: str) -> List[Assignment]:
        """Get all assignments for a coordinator"""
        assignments = self.store._load_file(self.assignments_file)
        return [Assignment.from_dict(a) for a in assignments.values() 
                if a['coordinator_username'] == coordinator_username]
    
    def delete_assignment(self, assignment_id: str):
        """Delete an assignment"""
        assignments = self.store._load_file(self.assignments_file)
        if assignment_id in assignments:
            del assignments[assignment_id]
            self.store._save_file(self.assignments_file, assignments)
    
    # Document operations
    def save_document(self, document: Document):
        """Save document submission"""
        documents = self.store._load_file(self.documents_file)
        documents[document.document_id] = document.to_dict()
        self.store._save_file(self.documents_file, documents)
    
    def get_documents_by_item(self, item_id: str) -> List[Document]:
        """Get all documents for an item"""
        documents = self.store._load_file(self.documents_file)
        return [Document.from_dict(d) for d in documents.values() 
                if d['item_id'] == item_id]
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Get document by ID"""
        documents = self.store._load_file(self.documents_file)
        if document_id in documents:
            return Document.from_dict(documents[document_id])
        return None

# Global database instance
audit_db = AuditDatabase()

# Made with Bob

    
    # Comment operations
    def save_comment(self, comment: Comment):
        """Save comment"""
        comments = self.store._load_file(self.comments_file)
        comments[comment.comment_id] = comment.to_dict()
        self.store._save_file(self.comments_file, comments)
    
    def get_comments_by_item(self, item_id: str) -> List[Comment]:
        """Get all comments for an item"""
        comments = self.store._load_file(self.comments_file)
        return [Comment.from_dict(c) for c in comments.values() 
                if c['item_id'] == item_id]
    
    # Activity log operations
    def save_activity_log(self, log: ActivityLog):
        """Save activity log entry"""
        logs = self.store._load_file(self.activity_logs_file)
        logs[log.log_id] = log.to_dict()
        self.store._save_file(self.activity_logs_file, logs)
    
    def get_activity_logs_by_item(self, item_id: str) -> List[ActivityLog]:
        """Get all activity logs for an item"""
        logs = self.store._load_file(self.activity_logs_file)
        result = [ActivityLog.from_dict(l) for l in logs.values() 
                  if l['item_id'] == item_id]
        # Sort by timestamp descending (newest first)
        result.sort(key=lambda x: x.timestamp, reverse=True)
        return result
    
    def get_activity_logs_by_user(self, username: str) -> List[ActivityLog]:
        """Get all activity logs for a user"""
        logs = self.store._load_file(self.activity_logs_file)
        result = [ActivityLog.from_dict(l) for l in logs.values() 
                  if l['user'] == username]
        result.sort(key=lambda x: x.timestamp, reverse=True)

# Global database instance
audit_db = AuditDatabase()
        return result
