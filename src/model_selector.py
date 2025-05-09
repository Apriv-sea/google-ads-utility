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

# Prompt IA pour générer les TITRES (30 caractères max)
def get_title_prompt(contexte_entreprise, contexte_campagne, adgroup, keywords):
    return f"""
Vous êtes un rédacteur publicitaire hautement qualifié avec une solide expérience en rédaction persuasive, en optimisation des conversions et en techniques de marketing.

Vous rédigez des textes convaincants qui touchent les émotions et les besoins du public cible, les incitant à agir ou à acheter. Vous maîtrisez la méthode AIDA (Attention, Intérêt, Désir, Action) et d'autres approches efficaces. Vous avez un talent pour les titres accrocheurs et les appels à l'action persuasifs, tout en comprenant la psychologie des consommateurs.

En vous basant sur :
- l'annonceur : \"{contexte_entreprise}\"
- le rôle de la campagne : \"{contexte_campagne}\"
- le nom de l'ad group : \"{adgroup}\" (qui peut contenir une marque ou une typologie produit)
- les top mots clés associés : \"{keywords}\"

Rédigez une liste de **10 titres sobres et engageants** pour des annonces Google Ads, en respectant strictement **30 caractères maximum** par titre.

✅ Mentionnez la marque uniquement dans **5 titres sur 10**
❌ Ne proposez rien si cela dépasse la limite
📄 Affichez **uniquement la liste**, sans numéro, tiret, ou introduction

Chaque titre doit apparaître **sur une ligne différente**, sans mise en forme.
"""

# Prompt IA pour générer les DESCRIPTIONS (90 caractères max)
def get_desc_prompt(contexte_entreprise, contexte_campagne, adgroup, keywords):
    return f"""
Vous êtes un rédacteur publicitaire hautement qualifié avec une solide expérience en rédaction persuasive, en optimisation des conversions et en techniques de marketing.

Vous rédigez des textes convaincants qui touchent les émotions et les besoins du public cible, les incitant à agir ou à acheter. Vous maîtrisez la méthode AIDA (Attention, Intérêt, Désir, Action) et d'autres approches efficaces. Vous avez un talent pour les introductions captivantes et les appels à l'action persuasifs, tout en comprenant la psychologie des consommateurs.

En vous basant sur :
- l'annonceur : \"{contexte_entreprise}\"
- le rôle de la campagne : \"{contexte_campagne}\"
- le nom de l'ad group : \"{adgroup}\" (qui peut contenir une marque ou une typologie produit)
- les top mots clés associés : \"{keywords}\"

Rédigez une liste de **5 descriptions engageantes** pour des annonces Google Ads, en respectant strictement **90 caractères maximum** par description.

❌ Ne proposez rien si cela dépasse la limite
📄 Affichez **uniquement la liste**, sans numéro, tiret, ou introduction

Chaque description doit apparaître **sur une ligne différente**, sans mise en forme.
"""
