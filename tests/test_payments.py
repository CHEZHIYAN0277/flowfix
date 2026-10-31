import pytest

from fulfillflow.errors import RefundFailed
from fulfillflow.payments import PaymentGateway


def test_successful_refund_is_recorded():
    gateway = PaymentGateway()
    gateway.refund("payment-1")
    assert "payment-1" in gateway.refunded


def test_rejected_refund_raises_and_is_not_recorded():
    gateway = PaymentGateway(rejected_refunds={"payment-1"})
    with pytest.raises(RefundFailed):
        gateway.refund("payment-1")
    assert "payment-1" not in gateway.refunded
