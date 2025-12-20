from typing import Iterable
import json

from src.domain.entities.group import Group
from src.services.config.paths import get_config_root


class GroupsRepository:
    def __init__(self):
        config_root = get_config_root()
        self._path = config_root / "whatsapp" / "groups" / "groups.json"

    def get_all(self) -> list[Group]:
        data = self._load()

        return [
            Group(
                id=raw["id"],
                name=name,
                type=raw.get("type", "default"),
                message_group_id=raw.get("message_group"),
            )
            for name, raw in data.get("groups", {}).items()
        ]

    def get_by_id(self, group_id: str) -> Group | None:
        return next(
            (group for group in self.get_all() if group.id == group_id),
            None,
        )

    def get_by_ids(self, ids: Iterable[str]) -> list[Group]:
        ids_set = set(ids)
        if not ids_set:
            return []

        return [
            group
            for group in self.get_all()
            if group.id in ids_set
        ]

    def get_by_name(self, name: str) -> Group | None:
        return next(
            (group for group in self.get_all() if group.name == name),
            None,
        )

    def get_version(self) -> int:
        data = self._load()
        return data.get("version", 1)

    def _load(self) -> dict:
        if not self._path.exists():
            return {}

        with self._path.open("r", encoding="utf-8") as f:
            return json.load(f)
