# Utilise une image Python légère
FROM python:3.10-slim

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances et installe-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le reste du projet
COPY . .

# Expose le port par défaut de Streamlit
EXPOSE 8501

# Commande pour lancer l'application
CMD ["streamlit", "run", "Accueil.py", "--server.port=8501", "--server.address=0.0.0.0"]