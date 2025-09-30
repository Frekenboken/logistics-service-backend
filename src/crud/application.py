from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.models import Application, Driver
from backend.src.schemas.application import ApplicationCreate, ApplicationRead, ApplicationUpdate


async def create_application(session: AsyncSession, application_in: ApplicationCreate) -> Application | None:
    result = await session.execute(
        select(Driver)
        .where(Driver.id == application_in.driver_id)
        .options(selectinload(Driver.applications))
    )
    driver = result.scalar_one_or_none()

    if driver:
        new_application = Application(name=application_in.name, description=application_in.description, driver_id=application_in.driver_id)
        driver.applications.append(new_application)
        await session.commit()
        return new_application
    return None


async def get_application(session: AsyncSession, application_id: int) -> Application | None:
    result = await session.execute(select(Application).where(Application.id == application_id))
    return result.scalar_one_or_none()


async def get_applications(session: AsyncSession):
    result = await session.execute(select(Application))
    return result.scalars().all()


async def delete_application(session: AsyncSession, application_id: int) -> Application | None:
    result = await session.execute(select(Application).where(Application.id == application_id))
    application = result.scalar_one_or_none()
    if not application:
        return None
    await session.delete(application)
    await session.commit()
    return application


async def update_application(session: AsyncSession, application_id: int, updates: ApplicationUpdate) -> Application | None:
    application = await get_application(session, application_id)
    if not application:
        return None
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(application, key, value)

    await session.commit()
    await session.refresh(application)

    return application
