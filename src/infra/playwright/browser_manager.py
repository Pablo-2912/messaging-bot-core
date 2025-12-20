from playwright.sync_api import sync_playwright

class BrowserManager:
    def __init__(self, user_data_dir: str):
        self.user_data_dir = user_data_dir

        self.playwright = None
        self.context = None
        self.page = None

    def start(self, headless: bool):
        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            self.user_data_dir,
            headless= headless,
            args=["--disable-blink-features=AutomationControlled"]
        )

        self.page = (
            self.context.pages[0]
            if self.context.pages
            else self.context.new_page()
        )

        return self

    def stop(self):
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
 