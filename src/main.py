from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import engine
from src.models import Base
from src.routers import applications, drivers, users
from src.auth import router as auth

from src.auth.security import security

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Адрес вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(applications.router)
app.include_router(drivers.router)
app.include_router(users.router)
app.include_router(auth.router)

security.handle_errors(app)

@app.on_event("startup")
async def on_startup():
    # создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # создаём тестового пользователя при запуске (если нет)
    # async with SessionLocal() as db:
    #     user = await get_user(db, "admin")
    #     if not user:
    #         db.add(User(username="admin", hashed_password=get_password_hash("1234")))
    #         await db.commit()
