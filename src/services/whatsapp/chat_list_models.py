from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ChatListScanResult:
    last_chat_name: str | None
    total_scrolled_px: int
    seen_chats: Optional[list[str]]

from enum import Enum

class ChatScrollDirection(Enum):
    VISIBLE = "visible"
    UP = "up"
    DOWN = "down"
    EMPTY = "empty"
