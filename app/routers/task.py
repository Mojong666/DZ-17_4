from fastapi import APIRouter
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")


router = APIRouter(
    prefix="/task",
    tags=["task"]
)

@router.get("/")
def all_tasks():
    return {"message": "All tasks"}

@router.get("/{task_id}")
def task_by_id(task_id: int):
    return {"message": f"Task {task_id}"}

@router.post("/create")
def create_task():
    return {"message": "Task created"}

@router.put("/update")
def update_task():
    return {"message": "Task updated"}

@router.delete("/delete")
def delete_task():
    return {"message": "Task deleted"}

