from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.db import engine
from backend.src.models import Base
from backend.src.routers import applications, drivers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:3000"],  # Адрес вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(applications.router)
app.include_router(drivers.router)

@app.on_event("startup")
async def on_startup():
    # создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
