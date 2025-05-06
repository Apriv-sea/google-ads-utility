import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

# ─── 0) Configuration de la page ─────────────────────────────────────────────
st.set_page_config(page_title="IA Ad Generator", layout="wide")

# ─── 1) Gestion du flow OAuth via bouton Streamlit ──────────────────────────
REDIRECT_URI = "https://votre-app.streamlit.app/"  # doit matcher vos credentials OAuth

# a) Si on revient avec auth_url en query params, on redirige immédiatement
params = st.experimental_get_query_params()
if "auth_url" in params:
    auth_url = params["auth_url"][0]
    st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}" />',
                unsafe_allow_html=True)
    st.experimental_set_query_params()  # nettoie l'URL
    st.stop()

# b) Si on n'a pas encore de code, afficher bouton "Continue with Google"
code = params.get("code", [None])[0]
if not code and not os.path.exists("token.json"):
    st.markdown("# Bienvenue sur l’IA Ad Generator")
    st.write("Pour commencer, connectez-vous avec votre compte Google ci-dessous.")
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    if st.button("Continue with Google"):
        st.experimental_set_query_params(auth_url=auth_url)
    st.stop()

# c) Si Google nous renvoie un code, on l'échange contre des credentials
if code:
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    # Sauvegarde du token pour réutilisation
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    # Nettoyer le code de l'URL
    st.experimental_set_query_params()
# d) Si token.json existe déjà, on considère l'utilisateur authentifié

# ─── 2) Import des modules métiers ─────────────────────────────────────────────
from clients.manager import ClientManager
from sheets.gsheets       import get_sheet_manager
from streamlit_contextualisation import page_contextualisation
from utils.prompts        import get_title_prompt, get_description_prompt
from generators.openai_provider import OpenAIProvider

# ─── 3) Instanciation des managers ────────────────────────────────────────────
client_manager = ClientManager()
sheet_manager  = get_sheet_manager()  # charge et rafraîchit token.json

# ─── 4) Définition des pages ─────────────────────────────────────────────────
def page_clients():
    st.header("Gestion des clients")
    client_manager.render_ui()

def page_brief_global():
    st.header("Brief global")
    client_manager.edit_global_brief(client_manager.current_client)

def page_google_sheet():
    st.header("Google Sheet")
    client = client_manager.current_client
    title  = st.text_input("Nom du Google Sheet à créer", value=f"{client}_template" if client else "")
    if st.button("Créer la feuille vierge dans Google Sheets"):
        try:
            sid = sheet_manager.create_template(title)
            st.success(f"✅ Sheet créé ! ID : {sid}")
            st.markdown(f"[Ouvrir le Google Sheet](https://docs.google.com/spreadsheets/d/{sid})")
            client_manager.save_sheet_id(client, sid)
        except Exception as e:
            st.error(f"Erreur lors de la création du sheet : {e}")

def page_contextualisation_wrapper():
    page_contextualisation()

def page_configuration_ia():
    st.header("Configuration IA")
    st.session_state.provider = st.selectbox("Prestataire IA", ["OpenAI", "Anthropic"])
    st.session_state.model    = st.selectbox(
        "Modèle",
        sheet_manager.get_available_models(st.session_state.provider)
    )
    st.session_state.language = st.selectbox("Langue", ["fr", "en"])
    st.session_state.ton      = st.select_slider("Ton", ["formel", "convivial", "persuasif"])
    st.session_state.length   = st.slider("Longueur souhaitée", 10, 100, 30)

def page_generation():
    st.header("Génération des annonces")
    client = client_manager.current_client
    if not client:
        st.warning("⚠️ Sélectionnez un client avant de générer.")
        return

    brief = client_manager.get_global_brief(client)
    sid   = client_manager.get_sheet_id(client)
    if not sid:
        st.warning("⚠️ Aucune feuille Google associée. Créez-la d’abord.")
        return

    records = sheet_manager.import_sheet(sid)
    if not records:
        st.info("ℹ️ Aucune donnée à traiter dans le sheet.")
        return

    for rec in records:
        camp = rec.get("Campagne")
        ag   = rec.get("Ad Group")
        kws  = rec.get("Top 3 Mots-Clés")
        ctx  = client_manager.get_campaign_context(client, camp)

        if st.button(f"Générer pour {camp} / {ag}"):
            tp    = get_title_prompt(brief, ctx, ag, kws)
            dp    = get_description_prompt(brief, ctx, ag, kws)
            prov  = OpenAIProvider(model=st.session_state.model)
            titles = prov.generate(tp)
            descs  = prov.generate(dp)
            sheet_manager.write_results(sid, camp, ag, titles, descs)
            st.success(f"Génération terminée pour {camp} / {ag}")

def page_results():
    st.header("Résultats")
    client = client_manager.current_client
    sid    = client_manager.get_sheet_id(client)
    if not sid:
        st.warning("⚠️ Aucune feuille Google associée. Rien à afficher.")
        return

    df = sheet_manager.fetch_sheet_dataframe(sid)
    if df.empty:
        st.info("ℹ️ Le sheet est vide.")
    else:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Télécharger CSV", data=csv, file_name=f"{client}_ads.csv")

# ─── 5) Navigation et exécution ────────────────────────────────────────────────
def main():
    st.sidebar.title("Navigation")
    choix = st.sidebar.radio("Aller à", [
        "Clients",
        "Brief Global",
        "Google Sheet",
        "Contextualisation",
        "Configuration IA",
        "Génération",
        "Résultats"
    ])

    if   choix == "Clients":           page_clients()
    elif choix == "Brief Global":      page_brief_global()
    elif choix == "Google Sheet":      page_google_sheet()
    elif choix == "Contextualisation": page_contextualisation_wrapper()
    elif choix == "Configuration IA":  page_configuration_ia()
    elif choix == "Génération":        page_generation()
    elif choix == "Résultats":         page_results()

if __name__ == "__main__":
    main()
