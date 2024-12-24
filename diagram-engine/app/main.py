import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import FileResponse

from middleware import RequestLoggingMiddleware
from routes import generate_flowchart_api, health_check
from logging_config import setup_logging


app = FastAPI()

# Настройка логирования
setup_logging()

# Настройка хоста и порта из переменных окружения
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", 8000))

# Создание приложения FastAPI
app.add_middleware(RequestLoggingMiddleware)

# Подключение маршрутов
app.add_api_route("/generate_flowchart/", generate_flowchart_api, response_class=FileResponse)
app.add_api_route("/health", health_check)

# Запуск приложения с uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        access_log=False,
    )
