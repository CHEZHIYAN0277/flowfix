import pytest

from fulfillflow.audit import AuditLog
from fulfillflow.inventory import InventoryLedger
from fulfillflow.models import Order
from fulfillflow.orders import OrderService
from fulfillflow.payments import PaymentGateway


@pytest.fixture
def workflow():
    inventory = InventoryLedger(available={"LAMP-01": 8})
    payments = PaymentGateway()
    audit = AuditLog()
    service = OrderService(inventory, payments, audit)
    order = Order(
        id="order-1001",
        sku="LAMP-01",
        quantity=2,
        payment_id="payment-1001",
    )
    return service, inventory, payments, audit, order
