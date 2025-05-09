# Google Ads AI Assistant

Un outil d’aide à la génération de titres et descriptions pour campagnes Google Ads via IA (OpenAI, Claude, Gemini).

## Déploiement
1. Remplacez `secrets/credentials.json` par vos identifiants OAuth2.
2. Construisez et déployez sur Google Cloud Run via :
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/google-ads-ai-assistant
gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/google-ads-ai-assistant --platform managed --region YOUR_REGION --allow-unauthenticated
```
3. L’URL vous sera fournie.
