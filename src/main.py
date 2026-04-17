from src.config.config import load_settings
from src.infra.playwright.browser_manager import BrowserManager
from src.handlers.bootstrap_whatsapp_handler import BootstrapWhatsAppHandler
from src.services.config.paths import get_config_root
from src.services.config.paths import get_event_root
from src.services.config.whatsapp_selectors_loader import load_whatsapp_selectors
from src.services.runtime.whatsapp_runtime import WhatsAppRuntime

from src.domain.errors.whatsapp_auth_errors import WhatsAppAuthTimeoutError
from src.domain.errors.browser_errors import BrowserUnstableError
from src.domain.errors.playwright_errors import PlaywrightBaseError

from src.infra.events.event_writer import EventWriter
from src.infra.events.event_listener import EventListener 
from src.services.runtime.runtime_status import RuntimeSatus

def main():
    try:
        # Pega configs
        config_root = get_config_root()
        event_root = get_event_root()
        settings = load_settings(config_root / "appsettings.json")

        # Inicializa serviços
        selectors = load_whatsapp_selectors(
            config_root / "whatsapp" / "whatsapp_selectors.json"
        )

        browser_manager = BrowserManager(
            user_data_dir="./session",
        )

        bootstrap = BootstrapWhatsAppHandler(
            settings=settings,
            browser=browser_manager,
            selectors=selectors
        )

        browser = bootstrap.handle()
        event_writer = EventWriter(event_root)
        event_listener = EventListener(event_root)
        
        runtime_status =  runtime_status ()
        
        whatsapp_runtime =  WhatsAppRuntime(
            selectors=selectors,
            settings=settings,
            browser=browser,
            event_writer=event_writer,
            event_listener=event_listener
        ) 
        
        # Inicia o bot
        whatsapp_runtime.start()

    except WhatsAppAuthTimeoutError:
        print("Login não realizado dentro do tempo limite. Serviço encerrado.")

    except BrowserUnstableError as e:
        print(f"Ambiente instável: {e}")

    except PlaywrightBaseError as e:
        print(f"Erro crítico do navegador: {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
