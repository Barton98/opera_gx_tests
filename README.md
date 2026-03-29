# Opera GX – Automated Tests

Projekt testów automatycznych dla przeglądarki Opera GX.
Testuje GX Corner (API gier i deali) oraz GX Control (persystencja ustawień RAM i Hard Limit).

## Wymagania

- **Python 3.10+** – [python.org/downloads](https://www.python.org/downloads/)
- **Opera GX** zainstalowana w domyślnej lokalizacji:
  `C:\Users\<TwójUser>\AppData\Local\Programs\Opera GX\opera.exe`

## Uruchomienie na nowym komputerze

### 1. Pobierz repozytorium
```
git clone https://github.com/<twoj-login>/opera-gx-tests.git
cd opera-gx-tests
```

### 2. Utwórz wirtualne środowisko i zainstaluj zależności
```
python -m venv venv
venv\Scripts\activate
pip install pytest pytest-playwright pytest-html
playwright install chromium
```

### 3. Uruchom testy
```
cd opera_gx_tests
python -m pytest
```

Raport HTML zostanie wygenerowany w `opera_gx_tests/reports/report.html`.

## Struktura projektu

```
opera_gx_tests/
├── pytest.ini              ← konfiguracja pytest (raport HTML, tryb headed)
├── conftest.py             ← konfiguracja Opera GX jako przeglądarki testowej
├── pages/
│   ├── base_page.py        ← klasa bazowa Page Object Model
│   ├── gx_corner_page.py   ← Page Object dla GX Corner (przechwytywanie API)
│   └── gx_control_page.py  ← Page Object dla GX Control (localStorage)
└── tests/
    ├── test_gx_corner.py   ← 5 testów: Smoke, API Validation, Element Visibility
    └── test_gx_control.py  ← 2 testy: persystencja RAM Limit i Hard Limit
```

## Testy

| Plik | Klasa | Test | Opis |
|------|-------|------|------|
| test_gx_corner.py | `TestGXCornerSmoke` | `test_sections_api_returns_200` | API GX Corner zwraca status 200 |
| test_gx_corner.py | `TestGXCornerAPIValidation` | `test_free_games_section_is_not_empty` | Sekcja Free Games zawiera gry |
| test_gx_corner.py | `TestGXCornerAPIValidation` | `test_free_games_have_valid_urls` | Każda gra ma poprawny URL |
| test_gx_corner.py | `TestGXCornerElementVisibility` | `test_all_tiles_have_thumbnails` | Każdy kafelek ma miniaturkę |
| test_gx_corner.py | `TestGXCornerElementVisibility` | `test_all_tiles_have_names` | Każdy kafelek ma nazwę |
| test_gx_control.py | `TestGXControlPersistence` | `test_ram_limit_persists_after_browser_restart` | RAM Limiter zapamiętuje wartość po restarcie |
| test_gx_control.py | `TestGXControlPersistence` | `test_hard_limit_persists_after_browser_restart` | Hard Limit zachowuje stan po restarcie |

## Struktura klas testowych

Testy są pogrupowane w klasy według poziomu testowania. Klasy nie są technicznie wymagane przez pytest – testy działałyby identycznie jako zwykłe funkcje. Są tu świadomą decyzją architektoniczną:

| Klasa | Poziom | Co weryfikuje |
|-------|--------|---------------|
| `TestGXCornerSmoke` | Smoke | Czy aplikacja w ogóle odpowiada (status 200) |
| `TestGXCornerAPIValidation` | API | Czy dane zwracane przez API są kompletne i poprawne |
| `TestGXCornerElementVisibility` | UI | Czy elementy widoczne dla użytkownika mają wymagane dane |
| `TestGXControlPersistence` | Persistence | Czy ustawienia przeżywają restart przeglądarki |

Taki podział pozwala uruchamiać selektywnie tylko wybrany poziom testów, np.:
```
python -m pytest tests/test_gx_corner.py::TestGXCornerSmoke
```

## Technologie

- [Python](https://python.org) 3.10+
- [Playwright](https://playwright.dev/python/) – automatyzacja przeglądarki
- [pytest](https://pytest.org) – framework testowy
- [pytest-html](https://pytest-html.readthedocs.io) – raportowanie HTML
