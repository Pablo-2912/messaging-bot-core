from playwright.sync_api import Page
from src.services.playwright.selectors_whatsapp import (
    chat_textbox,
    chat_textbox_skip_config,
    send_button
)
from src.config.whatsapp_selectors import WhatsAppSelectors
from src.services.whatsapp.selector import resolve_selector
from src.infra.playwright.playwright_base import (move_mouse_to_locator, mouse_click, type_text)

from src.infra.playwright.playwright_base import safe_click

def try_focus_message_textbox (page : Page, selectors : WhatsAppSelectors) -> bool:
    
    #Pegue selector do textbox
    _textbox_selectors = chat_textbox(selectors=selectors)
    
    skip = chat_textbox_skip_config(selectors=selectors)
    
    textbox_selector = resolve_selector(page=page, selectors=_textbox_selectors) 
    textbox_component = page.locator(textbox_selector).nth(skip)
    
    locator = page.locator(textbox_selector)

    count = locator.count()

    if count == 0:
        return False

    if skip >= count:
        textbox_component = locator.first
    else:
        textbox_component = locator.nth(skip)
    
    #Chama o metodo que move o mouse para cima do textbox
    x, y = move_mouse_to_locator(page=page, locator=textbox_component)
    
    #Chama o metodo que clica o botão direito do mouse
    mouse_click(page=page, x=x, y=y)
   
    return True
    
def write_message_in_chat(page : Page, selectors : WhatsAppSelectors, messages : list[str]) -> None:
    
    for message in messages: 
        type_text(page, message)

def clickSendButton(page ,selectors : WhatsAppSelectors):
    
    selector = resolve_selector(page,send_button(selectors))
    
    safe_click(page, selector)
