from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ArtistType:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 80:
            raise ValueError("Artist type must be 1 to 80 characters")
        if not re.fullmatch(r"[A-Za-z][A-Za-z -]*", self.value):
            raise ValueError("Artist type can only contain English letters, spaces, and hyphens")

    def __str__(self) -> str:
        return self.value
