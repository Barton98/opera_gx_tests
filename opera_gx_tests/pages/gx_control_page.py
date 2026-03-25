import json
import os

from playwright.sync_api import Page
from pages.base_page import BasePage

OPERA_PREFS_PATH = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Roaming", "Opera Software", "Opera GX Stable", "Default", "Preferences"
)


class GXControlPage(BasePage):

    PERSISTENCE_TEST_URL = "https://gx.games/"

    KEY_RAM_LIMIT  = "gx_ram_limit_mb"
    KEY_CPU_LIMIT  = "gx_cpu_limit_percent"
    KEY_HARD_LIMIT = "gx_hard_limit_enabled"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        super().navigate(self.PERSISTENCE_TEST_URL)

    @staticmethod
    def read_preferences() -> dict:
        if not os.path.exists(OPERA_PREFS_PATH):
            raise FileNotFoundError(
                f"Nie znaleziono pliku Preferences Opera GX!\n"
                f"Oczekiwana lokalizacja: {OPERA_PREFS_PATH}\n"
                f"Upewnij się że Opera GX jest zainstalowana i była uruchomiona co najmniej raz."
            )
        with open(OPERA_PREFS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
