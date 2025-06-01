from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

# Импорт роутеров
from app.routes.user import router as users_router
from app.routes.notes import router as notes_router

app = FastAPI()

# CORS настройки
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры (без префиксов)
app.include_router(users_router)
app.include_router(notes_router)

# Путь к директории фронта
frontend_path = Path(__file__).parent.parent / "frontend"

# Подключение статики
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Отдача главной страницы
@app.get("/")
def root():
    return FileResponse(frontend_path / "register.html")
