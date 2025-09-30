from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    # Отношение один ко многим
    applications = relationship("Application", back_populates="driver")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    driver_id = Column(Integer, ForeignKey("drivers.id"))

    # Обратная ссылка
    driver = relationship("Driver", back_populates="applications")

