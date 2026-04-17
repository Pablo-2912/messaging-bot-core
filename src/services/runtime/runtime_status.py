from src.services.event.eventService import EventService
from src.infra.events.event_listener import EventListener
from src.infra.events.event_writer import EventWriter

class RuntimeSatus:
    
    def __init__(self, event_writer: EventWriter, event_listener: EventListener, event_service: EventService | None = None):
        
        if event_service is None:
            event_service = EventService(writer=event_writer,listener=event_listener)
            
        self.event_service = event_service
        self.event_writer = event_writer
        self.event_listener = event_listener
    
    def get_status():
        
          
        
        pass