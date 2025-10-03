from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Enum as SQLEnum
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

    driver = relationship("Driver", back_populates="user", uselist=False)

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    from_ = Column('from', String, nullable=False)
    to = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    description = Column(String)
    driver_id = Column(Integer, ForeignKey("drivers.user_id"))

    # Обратная ссылка
    driver = relationship("Driver", back_populates="applications")


class Driver(Base):
    __tablename__ = "drivers"

    phone = Column(String, index=True)
    car = Column(String, index=True)
    is_active = Column(Boolean, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    user = relationship("User", back_populates="driver")

    # Отношение один ко многим
    applications = relationship("Application", back_populates="driver")
