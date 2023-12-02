from fastapi import FastAPI
from routers import user
from database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.router)
