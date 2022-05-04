import json
import uuid
from redis import Redis
from datetime import datetime
from sqlalchemy.orm import Session

from model import models
from dto import user_dto, feed_dto


def cache_user(r: Redis, user: models.User):
	r.set("user:" + str(user.user_id), json.dumps(user_dto.UserInDb.from_orm(user).dict(), default=str))


def remove_cache_user(r: Redis, user_id: uuid.UUID):
	r.delete("user:" + str(user_id))


def get_users(db: Session):
	return db.query(models.User).filter(models.User.deleted == 'False').all()


def get_user(r: Redis, db: Session, user_id: uuid.UUID, cache: bool = True):
	if not cache:
		return db.query(models.User).filter(models.User.user_id == user_id).first()

	user = r.get("user:{}".format(user_id))
	if user:
		return user_dto.UserInDb(**json.loads(user.decode('utf-8')))
	else:
		user = db.query(models.User).filter(models.User.user_id == user_id, models.User.deleted == 'False').first()
		if user is None:
			return None

		cache_user(r, user)
		return user


def get_user_email(db: Session, email: str):
	return db.query(models.User).filter(models.User.email == email, models.User.deleted == 'False').first()


def get_user_followers(db: Session, user_id: uuid.UUID):
	return get_user(db, user_id).followers


def get_user_followings(db: Session, user_id: uuid.UUID):
	return get_user(db, user_id).followings


def get_user_feed_page(r: Redis, db: Session, user_id: uuid.UUID):
	user = get_user(r, db, user_id)
	if user is None:
		return None

	feed_page = r.get("user_feed_page:" + str(user_id))
	if feed_page:
		return json.loads(feed_page.decode('utf-8'))
	else:
		feed_page = db.query(models.Feed).join(models.FollowUser, models.FollowUser.follow_user_id == models.Feed.user_id).\
			filter(models.FollowUser.user_id == user_id).all()

		feed_pages = [feed_dto.FeedOutUser.from_orm(feed).dict() for feed in feed_page]
		r.set("user_feed_page:" + str(user_id), json.dumps(feed_pages, default=str))
		r.expire("user_feed_page:" + str(user_id), 60 * 3)
		return feed_pages


def create_user(db, user_in: user_dto.UserIn):
	user = get_user_email(db, user_in.email)
	if user:
		return None

	new_user = models.User(**user_in.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user


def follow_user(r: Redis, db: Session, user_id: uuid.UUID, following_id: uuid.UUID):
	user = get_user(r, db, user_id, cache=False)
	following = get_user(r, db, following_id, cache=False)
	if user is None or following is None:
		return None

	user.followings.append(models.FollowUser(follow_user_id=following_id, user_id=user_id))
	db.commit()

	remove_cache_user(r, user_id)
	remove_cache_user(r, following_id)

	return user.followings[-1]


def unfollow_user(cache: Redis, db: Session, user_id: uuid.UUID, following_id: uuid.UUID):
	user = get_user(cache, db, user_id, cache=False)
	following = get_user(cache, db, following_id, cache=False)
	if user is None or following is None:
		return None

	user.followings.remove(models.FollowUser(follow_user_id=following_id, user_id=user_id))
	db.commit()

	remove_cache_user(cache, user_id)
	remove_cache_user(cache, following_id)

	return user


def update_user(r: Redis, db: Session, user_id: uuid.UUID, user_in: user_dto.UserUpdate):
	user = get_user(r, db, user_id, cache=False)
	if user is None:
		return None

	for key, value in user_in.dict().items():
		if value:
			setattr(user, key, value)
	setattr(user, 'updated_at', datetime.now())
	db.commit()

	remove_cache_user(r, user_id)
	return user


def delete_user(r: Redis, db: Session, user_delete_id: uuid.UUID, user_deleted_id: uuid.UUID):
	user_delete = get_user(r, db, user_delete_id, cache=False)
	user_deleted = get_user(r, db, user_deleted_id, cache=False)
	if user_deleted is None or user_delete is None:
		return None

	user_deleted.deleted = True
	user_deleted.deleted_at = datetime.now()
	user_deleted.followings = []
	user_deleted.followers = []
	user_deleted.feeds = []
	user_deleted.deleted_by_user_id = user_delete_id

	remove_cache_user(r, user_delete_id)

	db.commit()
	return user_deleted


