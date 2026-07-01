from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    value: Decimal

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Money must be greater than or equal to 0")

    def __str__(self) -> str:
        return str(self.value)
