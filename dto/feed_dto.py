import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class FeedBase(BaseModel):
    user_id: uuid.UUID
    type: str
    content: str

    class Config:
        orm_mode = True


class FeedIn(BaseModel):
    created_at: datetime
    feed_id: Optional[uuid.UUID] = None


class FeedUpdate(BaseModel):
    content: Optional[str] = None


class FeedOutUpdate(FeedIn):
    updated_at: datetime


class FeedDelete(FeedUpdate):
    deleted: bool
    deleted_at: datetime
    deleted_by_user_id: uuid.UUID


class FeedOutUser(FeedIn):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FeedOut(FeedBase):
    feed_id: uuid.UUID
    type: str
    content: str
    created_at: datetime
    updated_at: datetime
    deleted: bool
    deleted_at: Optional[str] = None
    deleted_by_user_id: Optional[int] = None
