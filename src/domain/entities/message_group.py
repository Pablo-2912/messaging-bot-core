from dataclasses import dataclass
from typing import Sequence

from src.domain.entities.message_template import MessageTemplate

@dataclass(frozen=True)
class MessageGroup:
    id: str                             # ID interno estável (ex: "msg_grp_default")
    name: str                           # Nome legível do grupo
    messages: Sequence[MessageTemplate]  # Mensagens pertencentes ao grupo
