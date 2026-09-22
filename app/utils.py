from contextlib import contextmanager
from functools import wraps
import logging
import os
import time

# --- CẤU HÌNH LOGGING GHI RA FILE VÀ TERMINAL ---
# Tạo thư mục 'logs' ở thư mục gốc nếu chưa có
os.makedirs("logs", exist_ok=True)
log_file_path = os.path.join("logs", "app_actions.log")

# Tạo một logger riêng cho ứng dụng
logger = logging.getLogger("TaskManagerLogger")
logger.setLevel(logging.INFO)

# Tránh bị lặp log handlers nếu module bị gọi nhiều lần
if not logger.handlers:
  # 1. Handler để ghi log vào file (app_actions.log)
  file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
  file_handler.setLevel(logging.INFO)

  # 2. Handler để hiển thị log ra Terminal (Console)
  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.INFO)

  # Định dạng cấu trúc hiển thị của log
  formatter = logging.Formatter(
      "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
  )
  file_handler.setFormatter(formatter)
  stream_handler.setFormatter(formatter)

  # Gắn cả 2 handler vào logger
  logger.addHandler(file_handler)
  logger.addHandler(stream_handler)


# --- CUSTOM CONTEXT MANAGER ---
@contextmanager
def execution_timer(action_name: str):
  """Context manager dùng để đo lường thời gian thực thi của một khối lệnh."""
  start_time = time.time()
  logger.info(f"==> [START] {action_name}")
  try:
    yield
  except Exception as e:
    logger.error(f"==> [ERROR] {action_name} thất bại: {e}")
    raise
  finally:
    elapsed_time = time.time() - start_time
    logger.info(
        f"==> [END] {action_name} hoàn thành trong {elapsed_time:.4f} giây"
    )


# --- CUSTOM DECORATOR ---
def log_action_time(func):
  """Decorator tự động log thời điểm gọi hàm và thời gian thực thi."""

  @wraps(func)
  def wrapper(*args, **kwargs):
    func_name = func.__name__
    logger.info(f"[DECORATOR] Bắt đầu gọi hàm: {func_name}")
    start = time.time()
    try:
      result = func(*args, **kwargs)
      duration = time.time() - start
      logger.info(
          f"[DECORATOR] Hàm {func_name} chạy thành công mất {duration:.4f}s"
      )
      return result
    except Exception as e:
      logger.error(f"[DECORATOR] Hàm {func_name} gặp lỗi: {e}")
      raise

  return wrapper