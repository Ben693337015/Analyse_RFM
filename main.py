# -*- coding: utf-8 -*-
"""
main.py — Point d'entrée de l'application RFM Analytics.
Crée l'AppController et lance la boucle Tkinter.
"""

import warnings
warnings.filterwarnings("ignore")

from controller.app_controller import AppController


def main() -> None:
    app = AppController()
    app.run()


if __name__ == "__main__":
    main()
