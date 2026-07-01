from dataclasses import dataclass


@dataclass(frozen=True)
class CheckInStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("not_checked_in", "checked_in")
        if self.value not in allowed_values:
            raise ValueError(f"Check-in status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value
