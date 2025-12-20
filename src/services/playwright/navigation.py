from playwright.async_api import Page

def open_url(page: Page, url: str):
     page.goto(url)
