from src.config.whatsapp_selectors import WhatsAppSelectors

def send_button(selectors: WhatsAppSelectors) -> str:
    return selectors.send_button


def chat_textbox(selectors: WhatsAppSelectors) -> str:
    return selectors.chat_textbox


def qr_code(selectors: WhatsAppSelectors) -> str:
    return selectors.qr_code_canvas


def chat_list(selectors: WhatsAppSelectors) -> str:
    return selectors.chat_list


def chat_item(selectors: WhatsAppSelectors) -> str:
    return selectors.chat_item


def unread_badge(selectors: WhatsAppSelectors) -> str:
    return selectors.unread_badge

def chat_name(selectors: WhatsAppSelectors) -> str:
    return selectors.chat_name
