from dataclasses import dataclass


@dataclass(frozen=True)
class AgeRestriction:
    value: int

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 100:
            raise ValueError("Age restriction must be between 0 and 100")

    def __int__(self) -> int:
        return self.value
