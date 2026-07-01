from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ContactNumber:
    value: str

    def __post_init__(self) -> None:
        if not 1 <= len(self.value) <= 20:
            raise ValueError("Contact number must be 1 to 20 characters")
        if not re.fullmatch(r"\+?[0-9][0-9 -]*", self.value):
            raise ValueError("Contact number can only contain digits, spaces, hyphens, and an optional leading plus")
        if "  " in self.value:
            raise ValueError("Contact number cannot contain consecutive spaces")

    def __str__(self) -> str:
        return self.value
