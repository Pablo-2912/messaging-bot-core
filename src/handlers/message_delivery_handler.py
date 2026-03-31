from playwright.sync_api import Page

from src.config.whatsapp_selectors import WhatsAppSelectors

from src.services.contact.messaging.send_message_command import SendMessageCommand
from src.services.whatsapp.chat_list import (
    scan_chat_list,
    try_click_chat_by_name
)

from src.services.whatsapp.chat import click_send_button

from src.services.event.eventService import EventService

from src.services.whatsapp.chat import (try_focus_message_textbox, write_message_in_chat)

from src.infra.playwright.playwright_base import  type_text

from src.domain.entities.message_template import MessageTemplate

from src.infra.events.event_writer import EventWriter

def deliver_message_to_chats (page : Page, commands : list[SendMessageCommand], selectors : WhatsAppSelectors, event_writer: EventWriter | None ) :
    
    # retorna todos os chats em uma lista
    scan_result =  scan_chat_list(page=page, selectors=selectors)

    for command in commands:
        
        #scroll_chat_list_to_top_hard(page, selectors=selectors)
        
        #loaded_chats = collect_loaded_chat_names(page=page, selectors=selectors)   
        
        #TODO : Chamar metodo para saber quais chats estou vendo agora 
        #visible_chats : list[str] = get_visible_chat_names(page=page,selectors=selectors)
        
        #TODO : Chamar policy para saber se tem de subir ou descer chat list
        #ContactResponsePolicy.decide_scroll_direction_for_target(visible_chats, command.name, sacn_result)
        
        #TODO : Chamar metodo que encontra e clica no chat
        
        name = command.name

        response : bool = try_click_chat_by_name(page=page, selectors=selectors, target_name=name, stop_at=scan_result.last_chat_name )
        
        whatsapp_event_writer = EventService(event_writer)
        
        if response:
           whatsapp_event_writer .chat_opened(command.number, command.name)
            
        #TODO : Verificar se há algum evento de pause ou stop do worker
        
        #Chama metodo que envia mensagens de acordo com os commands
        response = _try_send_messages_to_chat(page=page, command=command, selectors=selectors)
        
        if response:
            # Dispara Log de envio de mensagem
            whatsapp_event_writer.message_sent(command=command)
        
        # TODO : Atualiza historico
           
def _try_send_messages_to_chat(page : Page, command : SendMessageCommand, selectors : WhatsAppSelectors) -> bool : 
   
    #TODO: Rolar até o fim do chat
   
    templates: list[MessageTemplate] = command.message_template

    for template in templates:
        
       for message_part in template.parts:
        # Seleciona o textbox do chat
        try_focus_message_textbox(page=page, selectors=selectors)
        
        page.wait_for_timeout(500)
        
        # Escreve a mensagem
        type_text(page=page,text=message_part)
        
        #TODO : Logica que verifica se há eventos de pause ou stop
        
        #TODO: Logica que verifica novamente se o usuario já não respondeu o cliente 
        
        # Click no botão de enviar
        click_send_button(page=page, selectors=selectors)
        
        