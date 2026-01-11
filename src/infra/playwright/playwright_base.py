from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from src.domain.errors.playwright_errors import PlaywrightPageClosedError

def safe_click(page: Page, selector: str, timeout: int = 5000) -> None:
    try:
        page.wait_for_selector(selector, timeout=timeout)
        page.click(selector, timeout=timeout)

    except PlaywrightTimeoutError as e:
        raise TimeoutError(f"Timeout ao clicar no selector: {selector}") from e

    except PlaywrightError as e:
        raise PlaywrightPageClosedError(str(e)) from e

def move_mouse_to_locator(page: Page, locator: Locator) -> tuple[float, float]:
    try:
        box = locator.bounding_box()

        if box is None:
            raise RuntimeError("Não foi possível obter bounding box do elemento")

        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2

        page.mouse.move(x, y)

        return x, y

    except PlaywrightError as e:
        raise PlaywrightPageClosedError(str(e)) from e


def mouse_click(page: Page, x: float, y: float) -> None:
    try:
        page.mouse.click(x, y)

    except PlaywrightError as e:
        raise PlaywrightPageClosedError(str(e)) from e

def type_text(page: Page, text: str, delay_ms: int = 40) -> None:
    try:
        page.keyboard.type(text, delay=delay_ms)

    except PlaywrightError as e:
        raise PlaywrightPageClosedError(str(e)) from e