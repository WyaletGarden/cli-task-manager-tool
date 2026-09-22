from app.database import Base
from sqlalchemy import Boolean, Column, Integer, String


class TaskModel(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  title = Column(String, nullable=False)
  completed = Column(Boolean, default=False)