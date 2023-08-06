from typing import Optional

from pydantic import BaseModel, Field

from .number import Infinity, Number

__all__ = ("User",)


class User(BaseModel):
    """Representation of a Discord user."""

    id: int = Field(..., alias="user_id")
    cash: Number
    bank: Number
    rank: Optional[int] = None

    @property
    def total(self) -> Number:
        return self.cash + self.bank

    class Config:
        json_encoders = {Infinity: Infinity.__str__}
