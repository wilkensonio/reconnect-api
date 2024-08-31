from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel, ConfigDict, Field


class CommonBaseModel(BaseModel):
    # Shared configuration for all models
    Config: ClassVar = ConfigDict(from_attributes=True)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True
