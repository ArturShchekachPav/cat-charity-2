from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    model_config = ConfigDict(extra="forbid")


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    full_amount: Optional[PositiveInt] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("name", "description", "full_amount")
    @classmethod
    def fields_cannot_be_null(cls, value):
        if value is None:
            error = "Поле не может быть null при обновлении!"
            raise ValueError(error)
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
