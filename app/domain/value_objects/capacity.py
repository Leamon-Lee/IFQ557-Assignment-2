from dataclasses import dataclass


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
