from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 255:
            raise ValueError("Address must be 1 to 255 characters")
        if self.value.strip() != self.value:
            raise ValueError("Address cannot start or end with spaces")

    def __str__(self) -> str:
        return self.value
