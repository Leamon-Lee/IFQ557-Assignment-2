from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PaymentStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("pending", "paid", "refunded", "failed", "Pending", "Paid", "Refunded", "Failed")
        if self.value not in allowed_values:
            raise ValueError(f"Payment status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, PaymentStatus):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
