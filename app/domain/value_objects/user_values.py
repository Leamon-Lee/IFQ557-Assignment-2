from dataclasses import dataclass
from re import Pattern, compile


@dataclass(frozen=True)
class Nickname:
    value: str
    min_length: int = 1
    max_length: int = 50
    pattern: Pattern[str] = compile(r"^[A-Za-z0-9_]+$")


@dataclass(frozen=True)
class Email:
    value: str
    pattern: Pattern[str] = compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
