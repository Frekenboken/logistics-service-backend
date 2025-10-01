from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.core.db import get_session
from src.crud import user as user_crud

from src.auth.hashing import verify_password

from src.auth.security import security

from src.core.config import settings


class UserLogin(BaseModel):
    email: str
    password: str


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/")
async def login(credentials: UserLogin, response: Response, session: AsyncSession = Depends(get_session)):
    user = await user_crud.get_user_by_email(session, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(401, "Incorrct email or password")

    access_token = security.create_access_token(uid=str(user.id))
    response.set_cookie(security.config.JWT_ACCESS_COOKIE_NAME, access_token)
    return {"access_token": access_token}
