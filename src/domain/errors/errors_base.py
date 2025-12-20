from typing import Any

class BotError(Exception):
    """Erro base do bot."""

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        super().__init__(message)
        self.context = context or {}

    def __str__(self) -> str:
        if not self.context:
            return super().__str__()
        return f"{super().__str__()} | context={self.context}"


class TimeoutError(BotError):
    """Erro genérico de timeout."""
    pass


class RecoverableError(BotError):
    """Erro que permite retry."""
    pass


class FatalError(BotError):
    """Erro que deve encerrar o serviço."""
    pass
