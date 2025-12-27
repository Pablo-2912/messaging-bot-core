import time
from src.config.settings import Settings
from src.infra.playwright.browser_manager import BrowserManager
from src.handlers.auth_whatsapp_handler import WhatsAppAuth
from src.domain.errors.whatsapp_auth_errors import WhatsAppAuthTimeoutError
from src.config.whatsapp_selectors import WhatsAppSelectors
from src.services.playwright.navigation import open_url
from src.domain.errors.playwright_errors import PlaywrightPageClosedError
from src.domain.errors.browser_errors import BrowserUnstableError

class BootstrapWhatsAppHandler:
    def __init__(self, settings: Settings, browser: BrowserManager, selectors: WhatsAppSelectors ):
        self.settings = settings
        self.browser = browser
        self.selectors = selectors

    def open_browser(self, headless):
       return self.browser.start(
            headless = headless
        )
    
    def _open_whatsapp(self, page) -> None:
        url_base = self.settings.whatsapp.base_url
        open_url(page=page, url=url_base)
    
    def _create_whatsapp_auth_instance(self, page) ->  WhatsAppAuth:
        return WhatsAppAuth(
            page=page,
            selectors=self.selectors,
        )
    
    def handle(self) -> BrowserManager:
        headless_config = self.settings.playwright.headless
        headless = headless_config

        max_retries = 5
        retry_count = 0

        while True:
            browser = self.open_browser(headless)
            page = browser.page

            try:
                self._open_whatsapp(page)
                whatsapp_auth = self._create_whatsapp_auth_instance(page)

                is_logged = whatsapp_auth.is_whatsapp_logged_in()

                # Precisa mostrar QR Code
                if not is_logged and headless:
                    browser.stop()
                    headless = False
                    continue

                # Está logado, mas modo errado
                if is_logged and headless != headless_config:
                    browser.stop()
                    headless = headless_config
                    continue

                # Sucesso: já logado
                if is_logged:
                    retry_count = 0  # 🔁 reset
                    return browser

                # Tentativa de autenticação
                whatsapp_auth.authenticate_whatsapp(timeout_seconds=120)

                retry_count = 0  # 🔁 reset
                return browser

            except PlaywrightPageClosedError:
                browser.stop()
                retry_count += 1

                if retry_count >= max_retries:
                    # Falha ambiental repetida → encerra
                    raise BrowserUnstableError(
                        f"Browser fechou {retry_count} vezes consecutivas. Encerrando serviço."
                    )

                # Pequeno backoff
                time.sleep(2)
                continue

            except WhatsAppAuthTimeoutError:
                browser.stop()
                # Erro determinístico → não adianta retry
                raise

            except Exception:
                browser.stop()
                raise

                
        
  
    
        

        
