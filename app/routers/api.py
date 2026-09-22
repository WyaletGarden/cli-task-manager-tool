from app.crud import create_task, get_tasks
from app.database import get_db
from app.schemas import TaskCreate, TaskResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["API Tasks"])


@router.get("/tasks", response_model=list[TaskResponse])
def api_get_tasks(db: Session = Depends(get_db)):
  return get_tasks(db)


@router.post("/tasks", response_model=TaskResponse)
def api_create_task(task: TaskCreate, db: Session = Depends(get_db)):
  return create_task(db, task.title)