# -*- coding: utf-8 -*-
"""
main.py — Point d'entrée unique.

Flux :
  1. LoginWindow s'ouvre (racine Tk)
  2. Auth réussie → LoginWindow se détruit → user stocké
  3. AppController / MainWindow s'ouvre
  4. Logout → MainWindow se détruit → retour à l'étape 1 (nouvelle LoginWindow)
  5. Fermeture normale (X) → fin du programme
"""

import warnings
warnings.filterwarnings("ignore")

import sys
import os

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)


def main() -> None:
    while True:
        # ── Étape 1 : Authentification ──
        from views.login_view import LoginWindow
        login_win = LoginWindow()
        login_win.mainloop()

        user = login_win.authenticated_user
        if not user:
            # Fenêtre fermée sans connexion → quitter
            break

        # ── Étape 2 : Application principale ──
        from controller.app_controller import AppController
        app = AppController(current_user=user)
        app.run()

        # Si on revient ici c'est un logout → reboucler vers le login
        # Si c'est une fermeture normale (X sur MainWindow), break
        if not app.is_logout:
            break


if __name__ == "__main__":
    main()
