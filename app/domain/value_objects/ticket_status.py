from dataclasses import dataclass


@dataclass(frozen=True)
class TicketStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("valid", "cancelled", "used")
        if self.value not in allowed_values:
            raise ValueError(f"Ticket status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value
