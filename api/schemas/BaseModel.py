from pydantic import BaseModel, ConfigDict
from typing import ClassVar


class CommonBaseModel(BaseModel):
    # Shared configuration for all models
    Config: ClassVar = ConfigDict(from_attributes=True)

    # Example of a shared field, if needed
    created_at: str = "2024-01-01"

    class Config:
        # Example of common settings for all models
        anystr_strip_whitespace = True
        validate_assignment = True
