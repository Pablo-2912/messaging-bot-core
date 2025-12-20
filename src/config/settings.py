from pydantic import BaseModel

class PlaywrightSettings(BaseModel):
    headless: bool = False

class WhatsAppSettings(BaseModel):
    base_url: str
    
class Settings(BaseModel):
    playwright: PlaywrightSettings
    whatsapp: WhatsAppSettings
    
