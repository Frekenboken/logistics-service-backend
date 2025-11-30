from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime, UTC

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    DRIVER = "driver"
    MANAGER = "manager"
    USER = "user"

class ApplicationStatus(str, Enum):
    NEW = "new"
    CONFIRMED = "confirmed"
    PROGRESS = "progress"
    COMPLETED = "completed"



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
    cargo_content = Column(Text, nullable=False)
    notes = Column(Text, default='Замечаний нет.')
    declared_value = Column(Float, nullable=False)
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.NEW)

    # Контактная информация
    sender_name = Column(String, nullable=False)
    sender_phone = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    recipient_phone = Column(String, nullable=False)

    # Временные поля
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False)

    departure_time = Column(DateTime, nullable=True)
    estimated_delivery_time = Column(DateTime, nullable=True)
    actual_delivery_time = Column(DateTime, nullable=True)

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
