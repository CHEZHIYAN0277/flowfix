# Failed refunds corrupt reservation state

## Bug report

Cancelling a confirmed order calls the inventory release operation before the
payment refund is known to have succeeded. If the payment gateway rejects the
refund, `cancel_order` raises `RefundFailed`, but the inventory reservation has
already been removed.

## Expected behavior

The cancellation should behave atomically from the caller's perspective. When
the refund fails, the order must remain confirmed and its inventory must remain
reserved. Only a successful refund may release inventory and mark the order as
cancelled.

## Reproduction

```bash
python -m pytest -q tests/test_cancellation.py::test_failed_refund_preserves_order_and_reservation
```
