# portfolio-data
Là où je montre mes compètences.

# 📊 Portfolio Data Analyst & Engineering

Ceci est mon portfolio interactif développé avec **Streamlit** et conteneurisé avec **Docker**.

## 🚀 Objectif
Démontrer mes compétences en cycle de vie de la donnée : de l'extraction (APIs/Kaggle) jusqu'au déploiement en production.

## 🛠️ Stack Technique
- **Interface :** Streamlit
- **Traitement :** Pandas, Python 3.10
- **DevOps :** Docker, GitHub Actions
- **Cloud :** Streamlit Cloud

## 🏗️ Structure du Projet
- `app.py` : Application principale
- `Dockerfile` : Configuration pour la conteneurisation
- `requirements.txt` : Dépendances du projet

## ⚙️ Installation Locale (Docker)
```bash
docker build -t portfolio-app .
docker run -p 8501:8501 portfolio-app