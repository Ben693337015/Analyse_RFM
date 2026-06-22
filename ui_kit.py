# -*- coding: utf-8 -*-
"""
ui_kit.py — Composants UI partagés pour le thème "Pastel Bleu Marine".

customtkinter ne supporte pas le box-shadow CSS. Ce module simule :
  - des ombres douces  : superposition de cadres (frames) légèrement décalés
                         et teintés (SHADOW_SOFT / SHADOW_MED), créant un halo
                         derrière les cartes et les boutons.
  - des transitions fluides : interpolation de couleur image par image
                         (15 pas, ~150ms) au survol/relâchement des boutons,
                         au lieu d'un changement de couleur instantané.

Composants exportés :
  - SoftButton(parent, text, command, **kw)   : bouton avec halo + transition
  - SoftCard(parent, **kw)                    : conteneur "carte" avec halo
  - elevate(widget, ...)                      : applique un halo à un widget existant
"""

import customtkinter as ctk
from config import (
    BG_CARD, BORDER_SOFT, SHADOW_SOFT, SHADOW_MED,
    ACCENT, NAVY_SOFT,
)

_ANIM_STEPS    = 12     # nombre de pas d'interpolation
_ANIM_INTERVAL = 12     # ms entre chaque pas (~150ms au total)


# ── Interpolation de couleur ────────────────────────────────────────────────

def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)


def _lerp_color(c1: str, c2: str, t: float) -> str:
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    return _rgb_to_hex((
        r1 + (r2 - r1) * t,
        g1 + (g2 - g1) * t,
        b1 + (b2 - b1) * t,
    ))


# ── Bouton avec halo + transition fluide ────────────────────────────────────

class SoftButton(ctk.CTkFrame):
    """
    Bouton avec un halo doux (simule un box-shadow) et une transition de
    couleur fluide au survol/relâchement (au lieu d'un switch instantané).

    Usage : identique à CTkButton (text, command, height, font, ...).
    """

    def __init__(self, parent, text="", command=None,
                 height=46, width=None,
                 fg_color=ACCENT, hover_color=NAVY_SOFT,
                 text_color="white", font=None,
                 corner_radius=14, shadow_color=SHADOW_MED,
                 border_width=0, border_color=None,
                 variant="filled",  # "filled" ou "ghost"
                 **kwargs):
        # Le halo : un cadre légèrement plus grand, teinté, derrière le bouton.
        super().__init__(parent, fg_color="transparent", corner_radius=corner_radius)

        self._fg_color    = fg_color
        self._hover_color = hover_color
        self._command     = command
        self._anim_job     = None
        self._anim_step    = 0
        self._variant      = variant

        # Halo (visible seulement pour les boutons "filled" pleins)
        if variant == "filled":
            halo = ctk.CTkFrame(self, fg_color=shadow_color,
                                 corner_radius=corner_radius + 3)
            halo.place(x=0, y=3, relwidth=1, relheight=1)

        self._btn = ctk.CTkButton(
            self, text=text, command=self._on_click,
            height=height, width=width or 0,
            fg_color=fg_color if variant == "filled" else "transparent",
            hover_color=fg_color if variant == "filled" else "#eef2fa",
            text_color=text_color if variant == "filled" else fg_color,
            font=font or ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=border_color,
        )
        self._btn.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._btn.bind("<Enter>", self._on_enter)
        self._btn.bind("<Leave>", self._on_leave)
        self.bind("<Destroy>", self._on_destroy)

        if width:
            self.configure(width=width)
        self.configure(height=height + (3 if variant == "filled" else 0))

    def _on_destroy(self, _evt=None):
        if self._anim_job:
            try:
                self.after_cancel(self._anim_job)
            except Exception:
                pass
            self._anim_job = None

    def _on_click(self):
        if self._command:
            self._command()

    def _on_enter(self, _evt=None):
        if self._variant != "filled":
            return
        self._animate_to(self._hover_color)

    def _on_leave(self, _evt=None):
        if self._variant != "filled":
            return
        self._animate_to(self._fg_color)

    def _animate_to(self, target_color: str):
        if self._anim_job:
            self.after_cancel(self._anim_job)
        start_color = self._btn.cget("fg_color")
        if not isinstance(start_color, str) or not start_color.startswith("#"):
            start_color = self._fg_color
        steps = _ANIM_STEPS

        def _step(i=0):
            if not self.winfo_exists():
                self._anim_job = None
                return
            t = i / steps
            color = _lerp_color(start_color, target_color, t)
            try:
                self._btn.configure(fg_color=color, hover_color=color)
            except Exception:
                self._anim_job = None
                return
            if i < steps:
                self._anim_job = self.after(_ANIM_INTERVAL, lambda: _step(i + 1))
            else:
                self._anim_job = None

        _step()

    def configure(self, **kwargs):
        # Permet btn.configure(text=..., state=...) comme un CTkButton classique.
        passthrough = {}
        for key in ("text", "state", "command", "font", "text_color"):
            if key in kwargs:
                passthrough[key] = kwargs.pop(key)
        if passthrough:
            self._btn.configure(**passthrough)
        if kwargs:
            super().configure(**kwargs)

    def cget(self, key):
        if key in ("text", "state", "font", "text_color"):
            return self._btn.cget(key)
        return super().cget(key)


# ── Carte avec halo doux ─────────────────────────────────────────────────────

class SoftCard(ctk.CTkFrame):
    """
    Conteneur "carte" blanc avec un léger halo derrière (simule un box-shadow
    doux) et une bordure très fine. À utiliser comme un CTkFrame classique :
    le contenu se place dans `card.body` (avec .pack(), qui dimensionne
    automatiquement la carte à la taille de son contenu).
    """

    def __init__(self, parent, width=500, corner_radius=20,
                 shadow_color=SHADOW_SOFT, fg_color=BG_CARD,
                 border_color=BORDER_SOFT, border_width=1, **kwargs):
        super().__init__(parent, fg_color="transparent")

        # Le halo est un cadre de fond, en arrière-plan, légèrement décalé.
        # Il suit automatiquement la taille de `self` (le conteneur extérieur),
        # qui elle-même se dimensionne sur la taille réelle de `body` (voir plus bas).
        self._halo = ctk.CTkFrame(self, fg_color=shadow_color,
                                   corner_radius=corner_radius + 4)
        self._halo.place(x=0, y=6, relwidth=1, relheight=1)

        # `body` est empaqueté normalement (pack), donc il prend la taille de
        # son contenu réel — c'est lui qui détermine la taille de la carte.
        self.body = ctk.CTkFrame(self, fg_color=fg_color, corner_radius=corner_radius,
                                  border_width=border_width, border_color=border_color,
                                  width=width, **kwargs)
        self.body.pack(fill="both", expand=True)

        if width:
            self.configure(width=width)
