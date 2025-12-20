import json
from pathlib import Path

from src.config.settings import Settings

def load_settings(path: str | Path) -> Settings:
    path = Path(path)

    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    return Settings.model_validate(data)
