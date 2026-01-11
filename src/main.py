from src.config.config import load_settings
from src.infra.playwright.browser_manager import BrowserManager
from src.handlers.bootstrap_whatsapp_handler import BootstrapWhatsAppHandler
from src.services.config.paths import get_config_root
from src.services.config.whatsapp_selectors_loader import load_whatsapp_selectors
from src.services.runtime.whatsapp_runtime import WhatsAppRuntime

from src.domain.errors.whatsapp_auth_errors import WhatsAppAuthTimeoutError
from src.domain.errors.browser_errors import BrowserUnstableError
from src.domain.errors.playwright_errors import PlaywrightBaseError


def main():
    try:
        config_root = get_config_root()
        settings = load_settings(config_root / "appsettings.json")

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

        whatsapp_runtime =  WhatsAppRuntime(
            selectors=selectors,
            settings=settings,
            browser=browser
        )
        
        # 👇 A PARTIR DAQUI entra o serviço
        # run_whatsapp_service(browser, settings, selectors)
        
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
