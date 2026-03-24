# src/services/config/paths.py
import os
from pathlib import Path

def get_config_root() -> Path:
    env_path = os.getenv("BOT_CONFIG_PATH")
    if env_path:
        return Path(env_path)

    raise RuntimeError(
        "BOT_CONFIG_PATH não definido. "
        "Configure a variável de ambiente apontando para bot-config/config"
    )
 