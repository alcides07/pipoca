from fastapi import FastAPI
from routers import item, user
from database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(item.router)
app.include_router(user.router)
