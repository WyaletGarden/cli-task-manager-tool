from app.database import Base, engine
from app.routers import api, web
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Tự động tạo bảng `tasks` trong PostgreSQL dựa trên SQLAlchemy models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager Web App with PostgreSQL")

# Gắn thư mục static để phục vụ CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Đăng ký các Router giao diện Web và RESTful API
app.include_router(web.router)
app.include_router(api.router)

if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)