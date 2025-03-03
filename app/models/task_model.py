from sqlalchemy import Column, Integer, String, Boolean
from app.db.connection import Base


class Task(Base):
    """ SQLAlchemy model for the Task table """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
