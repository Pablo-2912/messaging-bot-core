from playwright.sync_api import Error as PlaywrightError


class PlaywrightBaseError(Exception):
    """Erro base para qualquer falha relacionada ao Playwright."""
    pass


class PlaywrightBrowserClosedError(PlaywrightBaseError):
    """Browser ou contexto foi fechado inesperadamente."""
    pass


class PlaywrightPageClosedError(PlaywrightBaseError):
    """Page foi fechada enquanto ainda era utilizada."""
    pass


class PlaywrightNavigationError(PlaywrightBaseError):
    """Erro ao navegar para uma página."""
    pass


def translate_playwright_error(error: PlaywrightError) -> PlaywrightBaseError:
    """
    Traduz erros do Playwright para erros de domínio.
    """
    message = str(error)

    if "Target page, context or browser has been closed" in message:
        return PlaywrightPageClosedError(message)

    if "Browser has been closed" in message:
        return PlaywrightBrowserClosedError(message)

    return PlaywrightBaseError(message)
