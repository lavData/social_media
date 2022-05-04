import uuid
from datetime import datetime
from sqlalchemy import Column, \
    Integer, \
    String, \
    ForeignKey, \
    DateTime, \
    Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from model.database import Base


class User(Base):
    __tablename__ = 'user_social'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    birth_date = Column(String(50), nullable=True)
    address = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted = Column(Boolean, nullable=False, default=0)
    deleted_by_user_id = Column(UUID(as_uuid=True), ForeignKey('user_social.user_id'), nullable=True)

    followers = relationship(
        'FollowUser', backref='followers',
        foreign_keys='FollowUser.follow_user_id',
        primaryjoin='FollowUser.follow_user_id == User.user_id',
        cascade='all, delete-orphan'
    )
    followings = relationship(
        'FollowUser', backref='followings',
        foreign_keys='FollowUser.user_id',
        primaryjoin='FollowUser.user_id == User.user_id',
        cascade='all, delete-orphan'
    )

    feeds = relationship(
        'Feed', back_populates='user',
        foreign_keys='Feed.user_id',
        primaryjoin='Feed.user_id == User.user_id',
        cascade='all, delete-orphan'
    )


class Feed(Base):
    __tablename__ = 'feed'

    feed_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_social.user_id'), nullable=False)
    type = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted = Column(Boolean, nullable=False, default=0)
    deleted_at = Column(String(50), nullable=True)
    deleted_by_user_id = Column(UUID(as_uuid=True), ForeignKey('user_social.user_id'), nullable=True)

    user = relationship(
        'User', back_populates='feeds',
        foreign_keys='Feed.user_id',
        primaryjoin='Feed.user_id == User.user_id',
        cascade='all, delete'
        )


class FollowUser(Base):
    __tablename__ = 'follow'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user_social.user_id'), primary_key=True)
    follow_user_id = Column(UUID(as_uuid=True), ForeignKey('user_social.user_id'), primary_key=True)

    def __eq__(self, other):
        if isinstance(other, FollowUser):
            return self.user_id == other.user_id and self.follow_user_id == other.follow_user_id
        return False

# class FeedUser(Base):
#     __tablename__ = 'feed_user'
#
#     feed_id = Column(Integer, ForeignKey('feed.feed_id'), primary_key=True)
#     user_id = Column(Integer, ForeignKey('user_social.user_id'), primary_key=True)
