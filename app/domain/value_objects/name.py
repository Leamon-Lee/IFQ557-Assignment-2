from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Name cannot be empty")
        if len(self.value) > 30:
            raise ValueError("Name cannot be longer than 30 characters")
        if not re.fullmatch(r"[A-Za-z]+", self.value):
            raise ValueError("Name can only contain English letters")

    def __str__(self) -> str:
        return self.value
