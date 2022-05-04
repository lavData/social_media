import uuid
from redis import Redis
from sqlalchemy.orm import Session

import config
from dto import user_dto
from repository import user_repo


def get_users(db: Session):
    return user_repo.get_users(db)


def get_user(cache: Redis, db: Session, user_id: uuid.UUID):
    return user_repo.get_user(cache, db, user_id)


def get_user_followers(cache: Redis, db: Session, user_id: uuid.UUID):
    return user_repo.get_user(cache, db, user_id).followers


def get_user_followings(cache: Redis, db: Session, user_id: uuid.UUID):
    return user_repo.get_user(cache, db, user_id).followings


def get_user_feeds(cache: Redis, db: Session, user_id: uuid.UUID):
    return user_repo.get_user(cache, db, user_id).feeds


def get_user_feed_page(cache: Redis, db: Session, user_id: uuid.UUID):
    return user_repo.get_user_feed_page(cache, db, user_id)


def create_user(db: Session, user_in: user_dto.UserIn):
    return user_repo.create_user(db, user_in)


def follow_user(cache: Redis, db: Session, user_id: uuid.UUID, follower_id: uuid.UUID):
    return user_repo.follow_user(cache, db, user_id, follower_id)


def unfollow_user(cache: Redis, db: Session, user_id: uuid.UUID, follower_id: uuid.UUID):
    return user_repo.unfollow_user(cache, db, user_id, follower_id)


def update_user(cache: Redis, db: Session, user_id: uuid.UUID, user_in: user_dto.UserUpdate):
    return user_repo.update_user(cache, db, user_id, user_in)


def delete_user(cache: Redis, db: Session, user_id: uuid.UUID):
    return user_repo.delete_user(cache, db, user_id, user_id)


def delete_user_token(cache: Redis, db: Session, user_id: uuid.UUID, user_deleted: uuid.UUID, token: str):
    if token != config.TOKEN:
        return "Invalid token"
    return user_repo.delete_user(cache, db, user_id, user_deleted)
