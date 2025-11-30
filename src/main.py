import os
from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import engine
from src.models import Base, UserRole, ApplicationStatus
from src.routers import applications, drivers, users
from src.auth import router as auth

from src.auth.security import security
from src.schemas.application import ApplicationCreate
from src.schemas.driver import DriverCreate
from src.schemas.user import UserCreate, UserUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from src.crud import user as user_crud
    from src.crud import driver as driver_crud
    from src.crud import application as applications_crud
    from src.core.db import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        # Создание менеджеров
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
                email="manager2@mail.ru",
                password="1",
                firstname="Анна",
                lastname="Смирнова"
            )
        )
        await user_crud.update_user(session, user_2.id, UserUpdate(role=UserRole.MANAGER))

        # Создание администраторов
        user_3 = await user_crud.create_user(
            session, UserCreate(
                email="admin@mail.ru",
                password="1",
                firstname="Андрей",
                lastname="Сидоров"
            )
        )
        await user_crud.update_user(session, user_3.id, UserUpdate(role=UserRole.ADMIN))

        user_4 = await user_crud.create_user(
            session, UserCreate(
                email="admin2@mail.ru",
                password="1",
                firstname="Екатерина",
                lastname="Иванова"
            )
        )
        await user_crud.update_user(session, user_4.id, UserUpdate(role=UserRole.ADMIN))

        # Создание водителей
        drivers_data = [
            {
                "email": "driver1@mail.ru",
                "password": "1",
                "firstname": "Дмитрий",
                "lastname": "Попов",
                "phone": "+79042260791",
                "car": "Volvo FH4",
                "is_active": False
            },
            {
                "email": "driver2@mail.ru",
                "password": "1",
                "firstname": "Денис",
                "lastname": "Гагарин",
                "phone": "+79042260792",
                "car": "Mercedes Actros",
                "is_active": True
            },
            {
                "email": "driver3@mail.ru",
                "password": "1",
                "firstname": "Даниил",
                "lastname": "Иванов",
                "phone": "+79042260793",
                "car": "Scania R450",
                "is_active": True
            },
            {
                "email": "driver4@mail.ru",
                "password": "1",
                "firstname": "Сергей",
                "lastname": "Кузнецов",
                "phone": "+79042260794",
                "car": "MAN TGX",
                "is_active": True
            },
            {
                "email": "driver5@mail.ru",
                "password": "1",
                "firstname": "Алексей",
                "lastname": "Федоров",
                "phone": "+79042260795",
                "car": "DAF XF",
                "is_active": True
            },
            {
                "email": "driver6@mail.ru",
                "password": "1",
                "firstname": "Михаил",
                "lastname": "Васильев",
                "phone": "+79042260796",
                "car": "Renault Magnum",
                "is_active": False
            }
        ]

        driver_users = []
        for driver_data in drivers_data:
            user = await user_crud.create_user(
                session, UserCreate(
                    email=driver_data["email"],
                    password=driver_data["password"],
                    firstname=driver_data["firstname"],
                    lastname=driver_data["lastname"]
                )
            )
            await driver_crud.create_driver(session, DriverCreate(
                user_id=user.id,
                phone=driver_data["phone"],
                car=driver_data["car"],
                is_active=driver_data["is_active"]
            ))
            driver_users.append(user)

        # Создание обычных пользователей (клиентов)
        clients_data = [
            {
                "email": "client1@mail.ru",
                "password": "1",
                "firstname": "Ольга",
                "lastname": "Новикова"
            },
            {
                "email": "client2@mail.ru",
                "password": "1",
                "firstname": "Ирина",
                "lastname": "Морозова"
            },
            {
                "email": "client3@mail.ru",
                "password": "1",
                "firstname": "Павел",
                "lastname": "Белов"
            }
        ]

        for client_data in clients_data:
            await user_crud.create_user(
                session, UserCreate(
                    email=client_data["email"],
                    password=client_data["password"],
                    firstname=client_data["firstname"],
                    lastname=client_data["lastname"]
                )
            )

        # Создание заявок с разными статусами и датами
        applications_data = [
            # Новые заявки
            {
                "from_": "Москва, ул. Тверская, 1",
                "to": "Санкт-Петербург, Невский проспект, 5",
                "weight": 1500.5,
                "volume": 12.8,
                "cargo_content": "Перевозка электроники и офисной техники",
                "notes": "Хрупкий груз, требуется осторожная погрузка",
                "declared_value": 250000.0,
                "status": ApplicationStatus.NEW,
                "sender_name": "Иван Петров",
                "sender_phone": "+79161234567",
                "recipient_name": "Алексей Сидоров",
                "recipient_phone": "+78129876543",
                "driver_id": driver_users[0].id,
                "created_at": datetime.now() - timedelta(days=1)
            },
            {
                "from_": "Казань, ул. Баумана, 10",
                "to": "Екатеринбург, ул. Ленина, 25",
                "weight": 800.0,
                "volume": 8.2,
                "cargo_content": "Доставка строительных материалов",
                "notes": "Паллеты с сухими смесями, защита от влаги",
                "declared_value": 75000.0,
                "status": ApplicationStatus.NEW,
                "sender_name": "ООО 'СтройМатериалы'",
                "sender_phone": "+78432567890",
                "recipient_name": "ООО 'УралСтрой'",
                "recipient_phone": "+73431234567",
                "driver_id": driver_users[0].id,
                "created_at": datetime.now() - timedelta(hours=12)
            },
            # Заявки в работе
            {
                "from_": "Новосибирск, Красный проспект, 15",
                "to": "Красноярск, ул. Карла Маркса, 30",
                "weight": 2500.75,
                "volume": 18.5,
                "cargo_content": "Перевозка промышленного оборудования",
                "notes": "Тяжелое оборудование, требуется кран для погрузки",
                "declared_value": 1800000.0,
                "status": ApplicationStatus.PROGRESS,
                "sender_name": "ПАО 'ЗаводСибирь'",
                "sender_phone": "+73832223344",
                "recipient_name": "ООО 'КрасноярскМаш'",
                "recipient_phone": "+73912227788",
                "driver_id": driver_users[1].id,
                "created_at": datetime.now() - timedelta(days=3)
            },
            {
                "from_": "Самара, ул. Куйбышева, 45",
                "to": "Уфа, проспект Октября, 15",
                "weight": 1200.0,
                "volume": 15.3,
                "cargo_content": "Перевозка продуктов питания",
                "notes": "Рефрижератор, температура +4°C",
                "declared_value": 350000.0,
                "status": ApplicationStatus.PROGRESS,
                "sender_name": "ООО 'ПродуктыПлюс'",
                "sender_phone": "+78462223344",
                "recipient_name": "ТК 'Башкирские товары'",
                "recipient_phone": "+73472223355",
                "driver_id": driver_users[2].id,
                "created_at": datetime.now() - timedelta(days=2)
            },
            # Выполненные заявки
            {
                "from_": "Ростов-на-Дону, ул. Большая Садовая, 10",
                "to": "Волгоград, проспект Ленина, 25",
                "weight": 950.5,
                "volume": 9.8,
                "cargo_content": "Перевозка мебели для офиса",
                "notes": "Мебель в упаковке, бережная погрузка",
                "declared_value": 180000.0,
                "status": ApplicationStatus.CONFIRMED,
                "sender_name": "ООО 'ОфисМебель'",
                "sender_phone": "+78632223344",
                "recipient_name": "ИП Семенов А.В.",
                "recipient_phone": "+78442223355",
                "driver_id": driver_users[3].id,
                "created_at": datetime.now() - timedelta(days=10),
                "completed_at": datetime.now() - timedelta(days=2)
            },
            {
                "from_": "Нижний Новгород, ул. Рождественская, 8",
                "to": "Воронеж, проспект Революции, 12",
                "weight": 1800.25,
                "volume": 14.2,
                "cargo_content": "Перевозка бытовой техники",
                "notes": "Холодильники и стиральные машины в заводской упаковке",
                "declared_value": 420000.0,
                "status": ApplicationStatus.COMPLETED,
                "sender_name": "ТК 'ТехноМир'",
                "sender_phone": "+78312223344",
                "recipient_name": "МВ 'ВоронежТехника'",
                "recipient_phone": "+74732223355",
                "driver_id": driver_users[4].id,
                "created_at": datetime.now() - timedelta(days=8),
                "completed_at": datetime.now() - timedelta(days=1)
            },
            # Отмененные заявки
            {
                "from_": "Тюмень, ул. Республики, 15",
                "to": "Омск, ул. Ленина, 30",
                "weight": 1300.0,
                "volume": 11.5,
                "cargo_content": "Перевозка химических реактивов",
                "notes": "Требуется специальное разрешение",
                "declared_value": 280000.0,
                "status": ApplicationStatus.CONFIRMED,
                "sender_name": "ООО 'ХимПром'",
                "sender_phone": "+78522223344",
                "recipient_name": "НПО 'ОмскХим'",
                "recipient_phone": "+73812223355",
                "driver_id": driver_users[0].id,
                "created_at": datetime.now() - timedelta(days=5),
                "cancelled_at": datetime.now() - timedelta(days=4)
            },
            # Заявки с разными характеристиками
            {
                "from_": "Владивосток, ул. Светланская, 20",
                "to": "Хабаровск, ул. Муравьева-Амурского, 15",
                "weight": 3200.0,
                "volume": 22.8,
                "cargo_content": "Перевозка автомобильных запчастей",
                "notes": "Крупная партия, срочная доставка",
                "declared_value": 650000.0,
                "status": ApplicationStatus.PROGRESS,
                "sender_name": "ООО 'ДальАвтоТрейд'",
                "sender_phone": "+79242223344",
                "recipient_name": "СТО 'ХабаровскАвто'",
                "recipient_phone": "+79422223355",
                "driver_id": driver_users[1].id,
                "created_at": datetime.now() - timedelta(days=1)
            },
            {
                "from_": "Калининград, Ленинский проспект, 10",
                "to": "Москва, шоссе Энтузиастов, 5",
                "weight": 750.5,
                "volume": 7.2,
                "cargo_content": "Перевозка медицинского оборудования",
                "notes": "Чувствительное оборудование, антистатическая упаковка",
                "declared_value": 1200000.0,
                "status": ApplicationStatus.NEW,
                "sender_name": "ООО 'МедТехника'",
                "sender_phone": "+79012223344",
                "recipient_name": "ГКБ №1",
                "recipient_phone": "+74952223355",
                "driver_id": driver_users[2].id,
                "created_at": datetime.now() - timedelta(hours=6)
            },
            {
                "from_": "Сочи, ул. Навагинская, 8",
                "to": "Краснодар, ул. Красная, 25",
                "weight": 550.0,
                "volume": 5.8,
                "cargo_content": "Перевозка товаров для магазина",
                "notes": "Мелкий опт, паллетирование",
                "declared_value": 85000.0,
                "status": ApplicationStatus.COMPLETED,
                "sender_name": "ИП Ковалев С.И.",
                "sender_phone": "+79182223344",
                "recipient_name": "Магазин 'Кубанские товары'",
                "recipient_phone": "+79612223355",
                "driver_id": driver_users[3].id,
                "created_at": datetime.now() - timedelta(days=7),
                "completed_at": datetime.now() - timedelta(days=3)
            }
        ]

        for app_data in applications_data:
            await applications_crud.create_application(session, ApplicationCreate(**app_data))

        print("Тестовые данные успешно созданы!")
        print(f"Создано:")
        print(f"- 2 менеджера")
        print(f"- 2 администратора")
        print(f"- 6 водителей (4 активных, 2 неактивных)")
        print(f"- 3 клиента")
        print(f"- 10 заявок с разными статусами")