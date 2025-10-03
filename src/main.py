import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import engine
from src.models import Base, UserRole
from src.routers import applications, drivers, users
from src.auth import router as auth

from src.auth.security import security
from src.schemas.application import ApplicationCreate
from src.schemas.driver import DriverCreate
from src.schemas.user import UserCreate, UserUpdate

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
    db_path = 'database.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Файл базы данных удален")
    else:
        print("Файл базы данных не существует")

    # создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from src.crud import user as user_crud
    from src.crud import driver as driver_crud
    from src.crud import application as applications_crud
    from src.core.db import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        user_1 = await user_crud.create_user(
            session, UserCreate(
                email="manager@mail.ru",
                password="1",
                firstname="Максим",
                lastname="Петров"
            )
        )
        await user_crud.update_user(session, user_1.id, UserUpdate(role=UserRole.MANAGER))

        user_2 = await user_crud.create_user(
            session, UserCreate(
                email="admin@mail.ru",
                password="1",
                firstname="Андрей",
                lastname="Сидоров"
            )
        )
        await user_crud.update_user(session, user_2.id, UserUpdate(role=UserRole.ADMIN))

        user_3 = await user_crud.create_user(
            session, UserCreate(
                email="driver1@mail.ru",
                password="1",
                firstname="Дмитрий",
                lastname="Попов"
            )
        )
        await driver_crud.create_driver(session, DriverCreate(
            user_id=user_3.id,
            phone="+79042260791",
            car="Volvo FH4",
            is_active=False
        ))

        user_4 = await user_crud.create_user(
            session, UserCreate(
                email="driver2@mail.ru",
                password="1",
                firstname="Денис",
                lastname="Гагарин"
            )
        )
        await driver_crud.create_driver(session, DriverCreate(
            user_id=user_4.id,
            phone="+79042260792",  # добавил телефон
            car="Mercedes Actros",  # добавил машину
            is_active=True  # добавил статус активности
        ))

        user_5 = await user_crud.create_user(
            session, UserCreate(
                email="driver3@mail.ru",
                password="1",
                firstname="Даниил",
                lastname="Иванов"
            )
        )
        await driver_crud.create_driver(session, DriverCreate(
            user_id=user_5.id,
            phone="+79042260793",  # добавил телефон
            car="Scania R450",  # добавил машину
            is_active=True  # добавил статус активности
        ))


        await applications_crud.create_application(session, ApplicationCreate(
            from_="Москва, ул. Тверская, 1",
            to="Санкт-Петербург, Невский проспект, 5",
            weight=1500.5,
            volume=12.8,
            description="Перевозка электроники и офисной техники",
            driver_id=user_3.id
        ))

        await applications_crud.create_application(session, ApplicationCreate(
            from_="Казань, ул. Баумана, 10",
            to="Екатеринбург, ул. Ленина, 25",
            weight=800.0,
            volume=8.2,
            description="Доставка строительных материалов",
            driver_id=user_3.id
        ))

        await applications_crud.create_application(session, ApplicationCreate(
            from_="Новосибирск, Красный проспект, 15",
            to="Красноярск, ул. Карла Маркса, 30",
            weight=2500.75,
            volume=18.5,
            description="Перевозка промышленного оборудования, требуется осторожность",
            driver_id=user_4.id
        ))

