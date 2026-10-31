import pytest

from fulfillflow.errors import InvalidOrderState
from fulfillflow.models import OrderStatus


def test_confirm_order_reserves_inventory(workflow):
    service, inventory, _, _, order = workflow
    service.confirm_order(order)
    assert order.status is OrderStatus.CONFIRMED
    assert inventory.is_reserved(order.id)
    assert inventory.available[order.sku] == 6


def test_confirm_order_records_audit_event(workflow):
    service, _, _, audit, order = workflow
    service.confirm_order(order)
    assert audit.events == [{"event": "order_confirmed", "order_id": order.id}]


def test_confirmed_order_cannot_be_confirmed_again(workflow):
    service, _, _, _, order = workflow
    service.confirm_order(order)
    with pytest.raises(InvalidOrderState):
        service.confirm_order(order)


def test_pending_order_cannot_be_cancelled(workflow):
    service, _, _, _, order = workflow
    with pytest.raises(InvalidOrderState):
        service.cancel_order(order)
