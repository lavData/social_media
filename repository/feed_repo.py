import json
import uuid
from redis import Redis
from datetime import datetime
from sqlalchemy.orm import Session

from model import models
from dto import feed_dto
from service import user_sv


def cache_feed(r: Redis, feed: models.Feed):
	r.set("feed:{}".format(feed.feed_id), json.dumps(feed_dto.FeedOut.from_orm(feed).dict(), default=str))


def remove_cache_feed(r: Redis, feed_id: uuid.UUID):
	r.delete("feed:{}".format(feed_id))


def get_feed(r: Redis, db: Session, feed_id: uuid.UUID, cache: bool = True):
	if not cache:
		return db.query(models.Feed).filter(models.Feed.id == feed_id).first()

	feed = r.get("feed:{}".format(feed_id))
	if feed:
		return feed_dto.FeedOut(**json.loads(feed.decode('utf-8')))
	else:
		feed = db.query(models.Feed).filter(models.Feed.feed_id == feed_id).first()
		if feed is None:
			return None
		cache_feed(r, feed)


def create_feed(r: Redis, db: Session, feed_in: feed_dto.FeedBase):
	user = user_sv.get_user(r, db, feed_in.user_id)
	if user is None:
		return None

	new_feed = models.Feed(**feed_in.dict())
	db.add(new_feed)
	db.commit()
	db.refresh(new_feed)
	return new_feed


def update_feed(r: Redis, db: Session, feed_id: uuid.UUID, feed_in: feed_dto.FeedUpdate):
	feed = get_feed(r, db, feed_id, cache=False)
	if feed is None:
		return None

	for key, value in feed_in.dict().items():
		if value:
			setattr(feed, key, value)
	setattr(feed, 'updated_at', datetime.now())
	db.commit()

	remove_cache_feed(r, feed_id)
	return feed


def delete_feed(r: Redis, db: Session, feed_id: uuid.UUID, delete_by: uuid.UUID = None):
	feed = get_feed(r, db, feed_id, cache=False)
	if feed is None:
		return None

	if delete_by is None:
		feed.deleted_by_user_id = feed.user_id
	else:
		feed.deleted_by_user_id = delete_by

	feed.deleted_at = datetime.now()
	feed.updated_at = datetime.now()
	feed.deleted = True

	remove_cache_feed(r, feed_id)

	db.commit()
	return feed
