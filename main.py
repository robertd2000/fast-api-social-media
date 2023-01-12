from fastapi import FastAPI

from db import engine, Base
from routers import auth, posts, users

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
