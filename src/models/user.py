from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime] = None
    friends: List[str] = []  # List of user IDs
    restricted_users: List[str] = []  # Users this user has restricted
    blocked_users: List[str] = []  # Users this user has blocked

class FriendRequest(BaseModel):
    from_user: str
    to_user: str
    status: str  # 'pending', 'accepted', 'declined'
    created_at: Optional[datetime] = None
