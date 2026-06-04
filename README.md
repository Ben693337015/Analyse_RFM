# RFM Analytics Pro — v2.0

## Structure
```
rfm_app/
├── main.py              # Point d'entrée
├── config.py            # Constantes centralisées
├── settings.py          # Préférences & clés API (keyring)
├── requirements.txt
├── controller/
│   └── app_controller.py
├── services/            # Logique métier pure (testable)
│   ├── rfm_service.py
│   ├── cluster_service.py
│   ├── persona_service.py
│   ├── email_service.py
│   └── pdf_service.py
├── infrastructure/      # I/O (fichiers, API, exports)
│   ├── data_loader.py
│   ├── ai_gateway.py
│   └── export_manager.py
└── views/               # UI Tkinter pure (aucune logique)
    ├── main_window.py
    ├── data_view.py
    ├── chart_view.py
    ├── persona_view.py
    ├── email_view.py
    ├── chat_view.py
    └── pdf_view.py
```

## Installation
```bash
pip install -r requirements.txt
python main.py
```
