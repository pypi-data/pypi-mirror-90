from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .user import User

__all__ = ("Guild", "Leaderboard", "Sort")


class Guild(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    owner_id: str
    member_count: int
    symbol: str


class Sort(Enum):
    Cash = "cash"
    Bank = "bank"
    Total = "total"


class Leaderboard(BaseModel):
    users: List[User]
    total_pages: Optional[int] = None

    @classmethod
    def parse_obj(cls, obj: Any) -> Leaderboard:  # type: ignore
        if not isinstance(obj, Dict):
            obj = {"users": obj}
        return super().parse_obj(obj)
