# -*- coding: utf-8 -*-
"""
config.py — Constantes globales centralisées.
Source unique de vérité pour la palette, les polices et les métadonnées des personas.
Aucun import tkinter ici — ce fichier est importable dans les services et tests.
"""

# ─────────────────────────────────────────────
#  PALETTE — Thème Bleu Pro
# ─────────────────────────────────────────────
BG_DARK   = "#050d1a"
BG_PANEL  = "#0a1628"
BG_CARD   = "#0f2040"
BG_INPUT  = "#112248"
ACCENT    = "#4da6ff"
ACCENT2   = "#00d4ff"
ACCENT3   = "#38e8a0"
TEXT_MAIN = "#e4eeff"
TEXT_SUB  = "#6a8cba"
SUCCESS   = "#38e8a0"
WARNING   = "#f9c74f"
DANGER    = "#ff5c7a"
BTN_RUN   = "#1a6dff"
BTN_HOVER = "#2d7dff"

# ─────────────────────────────────────────────
#  POLICES
# ─────────────────────────────────────────────
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_H2    = ("Segoe UI", 13, "bold")
FONT_H3    = ("Segoe UI", 10, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 9)

# ─────────────────────────────────────────────
#  PERSONAS
# ─────────────────────────────────────────────
PERSONA_INFO = {
    "Champions":          ("🏆", "#38e8a0", "Programmes VIP, produits exclusifs, ambassadeurs"),
    "Clients Fidèles":    ("💎", "#4da6ff", "Programmes de fidélité, upselling, récompenses"),
    "Clients Potentiels": ("🎯", "#f9c74f", "Offres personnalisées, campagnes de réactivation"),
    "Clients Perdus":     ("🔄", "#ff5c7a", "Campagnes de reconquête, offres de retour"),
    "Clients Récurrents": ("🔁", "#00d4ff", "Cross-selling, augmentation panier moyen"),
    "Nouveaux Clients":   ("🆕", "#ff9f43", "Onboarding, offres de bienvenue, engagement"),
}

PERSONA_ROW_COLORS = {
    "Champions":          "#0a2e1a",
    "Clients Fidèles":    "#0a1a3d",
    "Clients Potentiels": "#2e2800",
    "Clients Perdus":     "#2e0a14",
    "Clients Récurrents": "#082a38",
    "Nouveaux Clients":   "#2e1800",
}

PERSONA_ORDER = [
    "Champions", "Clients Fidèles", "Clients Récurrents",
    "Clients Potentiels", "Nouveaux Clients", "Clients Perdus",
]

PERSONA_RECO = {
    "Champions": {
        "actions": [
            "🏅 Programme VIP avec accès anticipé aux nouveautés",
            "🎁 Cadeaux exclusifs & invitations événements privés",
            "📣 Programme ambassadeur : parrainage & co-création",
            "💬 Enquête satisfaction pour co-construire l'offre",
        ],
        "kpi":  "Objectif : maintenir récence < 30 j, upsell +20 %",
        "risk": "⚠️  Risque : départ silencieux — surveiller la récence",
    },
    "Clients Fidèles": {
        "actions": [
            "💎 Carte de fidélité avec points doublés ce mois",
            "📈 Offres de montée en gamme (upselling ciblé)",
            "🎂 Email personnalisé anniversaire client + réduction",
            "🔔 Alertes push sur les articles consultés sans achat",
        ],
        "kpi":  "Objectif : fréquence +1 visite/mois, panier +15 %",
        "risk": "⚠️  Risque : attrition si pas de reconnaissance",
    },
    "Clients Potentiels": {
        "actions": [
            "🎯 Offre personnalisée basée sur l'historique de navigation",
            "📧 Séquence email 3 temps : intérêt → valeur → offre",
            "🛒 Relance panier abandonné avec réduction 5 %",
            "📞 Appel commercial si panier moyen > seuil VIP",
        ],
        "kpi":  "Objectif : convertir 30 % en Fidèles sur 90 j",
        "risk": "⚠️  Risque : sur-sollicitation → désabonnement",
    },
    "Clients Perdus": {
        "actions": [
            "🔄 Email 'Vous nous manquez' + bon de réduction 15 %",
            "📋 Enquête de départ : comprendre la raison d'inactivité",
            "🎁 Offre de retour exclusive limitée dans le temps",
            "🚫 Si aucune réaction après 3 relances : archiver",
        ],
        "kpi":  "Objectif : réactiver 10–15 % dans les 60 jours",
        "risk": "⚠️  Risque : nuire à la réputation si trop insistant",
    },
    "Clients Récurrents": {
        "actions": [
            "🔁 Abonnement ou livraison automatique récurrente",
            "🛍️  Cross-selling : produits complémentaires à chaque achat",
            "⭐ Programme de récompenses par paliers de fidélité",
            "📊 Dashboard client 'votre historique & économies réalisées'",
        ],
        "kpi":  "Objectif : augmenter panier moyen +10 %, LTV +25 %",
        "risk": "⚠️  Risque : stagnation si pas de nouveautés proposées",
    },
    "Nouveaux Clients": {
        "actions": [
            "🆕 Séquence d'onboarding (email J+1, J+3, J+7)",
            "🎓 Guide d'utilisation produit & FAQ interactive",
            "🤝 Offre de bienvenue : -10 % sur le 2ème achat",
            "📱 Invitation à télécharger l'appli + notification push",
        ],
        "kpi":  "Objectif : 2ème achat dans les 30 j, NPS > 8",
        "risk": "⚠️  Risque : churn après 1er achat si mauvaise expérience",
    },
}

# ─────────────────────────────────────────────
#  MODÈLES IA
# ─────────────────────────────────────────────
CLAUDE_MODEL   = "claude-sonnet-4-20250514"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
GEMINI_MODEL   = "gemini-2.5-flash"
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:streamGenerateContent?alt=sse&key={key}"
)
AI_PROVIDERS = ["Anthropic Claude", "Google Gemini"]

# ─────────────────────────────────────────────
#  FORMATS EXPORT EMAIL
# ─────────────────────────────────────────────
EMAIL_EXPORT_FORMATS = [
    ("mailchimp", "Mailchimp (.csv)"),
    ("brevo",     "Brevo / Sendinblue (.csv)"),
    ("generic",   "Générique (.csv)"),
    ("html",      "Template HTML (.html)"),
]

# ─────────────────────────────────────────────
#  SECTIONS RAPPORT PDF  (key, label, default, ~pages)
# ─────────────────────────────────────────────
PDF_SECTIONS = [
    ("cover",           "Page de garde",             True,  1),
    ("sommaire",        "Table des matières",         True,  1),
    ("kpis",            "KPIs globaux",               True,  1),
    ("distrib",         "Distributions RFM",          True,  1),
    ("elbow",           "Coude & GridSearch",         True,  1),
    ("clusters",        "Visualisation des segments", True,  1),
    ("personas_chart",  "Répartition & CA personas",  True,  1),
    ("personas_detail", "Fiches personas & recos",    True,  2),
    ("top20",           "Top 20 clients",             True,  1),
    ("tableau",         "Extrait tableau complet",    True,  2),
]
