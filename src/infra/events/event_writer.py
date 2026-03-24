import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
import threading
from domain.enuns.events.bot_whatsapp_events import WhatsappEvents

class EventWriter:

    def __init__(self, base_path: str = "events"):
        self.base_path = Path(base_path)
        self.lock = threading.Lock()

    def publish(self, event_type: WhatsappEvents, payload: dict, source: str):

        event = {
            "id": f"evt_{uuid.uuid4().hex[:8]}",
            "type": event_type.value,
            "source": source,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        date = datetime.now().strftime("%Y-%m-%d")

        event_dir = self.base_path / event_type.value
        event_dir.mkdir(parents=True, exist_ok=True)

        file_path = event_dir / f"{date}.jsonl"

        line = json.dumps(event, ensure_ascii=False)

        with self.lock:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

        return event