from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_session
from src.crud import driver as driver_crud
from src.schemas.driver import DriverCreate, DriverRead, DriverReadWithApplications, UserDriverRead
from src.schemas.user import UserRead

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverRead)
async def create_driver(driver: DriverCreate, session: AsyncSession = Depends(get_session)):
    return await driver_crud.create_driver(session, driver)


@router.get("/{driver_id}", response_model=DriverReadWithApplications)
async def read_driver(driver_id: int, session: AsyncSession = Depends(get_session)):
    db_driver = await driver_crud.get_driver_with_applications(session, driver_id)
    if db_driver is None:
        raise HTTPException(404, "Not found")
    return db_driver


@router.get("/", response_model=list[UserDriverRead])
async def read_drivers(session: AsyncSession = Depends(get_session)):
    drivers = await driver_crud.get_drivers_with_applications(session)
    if drivers is None:
        raise HTTPException(404, "Not found")
    print(drivers)
    return drivers
