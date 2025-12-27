from typing import Iterable
import json

from src.domain.entities.message_group import MessageGroup
from src.domain.entities.message_template import MessageTemplate
from src.services.config.paths import get_config_root


class MessageGroupsRepository:
    def __init__(self):
        config_root = get_config_root()
        self._path = config_root / "whatsapp" / "groups" / "groups_message.json"

    def get_all(self) -> list[MessageGroup]:
        data = self._load()

        return [
            MessageGroup(
                id=raw_group["id"],
                name=group_name, 
                messages=[
                    MessageTemplate(
                        id=raw_message["id"],
                        type=raw_message.get("type", "default"),
                        name=raw_message.get("name"),
                        parts=raw_message.get("parts", []),
                    )
                    for raw_message in raw_group.get("messages", [])
                ],
            )
            for group_name, raw_group
            in data.get("message_groups", {}).items()
        ]

    def get_by_id(self, group_id: str) -> MessageGroup | None:
        return next(
            (group for group in self.get_all() if group.id == group_id),
            None,
        )

    def get_by_ids(self, ids: Iterable[str]) -> list[MessageGroup]:
        ids_set = set(ids)
        if not ids_set:
            return []

        return [
            group
            for group in self.get_all()
            if group.id in ids_set
        ]

    def get_by_name(self, name: str) -> MessageGroup | None:
        return next(
            (group for group in self.get_all() if group.name == name),
            None,
        )

    def get_version(self) -> int:
        data = self._load()
        return data.get("version", 1)

    def _load(self) -> dict:
        if not self._path.exists():
            raise FileNotFoundError(f"Arquivo de config não encontrado: {self._path}")

        with self._path.open("r", encoding="utf-8") as f:
            return json.load(f)

