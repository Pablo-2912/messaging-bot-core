import json
from pathlib import Path
import threading
from src.domain.enuns.events.bot_lifecycle_status import WorkerLifecycleStatus
from src.domain.enuns.events.bot_lifecycle_events import BotLifecycleEvent
from src.domain.entities.bot_event import BotEvent

class EventListener:

    def __init__(self, base_path: str = "events"):
        
        self.lock = threading.Lock()

    def get_last_lifecycle_event(self, event_type: BotLifecycleEvent):
        event_path = self._resolve_event_path(event_type)

        if not event_path.exists() or not event_path.is_dir():
            return None

        with self.lock:
            files = list(event_path.glob("*.jsonl"))

            if not files:
                return None

            # Arquivo mais recente
            latest_file = max(files, key=lambda f: f.stat().st_mtime)

            try:
                with latest_file.open("r", encoding="utf-8") as f:
                    last_line = None

                    for line in f:
                        line = line.strip()
                        if line:
                            last_line = line

                    if not last_line:
                        return None

                    payload = json.loads(last_line)
                    return BotEvent.from_dict(payload)

            except Exception:
                return None
    
    def _resolve_event_path(self, event_type: BotLifecycleEvent) -> Path:
        return self.base_path / event_type.value