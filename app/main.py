from fastapi import FastAPI
from app.db.connection import engine, Base
from app.routers.task_router import router as task_router
from app.routers.extra_router import extra_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Simple Task API",
    description="A simple REST API for managing tasks",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.include_router(task_router)
app.include_router(extra_router)
