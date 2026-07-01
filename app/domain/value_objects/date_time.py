from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class DateTime:
    value: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.value, datetime):
            raise TypeError("DateTime value must be a datetime object")

    def __str__(self) -> str:
        return self.value.isoformat()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.value, name)
