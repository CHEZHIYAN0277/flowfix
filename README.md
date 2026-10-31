# FulfillFlow Recovery Fixture

FulfillFlow is a small order-management service used to demonstrate how an
autonomous repair system handles a failure that crosses module boundaries.

## Reported issue

When a customer cancels a confirmed order and the payment gateway rejects the
refund, the cancellation must fail without changing the order or its reserved
inventory. Currently, the inventory is released before the refund is attempted,
so a failed refund leaves the order confirmed but its stock available for sale.

### Acceptance criteria

- A failed refund raises `RefundFailed`.
- The order remains `CONFIRMED`.
- The order's inventory remains reserved.
- A successful refund still cancels the order and releases its inventory.
- Existing checkout, inventory, and payment behavior must continue to pass.

## Run the reproduction

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The repository intentionally contains one failing test:

```text
tests/test_cancellation.py::test_failed_refund_preserves_order_and_reservation
```

This is a controlled evaluation fixture. The bug in `fulfillflow/orders.py` is
intentional and should remain present until a repair system changes it.
