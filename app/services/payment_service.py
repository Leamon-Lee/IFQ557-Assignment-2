from decimal import Decimal


class PaymentService:
    def pay(self, registration_id: int, amount: Decimal, payment_method: str) -> int:
        return

    def refund(self, payment_id: int) -> bool:
        return

    def verifyPayment(self, payment_id: int) -> bool:
        return
