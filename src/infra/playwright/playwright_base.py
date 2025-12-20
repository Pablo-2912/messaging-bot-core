from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from src.domain.errors.playwright_errors import PlaywrightPageClosedError

def safe_click(page: Page, selector: str, timeout: int = 5000) -> None:
    try:
        page.wait_for_selector(selector, timeout=timeout)
        page.click(selector, timeout=timeout)

    except PlaywrightTimeoutError as e:
        raise TimeoutError(f"Timeout ao clicar no selector: {selector}") from e

    except PlaywrightError as e:
        raise PlaywrightPageClosedError(str(e)) from e
