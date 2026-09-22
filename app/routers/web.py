from app.crud import create_task, delete_task, get_tasks, toggle_task
from app.database import get_db
from app.utils import logger  # Import logger dùng chung
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
  logger.info("Người dùng truy cập trang chủ (Web UI)")
  tasks = get_tasks(db)
  return templates.TemplateResponse(request, "index.html", {"tasks": tasks})


@router.post("/add")
def add(title: str = Form(...), db: Session = Depends(get_db)):
  logger.info(f"Yêu cầu thêm task mới từ giao diện: {title}")
  create_task(db, title)
  return RedirectResponse(url="/", status_code=303)


@router.post("/complete/{task_id}")
def complete(task_id: int, db: Session = Depends(get_db)):
  logger.info(f"Yêu cầu đổi trạng thái task ID: {task_id}")
  toggle_task(db, task_id)
  return RedirectResponse(url="/", status_code=303)


@router.post("/delete/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db)):
  logger.info(f"Yêu cầu xóa task ID: {task_id}")
  delete_task(db, task_id)
  return RedirectResponse(url="/", status_code=303)