from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentStatus:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("pending", "paid", "refunded", "failed")
        if self.value not in allowed_values:
            raise ValueError(f"Payment status must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value
