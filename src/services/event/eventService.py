from src.domain.enuns.events.bot_whatsapp_events import WhatsappEvents
from src.infra.events.event_writer import EventWriter

from src.services.contact.messaging.send_message_command import SendMessageCommand

class EventService:

    def __init__(self, writer: EventWriter):
        self.writer = writer

    def chat_opened(self, number: str, name: str = ""):
        self._publish_contact_event(
            event_type=WhatsappEvents.CHAT_OPENED,
            number=number,
            name=name
        )

    def message_sent(self, command: SendMessageCommand):
        self._publish_event(
            event_type=WhatsappEvents.MESSAGE_SENT,
            payload=command.to_dict()
        )

    def message_viewed(self, number: str, name: str = ""):
        self._publish_contact_event(
            event_type=WhatsappEvents.MESSAGE_VIEWED,
            number=number,
            name=name
        )

    def media_sent(self, payload: dict | None = None):
        self._publish_event(
            event_type=WhatsappEvents.MEDIA_SENT,
            payload=payload or {}
        )

    def chat_closed(self, number: str, name: str = ""):
        self._publish_contact_event(
            event_type=WhatsappEvents.CHAT_CLOSED,
            number=number,
            name=name
        )

    def _publish_contact_event(self, event_type: WhatsappEvents, number: str, name: str):
        payload = {
            "number": number,
            "name": name
        }
        self._publish_event(event_type, payload)

    def _publish_event(self, event_type: WhatsappEvents, payload: dict):
        self.writer.publish(
            event_type=event_type,
            payload=payload,
            source=event_type.value 
        )