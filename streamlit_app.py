import streamlit as st

# ─── 0) Configuration de la page ─────────────────────────────────────────────
st.set_page_config(page_title="IA Ad Generator", layout="wide")

# ─── 1) Message d’accueil ─────────────────────────────────────────────────────
st.markdown("""
# Bienvenue sur l’IA Ad Generator

Cet utilitaire Web vous aide à :
- Gérer vos clients (dossiers, briefs).
- Générer automatiquement, via l’IA (OpenAI/Anthropic), **10 titres** et **5 descriptions** d’annonces Google.
- Synchroniser directement avec Google Sheets pour remplir vos campagnes et Ad Groups.
- Exporter vos résultats en un clic.

Pour commencer, connectez-vous avec votre compte Google ci-dessous.
""")

# ─── 2) Bouton “Continue with Google” (Google Identity Services) ──────────────
GSI_CLIENT_ID = "850645921594-fk7ui31vi4dmn28keau12f1nlu001967.apps.googleusercontent.com"           # Remplacez par votre client_id
REDIRECT_URI  = "https://app-ads-utility-t9injwcft7vwzxhtpaxwia.streamlit.app/"  # L’URL publique de votre app

st.markdown(f"""
<script src="https://accounts.google.com/gsi/client" async defer></script>

<div id="g_id_onload"
     data-client_id="{GSI_CLIENT_ID}"
     data-login_uri="{REDIRECT_URI}"
     data-auto_prompt="false">
</div>

<div class="g_id_signin"
     data-type="standard"
     data-size="large"
     data-theme="outline"
     data-text="signin_with"
     data-shape="rectangular"
     data-logo_alignment="left">
</div>
""", unsafe_allow_html=True)

# ─── 3) Récupération et validation du token Google ─────────────────────────────
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from google.oauth2.credentials import Credentials
import os

params   = st.experimental_get_query_params()
raw_tok  = params.get("credential", [None])[0]

if not raw_tok:
    # L’utilisateur n’a pas encore cliqué ou consenti : on bloque tout le reste
    st.stop()

try:
    # Vérifier l’ID token reçu
    id_info = google_id_token.verify_oauth2_token(raw_tok, google_requests.Request(), GSI_CLIENT_ID)
    # Construire les Credentials pour Sheets API (ici on suppose offline access/config côté GCP)
    creds = Credentials(
        token=None,
        refresh_token=id_info.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GSI_CLIENT_ID,
        client_secret="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"
    )
    # Sauvegarde pour réutilisation
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(creds.to_json())
except ValueError:
    st.error("Authentification Google invalide, veuillez réessayer.")
    st.stop()

# ─── 4) Import des modules métiers ─────────────────────────────────────────────
from clients.manager import ClientManager
from sheets.gsheets       import get_sheet_manager
from streamlit_contextualisation import page_contextualisation
from utils.prompts        import get_title_prompt, get_description_prompt
from generators.openai_provider import OpenAIProvider

# ─── 5) Managers ───────────────────────────────────────────────────────────────
client_manager = ClientManager()
sheet_manager  = get_sheet_manager()  # Chargera token.json et rafraîchira si besoin

# ─── 6) Définition des pages ─────────────────────────────────────────────────
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
            st.success(f"Sheet créé avec succès ! ID : {sid}")
            st.markdown(f"[Ouvrir le Google Sheet](https://docs.google.com/spreadsheets/d/{sid})")
            client_manager.save_sheet_id(client, sid)
        except Exception as e:
            st.error(f"Erreur lors de la création du Sheet : {e}")

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
        st.warning("Sélectionnez un client avant de générer.")
        return

    brief = client_manager.get_global_brief(client)
    sid   = client_manager.get_sheet_id(client)
    if not sid:
        st.warning("Aucun Google Sheet associé. Créez-le d’abord.")
        return

    records = sheet_manager.import_sheet(sid)
    if not records:
        st.info("Aucune donnée à traiter dans le sheet.")
        return

    for rec in records:
        camp = rec.get("Campagne")
        ag   = rec.get("Ad Group")
        kws  = rec.get("Top 3 Mots-Clés")
        ctx  = client_manager.get_campaign_context(client, camp)

        if st.button(f"Générer pour {camp} / {ag}"):
            tp = get_title_prompt(brief, ctx, ag, kws)
            dp = get_description_prompt(brief, ctx, ag, kws)
            prov = OpenAIProvider(model=st.session_state.model)
            titles = prov.generate(tp)
            descs  = prov.generate(dp)
            sheet_manager.write_results(sid, camp, ag, titles, descs)
            st.success(f"Génération terminée pour {camp} / {ag}")

def page_results():
    st.header("Résultats")
    client = client_manager.current_client
    sid    = client_manager.get_sheet_id(client)
    if not sid:
        st.warning("Aucun Google Sheet associé. Rien à afficher.")
        return

    df = sheet_manager.fetch_sheet_dataframe(sid)
    if df.empty:
        st.info("Le sheet est vide.")
    else:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Télécharger CSV", data=csv, file_name=f"{client}_ads.csv")

# ─── 7) Navigation et exécution ────────────────────────────────────────────────
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

    if   choix == "Clients":          page_clients()
    elif choix == "Brief Global":     page_brief_global()
    elif choix == "Google Sheet":     page_google_sheet()
    elif choix == "Contextualisation":page_contextualisation_wrapper()
    elif choix == "Configuration IA": page_configuration_ia()
    elif choix == "Génération":       page_generation()
    elif choix == "Résultats":        page_results()

if __name__ == "__main__":
    main()
