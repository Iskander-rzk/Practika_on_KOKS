
from .database import init_db
from .user_database import init_user_db

def init_databases():
    init_db()
    init_user_db()

__all__ = ['init_databases']