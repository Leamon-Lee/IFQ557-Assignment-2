from dataclasses import dataclass


@dataclass(frozen=True)
class RegistrationStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("pending", "confirmed", "cancelled")
        if self.value not in allowed_values:
            raise ValueError(f"Registration status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value
