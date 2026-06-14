# -*- coding: utf-8 -*-
"""
config.py — Source unique de vérité.
Palette, polices, métadonnées personas, modèles IA, formats export.
Aucun import tkinter — importable dans services et tests.
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
    # Définitions RFM standardisées — cohérentes avec les critères de segmentation
    # Champions    : R élevée + F élevée + M élevé  (meilleurs sur les 3 axes)
    # Fidèles      : R bonne  + F élevée + M moyen–élevé  (acheteurs réguliers reconnus)
    # Récurrents   : R moyenne + F moyenne + M moyen  (acheteurs habituels sans pic de valeur)
    #                ≠ Fidèles : différence sur la Récence et le Montant, pas la Fréquence seule
    # Potentiels   : R récente + F faible (1–2 achats) + M correct  (récents à fidéliser)
    # Nouveaux     : R très récente + F = 1 + M faible–moyen  (1 seul achat, onboarding)
    # Perdus       : R très ancienne + F quelconque  (inactifs longue durée)
    "Champions":          ("🏆", "#38e8a0", "R↑ F↑ M↑ — VIP, ambassadeurs, accès exclusifs"),
    "Clients Fidèles":    ("💎", "#4da6ff", "R↑ F↑ M↑ — Fidélité, upselling, reconnaissance"),
    "Clients Récurrents": ("🔁", "#00d4ff", "R≈ F≈ M≈ — Abonnement, cross-sell, montée en valeur"),
    "Clients Potentiels": ("🎯", "#f9c74f", "R↑ F faible M≈ — Cross-sell 2e/3e achat, découverte"),
    "Nouveaux Clients":   ("🆕", "#ff9f43", "R↑↑ F=1 M≈ — Onboarding, déclenchement 2e achat"),
    "Clients Perdus":     ("🔄", "#ff5c7a", "R↓↓ — Reconquête ciblée ou archivage"),
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
        # [FIX 3] Le vrai risque d'un Champion (R↑ F↑ M↑) n'est PAS le départ
        # silencieux immédiat — sa récence actuelle est excellente par définition.
        # Le risque réel est la sur-sollicitation (fatigue marketing) qui dégrade
        # l'expérience. C'est dans "Clients Fidèles" (R qui remonte) que guette
        # le départ silencieux.
        "kpi":  "Objectif : maintenir récence < 30 j · upsell +20 % · NPS > 9",
        "risk": "⚠️  Risque : sur-sollicitation & fatigue marketing — espacer les contacts, prioriser la qualité sur la quantité",
    },
    "Clients Fidèles": {
        "actions": [
            "💎 Carte de fidélité avec points doublés ce mois",
            "📈 Offres de montée en gamme (upselling ciblé)",
            "🎂 Email personnalisé anniversaire client + réduction",
            "🔔 Alertes push personnalisées sur les nouvelles gammes",
        ],
        # [FIX 2] Clients Fidèles = R bonne + F élevée + M moyen–élevé.
        # Différence avec Récurrents : récence légèrement meilleure ET montant plus fort.
        # Stratégie = montée en valeur (upsell), vs cross-sell pur pour les Récurrents.
        # [FIX 3] Le "départ silencieux" guette ICI : récence qui remonte discrètement.
        "kpi":  "Objectif : fréquence +1 visite/mois · panier +15 % · récence < 45 j",
        "risk": "⚠️  Risque : départ silencieux — surveiller la récence (>45 j = signal d'alerte précoce vers Récurrents)",
    },
    "Clients Récurrents": {
        "actions": [
            "🔁 Abonnement ou livraison automatique récurrente",
            "🛍️  Cross-selling : produits complémentaires à chaque achat",
            "⭐ Programme de récompenses par paliers pour monter en Fidèle",
            "📊 Dashboard client 'votre historique & économies réalisées'",
        ],
        # [FIX 2] Clients Récurrents = R moyenne + F moyenne + M moyen.
        # Distinct des Fidèles par une récence moins fraîche et un montant moindre.
        # Objectif : faire monter ces clients vers le segment Fidèles (F et M ↑).
        "kpi":  "Objectif : panier moyen +10 % · LTV +25 % · migration vers Fidèles sur 6 mois",
        "risk": "⚠️  Risque : stagnation si aucune nouveauté ni incentive à monter en valeur",
    },
    "Clients Potentiels": {
        "actions": [
            "🎯 Cross-selling : présenter des gammes complémentaires à leur 1er–2e achat",
            "📧 Séquence email 3 temps : découverte → valeur → offre 2e/3e achat",
            # [FIX 4] Suppression de la relance panier abandonné : donnée comportementale
            # (Web Analytics) absente d'un fichier transactionnel RFM.
            # Remplacée par des actions exploitables depuis l'historique d'achats.
            "🎁 Offre de découverte gamme premium : -10 % sur une catégorie non encore achetée",
            "📞 Appel commercial si montant moyen > seuil VIP",
        ],
        # [FIX 4] KPI ancré sur les données transactionnelles (fréquence, montant)
        # et non sur des métriques comportementales non disponibles (panier abandonné).
        "kpi":  "Objectif : déclencher 2e–3e achat · convertir 30 % en Récurrents sur 90 j",
        "risk": "⚠️  Risque : sur-sollicitation → désabonnement si séquence trop agressive",
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
    "Nouveaux Clients": {
        "actions": [
            "🆕 Séquence d'onboarding transactionnel (email J+1, J+3, J+7)",
            "🎓 Guide d'utilisation produit & FAQ interactive",
            # [FIX 1] L'offre -10% sur le 2e achat est correcte et intentionnelle :
            # son succès doit se mesurer par la MIGRATION du client vers Clients Potentiels
            # ou Récurrents (la fréquence passe de 1 à 2+). Cela est explicité dans le KPI.
            "🤝 Offre de bienvenue : -10 % sur le 2e achat pour déclencher la récurrence",
            "📱 Invitation à s'abonner à la newsletter + notification push",
        ],
        # [FIX 1] KPI reformulé : le succès = migration hors du segment.
        # Un Nouveau Client qui réalise son 2e achat sort du segment par définition
        # (fréquence passe à 2 → Potentiel ou Récurrent). C'est le but recherché.
        "kpi":  "Objectif : déclencher le 2e achat dans les 30 j · succès = migration vers Clients Potentiels/Récurrents",
        "risk": "⚠️  Risque : churn après 1er achat si mauvaise expérience produit ou silence post-achat",
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
#  SECTIONS RAPPORT PDF
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

# ── DEVISE (modifié dynamiquement par le détecteur) ──────────────────────────
CURRENCY_SYMBOL = "€"   # valeur par défaut, écrasée à la détection
