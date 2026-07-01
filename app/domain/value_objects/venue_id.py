from dataclasses import dataclass


@dataclass(frozen=True)
class VenueId:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("VenueId must be an integer")
        if self.value <= 0:
            raise ValueError("VenueId must be greater than 0")

    def __int__(self) -> int:
        return self.value
