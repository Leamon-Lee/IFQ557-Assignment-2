from dataclasses import dataclass


@dataclass(frozen=True)
class TicketStatus:
    value: str
    allowed_values: tuple[str, ...] = ("valid", "cancelled", "used")


@dataclass(frozen=True)
class TicketType:
    value: str
    allowed_values: tuple[str, ...] = ("free", "standard", "vip")
