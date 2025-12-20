class BrowserUnstableError(Exception):
    """
    Levantado quando o browser fecha repetidamente,
    indicando instabilidade do ambiente ou ação do usuário.
    """

    def __init__(self, message: str | None = None):
        super().__init__(
            message or "Browser apresentou instabilidade e foi encerrado."
        )
