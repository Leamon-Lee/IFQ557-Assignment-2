from dataclasses import dataclass


@dataclass(frozen=True)
class VenueName:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Venue name cannot be empty")

    def __str__(self) -> str:
        return self.value
