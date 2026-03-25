import os
import pytest

from pages.gx_control_page import GXControlPage


OPERA_GX_PATH = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Local", "Programs", "Opera GX", "opera.exe"
)


# =============================================================================
# GX CONTROL – persystencja ustawień RAM i Hard Limit po restarcie przeglądarki
# =============================================================================

class TestGXControlPersistence:

    def test_ram_limit_persists_after_browser_restart(self, playwright, tmp_path):
        """RAM Limiter powinien pamiętać ustawioną wartość po ponownym uruchomieniu."""

        RAM_VALUE = "4096"

        # ── SESJA 1: zapisz ustawienie ───────────────────────────────────────
        context1 = playwright.chromium.launch_persistent_context(
            user_data_dir=str(tmp_path),
            executable_path=OPERA_GX_PATH,
            headless=False,
            slow_mo=300,
        )
        page1 = context1.new_page()
        gx1 = GXControlPage(page1)
        gx1.navigate()
        gx1.save_to_storage(GXControlPage.KEY_RAM_LIMIT, RAM_VALUE)

        saved = gx1.read_from_storage(GXControlPage.KEY_RAM_LIMIT)
        assert saved == RAM_VALUE, f"Zapis nie powiódł się przed restartem! Otrzymano: '{saved}'"

        context1.close()

        # ── SESJA 2: ten sam profil – sprawdź czy wartość przetrwała ─────────
        context2 = playwright.chromium.launch_persistent_context(
            user_data_dir=str(tmp_path),
            executable_path=OPERA_GX_PATH,
            headless=False,
            slow_mo=300,
        )
        page2 = context2.new_page()
        gx2 = GXControlPage(page2)
        gx2.navigate()

        persisted = gx2.read_from_storage(GXControlPage.KEY_RAM_LIMIT)
        context2.close()

        assert persisted == RAM_VALUE, (
            f"BŁĄD PERSYSTENCJI! RAM Limiter nie przetrwał restartu.\n"
            f"Oczekiwano: '{RAM_VALUE}' MB (4GB), Otrzymano: '{persisted}'"
        )

    def test_hard_limit_persists_after_browser_restart(self, playwright, tmp_path):
        """Hard Limit (toggle true/false) powinien zachować stan po restarcie przeglądarki."""

        HARD_LIMIT_VALUE = "true"

        # ── SESJA 1: włącz Hard Limit ────────────────────────────────────────
        context1 = playwright.chromium.launch_persistent_context(
            user_data_dir=str(tmp_path),
            executable_path=OPERA_GX_PATH,
            headless=False,
            slow_mo=300,
        )
        page1 = context1.new_page()
        gx1 = GXControlPage(page1)
        gx1.navigate()
        gx1.save_to_storage(GXControlPage.KEY_HARD_LIMIT, HARD_LIMIT_VALUE)

        saved = gx1.read_from_storage(GXControlPage.KEY_HARD_LIMIT)
        assert saved == HARD_LIMIT_VALUE, f"Zapis Hard Limit nie powiódł się! Otrzymano: '{saved}'"

        context1.close()

        # ── SESJA 2: sprawdź czy toggle pozostał włączony ────────────────────
        context2 = playwright.chromium.launch_persistent_context(
            user_data_dir=str(tmp_path),
            executable_path=OPERA_GX_PATH,
            headless=False,
            slow_mo=300,
        )
        page2 = context2.new_page()
        gx2 = GXControlPage(page2)
        gx2.navigate()

        persisted = gx2.read_from_storage(GXControlPage.KEY_HARD_LIMIT)
        context2.close()

        assert persisted == HARD_LIMIT_VALUE, (
            f"BŁĄD PERSYSTENCJI! Hard Limit nie przetrwał restartu.\n"
            f"Oczekiwano: '{HARD_LIMIT_VALUE}', Otrzymano: '{persisted}'"
        )
