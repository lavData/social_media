import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from dto.feed_dto import FeedOutUser


class FollowUser(BaseModel):
    user_id: uuid.UUID
    follow_user_id: uuid.UUID

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str


class UserIn(UserBase):
    password: str


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
    birth_date: Optional[str] = None


class UserOut(UserBase):
    user_id: uuid.UUID
    birth_date: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserDelete(UserBase):
    user_id: uuid.UUID
    deleted: bool
    deleted_by_user_id: int


class UserInDb(UserBase):
    user_id: uuid.UUID
    password: str
    birth_date: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted: bool
    deleted_by_user_id: Optional[uuid.UUID] = None

    followers: List[FollowUser] = []
    followings: List[FollowUser] = []
    feeds: list[FeedOutUser] = []

    class Config:
        orm_mode = True


class UserFollowers(BaseModel):
    user_id: uuid.UUID

    class Config:
        orm_mode = True


class UserFollowings(BaseModel):
    follow_user_id: uuid.UUID

    class Config:
        orm_mode = True


class UserFollowing(UserFollowings):
    user_id: uuid.UUID

    class Config:
        orm_mode = True
