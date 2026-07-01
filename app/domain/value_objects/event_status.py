from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EventStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = (
            "draft",
            "pending",
            "approved",
            "rejected",
            "published",
            "cancelled",
            "finished",
            "Open",
            "Cancelled",
            "Sold Out",
            "Inactive",
        )
        if self.value not in allowed_values:
            raise ValueError(f"Event status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EventStatus):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
