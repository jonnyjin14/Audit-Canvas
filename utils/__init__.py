"""
Utility modules for file handling, validation, configuration, authentication, and session management
"""

# Backend utilities
__version__ = "1.0.0"

# Frontend utilities (from Jonny's branch)
from .auth import check_authentication, login_page, logout_user
from .session import initialize_session_state, reset_session, get_session_info

__all__ = [
    'check_authentication',
    'login_page',
    'logout_user',
    'initialize_session_state',
    'reset_session',
    'get_session_info'
]

# Made with Bob
