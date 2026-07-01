from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Capacity:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("Capacity must be an integer")
        if self.value <= 0:
            raise ValueError("Capacity must be greater than 0")
        if self.value > 100000:
            raise ValueError("Capacity cannot be greater than 100000")

    def __int__(self) -> int:
        return self.value

    def __index__(self) -> int:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Capacity):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return False

    def __lt__(self, other: Any) -> bool:
        return self.value < int(other)

    def __le__(self, other: Any) -> bool:
        return self.value <= int(other)

    def __gt__(self, other: Any) -> bool:
        return self.value > int(other)

    def __ge__(self, other: Any) -> bool:
        return self.value >= int(other)

    def __sub__(self, other: Any) -> int:
        return self.value - int(other)

    def __rsub__(self, other: Any) -> int:
        return int(other) - self.value

    def __str__(self) -> str:
        return str(self.value)
