from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Nickname:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 50:
            raise ValueError("Nickname must be 1 to 50 characters")
        if not re.fullmatch(r"[A-Za-z0-9_]+", self.value):
            raise ValueError("Nickname can only contain English letters, numbers, and underscores")

    def __str__(self) -> str:
        return self.value
