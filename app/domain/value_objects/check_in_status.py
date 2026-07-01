from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CheckInStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("not_checked_in", "checked_in", "NotCheckedIn", "CheckedIn")
        if self.value not in allowed_values:
            raise ValueError(f"Check-in status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CheckInStatus):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
