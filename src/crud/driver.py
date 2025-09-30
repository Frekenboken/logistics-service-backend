from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.models import Application, Driver
from backend.src.schemas.driver import DriverCreate, DriverRead, DriverUpdate


async def create_driver(session: AsyncSession, driver_in: DriverCreate) -> Driver:
    driver = Driver(name=driver_in.name, email=driver_in.email)
    session.add(driver)
    await session.commit()
    await session.refresh(driver)
    return driver

async def get_driver_with_applications(session: AsyncSession, driver_id: int):
    result = await session.execute(
        select(Driver)
        .where(Driver.id == driver_id)
        .options(selectinload(Driver.applications))
    )
    driver = result.scalar_one_or_none()
    return driver