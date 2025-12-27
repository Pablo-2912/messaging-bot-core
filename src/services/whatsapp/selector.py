from playwright.sync_api import Page

def resolve_selector(page: Page, selectors: list[str]) -> str:
    """
    Retorna o primeiro selector que existe no DOM.
    Se nenhum existir, assume o PRIMEIRO da lista (mais confiável por definição).
    """
    if not selectors:
        raise RuntimeError("Lista de selectors vazia")

    for selector in selectors:
        try:
            if page.locator(selector).count() > 0:
                return selector
        except Exception:
            continue

    # fallback explícito: assume o primeiro
    return selectors[0]
