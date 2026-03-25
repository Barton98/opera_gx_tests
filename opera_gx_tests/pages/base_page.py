class BasePage:

    def __init__(self, page):
        self.page = page

    # -------------------------------------------------------------------------
    # Nawigacja
    # -------------------------------------------------------------------------

    def navigate(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def reload(self) -> None:
        self.page.reload()
        self.page.wait_for_load_state("domcontentloaded")

    # -------------------------------------------------------------------------
    # Informacje o stronie
    # -------------------------------------------------------------------------

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    # -------------------------------------------------------------------------
    # localStorage – przechowywanie danych między sesjami
    # -------------------------------------------------------------------------

    def save_to_storage(self, key: str, value: str) -> None:
        self.page.evaluate(f"localStorage.setItem('{key}', '{value}')")

    def read_from_storage(self, key: str) -> str | None:
        return self.page.evaluate(f"localStorage.getItem('{key}')")
