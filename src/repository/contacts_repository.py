import json
from typing import Optional

from src.domain.entities.contact import Contact
from src.domain.entities.last_interaction import LastInteraction
from src.services.config.paths import get_config_root


class ContactsRepository:
    def __init__(self):
        config_root = get_config_root()
        self._path = config_root / "whatsapp" / "contacts" / "contacts.json"

    # -------------------------
    # Public API
    # -------------------------

    def get_all(self) -> list[Contact]:
        """
        Retorna todos os contatos configurados.
        Se o arquivo não existir ou estiver vazio, retorna lista vazia.
        """
        data = self._load()
        contacts: list[Contact] = []

        for _, raw in data.get("contacts", {}).items():
            contacts.append(self._parse_contact(raw))

        return contacts

    def get_by_id(self, contact_id: str) -> Optional[Contact]:
        """
        Retorna um contato pelo ID.
        """
        return next(
            (c for c in self.get_all() if c.id == contact_id),
            None,
        )

    def get_by_number(self, number: str) -> Optional[Contact]:
        """
        Retorna um contato pelo número de telefone.
        """
        return next(
            (c for c in self.get_all() if c.number == number),
            None,
        )
        
    def get_by_group_id(self, group_id: str) -> list[Contact]:
        return [
            c
            for c in self.get_all()
            if c.group_id == group_id
        ]

    def get_version(self) -> int:
        """
        Retorna a versão do arquivo de contatos.
        Se não existir, assume versão 1.
        """
        data = self._load()
        return data.get("version", 1)

    # -------------------------
    # Internal helpers
    # -------------------------

    def _parse_contact(self, raw: dict) -> Contact:
        last_interaction_raw = raw.get("last_interaction")

        last_interaction = None
        if last_interaction_raw:
            last_interaction = LastInteraction(
                at=last_interaction_raw["at"],
                direction=last_interaction_raw["direction"],
                sender=last_interaction_raw["sender"],
                last_auto_message_id=last_interaction_raw.get(
                    "last_auto_message_id"
                ),
            )

        return Contact(
            id=raw["id"],
            name=raw["name"],
            number=raw["number"],
            group_id=raw["group_id"],
            note=raw.get("note"),
            last_interaction=last_interaction,
        )

    def _load(self) -> dict:
        """
        Carrega o JSON de contatos.
        - Arquivo inexistente → retorna dict vazio
        - JSON inválido → exception (estado corrupto)
        """
        if not self._path.exists():
            return {}

        with self._path.open("r", encoding="utf-8") as f:
            return json.load(f)
