from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routers.task_router import router as task_router
from app.routers.extra_router import extra_router

app = FastAPI(
    title="Simple Task API",
    description="A simple REST API for managing tasks",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("app/static", "index.html"))


app.include_router(task_router)
app.include_router(extra_router)
