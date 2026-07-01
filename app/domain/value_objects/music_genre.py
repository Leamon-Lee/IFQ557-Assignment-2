from dataclasses import dataclass
import re


@dataclass(frozen=True)
class MusicGenre:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 80:
            raise ValueError("Music genre must be 1 to 80 characters")
        if not re.fullmatch(r"[A-Za-z][A-Za-z -]*", self.value):
            raise ValueError("Music genre can only contain English letters, spaces, and hyphens")

    def __eq__(self, other):
        if isinstance(other, MusicGenre):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return NotImplemented

    def __hash__(self):
        return hash(self.value)

    def __str__(self) -> str:
        return self.value
