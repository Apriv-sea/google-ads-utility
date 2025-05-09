
# main.py — assistant structuré avec menu latéral
import streamlit as st
from model_selector import select_model
from context_storage import save_client_context, load_client_context
from auth import load_google_credentials
from sheets import create_template_sheet
from generation import generate_ads_for_sheet

st.set_page_config(page_title="Google Ads AI Assistant", layout="wide")

# --- SESSION INIT ---
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧭 Navigation")
    menu = st.radio("Aller vers :", ["Accueil", "Mon compte", "Mes clients"])
    if st.session_state.user_email:
        if st.button("🚪 Se déconnecter"):
            st.session_state.clear()
            st.experimental_rerun()
    st.session_state.page = menu

# --- ACCUEIL ---
if st.session_state.page == "Accueil":
    st.title("🚀 Bienvenue dans Google Ads AI Assistant")
    st.markdown("""
    Cet outil vous aide à générer des titres et descriptions pour vos campagnes Google Ads à l’aide de différents modèles d’intelligence artificielle (OpenAI, Anthropic, Gemini).

    👉 Utilisez le menu à gauche pour démarrer.
    """)

# --- MON COMPTE ---
elif st.session_state.page == "Mon compte":
    st.header("🔐 Connexion et API")
    credentials_dict = load_google_credentials()
    user_email = credentials_dict.get("client_email", "default")
    st.session_state.user_email = user_email
    st.success(f"Connecté avec : {user_email}")

    st.subheader("Clés API personnelles")
    openai_key = st.text_input("Clé API OpenAI", type="password")
    anthropic_key = st.text_input("Clé API Anthropic", type="password")
    gemini_key = st.text_input("Clé API Gemini", type="password")

    if st.button("💾 Sauvegarder mes clés"):
        context_data = load_client_context(user_email, "_meta") or {}
        context_data.update({
            "openai_key": openai_key,
            "anthropic_key": anthropic_key,
            "gemini_key": gemini_key,
        })
        save_client_context(user_email, "_meta", context_data)
        st.success("Clés API sauvegardées !")

# --- CLIENTS ---
elif st.session_state.page == "Mes clients":
    st.header("📁 Gestion de vos clients")
    client_name = st.text_input("Nom du client")
    user_email = st.session_state.user_email

    if user_email and client_name:
        context_data = load_client_context(user_email, client_name)
        context_entreprise = st.text_area("Contexte entreprise", value=context_data.get("context_entreprise", ""))
        context_campagne = st.text_area("Contexte campagne", value=context_data.get("context_campagne", ""))
        context_adgroup = st.text_area("Contexte Ad Group", value=context_data.get("context_adgroup", ""))

        if st.button("💾 Sauvegarder le contexte"):
            context_data.update({
                "context_entreprise": context_entreprise,
                "context_campagne": context_campagne,
                "context_adgroup": context_adgroup,
            })
            save_client_context(user_email, client_name, context_data)
            st.success("Contexte sauvegardé ✅")

        if st.button("📄 Créer la feuille Google Sheets"):
            sheet_url, sheet_id = create_template_sheet(credentials_dict, client_name)
            context_data["sheet_id"] = sheet_id
            save_client_context(user_email, client_name, context_data)
            st.session_state.sheet_url = sheet_url
            st.session_state.sheet_id = sheet_id
            st.success(f"[Feuille créée avec succès]({sheet_url})")

        if "sheet_id" in context_data:
            st.markdown(f"[📄 Ouvrir la feuille existante]({context_data['sheet_id']})")
            st.subheader("🤖 Génération IA")
            provider, model = select_model()
            api_keys = load_client_context(user_email, "_meta") or {}
            selected_key = api_keys.get(f"{provider.lower()}_key")

            if st.button("⚙️ Générer les assets IA"):
                with st.spinner("Génération en cours..."):
                    generate_ads_for_sheet(
                        credentials_dict,
                        context_data["sheet_id"],
                        context_data,
                        provider,
                        model,
                        selected_key
                    )
                st.success("Génération terminée ! 🎉")
