from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_session
from src.crud import application as application_crud
from src.schemas.application import ApplicationCreate, ApplicationRead, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationRead)
async def create_application(application: ApplicationCreate, session: AsyncSession = Depends(get_session)):
    return await application_crud.create_application(session, application)


@router.get("/{application_id}", response_model=ApplicationRead)
async def read_application(application_id: int, session: AsyncSession = Depends(get_session)):
    db_application = await application_crud.get_application(session, application_id)
    if db_application is None:
        raise HTTPException(404, "Not found")
    return db_application


@router.get("/", response_model=list[ApplicationRead])
async def read_applications(session: AsyncSession = Depends(get_session)):
    db_applications = await application_crud.get_applications(session)
    if db_applications is None:
        raise HTTPException(404, "Not found")
    return db_applications


@router.delete("/{application_id}", response_model=ApplicationRead)
async def delete_application(application_id: int, session: AsyncSession = Depends(get_session)):
    db_application = await application_crud.delete_application(session, application_id)
    if db_application is None:
        raise HTTPException(404, "Not found")
    return db_application


@router.put("/{application_id}", response_model=ApplicationRead)
async def update_application(application_id: int, updates: ApplicationUpdate, session: AsyncSession = Depends(get_session)):
    db_application = await application_crud.update_application(session, application_id, updates)
    if db_application is None:
        raise HTTPException(404, "Not found")
    return db_application
