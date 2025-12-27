# Domain
from src.domain.entities.contact import Contact
from src.domain.entities.group import Group
from src.domain.entities.message_group import MessageGroup

# Policy
from src.policy.chat_processing_policy import ContactResponsePolicy

# Repositories
from src.repository.contacts_repository import ContactsRepository
from src.repository.groups_repository import GroupsRepository
from src.repository.message_groups_repository import MessageGroupsRepository

# Services
from src.services.contact.contact_mapper import ContactMapper
from src.services.contact.messaging.send_message_command import SendMessageCommand

#External 
from typing import Sequence

ID_GROUP_BLACK_LIST = "grp_blacklist"

def process_unread_chats(chat_identifiers: list[str]) -> list[Contact]:

    contacts_repo = ContactsRepository()
    blacklisted_contacts = contacts_repo.get_by_group_id(ID_GROUP_BLACK_LIST)
    
    not_blacklisted_contacts = ContactResponsePolicy.filter_respondable_unread_contacts(chat_identifiers , blacklisted_contacts)
    
    mapper = ContactMapper(contacts_repository= contacts_repo)
    contacts = mapper.map_from_identifiers(not_blacklisted_contacts)
    
    return contacts

#Fluxo para decidir se manda ou não mensagem para os contatos
def filter_contacts_to_respond(contacts: list[Contact]) -> list[Contact]:
    """
    Orquestra o fluxo que decide QUAIS contatos
    devem receber resposta automática.
    (histórico, regras futuras, policies, etc)
    """
    respondable_contacts = ContactResponsePolicy.filter_respondable_contacts(contacts=contacts)
    
    return respondable_contacts

#Fluxo para decidir qual mensagem enviar
def build_responses(contacts: list[Contact]) -> list[SendMessageCommand]:
    """
    Orquestra a decisão de qual mensagem enviar
    para cada contato.
    Retorna pares (Contact, mensagem).
    """
    
    _groups_repository = GroupsRepository()
    _message_group = MessageGroupsRepository()
    _mapper = ContactMapper()
    
    send_message_commands : list[SendMessageCommand] = []
    
    #TODO : Alterar para chamar os grupos sob demanda, e não todos ( pelo id do grupo nos contatos)
    groups = _groups_repository.get_all()

    #TODO : Alterar para chamar os grupos messages sob demanda ( pelos ids em groups )
    message_groups = _message_group.get_all()
    

    # 1️⃣ Lookup de groups por id
    groups_by_id: dict[str, Group] = {
        group.id: group for group in groups
    }

    # 2️⃣ Lookup de message groups por id
    message_groups_by_id: dict[str, MessageGroup] = {
        msg_group.id: msg_group for msg_group in message_groups
    }
    
    #TODO : Criar Loop iterando pelos contatos
    for contact in contacts:
        
        group : Group | None= groups_by_id[contact.group_id]
        
        message_group: MessageGroup | None = message_groups_by_id[group.message_group_id]
        
        response : Sequence[str] = ContactResponsePolicy.decide_response_message( contact=contact, group=group, message_group=message_group)
        
        #TODO : Chamar metodo que mapeia contato + response em command
        command = _mapper.map_to_send_message_command(contact=contact, messages=response)
        
        send_message_commands.append(command)
    
    return send_message_commands


# TODO: adicionar filtro por histórico (evitar múltiplas respostas por período)
# Ex: ( Já respondeu hoje com uma mensagem de encerramento )

#TODO : Adicionar metodo que decide qual a mensagem a ser
