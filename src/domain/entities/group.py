from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Group:
    id: str                     # ID interno estável (ex: "grp_blacklist")
    name: str                   # Nome do grupo (chave legível no JSON / UI)
    type: str                   # "blacklist", "default", etc
    message_group_id: Optional[str]  # Grupo de mensagens associado (None p/ blacklist)
