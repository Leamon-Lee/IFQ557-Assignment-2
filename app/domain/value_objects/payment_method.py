from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentMethod:
    value: str

    def __post_init__(self) -> None:
        allowed_values = ("card", "paypal", "bank_transfer", "free")
        if self.value not in allowed_values:
            raise ValueError(f"Payment method must be one of: {', '.join(allowed_values)}")

    def __str__(self) -> str:
        return self.value
