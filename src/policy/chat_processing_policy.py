from datetime import datetime, timedelta, timezone
from typing import Sequence

from src.domain.entities.contact import Contact
from src.domain.entities.group import Group
from src.domain.entities.last_interaction import LastInteraction
from src.domain.entities.message_group import MessageGroup

from src.services.whatsapp.chat_list_models import (
    ChatListScanResult,
    ChatScrollDirection,
)

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
        def decide_response_message(
        contact: Contact,
        group: Group,
        message_group: MessageGroup
        ) -> Sequence[str]:
            """
            Decide qual mensagem automática deve ser enviada
            para o contato.
            Retorna None se não houver resposta.
            """

            if group.message_group_id is None:
                return None

            if not message_group or not message_group.messages:
                return None

            last_interaction = contact.last_interaction
            
            messages =  ContactResponsePolicy._decide_message_to_unred_chat(last_interaction=last_interaction, message_group=message_group)

            # Retorna as mensagens ideias para aquele contato
            return messages

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
        
        # TODO : Passar o historico de mensagens do cara
        @staticmethod
        def _decide_message_to_unred_chat(
            last_interaction: LastInteraction,
            message_group: MessageGroup
        ) -> Sequence[str]:
            # TODO : Pegar pelo historico, não apenas pela ultima interação
            if last_interaction is None:
                return [
                    msg
                    for msg in message_group.messages
                    if msg.type == "reception"
                ]

            direction = last_interaction.direction
            sender = last_interaction.sender

            messages: Sequence[str] = []
            messages_group = message_group.messages

            # TODO : Fazer filtragem usando apenas o lastInteraction
            # TODO : Apagar depois e substituir pelo histórico
            if direction == "inbound" and sender == "seller":
                messages = [
                    msg
                    for msg in messages_group
                    if msg.type == "wait"
                ]

            elif direction == "outbound" and sender == "auto":
                messages = [
                    msg
                    for msg in messages_group
                    if msg.type == "wait"
                ]

            elif direction == "inbound" and sender == "contact":
                messages = [
                    msg
                    for msg in messages_group
                    if msg.type == "reception"
                ]

            return messages

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

        @staticmethod
        def decide_scroll_direction_for_target(
            visible_chats: list[str],
            target_name: str,
            seen_chats: list[str],
        ) -> ChatScrollDirection:

            if not seen_chats:
                return ChatScrollDirection.EMPTY

            full_list = seen_chats

            if target_name in visible_chats:
                return ChatScrollDirection.VISIBLE

            if target_name not in full_list:
                return ChatScrollDirection.EMPTY

            target_index = full_list.index(target_name)

            first_visible = visible_chats[0]
            last_visible = visible_chats[-1]

            first_index = full_list.index(first_visible)
            last_index = full_list.index(last_visible)

            if target_index < first_index:
                return ChatScrollDirection.UP

            return ChatScrollDirection.DOWN