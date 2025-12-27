from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError


def scroll_chat_list(page: Page, chat_list: Page, scroll_down: bool = True, amount: int = 150) -> None:
    """
    Executa o scroll na lista de conversas do WhatsApp.
    :param page: Objeto Playwright page.
    :param chat_list: Locator da lista de conversas.
    :param scroll_down: Se True, realiza scroll para baixo, caso contrário para cima.
    :param amount: Quantidade de scroll vertical (default: 150).
    """
    chat_list.hover()
    scroll_direction = amount if scroll_down else -amount
    page.mouse.wheel(0, scroll_direction)
    page.wait_for_timeout(170)  # Espera para garantir que os chats carreguem
    
def reached_end_of_chat_list(
    seen_chats: set[str],
    previous_seen: set[str],
    empty_loop_count: int,
    max_empty_loops: int,
) -> tuple[bool, int]:
    """
    Decide se chegou ao fim da lista de chats.
    Retorna:
        (should_break, new_empty_loop_count)
    """

    if seen_chats == previous_seen:
        empty_loop_count += 1
    else:
        empty_loop_count = 0

    should_break = empty_loop_count >= max_empty_loops
    return should_break, empty_loop_count

def safe_click(
    page: Page,
    element,
    *,
    timeout_ms: int = 3000,
    delay_ms: int = 300,
) -> bool:
    try:
        element.click(timeout=timeout_ms)
        page.wait_for_timeout(delay_ms)
        return True
    except (PlaywrightTimeoutError, PlaywrightError):
        return False
