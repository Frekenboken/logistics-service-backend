from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import Application, Driver, User, UserRole
from src.schemas.driver import DriverCreate, DriverRead, DriverUpdate


async def create_driver(session: AsyncSession, driver_in: DriverCreate) -> Driver | None:
    result = await session.execute(
        select(User)
        .where(User.id == driver_in.user_id)
        .options(selectinload(User.driver))
    )
    user = result.scalars().first()
    if not user or user.driver:
        return None

    # Создаём запись в Driver
    driver = Driver(**driver_in.model_dump())
    session.add(driver)

    # Меняем роль пользователя
    user.role = UserRole.DRIVER

    await session.commit()
    await session.refresh(user)

    return driver


async def get_driver_with_applications(session: AsyncSession, driver_id: int):
    result = await session.execute(
        select(Driver)
        .where(Driver.user_id == driver_id)
        .options(selectinload(Driver.applications))
    )
    driver = result.scalar_one_or_none()
    return driver


async def get_drivers_with_applications(session: AsyncSession):
    """
    Возвращает всех пользователей с ролью DRIVER вместе с их заявками.
    Использует selectinload для загрузки связей.
    """
    result = await session.execute(
        select(User)
        .where(User.role == UserRole.DRIVER)
        .options(
            selectinload(User.driver).selectinload(Driver.applications)
        )
    )
    users = result.scalars().all()
    return users
