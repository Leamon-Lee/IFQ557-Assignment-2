from dataclasses import dataclass

from app.domain.value_objects.age import Age


@dataclass(frozen=True)
class AgeRestriction:
    value: int

    def __post_init__(self) -> None:
        Age(self.value)

    def __int__(self) -> int:
        return self.value
