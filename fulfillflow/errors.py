class FulfillFlowError(Exception):
    """Base exception for the service."""


class InsufficientStock(FulfillFlowError):
    """Raised when an inventory reservation cannot be created."""


class InvalidOrderState(FulfillFlowError):
    """Raised when an operation is invalid for the current order state."""


class RefundFailed(FulfillFlowError):
    """Raised when the payment provider rejects a refund."""
