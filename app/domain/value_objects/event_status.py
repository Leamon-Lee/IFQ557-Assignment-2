from dataclasses import dataclass


@dataclass(frozen=True)
class EventStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("draft", "pending", "approved", "rejected", "published", "cancelled", "finished")
        if self.value not in allowed_values:
            raise ValueError(f"Event status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value
