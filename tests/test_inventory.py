import pytest

from fulfillflow.errors import InsufficientStock
from fulfillflow.inventory import InventoryLedger


def test_reservation_reduces_available_stock():
    ledger = InventoryLedger(available={"SKU": 5})
    ledger.reserve("order-1", "SKU", 2)
    assert ledger.available["SKU"] == 3
    assert ledger.is_reserved("order-1")


def test_release_restores_available_stock():
    ledger = InventoryLedger(available={"SKU": 5})
    ledger.reserve("order-1", "SKU", 2)
    ledger.release("order-1")
    assert ledger.available["SKU"] == 5
    assert not ledger.is_reserved("order-1")


def test_release_is_idempotent_for_unknown_order():
    ledger = InventoryLedger(available={"SKU": 5})
    ledger.release("missing")
    assert ledger.available["SKU"] == 5


def test_reservation_rejects_insufficient_stock():
    ledger = InventoryLedger(available={"SKU": 1})
    with pytest.raises(InsufficientStock):
        ledger.reserve("order-1", "SKU", 2)


def test_reservation_rejects_non_positive_quantity():
    ledger = InventoryLedger(available={"SKU": 5})
    with pytest.raises(ValueError, match="positive"):
        ledger.reserve("order-1", "SKU", 0)
