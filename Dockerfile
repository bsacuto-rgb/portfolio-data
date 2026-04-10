# 1. Utilise une image Python standard (un peu plus lourde mais contient déjà les outils de base)
FROM python:3.10

# 2. Dossier de travail
WORKDIR /app

# 3. On copie le fichier des dépendances
COPY requirements.txt .

# 4. Installation des bibliothèques
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie du code
COPY . .

# 6. Port
EXPOSE 8501

# 7. Lancement
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]