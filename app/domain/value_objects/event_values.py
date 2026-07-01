from dataclasses import dataclass


@dataclass(frozen=True)
class EventTitle:
    value: str
    min_length: int = 1
    max_length: int = 100


@dataclass(frozen=True)
class Capacity:
    value: int
    min_value: int = 1


@dataclass(frozen=True)
class AgeRestriction:
    value: int
    min_value: int = 0
    max_value: int = 100


@dataclass(frozen=True)
class EventStatus:
    value: str
    allowed_values: tuple[str, ...] = (
        "draft",
        "pending",
        "approved",
        "rejected",
        "published",
        "cancelled",
        "finished",
    )
