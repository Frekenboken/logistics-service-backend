from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import User
from src.schemas.user import UserCreate, UserRead, UserUpdate

from src.auth.hashing import get_password_hash


async def create_user(session: AsyncSession, user_in: UserCreate) -> User | None:
    driver = User(email=user_in.email,
                  firstname=user_in.firstname,
                  lastname=user_in.lastname,
                  hashed_password=get_password_hash(user_in.password))
    session.add(driver)
    await session.commit()
    await session.refresh(driver)
    return driver


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()


async def delete_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    await session.delete(user)
    await session.commit()
    return user


async def update_user(session: AsyncSession, user_id: int, updates: UserUpdate) -> User | None:
    user = await get_user(session, user_id)
    if not user:
        return None
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return user
