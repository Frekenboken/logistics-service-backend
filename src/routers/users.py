from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_session
from src.crud import user as user_crud
from src.schemas.user import UserCreate, UserRead, UserUpdate

from src.auth.security import security

router = APIRouter(prefix="/users", tags=["users"])


# @router.post("/", response_model=UserRead)
# async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
#     return await user_crud.create_user(session, user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    db_user = await user_crud.get_user(session, user_id)
    if db_user is None:
        raise HTTPException(404, "Not found")
    return db_user

# , dependencies=[Depends(security.access_token_required)]
@router.get("/", response_model=list[UserRead])
async def read_users(session: AsyncSession = Depends(get_session)):
    db_users = await user_crud.get_users(session)
    if db_users is None:
        raise HTTPException(404, "Not found")
    return db_users


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    db_user = await user_crud.delete_user(session, user_id)
    if db_user is None:
        raise HTTPException(404, "Not found")
    return db_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, updates: UserUpdate, session: AsyncSession = Depends(get_session)):
    db_user = await user_crud.update_user(session, user_id, updates)
    if db_user is None:
        raise HTTPException(404, "Not found")
    return db_user
