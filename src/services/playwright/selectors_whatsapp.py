from src.config.whatsapp_selectors import WhatsAppSelectors
from typing import List, Optional


def send_button(selectors: WhatsAppSelectors) -> Optional[List[str]]:
    return selectors.send_button


def chat_textbox(selectors: WhatsAppSelectors) -> Optional[List[str]]:
    return selectors.chat_textbox


def qr_code(selectors: WhatsAppSelectors) -> List[str]:
    return selectors.qr_code_canvas


def chat_list(selectors: WhatsAppSelectors) -> List[str]:
    return selectors.chat_list


def chat_item(selectors: WhatsAppSelectors) -> Optional[List[str]]:
    return selectors.chat_item


def unread_badge(selectors: WhatsAppSelectors) -> Optional[List[str]]:
    return selectors.unread_badge


def chat_name(selectors: WhatsAppSelectors) -> Optional[List[str]]:
    return selectors.chat_name
