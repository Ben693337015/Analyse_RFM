# -*- coding: utf-8 -*-
"""
i18n.py — Système d'internationalisation (i18n) léger pour BEST_RFM_v2.

Objectif :
  Externaliser toutes les chaînes affichées à l'utilisateur (labels, messages,
  titres, tooltips) dans des fichiers de traduction JSON plutôt que de les
  coder en dur dans les vues/services. Permet d'ajouter une langue sans
  toucher au code Python.

Usage dans le code :
    from i18n import _

    label = _("login.title")                      # "Connexion"
    msg   = _("data.loaded", n=120, clients=45)    # interpolation par nom

Structure des fichiers :
  locales/fr.json   — langue de référence (clés + traductions françaises)
  locales/en.json    — traductions anglaises
  (ajout d'une langue = copier fr.json, traduire les valeurs, déclarer
   le code dans AVAILABLE_LANGUAGES)

Format de clé : "domaine.sous_clé" en snake_case, regroupé par écran/module
  (ex: "login.title", "login.btn_submit", "gridsearch.error_k_max")

Interpolation :
  Les valeurs peuvent contenir des placeholders Python str.format() :
    "data.loaded": "{n} transactions chargées pour {clients} clients"
  Appel : _("data.loaded", n=120, clients=45)

Fallback :
  Si une clé est absente de la langue active, on retombe sur le français
  (langue de référence). Si absente des deux, on retourne la clé elle-même
  entre crochets pour repérer facilement les chaînes non traduites
  pendant le développement : "[login.titre_manquant]".
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

_LOCALES_DIR = Path(__file__).parent / "locales"
_REFERENCE_LANG = "fr"

# Langues disponibles dans l'application — code ISO 639-1 → nom affiché
AVAILABLE_LANGUAGES = {
    "fr": "Français",
    "en": "English",
}

_lock = threading.Lock()
_cache: dict[str, dict] = {}          # {lang_code: {key: value}}
_current_lang: str = _REFERENCE_LANG  # langue active (modifiable via set_language)


def _load_lang_file(lang_code: str) -> dict:
    """Charge et met en cache le fichier JSON d'une langue. {} si absent/invalide."""
    if lang_code in _cache:
        return _cache[lang_code]

    path = _LOCALES_DIR / f"{lang_code}.json"
    if not path.exists():
        _cache[lang_code] = {}
        return {}

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        _cache[lang_code] = data
        return data
    except Exception:
        _cache[lang_code] = {}
        return {}


def set_language(lang_code: str) -> None:
    """
    Change la langue active de l'application.
    Si le code n'est pas dans AVAILABLE_LANGUAGES, ignore silencieusement
    (garde la langue précédente) pour ne jamais planter l'UI sur une
    préférence corrompue.
    """
    global _current_lang
    with _lock:
        if lang_code in AVAILABLE_LANGUAGES:
            _current_lang = lang_code
            _load_lang_file(lang_code)   # précharge / met en cache


def get_language() -> str:
    """Retourne le code de la langue actuellement active."""
    return _current_lang


def reload_cache() -> None:
    """Vide le cache et recharge les fichiers de langue depuis le disque.
    Utile si les fichiers JSON sont modifiés pendant l'exécution (dev/debug)."""
    with _lock:
        _cache.clear()


def _(key: str, **kwargs) -> str:
    """
    Fonction de traduction principale. À importer partout où une chaîne
    utilisateur est affichée :   from i18n import _

    Args:
        key: clé de traduction, ex "login.title"
        **kwargs: valeurs d'interpolation pour les placeholders {nom}

    Retourne la chaîne traduite, avec fallback français puis fallback
    "[clé]" si introuvable dans les deux langues (pour repérer les trous
    de traduction sans jamais planter l'affichage).
    """
    lang_data = _load_lang_file(_current_lang)
    template = lang_data.get(key)

    if template is None and _current_lang != _REFERENCE_LANG:
        ref_data = _load_lang_file(_REFERENCE_LANG)
        template = ref_data.get(key)

    if template is None:
        return f"[{key}]"

    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            # Placeholder manquant dans les kwargs → retourne le template brut
            # plutôt que de planter l'affichage utilisateur.
            return template

    return template


def init_from_preferences() -> None:
    """
    Initialise la langue active à partir des préférences utilisateur
    (settings.py). À appeler une fois au démarrage de l'application,
    avant la création de la première fenêtre.
    """
    try:
        import settings
        lang = settings.get("language", _REFERENCE_LANG)
    except Exception:
        lang = _REFERENCE_LANG
    set_language(lang)
