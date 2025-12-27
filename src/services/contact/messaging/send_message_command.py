from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class SendMessageCommand:
    """
    Intenção de enviar uma mensagem para um contato.
    A mensagem é composta por múltiplas partes (parts),
    que serão enviadas em sequência pelo canal.
    """
    
    number: str | None
    name: str
    parts: Sequence[str]
    
