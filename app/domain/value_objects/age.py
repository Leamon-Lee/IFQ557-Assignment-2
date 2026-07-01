from dataclasses import dataclass


@dataclass(frozen=True)
class Age:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("Age must be an integer")
        if not 0 <= self.value <= 100:
            raise ValueError("Age must be between 0 and 100")

    def __int__(self) -> int:
        return self.value
