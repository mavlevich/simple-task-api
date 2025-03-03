from fastapi import FastAPI
from app.db.connection import engine, Base
from app.routers.task_router import router as task_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple Task Management API")

app.include_router(task_router)
