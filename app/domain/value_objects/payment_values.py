from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    value: Decimal
    min_value: int = 0


@dataclass(frozen=True)
class PaymentMethod:
    value: str
    allowed_values: tuple[str, ...] = ("card", "paypal", "bank_transfer", "free")


@dataclass(frozen=True)
class PaymentStatus:
    value: str
    allowed_values: tuple[str, ...] = ("pending", "paid", "refunded", "failed")
