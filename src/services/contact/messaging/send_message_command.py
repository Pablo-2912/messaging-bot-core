from dataclasses import dataclass
from typing import Sequence
from src.domain.entities.message_template import MessageTemplate
@dataclass(frozen=True)
class SendMessageCommand:
    """
    Intenção de enviar uma mensagem para um contato.
    A mensagem é composta por múltiplas partes (parts),
    que serão enviadas em sequência pelo canal.
    """
    
    number: str | None 
    name: str
    message_template : MessageTemplate
    
    def to_dict(self) -> dict:
        return {
            "contact": {
                "name": self.name,
                "number": self.number,
            },
            "message": self.message_template.to_dict(),
        }
    

    
