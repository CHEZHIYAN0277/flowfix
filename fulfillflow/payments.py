from dataclasses import dataclass, field

from .errors import RefundFailed


@dataclass
class PaymentGateway:
    rejected_refunds: set[str] = field(default_factory=set)
    refunded: set[str] = field(default_factory=set)

    def refund(self, payment_id: str) -> None:
        if payment_id in self.rejected_refunds:
            raise RefundFailed(f"refund rejected for {payment_id}")
        self.refunded.add(payment_id)
