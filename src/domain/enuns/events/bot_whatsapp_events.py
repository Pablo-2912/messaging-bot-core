from enum import Enum

class WhatsappEvents(Enum):
    CHAT_OPENED = "chat_aberto"
    MESSAGE_SENT = "mensagem_enviada"
    MESSAGE_VIEWED = "mensagem_visualizada"
    MEDIA_SENT = "midia_enviada"
    CHAT_CLOSED = "chat_fechado"