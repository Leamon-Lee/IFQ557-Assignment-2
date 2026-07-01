from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentId:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("PaymentId must be an integer")
        if self.value <= 0:
            raise ValueError("PaymentId must be greater than 0")

    def __int__(self) -> int:
        return self.value
