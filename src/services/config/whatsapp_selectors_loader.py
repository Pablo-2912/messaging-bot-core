from pathlib import Path
from src.config.whatsapp_selectors import WhatsAppSelectors

def load_whatsapp_selectors(path: Path) -> WhatsAppSelectors:
    with path.open(encoding="utf-8") as f:
        return WhatsAppSelectors.model_validate_json(f.read())