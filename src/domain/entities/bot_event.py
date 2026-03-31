from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
import json
import uuid

@dataclass(frozen=True)
class BotEvent:
    id: uuid.UUID
    action: str
    timestamp: datetime
    version: str
    origin: str
    data: Dict[str, Any]

    @staticmethod
    def from_dict(payload: dict) -> BotEvent:
        try:
            return BotEvent(
                id=uuid.UUID(payload["id"]),
                action=payload["action"],
                timestamp=datetime.fromisoformat(payload["timestamp"]),
                version=payload["version"],
                origin=payload["origin"],
                data=payload.get("data", {})
            )
        except Exception as e:
            raise ValueError(f"Invalid payload for BotEvent: {e}")

    @staticmethod
    def from_json(json_str: str) -> BotEvent:
        try:
            payload = json.loads(json_str)
            return BotEvent.from_dict(payload)
        except Exception as e:
            raise ValueError("Invalid JSON for BotEvent") from e