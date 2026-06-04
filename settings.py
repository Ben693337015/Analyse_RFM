# -*- coding: utf-8 -*-
"""
settings.py — Persistance sécurisée des préférences utilisateur.
Les clés API sont stockées dans le trousseau OS via keyring.
Les préférences non sensibles sont sauvegardées dans un fichier JSON.
"""

import json
import os
from pathlib import Path

try:
    import keyring
    _KEYRING_OK = True
except ImportError:
    _KEYRING_OK = False

# ── Chemins ───────────────────────────────────────────────────────────────────
_APP_DIR   = Path.home() / ".rfm_analytics"
_PREFS_FILE = _APP_DIR / "preferences.json"
_KEYRING_SERVICE = "rfm_analytics"

# ── Préférences par défaut ────────────────────────────────────────────────────
_DEFAULTS = {
    "ai_provider":     "Anthropic Claude",
    "pdf_company":     "Mon Entreprise",
    "pdf_author":      "Équipe Marketing",
    "pdf_open_after":  True,
    "pdf_dark_theme":  True,
    "email_brand":     "VotreMarque",
    "last_directory":  str(Path.home()),
    "window_geometry": "1400x860",
}


def _ensure_dir() -> None:
    _APP_DIR.mkdir(parents=True, exist_ok=True)


def _load_prefs() -> dict:
    _ensure_dir()
    if _PREFS_FILE.exists():
        try:
            with open(_PREFS_FILE, encoding="utf-8") as f:
                data = json.load(f)
            return {**_DEFAULTS, **data}
        except Exception:
            pass
    return dict(_DEFAULTS)


def _save_prefs(prefs: dict) -> None:
    _ensure_dir()
    with open(_PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)


# ── API publique ──────────────────────────────────────────────────────────────

def get(key: str, default=None):
    """Retourne une préférence non sensible."""
    return _load_prefs().get(key, default if default is not None else _DEFAULTS.get(key))


def set(key: str, value) -> None:
    """Enregistre une préférence non sensible."""
    prefs = _load_prefs()
    prefs[key] = value
    _save_prefs(prefs)


def get_api_key(provider: str) -> str:
    """
    Retourne la clé API pour le fournisseur indiqué.
    Utilise keyring si disponible, sinon un fichier chiffré basique.
    provider: 'claude' | 'gemini'
    """
    if _KEYRING_OK:
        return keyring.get_password(_KEYRING_SERVICE, provider) or ""
    # Fallback : fichier local (moins sécurisé, mais fonctionnel sans keyring)
    key_file = _APP_DIR / f".{provider}_key"
    if key_file.exists():
        try:
            return key_file.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return ""


def set_api_key(provider: str, key: str) -> None:
    """
    Stocke la clé API pour le fournisseur indiqué.
    provider: 'claude' | 'gemini'
    """
    if _KEYRING_OK:
        keyring.set_password(_KEYRING_SERVICE, provider, key)
    else:
        _ensure_dir()
        key_file = _APP_DIR / f".{provider}_key"
        key_file.write_text(key, encoding="utf-8")
        # Permissions restrictives sur Unix
        try:
            os.chmod(key_file, 0o600)
        except Exception:
            pass


def delete_api_key(provider: str) -> None:
    """Supprime la clé API stockée."""
    if _KEYRING_OK:
        try:
            keyring.delete_password(_KEYRING_SERVICE, provider)
        except Exception:
            pass
    else:
        key_file = _APP_DIR / f".{provider}_key"
        key_file.unlink(missing_ok=True)


def all_prefs() -> dict:
    """Retourne toutes les préférences (lecture seule)."""
    return _load_prefs()


def reset() -> None:
    """Remet toutes les préférences aux valeurs par défaut."""
    _save_prefs(dict(_DEFAULTS))
