from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.task_model import Task
from app.schemas.task_schema import TaskResponse
from typing import List, Optional

extra_router = APIRouter(prefix="/extra-tasks", tags=["Additional functionality"])


@extra_router.get("/search-by-title", response_model=List[TaskResponse])
def search_tasks_by_title(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None, description="Search for tasks by name"),
):
    if not title:
        return []

    tasks = db.query(Task).filter(Task.title.ilike(f"%{title}%")).all()

    return [TaskResponse(id=t.id, title=t.title, description=t.description, completed=t.completed) for t in tasks]


@extra_router.get("/search-by-description", response_model=List[TaskResponse])
def search_tasks_by_description(
    db: Session = Depends(get_db),
    description: Optional[str] = Query(None, description="Search for tasks by description"),
):
    if not description:
        return []

    tasks = db.query(Task).filter(Task.description.ilike(f"%{description}%")).all()

    return [TaskResponse(id=t.id, title=t.title, description=t.description, completed=t.completed) for t in tasks]
