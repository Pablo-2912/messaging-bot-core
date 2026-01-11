from src.infra.playwright.browser_manager import BrowserManager
from src.config.settings import Settings
from src.config.whatsapp_selectors import WhatsAppSelectors
from src.services.whatsapp.chat_list import get_unread_chats
from src.domain.errors.errors_base import TimeoutError
from src.handlers.chat_processing_handler import process_unread_chats
from src.domain.entities.contact import Contact
from src.handlers.chat_processing_handler import build_responses
from src.handlers.message_delivery_handler import deliver_message_to_chats
class WhatsAppRuntime:
    def __init__(
        self,
        browser: BrowserManager,
        settings: Settings,
        selectors: WhatsAppSelectors,
    ):
        self.browser = browser
        self.settings = settings
        self.selectors = selectors

        self.running = False
        self.page = browser.page

    def start(self) -> None:
        self.running = True
        self._run_loop()

    def stop(self) -> None:
        self.running = False
        self.browser.stop()

    def _get_unread_chats(self) -> list[str]:
        retries = 0
        max_retries = 1

        while True:
            try:
                #TODO : Tirar depois
                #return ["Pai"]
                
                return get_unread_chats(
                    page=self.browser.page,
                    selectors=self.selectors,
                    timeout=300,
                )

            except TimeoutError as e:
                retries += 1

                if retries > max_retries:
                    # abandona este ciclo
                    return []

    def _proccess_unread_chats(self, unread_chats : list[str] ) -> list[str]:
        
        #Chama metodo que separa os chats que devem ser respondidos dos que não devem
        contacts : Contact = process_unread_chats(chat_identifiers=unread_chats)
        return contacts

    def _send_responses_to_contacts(self, contacts : list[Contact]) -> None:
        
        if not contacts:
            return
        
        # Cria o command 
        responses = build_responses(contacts=contacts)
        
        deliver_message_to_chats(self.page, responses, selectors=self.selectors)

    def _run_loop(self) -> None: 
           while self.running:
            
            unread_contacts : list[Contact] = []
            
            # Pega as mensagens não lidas
            unread_chats = self._get_unread_chats()
            
            if unread_chats:
                unread_contacts = self._proccess_unread_chats(unread_chats)
            
            # TODO: Responder chats
            self. _send_responses_to_contacts(unread_contacts)
                
            # TODO: sleep curto
            
            
            
    