import time

from src.infra.playwright.whatsapp_actions import (
    scroll_chat_list,
    reached_end_of_chat_list,
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

    seen_chats_ordered: list[str] = []
    seen_chats_set: set[str] = set()

    chat_item_selector = chat_item(selectors)
    unread_badge_selector = unread_badge(selectors)
    chat_name_selector = chat_name(selectors)
    chat_list_selector = chat_list(selectors)

    chat_list_comp = page.locator(chat_list_selector)

    # ==========================
    # FASE 1 — SCROLL GRANDE
    # ==========================
    max_empty_loops = 4
    empty_loop_count = 0

    scroll_amount = 600
    total_scrolled_px = 0

    while True:
        check_timeout()

        chat_items = page.locator(chat_item_selector)
        total_chats = chat_items.count()
        current_seen = set(seen_chats_set)

        for i in range(total_chats):
            check_timeout()

            chat = chat_items.nth(i)
            contact_name = (
                chat.locator(chat_name_selector)
                .first
                .inner_text()
                .strip()
            )

            if contact_name in seen_chats_set:
                continue

            seen_chats_set.add(contact_name)
            seen_chats_ordered.append(contact_name)

        scroll_chat_list(page, chat_list_comp, amount=scroll_amount)
        total_scrolled_px += scroll_amount

        should_break, empty_loop_count = reached_end_of_chat_list(
            seen_chats_set,
            current_seen,
            empty_loop_count,
            max_empty_loops,
        )

        if should_break:
            break

    # último chat real da lista
    last_chat_name = seen_chats_ordered[-1] if seen_chats_ordered else None

    # ==========================
    # VOLTA AO TOPO
    # ==========================
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

    # ==========================
    # FASE 2 — SCROLL FINO
    # ==========================
    reached_last_chat = False

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

            if chat.locator(unread_badge_selector).count() > 0:
                if contact_name not in unread_chats:
                    unread_chats.append(contact_name)

            if contact_name == last_chat_name:
                reached_last_chat = True
                break

        if not reached_last_chat:
            scroll_chat_list(page, chat_list_comp, amount=150)

    return unread_chats
