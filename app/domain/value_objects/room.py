from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Room cannot be empty")

    def __str__(self) -> str:
        return self.value
