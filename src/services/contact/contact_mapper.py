from src.domain.entities.contact import Contact
from src.repository.contacts_repository import ContactsRepository
from src.services.helper.format_helper import normalize_mobile_number

class ContactMapper:
    """
    Responsável por mapear um identificador externo (ex: nome vindo do WhatsApp)
    para uma entidade Contact do domínio.

    - Resolve contato existente (por número ou nome)
    - Caso não exista, cria um Contact mínimo (apenas para runtime)
    """

    DEFAULT_GROUP_ID = "grp_default"

    def __init__(self, contacts_repository: ContactsRepository):
        self._contacts_repository = contacts_repository

    def map_from_identifier(self, identifier: str) -> Contact:
        """
        Recebe um identificador cru (nome ou número) e retorna um Contact.
        Nunca retorna None.
        """

        identifier = identifier.strip()

        # 1️⃣ Tenta resolver como número (normalizado)
        normalized_number = normalize_mobile_number(identifier)
        if normalized_number:
            contact = self._contacts_repository.get_by_number(normalized_number)
            if contact:
                return contact

        # 2️⃣ Tenta resolver como nome (somente se não achou por número)
        contact = self._find_by_name(identifier)
        if contact:
            return contact

        minimal_contact = self._create_minimal_contact(
            name=identifier if not normalized_number else identifier
        )

        return  minimal_contact
        
    def map_from_identifiers(self, identifiers: list[str]) -> list[Contact]:
        contacts: list[Contact] = []

        for identifier in identifiers:
            contact = self.map_from_identifier(identifier)
            contacts.append(contact)

        return contacts

    # -------------------------
    # Internal helpers
    # -------------------------

    def _find_by_name(self, name: str) -> Contact | None:
        """
        Busca contato por nome exato (case-sensitive, contrato do sistema).
        """
        contacts =  self._contacts_repository.get_all()
        
        for contact in contacts:
            if contact.name == name:
                return contact
        return None

    def _create_minimal_contact(self, name: str) -> Contact:
        """
        Cria um Contact mínimo apenas para uso em runtime.
        Não deve ser persistido diretamente.
        """
        contact =  Contact(
            id=self._generate_runtime_id(name),
            name=name,
            number="",
            group_id=self.DEFAULT_GROUP_ID,
            note=None,
            last_interaction=None,
        )

        return contact

    def _generate_runtime_id(self, name: str) -> str:
        """
        Gera um ID temporário, apenas para uso em memória.
        Não é persistente nem estável entre execuções.
        """
        return f"runtime::{name}"
