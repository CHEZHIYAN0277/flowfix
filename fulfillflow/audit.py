from dataclasses import dataclass, field


@dataclass
class AuditLog:
    events: list[dict[str, str]] = field(default_factory=list)

    def record(self, event: str, order_id: str) -> None:
        self.events.append({"event": event, "order_id": order_id})
