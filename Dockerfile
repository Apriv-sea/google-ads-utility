FROM python:3.10-slim

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y build-essential

# Définir le dossier de travail
WORKDIR /app

# Copier tous les fichiers du projet dans l'image
COPY . .

# Installer les packages Python
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run attend que l’app écoute sur ce port
EXPOSE 8080

# Lancer Streamlit sur le bon port
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.enableCORS=false"]
