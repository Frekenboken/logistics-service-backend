from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    name: str
    description: str | None = None
    driver_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ApplicationUpdate(ApplicationBase):
    name: str | None = None
    description: str | None = None
    driver_id: int | None = None
