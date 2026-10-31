import pytest

from fulfillflow.errors import RefundFailed
from fulfillflow.models import OrderStatus


def test_successful_cancellation_refunds_and_releases_inventory(workflow):
    service, inventory, payments, audit, order = workflow
    service.confirm_order(order)

    service.cancel_order(order)

    assert order.status is OrderStatus.CANCELLED
    assert not inventory.is_reserved(order.id)
    assert inventory.available[order.sku] == 8
    assert order.payment_id in payments.refunded
    assert audit.events[-1] == {"event": "order_cancelled", "order_id": order.id}


def test_cancelled_order_cannot_be_cancelled_again(workflow):
    service, _, _, _, order = workflow
    service.confirm_order(order)
    service.cancel_order(order)
    with pytest.raises(Exception, match="only confirmed"):
        service.cancel_order(order)


def test_failed_refund_preserves_order_and_reservation(workflow):
    service, inventory, payments, audit, order = workflow
    service.confirm_order(order)
    payments.rejected_refunds.add(order.payment_id)

    with pytest.raises(RefundFailed):
        service.cancel_order(order)

    assert order.status is OrderStatus.CONFIRMED
    assert inventory.is_reserved(order.id)
    assert inventory.available[order.sku] == 6
    assert audit.events == [{"event": "order_confirmed", "order_id": order.id}]
