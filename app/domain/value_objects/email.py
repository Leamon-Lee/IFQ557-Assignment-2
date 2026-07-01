from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not 3 <= len(self.value) <= 120:
            raise ValueError("Email must be 3 to 120 characters")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", self.value):
            raise ValueError("Email format is invalid")

    def __str__(self) -> str:
        return self.value
