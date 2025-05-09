import streamlit as st

# Liste des modèles IA disponibles par fournisseur
MODELS = {
    "OpenAI": ["gpt-4", "gpt-4o", "gpt-3.5-turbo"],
    "Anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229"],
    "Gemini": ["gemini-pro", "gemini-pro-vision"]
}

def select_model():
    provider = st.selectbox("Fournisseur IA", list(MODELS.keys()))
    model = st.selectbox("Modèle", MODELS[provider])
    return provider, model

# Prompts pour la génération IA
def get_title_prompt(contexte_entreprise, contexte_campagne, adgroup, keywords):
    return f"""
Tu es un expert en rédaction publicitaire Google Ads.
Voici les informations à connaître :
Entreprise : {contexte_entreprise}
Campagne : {contexte_campagne}
Groupe d'annonces : {adgroup}
Mots clés : {keywords}

Ta mission est de générer une liste JSON contenant **exactement 10 titres** de 30 caractères maximum chacun, parfaitement adaptés.
Réponds uniquement avec un tableau JSON de chaînes, sans autre texte.
"""

def get_desc_prompt(contexte_entreprise, contexte_campagne, adgroup, keywords):
    return f"""
Tu es un expert en rédaction publicitaire Google Ads.
Voici les informations à connaître :
Entreprise : {contexte_entreprise}
Campagne : {contexte_campagne}
Groupe d'annonces : {adgroup}
Mots clés : {keywords}

Ta mission est de générer une liste JSON contenant **exactement 5 descriptions** de 90 caractères maximum chacune.
Réponds uniquement avec un tableau JSON de chaînes, sans autre texte.
"""
