import uuid
from redis import Redis
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException

from dto import feed_dto
from service import feed_sv
from model.database import SessionLocal, pool

router = APIRouter(prefix='/feed', tags=['feed'])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache():
    return Redis(connection_pool=pool)


@router.get('/', response_model=feed_dto.FeedOut)
async def get_feed(feed_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    feed = feed_sv.get_feed(cache, db, feed_id)
    if feed is None:
        raise HTTPException(status_code=404, detail='Feed not found')
    return feed


@router.post('/', response_model=feed_dto.FeedOut)
async def create_feed(feed_in: feed_dto.FeedBase, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    feed = feed_sv.create_feed(cache, db, feed_in)
    if feed is None:
        raise HTTPException(status_code=404, detail='User not found')
    return feed


@router.put('/{feed_id}', response_model=feed_dto.FeedOutUpdate)
async def update_feed(feed_id: uuid.UUID,  feed_in: feed_dto.FeedUpdate,
                      db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    feed = feed_sv.update_feed(cache, db, feed_id, feed_in)
    if feed is None:
        raise HTTPException(status_code=404, detail='Feed not found')
    return feed


@router.delete('/{feed_id}', response_model=feed_dto.FeedOut)
async def delete_feed(feed_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    feed = feed_sv.delete_feed(cache, db, feed_id)
    if feed is None:
        raise HTTPException(status_code=404, detail='Feed not found')
    return feed


@router.delete('/{feed_id}/token', response_model=feed_dto.FeedOut)
async def delete_feed_token(feed_id: uuid.UUID, deleted_by: uuid.UUID,
                            token: str, db: Session = Depends(get_db),
                            cache: Redis = Depends(get_cache)):
    feed = feed_sv.delete_feed_token(cache, db, feed_id, deleted_by, token)
    if feed is None:
        raise HTTPException(status_code=404, detail='Feed not found')
    elif feed == "Invalid token":
        raise HTTPException(status_code=401, detail='Invalid token')
    return feed




