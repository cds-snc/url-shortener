from unittest.mock import MagicMock, patch
from utils import i18n

@patch("utils.i18n.LANGUAGES", {"fr": {"language": "Francais", "locale": "fr"}})
def test_get_language_exists():
    assert i18n.get_language("fr") == {"language": "Francais", "locale": "fr"}

@patch("utils.i18n.DEFAULT_LOCALE", "en")
@patch("utils.i18n.LANGUAGES", {"en": {"language": "English", "locale": "en"}})
def test_get_language_does_not_exist():
    assert i18n.get_language("es") == {"language": "English", "locale": "en"}

@patch("utils.i18n.DEFAULT_LOCALE", "en")
def test_get_locale_from_path():
    assert i18n.get_locale_from_path("/fr/path") == "fr"
    assert i18n.get_locale_from_path("/en/path") == "en"
    assert i18n.get_locale_from_path("/es/fr/path") == "en"
    assert i18n.get_locale_from_path("") == "en"
    assert i18n.get_locale_from_path(None) == "en"


@patch("utils.i18n.glob.glob")
@patch("utils.i18n.open")
def test_generate_languages(mock_open, mock_glob):
    mock_glob.return_value = ["i18n/en.json", "i18n/fr.json", "i18n/es.json"]
    mock_open.return_value.__enter__.return_value.read.side_effect = [
        '{"language": "English", "locale": "en"}',
        '{"language": "Francais", "locale": "fr"}',
        '{"language": "Espangnol", "locale": "es"}',
    ]
    assert i18n.generate_languages("i18n/*.json") == {
        "en": {"language": "English", "locale": "en"},
        "fr": {"language": "Francais", "locale": "fr"},
        "es": {"language": "Espangnol", "locale": "es"},
    }