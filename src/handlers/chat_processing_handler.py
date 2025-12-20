from src.repository.contacts_repository import ContactsRepository
from src.policy.chat_processing_policy import ContactResponsePolicy
from src.services.contact.contact_mapper import ContactMapper
from src.domain.entities.contact import Contact
from src.services.contact.messaging.send_message_command import SendMessageCommand

ID_GROUP_BLACK_LIST = "grp_blacklist"

def proccess_unread_chats(chat_identifiers: list[str]) -> list[Contact]:

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
#TODO : Alterear o retorno para um DTO decente
def build_responses(contacts: list[Contact]) -> list[SendMessageCommand]:
    """
    Orquestra a decisão de qual mensagem enviar
    para cada contato.
    Retorna pares (Contact, mensagem).
    """
    pass


# TODO: adicionar filtro por histórico (evitar múltiplas respostas por período)
# Ex: ( Já respondeu hoje com uma mensagem de encerramento )

#TODO : Adicionar metodo que decide qual a mensagem a ser
