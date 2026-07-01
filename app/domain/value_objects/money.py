from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    value: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            raise TypeError("Money must be a Decimal")
        if self.value < 0:
            raise ValueError("Money must be greater than or equal to 0")
        if self.value.as_tuple().exponent < -2:
            raise ValueError("Money cannot have more than 2 decimal places")

    def __str__(self) -> str:
        return str(self.value)
