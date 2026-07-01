from dataclasses import dataclass


@dataclass(frozen=True)
class TicketType:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("free", "standard", "vip")
        if self.value not in allowed_values:
            raise ValueError(f"Ticket type must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value
