from pydantic import BaseModel, ConfigDict

from backend.src.schemas.application import ApplicationRead


class DriverBase(BaseModel):
    name: str
    email: str


class DriverCreate(DriverBase):
    pass


class DriverRead(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class DriverReadWithApplications(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    applications: list[ApplicationRead]


class DriverUpdate(DriverBase):
    name: str | None = None
    email: str | None = None
