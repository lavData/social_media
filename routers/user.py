import uuid
from redis import Redis
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException

from service import user_sv
from dto import user_dto, feed_dto
from model.database import SessionLocal, pool

router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache():
    return Redis(connection_pool=pool)


@router.get("/", response_model=list[user_dto.UserOut])
async def get_users(db: Session = Depends(get_db)):
    return user_sv.get_users(db)


@router.get("/{user_id}", response_model=user_dto.UserOut)
async def get_user(user_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    user = user_sv.get_user(cache, db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/feeds", response_model=list[feed_dto.FeedOutUser])
async def get_user_feeds(user_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    user_feeds = user_sv.get_user_feeds(cache, db, user_id)
    if user_feeds is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_feeds


@router.get("/{user_id/feeds_page}", response_model=list[feed_dto.FeedOutUser])
async def get_feeds_page(user_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    feeds_page = user_sv.get_user_feed_page(cache, db, user_id)
    if feeds_page is None:
        raise HTTPException(status_code=404, detail="User not found")
    return feeds_page


@router.get("/{user_id}/followers", response_model=list[user_dto.UserFollowers])
async def get_user_followers(user_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    user_followers = user_sv.get_user_followers(cache, db, user_id)
    if user_followers is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_followers


@router.get("{user_id}/followings", response_model=list[user_dto.UserFollowings])
async def get_user_followings(user_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    user_followings = user_sv.get_user_followings(cache, db, user_id)
    if user_followings is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_followings


@router.post("/", response_model=user_dto.UserOut)
async def create_user(user_in: user_dto.UserIn, db: Session = Depends(get_db)):
    user = user_sv.create_user(db, user_in)
    if user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return user


@router.post("/{user_id}/following", response_model=user_dto.UserFollowing)
async def follow_user(user_id: uuid.UUID, following_id: uuid.UUID,
                      db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    follow_users = user_sv.follow_user(cache, db, user_id, following_id)
    if follow_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return follow_users


@router.delete("/{user_id}/unfollowing")
async def unfollow_user(user_id: uuid.UUID, following_id: uuid.UUID,
                        db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    unfollow_users = user_sv.unfollow_user(cache, db, user_id, following_id)
    if unfollow_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return unfollow_users


@router.put("/{user_id}", response_model=user_dto.UserOut)
async def update_user(user_id: uuid.UUID, user_update: user_dto.UserUpdate,
                      db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    user = user_sv.update_user(cache, db, user_id, user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=user_dto.UserDelete)
async def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    user = user_sv.delete_user(cache, db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}/token", response_model=user_dto.UserDelete)
async def delete_user_token(
        user_id: uuid.UUID, user_deleted: uuid.UUID,
        token: str, db: Session = Depends(get_db),
        cache: Redis = Depends(get_cache)):
    user = user_sv.delete_user_token(cache, db, user_id, user_deleted, token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    elif user == "Invalid token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
