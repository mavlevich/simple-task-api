from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict


class TaskCreate(BaseModel):
    """ Pydantic schema for task creation """
    title: str = Field(..., min_length=3, max_length=100, example="Make a task")
    description: Optional[str] = Field(None, max_length=255, example="Internship Software Engineer Exercise")
    completed: bool = False


class TaskResponse(BaseModel):
    """ Pydantic schema for task response """
    id: int
    title: str
    description: Optional[str]
    completed: bool
