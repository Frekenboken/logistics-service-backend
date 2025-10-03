from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    from_: str
    to: str
    weight: float
    volume: float
    description: str
    driver_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ApplicationUpdate(ApplicationBase):
    from_: str | None = None
    to: str | None = None
    weight: float | None = None
    volume: float | None = None
    description: str | None = None
    driver_id: int | None = None
