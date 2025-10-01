from pydantic import BaseModel, ConfigDict

from src.schemas.application import ApplicationRead


class DriverBase(BaseModel):
    user_id: int


class DriverCreate(DriverBase):
    pass


class DriverRead(DriverBase):
    model_config = ConfigDict(from_attributes=True)


class DriverReadWithApplications(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    applications: list[ApplicationRead]


class DriverUpdate(DriverBase):
    name: str | None = None
