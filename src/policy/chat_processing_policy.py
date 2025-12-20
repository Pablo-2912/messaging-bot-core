from src.domain.entities.contact import Contact
from src.domain.entities.group import Group
from src.domain.entities.last_interaction import LastInteraction
from datetime import datetime, timedelta, timezone

class ContactResponsePolicy:

        @staticmethod
        def filter_respondable_unread_contacts(
            chat_identifiers: list[str],
            contacts_black_list: list[Contact],
        ) -> list[str]:

            if not chat_identifiers:
                return []

            if not contacts_black_list:
                return list(dict.fromkeys(chat_identifiers))


            blacklist_identifiers = ContactResponsePolicy._extract_blacklist_identifiers(
                contacts_black_list
            )

            return ContactResponsePolicy._filter_blacklisted_and_duplicates(
                chat_identifiers,
                blacklist_identifiers,
            )
            
        @staticmethod
        def filter_respondable_contacts(
            contacts: list[Contact],
        ) -> list[Contact]:

            if len(contacts) < 1:
                return []
            
            not_replied_recently = ContactResponsePolicy._filter_chats_not_replied_recently(contacts=contacts)
            
            #TODO : Chama metodo que faz filtro pelo histórico 
            
            allowed = not_replied_recently
            
            return  allowed

        @staticmethod
        def _filter_chats_not_replied_recently(
            contacts: list["Contact"],
            cooldown_hours: int = 24
        ) -> list[Contact]:

            allowed: list["Contact"] = []
            now = datetime.now(timezone.utc)
            cooldown_delta = timedelta(hours=cooldown_hours)

            for contact in contacts:
                last_interaction : LastInteraction = contact.last_interaction

                # nunca interagiu → pode responder
                if last_interaction is None:
                    allowed.append(contact)
                    continue

                try:
                    last_at = datetime.fromisoformat(
                        last_interaction.at.replace("Z", "+00:00")
                    )
                except Exception:
                    # data inválida → não bloqueia
                    allowed.append(contact)
                    continue

                is_bot_message = (
                    last_interaction.sender == "auto"
                    or last_interaction.direction == "outbound"
                )


                # se foi o bot e está dentro do cooldown → ignora
                if  is_bot_message and (now - last_at) < cooldown_delta:
                    continue

                allowed.append(contact)

            return allowed

        @staticmethod
        def _extract_blacklist_identifiers(
            contacts_black_list: list[Contact],
        ) -> set[str]:
            """
            Extrai todos os identificadores possíveis da blacklist:
            - nome
            - número
            Comparação case-sensitive.
            """
            identifiers: set[str] = set()

            for contact in contacts_black_list:
                if contact.name:
                    identifiers.add(contact.name)

                if contact.number:
                    identifiers.add(contact.number)

            return identifiers
        
        @staticmethod
        def _filter_blacklisted_and_duplicates(
            chat_identifiers: list[str],
            blacklist_identifiers: set[str],
        ) -> list[str]:
            """
            Remove identificadores que estejam na blacklist
            e elimina duplicados.
            Comparação case-sensitive.
            """
            allowed: list[str] = []
            seen: set[str] = set()

            for identifier in chat_identifiers:
                if identifier in blacklist_identifiers:
                    continue

                if identifier in seen:
                    continue

                seen.add(identifier)
                allowed.append(identifier)

            return allowed
