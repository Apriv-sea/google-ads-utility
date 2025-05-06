import os
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# ─── 0) Configuration de la page ─────────────────────────────────────────────
st.set_page_config(page_title="IA Ad Generator", layout="wide")

# ─── 1) INITIALISATION DU FLOW GOOGLE OAUTH ─────────────────────────────────
# ⚠️ Remplacez cette URI par celle configurée dans votre console Google Cloud (slash final inclus)
REDIRECT_URI = "https://app-ads-utility-t9injwcft7vwzxhtpaxwia.streamlit.app/"

flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
    redirect_uri=REDIRECT_URI
)
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

# ─── 2) GESTION DU LOGIN ──────────────────────────────────────────────────────
params = st.query_params
code   = params.get("code", [None])[0]

# a) Si on vient juste de cliquer sur “Continue with Google”, on redirige
if "auth_url" in params:
    st.experimental_set_query_params()  # nettoie l’URL
    st.markdown(
        f'<meta http-equiv="refresh" content="0; url={auth_url}" />',
        unsafe_allow_html=True
    )
    st.stop()

# b) Si on n’a ni code OAuth ni token.json, on affiche la page d’accueil
if code is None and not os.path.exists("token.json"):
    st.title("Welcome to IA Ad Generator")
    st.write(
        "I am your AI assistant—ready to help you generate high-impact Google Ads titles "
        "and descriptions directly in your Google Sheet."
    )
    btn_img = "https://developers.google.com/identity/images/btn_google_signin_light_normal_web.png"
    st.markdown(f"[![Continue with Google]({btn_img})]({auth_url})", unsafe_allow_html=True)
    st.stop()

# c) Si Google renvoie un code, on l’échange contre un token
if code:
    flow.fetch_token(code=code)
    creds = flow.credentials
    # Sauvegarde pour réutilisation
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    st.experimental_set_query_params()  # nettoie l’URL

# ─── 3) AUTHENTIFICATION OK → CHARGEMENT DES LIBS MÉTIER ─────────────────────
from clients.manager import ClientManager
from sheets.gsheets import get_sheet_manager
from streamlit_contextualisation import page_contextualisation
from utils.prompts import get_title_prompt, get_description_prompt
from generators.openai_provider import OpenAIProvider

# ─── 4) Instanciation des managers ────────────────────────────────────────────
client_manager = ClientManager()
sheet_manager  = get_sheet_manager()  # charge & rafraîchit token.json si besoin

# ─── 5) Définition des pages ─────────────────────────────────────────────────
def page_clients():
    st.header("Gestion des clients")
    client_manager.render_ui()

def page_brief_global():
    st.header("Brief global")
    client_manager.edit_global_brief(client_manager.current_client)

def page_google_sheet():
    st.header("Google Sheet")
    client = client_manager.current_client
    title  = st.text_input(
        "Nom du Google Sheet à créer",
        value=f"{client}_template" if client else ""
    )
    if st.button("Créer la feuille vierge"):
        try:
            sid = sheet_manager.create_template(title)
            st.success(f"✅ Sheet créé – ID : {sid}")
            st.markdown(f"[Ouvrir le sheet](https://docs.google.com/spreadsheets/d/{sid})")
            client_manager.save_sheet_id(client, sid)
        except Exception as e:
            st.error(f"Erreur lors de la création du sheet : {e}")

def page_contextualisation_wrapper():
    page_contextualisation()

def page_configuration_ia():
    st.header("Configuration IA")
    st.session_state.provider = st.selectbox("Prestataire", ["OpenAI", "Anthropic"])
    st.session_state.model = st.selectbox(
        "Modèle",
        sheet_manager.get_available_models(st.session_state.provider)
    )
    st.session_state.language = st.selectbox("Langue", ["fr", "en"])
    st.session_state.ton = st.select_slider("Ton", ["formel", "convivial", "persuasif"])
    st.session_state.length = st.slider("Longueur souhaitée", 10, 100, 30)

def page_generation():
    st.header("Génération des annonces")
    client = client_manager.current_client
    if not client:
        st.warning("⚠️ Sélectionnez un client d’abord.")
        return

    brief = client_manager.get_global_brief(client)
    sid = client_manager.get_sheet_id(client)
    if not sid:
        st.warning("⚠️ Créez d’abord le Google Sheet.")
        return

    records = sheet_manager.import_sheet(sid)
    if not records:
        st.info("ℹ️ Aucune donnée à traiter dans le sheet.")
        return

    for rec in records:
        camp = rec["Campagne"]
        ag   = rec["Ad Group"]
        kws  = rec["Top 3 Mots-Clés"]
        ctx  = client_manager.get_campaign_context(client, camp)

        if st.button(f"Générer {camp}/{ag}"):
            tp = get_title_prompt(brief, ctx, ag, kws)
            dp = get_description_prompt(brief, ctx, ag, kws)
            prov = OpenAIProvider(model=st.session_state.model)
            titles = prov.generate(tp)
            descs  = prov.generate(dp)
            sheet_manager.write_results(sid, camp, ag, titles, descs)
            st.success(f"Terminé pour {camp}/{ag}")

def page_results():
    st.header("Résultats")
    client = client_manager.current_client
    sid    = client_manager.get_sheet_id(client)
    if not sid:
        st.warning("⚠️ Aucune feuille à afficher.")
        return

    df = sheet_manager.fetch_sheet_dataframe(sid)
    if df.empty:
        st.info("ℹ️ Le sheet est vide.")
    else:
        st.dataframe(df)
        st.download_button(
            "Télécharger CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name=f"{client}_ads.csv"
        )

# ─── 6) Navigation ────────────────────────────────────────────────────────────
def main():
    st.sidebar.title("Navigation")
    choices = [
        "Clients",
        "Brief Global",
        "Google Sheet",
        "Contextualisation",
        "Configuration IA",
        "Génération",
        "Résultats"
    ]
    choice = st.sidebar.radio("Aller à", choices)

    page_map = {
        "Clients":          page_clients,
        "Brief Global":     page_brief_global,
        "Google Sheet":     page_google_sheet,
        "Contextualisation":page_contextualisation_wrapper,
        "Configuration IA": page_configuration_ia,
        "Génération":       page_generation,
        "Résultats":        page_results
    }
    page_map[choice]()

if __name__ == "__main__":
    main()
