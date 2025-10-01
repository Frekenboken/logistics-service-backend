from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    DRIVER = "driver"
    MANAGER = "manager"
    USER = "user"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    hashed_password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    driver_id = Column(Integer, ForeignKey("drivers.user_id"))

    # Обратная ссылка
    driver = relationship("Driver", back_populates="applications")


class Driver(Base):
    __tablename__ = "drivers"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)

    # Отношение один ко многим
    applications = relationship("Application", back_populates="driver")
