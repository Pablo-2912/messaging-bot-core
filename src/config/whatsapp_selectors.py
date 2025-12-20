from pydantic import BaseModel, Field

class WhatsAppSelectors(BaseModel):
    qr_code_canvas: str = Field(alias="qrCodeCanvas")
    chat_list: str = Field(alias="chatList")

    chat_item: str | None = Field(default=None, alias="chatItem")
    chat_name: str | None = Field(default=None, alias="chatName")
    send_button: str | None = Field(default=None, alias="sendButton")
    chat_textbox: str | None = Field(default=None, alias="chatTextbox")
    unread_badge: str | None = Field(default=None, alias="unreadBadge")

    model_config = {
        "populate_by_name": True
    }
