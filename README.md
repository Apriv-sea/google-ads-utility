# 🧠 Google Ads Utility – Générateur IA pour Titres & Descriptions Google Ads

**Google Ads Utility** est un assistant intelligent qui vous aide à générer rapidement des titres et descriptions optimisés pour vos annonces Google Ads, en combinant :

- ✍️ Rédaction persuasive avec méthode AIDA
- 🤖 IA multi-modèles (OpenAI, Anthropic, Gemini)
- 📄 Intégration automatique avec Google Sheets
- 🔐 Authentification Google OAuth sécurisée

---

## 🚀 Fonctionnalités principales

- 🔐 Connexion avec votre compte Google
- 🧩 Ajout et gestion de vos propres clés API IA (OpenAI, Anthropic, Gemini)
- 📁 Création de dossiers clients avec contexte entreprise, campagne et ad group
- 📄 Génération automatique d’un template Google Sheets pour saisir les données
- 🧠 Génération IA de 10 titres et 5 descriptions **personnalisés et formatés**
- 💾 Sauvegarde des résultats dans la feuille Google associée

---

## 🛠️ Déploiement avec Google Cloud Run

1. **Créer une app OAuth 2.0** sur [console.cloud.google.com](https://console.cloud.google.com/apis/credentials)
    - Ajouter l’URL Cloud Run comme URI de redirection autorisé

2. **Configurer `.streamlit/secrets.toml` :**

```toml
[oauth]
client_id = "TON_CLIENT_ID.apps.googleusercontent.com"
client_secret = "TON_CLIENT_SECRET"
redirect_uri = "https://TON_PROJECT_ID.a.run.app"
