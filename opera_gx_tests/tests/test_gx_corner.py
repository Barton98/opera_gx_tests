import pytest
from pages.gx_corner_page import GXCornerPage


@pytest.fixture()
def gx(page):
    gx_corner = GXCornerPage(page)
    gx_corner.navigate_and_capture_responses()
    return gx_corner


class TestGXCornerSmoke:

    def test_sections_api_returns_200(self, gx):
        status = gx.get_sections_status()
        assert status == 200, f"API sekcji GX Corner zwróciło {status} zamiast 200! Backend może być niedostępny."


class TestGXCornerAPIValidation:

    def test_free_games_section_is_not_empty(self, gx):
        games = gx.get_free_games()
        assert len(games) > 0, "Sekcja Free Games jest pusta! Problem z dostarczaniem danych z API."

    def test_free_games_have_valid_urls(self, gx):
        games = gx.get_free_games()
        for game in games:
            url = game.get("url", "")
            assert url.startswith("http"), \
                f"Gra '{game.get('name')}' ma niepoprawny URL: '{url}'"


class TestGXCornerElementVisibility:

    def test_all_tiles_have_thumbnails(self, gx):
        broken = gx.get_tiles_with_missing_images()
        assert len(broken) == 0, (
            f"Znaleziono {len(broken)} kafelków z brakującym obrazkiem!\n"
            f"Przykłady: {[item.get('name', '?') for item in broken[:3]]}"
        )

    def test_all_tiles_have_names(self, gx):
        broken = gx.get_tiles_with_missing_names()
        assert len(broken) == 0, (
            f"Znaleziono {len(broken)} kafelków bez tytułu!\n"
            f"Dane: {broken[:3]}"
        )
