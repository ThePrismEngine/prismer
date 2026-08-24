import gettext
import locale
import os
import logging
from threading import local

logger = logging.getLogger(__name__)

LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")
DOMAIN = "messages"
DEFAULT_LANG = "ru"

_state = local()
_available_languages: set[str] | None = None  # кэш


def discover_languages() -> set[str]:
    global _available_languages
    if _available_languages is not None:
        return _available_languages

    langs: set[str] = set()

    if not os.path.isdir(LOCALE_DIR):
        logger.warning("i18n: locales directory not found: %s", LOCALE_DIR)
        _available_languages = {DEFAULT_LANG}
        return _available_languages

    for entry in os.listdir(LOCALE_DIR):
        lang_dir = os.path.join(LOCALE_DIR, entry, "LC_MESSAGES")
        mo_file = os.path.join(lang_dir, f"{DOMAIN}.mo")

        if os.path.isdir(lang_dir) and os.path.isfile(mo_file):
            langs.add(entry)

    if not langs:
        logger.warning("i18n: no translations found in %s", LOCALE_DIR)

    _available_languages = langs
    logger.info("i18n: discovered languages: %s", sorted(langs))
    return langs


def rescan_languages() -> set[str]:
    global _available_languages
    _available_languages = None
    return discover_languages()


def get_available_languages() -> list[str]:
    return sorted(discover_languages())


def _parse_lang_code(raw: str) -> str | None:
    if not raw:
        return None
    return raw.split("_")[0].split("-")[0].split(".")[0].split("@")[0].strip().lower() or None


def _is_available(code: str | None) -> bool:
    if not code:
        return False
    return code in discover_languages()


def _lang_from_env() -> str | None:
    available = discover_languages()

    language_var = os.environ.get("LANGUAGE", "")
    if language_var:
        for part in language_var.split(":"):
            code = _parse_lang_code(part)
            if code in available:
                return code

    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        code = _parse_lang_code(os.environ.get(var, ""))
        if code in available:
            return code

    return None


def _lang_from_system() -> str | None:
    available = discover_languages()

    for getter in (locale.getlocale, getattr(locale, "getdefaultlocale", None)):
        if getter is None:
            continue
        try:
            loc = getter()
            if loc and loc[0]:
                code = _parse_lang_code(loc[0])
                if code in available:
                    return code
        except (ValueError, TypeError):
            continue

    return None


def detect_language() -> str:
    explicit = getattr(_state, "explicit_lang", None)
    if explicit:
        return explicit

    env = _lang_from_env()
    if env:
        return env

    sys_lang = _lang_from_system()
    if sys_lang:
        return sys_lang

    return DEFAULT_LANG


def _build_translation(lang: str):
    return gettext.translation(DOMAIN, localedir=LOCALE_DIR, languages=[lang], fallback=True)


def set_language(lang: str) -> None:
    code = _parse_lang_code(lang)
    available = discover_languages()

    if code not in available:
        logger.warning(
            "i18n: language '%s' not available (found: %s). Falling back to '%s'.",
            lang, sorted(available), DEFAULT_LANG
        )
        code = DEFAULT_LANG

    _state.explicit_lang = code
    _state.current_lang = code
    _state.translation = _build_translation(code)
    logger.info("i18n: language set to '%s'", code)


def get_language() -> str:
    return getattr(_state, "current_lang", DEFAULT_LANG)


def _(message: str) -> str:
    t = getattr(_state, "translation", None)
    return t.gettext(message) if t else message


def ngettext(singular: str, plural: str, n: int) -> str:
    t = getattr(_state, "translation", None)
    if t is None:
        return singular if n == 1 else plural
    return t.ngettext(singular, plural, n)


def pgettext(context: str, message: str) -> str:
    t = getattr(_state, "translation", None)
    return t.pgettext(context, message) if t else message


def _init():
    lang = detect_language()
    _state.current_lang = lang
    _state.translation = _build_translation(lang)
    logger.info("i18n: initialized with language '%s'", lang)

_init()