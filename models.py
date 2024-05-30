from enum import Enum
from typing import Optional

class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    SUPERADMIN = 'SUPERADMIN'

class UserStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    BLOCKED = 'BLOCKED'

class TodoType(Enum):
    OPTIONAL = 'optional'
    PERSONAL = 'personal'
    SHOPPING = 'shopping'

class User:
    def __init__(self,
                 username: str,
                 password: str,
                 user_id: Optional[int] = None,
                 role: Optional[UserRole] = None,
                 status: Optional[UserStatus] = None,
                 login_try_count: Optional[int] = None
                 ):
        self.username = username
        self.password = password
        self.id = user_id
        self.role = role or UserRole.USER
        self.status = status or UserStatus.INACTIVE
        self.login_try_count = login_try_count or 0

    def __str__(self):
        return f'{self.role.value} => {self.username}'

class Todo:
    def __init__(self,
                 title: str,
                 user_id: int,
                 todo_type: Optional[TodoType] = None,
                 ):
        self.title = title
        self.user_id = user_id
        self.todo_type = todo_type or TodoType.OPTIONAL
