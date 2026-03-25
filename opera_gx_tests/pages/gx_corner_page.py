from playwright.sync_api import Page, Response
from pages.base_page import BasePage


class GXCornerPage(BasePage):
    API_SECTIONS = "https://proxy.gxcorner.games/new-content/sd-widget-sections"
    API_TEASER   = "https://merchandise.opera-api2.com/api/v4/teaser"
    API_WEATHER  = "https://weather.opera-api2.com/location"

    def __init__(self, page: Page):
        self.page = page
        self.url = "opera://startpage"
        self._api_responses: dict[str, Response] = {}

    # -------------------------------------------------------------------------
    # Nawigacja + przechwytywanie odpowiedzi API
    # -------------------------------------------------------------------------

    def navigate_and_capture_responses(self) -> None:

        def on_response(response: Response):
            if self.API_SECTIONS in response.url:
                self._api_responses["sections"] = response
            elif self.API_TEASER in response.url:
                self._api_responses["teaser"] = response
            elif self.API_WEATHER in response.url:
                self._api_responses["weather"] = response

        self.page.on("response", on_response)
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle", timeout=20000)

    # -------------------------------------------------------------------------
    # Smoke Test: Status HTTP
    # -------------------------------------------------------------------------

    def get_sections_status(self) -> int:
        if "sections" not in self._api_responses:
            raise AssertionError("Brak odpowiedzi z API sekcji – request nie został wykonany!")
        return self._api_responses["sections"].status

    # -------------------------------------------------------------------------
    # API Validation: zawartość Free Games
    # -------------------------------------------------------------------------

    def get_free_games(self) -> list:
        if "sections" not in self._api_responses:
            raise AssertionError("Brak odpowiedzi z API sekcji!")
        data = self._api_responses["sections"].json().get("data", [])
        for section in data:
            if section.get("component") == "speed-dial.gx-games":
                return section.get("items", [])
        return []

    def get_all_sections(self) -> list:
        if "sections" not in self._api_responses:
            raise AssertionError("Brak odpowiedzi z API sekcji!")
        return self._api_responses["sections"].json().get("data", [])

    # -------------------------------------------------------------------------
    # Element Visibility: obrazki i teksty kafelków
    # -------------------------------------------------------------------------

    def get_tiles_with_missing_images(self) -> list:
        all_sections = self.get_all_sections()
        broken = []
        for section in all_sections:
            for item in section.get("items", []):
                thumbnail = item.get("thumbnail", "")
                if not thumbnail or not thumbnail.startswith("http"):
                    broken.append(item)
        return broken

    def get_tiles_with_missing_names(self) -> list:
        all_sections = self.get_all_sections()
        broken = []
        for section in all_sections:
            for item in section.get("items", []):
                name = item.get("name", "")
                if not name or len(name.strip()) == 0:
                    broken.append(item)
        return broken
