import uuid
from redis import Redis
from sqlalchemy.orm import Session

import config
from dto import feed_dto
from repository import feed_repo


def get_feed(cache: Redis, db: Session, feed_id: uuid.UUID):
	return feed_repo.get_feed(cache, db, feed_id)


def create_feed(cache: Redis, db: Session, feed_in: feed_dto.FeedBase):
	return feed_repo.create_feed(cache, db, feed_in)


def update_feed(cache: Redis, db: Session, feed_id: uuid.UUID, feed_in: feed_dto.FeedUpdate):
	return feed_repo.update_feed(cache, db, feed_id, feed_in)


def delete_feed(cache: Redis, db: Session, feed_id: uuid.UUID, delete_by: uuid.UUID = None):
	return feed_repo.delete_feed(cache, db, feed_id, delete_by)


def delete_feed_token(cache: Redis, db: Session, feed_id: uuid.UUID, deleted_by: uuid.UUID, token: str):
	if token != config.TOKEN:
		return "Invalid token"
	return feed_repo.delete_feed(cache, db, feed_id, deleted_by)
