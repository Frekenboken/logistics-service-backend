from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.models import ApplicationStatus

class ApplicationBase(BaseModel):
    from_: str
    to: str
    weight: float
    volume: float
    cargo_content: str
    notes: str | None
    declared_value: float
    status: ApplicationStatus = ApplicationStatus.NEW
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    driver_id: int | None = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    departure_time: datetime | None = None
    estimated_delivery_time: datetime | None = None
    actual_delivery_time: datetime | None = None

class ApplicationUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    from_: str | None = None
    to: str | None = None
    weight: float | None = None
    volume: float | None = None
    cargo_content: str | None = None
    notes: str | None = None
    declared_value: float | None = None
    status: ApplicationStatus | None = None
    sender_name: str | None = None
    sender_phone: str | None = None
    recipient_name: str | None = None
    recipient_phone: str | None = None
    driver_id: int | None = None
    departure_time: datetime | None = None
    estimated_delivery_time: datetime | None = None
    actual_delivery_time: datetime | None = None