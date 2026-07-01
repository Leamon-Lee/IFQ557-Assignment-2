from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordHash:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Password hash cannot be empty")
        if len(self.value) > 255:
            raise ValueError("Password hash cannot be longer than 255 characters")

    def __str__(self) -> str:
        return self.value
