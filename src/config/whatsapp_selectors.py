from pydantic import BaseModel, Field
from typing import List, Optional


class WhatsAppSelectors(BaseModel):
    qr_code_canvas: List[str] = Field(alias="qrCodeCanvas")
    chat_list: List[str] = Field(alias="chatList")

    chat_item: Optional[List[str]] = Field(default=None, alias="chatItem")
    chat_name: Optional[List[str]] = Field(default=None, alias="chatName")
    send_button: Optional[List[str]] = Field(default=None, alias="sendButton")
    chat_textbox: Optional[List[str]] = Field(default=None, alias="chatTextbox")
    unread_badge: Optional[List[str]] = Field(default=None, alias="unreadBadge")

    model_config = {
        "populate_by_name": True
    }
