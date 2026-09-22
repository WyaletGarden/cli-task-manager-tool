from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
  title: str


class TaskResponse(BaseModel):
  id: int
  title: str
  completed: bool

  # Cho phép Pydantic đọc dữ liệu trực tiếp từ SQLAlchemy Model object
  model_config = ConfigDict(from_attributes=True)