from dataclasses import dataclass
import re


@dataclass(frozen=True)
class City:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 80:
            raise ValueError("City must be 1 to 80 characters")
        if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", self.value):
            raise ValueError("City can only contain English letters, spaces, dots, apostrophes, and hyphens")

    def __str__(self) -> str:
        return self.value
