import time

from playwright.sync_api import Page, Error as PlaywrightError

from src.services.playwright.selectors_whatsapp import qr_code, chat_list
from src.domain.errors.whatsapp_auth_errors import WhatsAppAuthTimeoutError
from src.domain.errors.playwright_errors import (
    translate_playwright_error,
)
from src.config.settings import Settings
from src.config.whatsapp_selectors import WhatsAppSelectors
from src.services.whatsapp.selector import resolve_selector


class WhatsAppAuth:
    def __init__(
        self,
        page: Page,
        selectors: WhatsAppSelectors,
    ) -> None:
        self.page = page

        self._qr_code_selector = resolve_selector(
            page,
            qr_code(selectors),
        )

        self._chat_list_selector = resolve_selector(
            page,
            chat_list(selectors),
        )

    def authenticate_whatsapp(self, timeout_seconds: int = 120) -> None:
        """
        Garante que o WhatsApp esteja autenticado.
        Pode levantar:
        - WhatsAppAuthTimeoutError
        - PlaywrightBaseError (browser/page fechado)
        """
        self._wait_for_whatsapp_initial_state(timeout_seconds)

        if not self._is_login_required():
            return

        self._wait_until_logged(timeout_seconds)
        self._wait_for_whatsapp_initial_state(120)

    def _wait_for_whatsapp_initial_state(self, timeout_seconds: int) -> None:
        """
        Aguarda o WhatsApp carregar o estado inicial:
        - Tela de QR Code
        - OU lista de chats
        """
        start = time.time()

        while True:
            try:
                if (
                    self.page.locator(self._qr_code_selector).count() > 0
                    or self.page.locator(self._chat_list_selector).count() > 0
                ):
                    return

            except PlaywrightError as e:
                raise translate_playwright_error(e)

            if time.time() - start > timeout_seconds:
                raise WhatsAppAuthTimeoutError(
                    "WhatsApp não carregou estado inicial (QR ou chat)"
                )

            time.sleep(0.5)


    def _is_login_required(self) -> bool:
        """
        Retorna True se o QR Code ainda estiver visível.
        """
        try:
            return self.page.locator(self._qr_code_selector).count() > 0
        except PlaywrightError as e:
            raise translate_playwright_error(e)


    def _wait_until_logged(self, timeout_seconds: int) -> None:
        """
        Aguarda até que o QR Code desapareça (login concluído).
        """
        start = time.time()

        while self._is_login_required():
            if time.time() - start > timeout_seconds:
                raise WhatsAppAuthTimeoutError(
                    f"Timeout ao aguardar login do WhatsApp ({timeout_seconds}s)"
                )

            time.sleep(1)

    def is_whatsapp_logged_in(self, timeout_seconds: int = 120) -> bool:
        """
        Verifica se o WhatsApp já está autenticado.
        """
        self._wait_for_whatsapp_initial_state(timeout_seconds)

        try:
            return self.page.locator(self._chat_list_selector).count() > 0
        except PlaywrightError as e:
            raise translate_playwright_error(e)

