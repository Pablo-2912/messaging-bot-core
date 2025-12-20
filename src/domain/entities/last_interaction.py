from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LastInteraction:
    at: str                     # ISO 8601 datetime
    direction: str              # "inbound" | "outbound"
    sender: str                 # "auto" | "seller" | "contact"
    last_auto_message_id: Optional[str] = None
