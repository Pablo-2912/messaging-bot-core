from dataclasses import dataclass
from typing import Optional

from src.domain.entities.last_interaction import LastInteraction

@dataclass(frozen=True)
class Contact:
    id: str                     # ID interno estável (ex: "ct_001")
    name: str                   # Nome do contato
    number: str                 # Número do WhatsApp
    group_id: str               # Grupo ao qual o contato pertence
    note: Optional[str] = None  # Observação humana (CRM)
    last_interaction: Optional[LastInteraction] = None

