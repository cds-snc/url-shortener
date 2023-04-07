import glob
import json
import os
from enum import Enum


class Locale(str, Enum):
    """
    Enum for the supported locales.  It is expected that for each value in the enum,
    there is a corresponding JSON file in the `api/i18n` folder with the same name.
    """

    def __str__(self):
        return str(self.value)

    en = "en"
    fr = "fr"


DEFAULT_LOCALE = Locale.en


def get_language(locale):
    """Gets the language labels for the given locale"""
    return LANGUAGES[locale] if locale in LANGUAGES else LANGUAGES[DEFAULT_LOCALE]


def get_locale_from_path(path):
    """Gets the locale from the path.  If no locale is found, the default locale is returned."""
    path_parts = path.split("/") if isinstance(path, str) else []
    if len(path_parts) > 1 and any(l.value == path_parts[1] for l in Locale):
        return Locale(path_parts[1])
    return DEFAULT_LOCALE


def generate_languages(locale_files):
    """Generates a dictionary of languages from the JSON files in the i18n folder"""
    languages = {}
    language_list = glob.glob(locale_files)
    for lang in language_list:
        filename = lang.split(os.path.sep)
        lang_code = filename[1].split(".")[0]

        with open(lang, "r", encoding="utf8") as file:
            languages[lang_code] = json.load(file)
    return languages


LANGUAGES = generate_languages("i18n/*.json")
