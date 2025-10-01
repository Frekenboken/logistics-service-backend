from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_session
from src.crud import driver as driver_crud
from src.schemas.driver import DriverCreate, DriverRead, DriverReadWithApplications

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverRead)
async def create_application(driver: DriverCreate, session: AsyncSession = Depends(get_session)):
    return await driver_crud.create_driver(session, driver)


@router.get("/{driver_id}", response_model=DriverReadWithApplications)
async def read_application(driver_id: int, session: AsyncSession = Depends(get_session)):
    db_driver = await driver_crud.get_driver_with_applications(session, driver_id)
    if db_driver is None:
        raise HTTPException(404, "Not found")
    return db_driver
