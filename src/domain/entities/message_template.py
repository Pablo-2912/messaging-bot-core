from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class MessageTemplate:
    id: str                 # ID interno estável (ex: "msg_default_reception")
    type: str               # Tipo lógico (ex: "reception", "followup")
    name: str               # Nome legível (UI / debug)
    parts: Sequence[str]    # Partes da mensagem (enviadas em sequência)
