from sqlalchemy.orm import Session
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskResponse
from app.repositories.task_repo import TaskRepository


class TaskService:
    """ Service for working with tasks """

    def __init__(self, db: Session):
        self.db = db

    def get_tasks(self):
        tasks = TaskRepository.get_tasks(self.db)
        return [TaskResponse(**task.__dict__) for task in tasks]

    def get_task(self, task_id: int):
        task = TaskRepository.get_task(self.db, task_id)
        if task:
            return TaskResponse(**task.__dict__)
        return None

    def create_task(self, task_data: TaskCreate):
        task = TaskRepository.create_task(self.db, task_data)
        return TaskResponse(**task.__dict__)

    def update_task(self, task_id: int, updated_task: TaskCreate):
        task = TaskRepository.update_task(self.db, task_id, updated_task)
        if task:
            return TaskResponse(**task.__dict__)
        return None

    def delete_task(self, task_id: int):
        return TaskRepository.delete_task(self.db, task_id)
