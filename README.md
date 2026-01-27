# 📝 Todo App

Une application Todo simple avec un backend **FastAPI** et un frontend en **HTML / CSS / JavaScript** vanilla.

Ce projet a pour but de pratiquer :
- une API REST avec FastAPI
- un frontend modulaire sans framework
- la communication frontend / backend
- la structuration d’un projet fullstack

---

## 🚀 Fonctionnalités

- Création, modification et suppression de tâches
- Marquer une tâche comme complétée
- Gestion de listes de tâches
- Filtrage :
  - toutes les tâches
  - tâches en cours
  - tâches complétées
- Interface en 3 panneaux :
  - listes (gauche)
  - tâches (centre)
  - détails / édition (droite)

---

## 🛠️ Stack technique

### Backend
- Python
- FastAPI
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript (ES Modules, sans framework)

---

## 📁 Structure du projet

```text
TodoApp/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── base.css
│   └── js/
│       ├── main.js
│       ├── api/
│       └── ui/
│
└── README.md
