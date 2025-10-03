from pydantic import BaseModel, ConfigDict

from src.models import UserRole
from src.schemas.application import ApplicationRead
from src.schemas.user import UserBase


class DriverBase(BaseModel):
    user_id: int
    phone: str
    car: str
    is_active: bool


class DriverCreate(DriverBase):
    pass


class DriverRead(DriverBase):
    model_config = ConfigDict(from_attributes=True)


class DriverReadWithApplications(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    applications: list[ApplicationRead]


class UserDriverRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRole
    driver: DriverReadWithApplications


class DriverUpdate(DriverBase):
    name: str | None = None
