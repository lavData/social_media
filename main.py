from fastapi import FastAPI
from sqlalchemy.orm import Session

from routers import user, feed
from model.database import engine, SessionLocal
from model.models import Base

app = FastAPI()

app.include_router(user.router)
app.include_router(feed.router)

# Base.metadata.drop_all(bind=engine, tables=[Base.metadata.tables['feed']])
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
