from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RegistrationStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("pending", "confirmed", "cancelled", "Pending", "Confirmed", "Cancelled")
        if self.value not in allowed_values:
            raise ValueError(f"Registration status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RegistrationStatus):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
