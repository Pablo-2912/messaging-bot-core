from enum import Enum

class BotLifecycleEvent(Enum):
    START_REQUESTED = "start_requested"
    STOP_REQUESTED = "stop_requested"
    PAUSE_REQUESTED = "pause_requested"  
    