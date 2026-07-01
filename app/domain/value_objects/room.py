from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 80:
            raise ValueError("Room must be 1 to 80 characters")
        if self.value.strip() != self.value:
            raise ValueError("Room cannot start or end with spaces")

    def __str__(self) -> str:
        return self.value
