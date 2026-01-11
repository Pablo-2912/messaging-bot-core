import time

from src.infra.playwright.whatsapp_actions import (
    scroll_chat_list,
    reached_end_of_chat_list,
    safe_click
)
from src.config.whatsapp_selectors import WhatsAppSelectors
from playwright.sync_api import Page
from src.services.playwright.selectors_whatsapp import (
    chat_item,
    chat_list,
    chat_name,
    unread_badge,
)
from src.domain.errors.errors_base import TimeoutError
from src.services.whatsapp.chat_list_models import ChatListScanResult
from src.services.whatsapp.selector import resolve_selector
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def get_unread_chats(
    page: Page,
    selectors: WhatsAppSelectors,
    timeout: int = 300,
) -> list[str]:

    start_time = time.monotonic()

    def check_timeout() -> None:
        if time.monotonic() - start_time > timeout:
            raise TimeoutError(
                f"Timeout ao buscar chats não lidos ({timeout}s)"
            )

    unread_chats: list[str] = []

    # ==========================
    # RESOLVE SELECTORS (1 VEZ)
    # ==========================
    chat_item_selector = resolve_selector(
        page,
        chat_item(selectors),
    )

    chat_name_selector = resolve_selector(
        page,
        chat_name(selectors),
    )

    chat_list_selector = resolve_selector(
        page,
        chat_list(selectors),
    )

    unread_badge_selector = resolve_selector(
        page,
        unread_badge(selectors),
    )

    chat_list_comp = page.locator(chat_list_selector)

    # ==========================
    # FASE 1 — SCAN DA LISTA
    # ==========================
    scan_result = scan_chat_list(
        page,
        selectors,
        timeout=timeout,
    )

    last_chat_name = scan_result.last_chat_name
    total_scrolled_px = scan_result.total_scrolled_px

    # ==========================
    # VOLTA AO TOPO
    # ==========================
    scroll_chat_list_to_top(
        page,
        chat_list_comp,
        total_scrolled_px,
        timeout=timeout,
    )

    # ==========================
    # FASE 2 — SCROLL FINO
    # ==========================
    reached_last_chat = False
    fine_scrolled_px = 0
    scroll_amount_fine = 400

    while not reached_last_chat:
        check_timeout()

        chat_items = page.locator(chat_item_selector)
        total_chats = chat_items.count()

        for i in range(total_chats):
            check_timeout()

            chat = chat_items.nth(i)

            contact_name = (
                chat.locator(chat_name_selector)
                .first
                .inner_text()
                .strip()
            )

            has_unread = False

            for badge_selector in unread_badge(selectors):
                if chat.locator(badge_selector).count() > 0:
                    has_unread = True
                    break

            # 👇 ISSO TEM QUE SER FORA DO LOOP DE SELECTOR
            if has_unread and contact_name and contact_name not in unread_chats:
                unread_chats.append(contact_name)

            if last_chat_name and contact_name == last_chat_name:
                reached_last_chat = True
                break

        if not reached_last_chat:
            scroll_chat_list(
                page,
                chat_list_comp,
                amount=scroll_amount_fine,
            )
            fine_scrolled_px += scroll_amount_fine

    # ==========================
    # VOLTA AO TOPO FINAL
    # ==========================
    scroll_chat_list_to_top(
        page,
        chat_list_comp,
        total_scrolled_px + fine_scrolled_px,
        timeout=timeout,
    )

    return unread_chats

def scroll_chat_list_to_top(
    page: Page,
    chat_list_comp,
    total_scrolled_px: int,
    *,
    timeout: int,
) -> None:
    start_time = time.monotonic()

    def check_timeout() -> None:
        if time.monotonic() - start_time > timeout:
            raise TimeoutError(
                f"Timeout ao voltar chat list para o topo ({timeout}s)"
            )

    scroll_step = 1500
    steps = (total_scrolled_px // scroll_step) + 1

    for _ in range(steps):
        check_timeout()
        scroll_chat_list(
            page,
            chat_list_comp,
            scroll_down=False,
            amount=scroll_step,
        )

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def collect_loaded_chat_names(
    page: Page,
    selectors: WhatsAppSelectors,
) -> list[str]:
    """
    Retorna os nomes dos chats atualmente carregados no DOM.
    NÃO mantém estado.
    """

    chat_list_selector = resolve_selector(
        page,
        chat_list(selectors),
    )

    chat_item_selector = resolve_selector(
        page,
        chat_item(selectors),
    )

    chat_name_selector = resolve_selector(
        page,
        chat_name(selectors),
    )

    chat_list_component = page.locator(chat_list_selector)
    chat_items = chat_list_component.locator(chat_item_selector)

    total_chats = chat_items.count()

    collected: list[str] = []

    for i in range(total_chats):
        chat = chat_items.nth(i)

        try:
            name_locator = chat.locator(chat_name_selector).first

            name = name_locator.get_attribute("title", timeout=300)

            if not name:
                name = name_locator.inner_text(timeout=300).strip()

        except PlaywrightTimeoutError:
            break  # parou de achar nomes válidos = fim da lista carregada

        if name:
            collected.append(name)

    return collected


def scan_chat_list(
    page: Page,
    selectors: WhatsAppSelectors,
    *,
    timeout: int = 180,
) -> ChatListScanResult:

    start_time = time.monotonic()

    def check_timeout() -> None:
        if time.monotonic() - start_time > timeout:
            raise TimeoutError(
                f"Timeout ao escanear lista de chats ({timeout}s)"
            )

    seen_chats_ordered: list[str] = []
    seen_chats_set: set[str] = set()

    # ==========================
    # RESOLVE SELECTORS (1 VEZ)
    # ==========================
    chat_item_selector = resolve_selector(
        page,
        chat_item(selectors),
    )

    chat_name_selector = resolve_selector(
        page,
        chat_name(selectors),
    )

    chat_list_selector = resolve_selector(
        page,
        chat_list(selectors),
    )

    chat_list_comp = page.locator(chat_list_selector)

    max_empty_loops = 4
    empty_loop_count = 0

    scroll_amount = 600
    total_scrolled_px = 0

    # ==========================
    # SCAN — TOPO → FIM
    # ==========================
    while True:
        check_timeout()

        current_seen = set(seen_chats_set)

        chat_items = page.locator(chat_item_selector)
        total_chats = chat_items.count()

        for i in range(total_chats):
            check_timeout()

            chat = chat_items.nth(i)
            name = (
                chat.locator(chat_name_selector)
                .first
                .inner_text()
                .strip()
            )

            if name and name not in seen_chats_set:
                seen_chats_set.add(name)
                seen_chats_ordered.append(name)

        scroll_chat_list(
            page,
            chat_list_comp,
            amount=scroll_amount,
        )
        total_scrolled_px += scroll_amount

        should_break, empty_loop_count = reached_end_of_chat_list(
            seen_chats_set,
            current_seen,
            empty_loop_count,
            max_empty_loops,
        )

        if should_break:
            break

    return ChatListScanResult(
        last_chat_name=seen_chats_ordered[-1] if seen_chats_ordered else None,
        total_scrolled_px=total_scrolled_px,
        seen_chats=seen_chats_ordered,
    )

def scroll_chat_list_to_top_hard(
    page: Page,
    selectors: WhatsAppSelectors,
    *,
    timeout: int = 120,
) -> None:
    start_time = time.monotonic()

    def check_timeout() -> None:
        if time.monotonic() - start_time > timeout:
            raise TimeoutError(
                f"Timeout ao subir chat list até o topo ({timeout}s)"
            )

    chat_item_selector = resolve_selector(
        page,
        chat_item(selectors),
    )

    chat_list_selector = resolve_selector(
        page,
        chat_list(selectors),
    )

    chat_list_comp = page.locator(chat_list_selector)

    max_empty_loops = 4
    empty_loop_count = 0
    scroll_amount = 1200  # scroll grande e agressivo

    last_seen_first_chat: str | None = None

    while True:
        check_timeout()

        chat_items = page.locator(chat_item_selector)
        total_chats = chat_items.count()

        if total_chats == 0:
            return

        first_chat = chat_items.nth(0)
        first_name = first_chat.inner_text().strip()

        if first_name == last_seen_first_chat:
            empty_loop_count += 1
        else:
            empty_loop_count = 0
            last_seen_first_chat = first_name

        if empty_loop_count >= max_empty_loops:
            return

        scroll_chat_list(
            page,
            chat_list_comp,
            scroll_down=False,
            amount=scroll_amount,
        )

        page.wait_for_timeout(200)

def try_click_chat_by_name(
    page: Page,
    selectors: WhatsAppSelectors,
    target_name: str,
    *,
    stop_at: str | None = None,
    max_scrolls: int = 50,
) -> bool:
    """
    Tenta localizar e clicar em um chat pelo nome.
    Usa find_chat_row para garantir que o chat esteja carregado.
    """

    chat_item_selector = resolve_selector(
        page,
        chat_item(selectors),
    )


    chat_list_selector = resolve_selector(
        page,
        chat_list(selectors),
    )

    chat_list_comp = page.locator(chat_list_selector)
    if chat_list_comp.count() == 0:
        return False

    target = target_name.strip()

    # garante que o chat esteja carregado (com scroll)
    found = find_chat_row(
        page=page,
        selectors=selectors,
        name=target,
        last_chat_name=stop_at,
        max_scrolls=max_scrolls,
    )

    if not found:
        return False

    # agora só procura nos chats carregados e clica
    chat_items = page.locator(chat_item_selector)
    total_chats = chat_items.count()

    for i in range(total_chats):
        
        chat_name_selector = resolve_selector(
            page,
            chat_name(selectors),
        )
        
        chat = chat_items.nth(i)
        contact_name = (
            chat.locator(chat_name_selector)
            .first
            .inner_text()
            .strip()
        )

        if contact_name == target:
            return safe_click(page=page, element=chat)

    return False

def get_visible_chat_names(
    page: Page,
    selectors: WhatsAppSelectors,
    scrolled : int
    #min_visible_ratio: float = 0.5,
) -> list[str]:
   
   pane_height = get_pane_side_height(page=page)
   archived_button_height = get_archived_button_height(page=page)
   chat_row_height = get_chat_row_height(page=page, selectors=selectors)
   
   visible_button_archive_heght : int = scrolled - archived_button_height
   
   
   pass

def get_pane_side_height(page: Page) -> int:
    """
    Retorna a altura (em px) do div #pane-side.
    """
    return page.evaluate(
        """
        () => {
            const pane = document.querySelector('#pane-side');
            if (!pane) return 0;
            return pane.getBoundingClientRect().height;
        }
        """
    )

def get_archived_button_height(page: Page) -> int:
    """
    Retorna a altura (em px) do botão 'Arquivadas'.
    Se não existir, retorna 0.
    """
    return page.evaluate(
        """
        () => {
            const btn = document.querySelector(
                'button[aria-label^="Arquivadas"]'
            );
            if (!btn) return 0;
            return btn.getBoundingClientRect().height;
        }
        """
    )

def get_chat_row_height(page: Page, selectors: WhatsAppSelectors) -> int:
    """
    Retorna a altura (em px) de um item de chat (row) da chat list.
    """
    chat_item_selector = chat_item(selectors)

    return page.evaluate(
        """
        (selector) => {
            const el = document.querySelector(selector);
            if (!el) return 0;
            return el.getBoundingClientRect().height;
        }
        """,
        chat_item_selector,
    )

def find_chat_row(
    page: Page,
    selectors: WhatsAppSelectors,
    name: str,
    *,
    last_chat_name: str | None = None,
    scroll_amount: int = 600,
    max_scrolls: int = 50,
) -> bool:
    """
    Garante que o chat esteja carregado no DOM.
    Rola a chat list até encontrar o chat ou atingir o final conhecido.

    Retorna True se encontrou (logo, clicável).
    Retorna False se chegou ao fim da lista.
    """

    scroll_chat_list_to_top_hard(page=page, selectors=selectors)

    chat_list_selector = resolve_selector(
        page,
        chat_list(selectors),
    )

    chat_list_comp = page.locator(chat_list_selector)

    seen_last = False
    target = name.strip()

    for _ in range(max_scrolls):
        loaded_names = collect_loaded_chat_names(
            page=page,
            selectors=selectors,
        )

        if target in loaded_names:
            return True

        if last_chat_name and last_chat_name in loaded_names:
            if seen_last:
                return False
            seen_last = True

        scroll_chat_list(
            page=page,
            chat_list_comp=chat_list_comp,
            amount=scroll_amount,
        )

    return False
