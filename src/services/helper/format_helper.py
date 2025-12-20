import re 

def only_digits(value: str) -> str:
    """
    Retorna apenas os dígitos da string.
    """
    try:
        return re.sub(r"[^\d]", "", value or "")
    except Exception:
        return ""
    
def normalize_mobile_number(value: str) -> str | None:
        """
        Normaliza número de celular brasileiro para o formato:
        55 + DDD + 9 + XXXXXXXX

        Retorna número inválido padrão se não passar nas validações.
        """
        try:
            digits = only_digits(value)

            if not digits:
                return None

            # Remove DDI se já vier
            if digits.startswith("55"):
                digits = digits[2:]

            # Se tiver 10 dígitos, insere o 9
            if len(digits) == 10:
                digits = digits[:2] + "9" + digits[2:]

            # Precisa ter exatamente 11 dígitos agora
            if len(digits) != 11:
                return None

            # Validação: DDD (2) + 9 + 8 dígitos
            if not re.fullmatch(r"\d{2}9\d{8}", digits):
                return None

            return "55" + digits

        except Exception:
            return None
