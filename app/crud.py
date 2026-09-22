from app.models import TaskModel
from app.utils import execution_timer, log_action_time
from sqlalchemy.orm import Session


@log_action_time
def get_tasks(db: Session) -> list[TaskModel]:
  """Lấy danh sách tất cả các task từ database."""
  with execution_timer("Truy vấn danh sách Task từ PostgreSQL"):
    return db.query(TaskModel).all()


@log_action_time
def create_task(db: Session, title: str) -> TaskModel:
  """Thêm mới một task vào database."""
  with execution_timer(f"Thêm task mới: '{title}'"):
    db_task = TaskModel(title=title, completed=False)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@log_action_time
def toggle_task(db: Session, task_id: int) -> TaskModel | None:
  """Đổi trạng thái hoàn thành của task."""
  with execution_timer(f"Đổi trạng thái task ID {task_id}"):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
      task.completed = not task.completed
      db.commit()
      db.refresh(task)
    return task


@log_action_time
def delete_task(db: Session, task_id: int) -> TaskModel | None:
  """Xóa một task khỏi database dựa theo ID."""
  with execution_timer(f"Xóa task ID {task_id}"):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
      db.delete(task)
      db.commit()
    return task