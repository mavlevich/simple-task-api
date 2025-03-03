from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate
from typing import List, Optional


class TaskRepository:
    @staticmethod
    def get_tasks(db: Session) -> List[Task]:
        """Returns a list of all tasks"""
        result = db.execute(select(Task)).scalars().all()
        return result

    @staticmethod
    def create_task(db: Session, task: TaskCreate) -> Task:
        """Creates a new task"""
        new_task = Task(**task.dict())
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    @staticmethod
    def get_task(db: Session, task_id: int) -> Optional[Task]:
        """Gets the task by ID"""
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def update_task(db: Session, task_id: int, updated_task: TaskCreate) -> Optional[Task]:
        """Updates the task by ID"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            return None
        task.title = updated_task.title
        task.description = updated_task.description
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> Optional[Task]:
        """Deletes a task by ID"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            return None
        db.delete(task)
        db.commit()
        return task
