import streamlit as st

# 1) Page config : première commande
st.set_page_config(page_title="IA Ad Generator", layout="wide")

# 2) Imports métiers
from clients.manager import ClientManager
from sheets.gsheets import get_sheet_manager
from streamlit_contextualisation import page_contextualisation
from utils.prompts import get_title_prompt, get_description_prompt
from generators.openai_provider import OpenAIProvider

# 3) Gestion du login Google : on tente d'obtenir un manager valide
#    Si l'utilisateur n'a pas encore autorisé, cette ligne va déclencher
#    l'affichage du lien OAuth et du champ de code, et bloquer la suite.
try:
    sheet_manager = get_sheet_manager()
    authenticated = True
except Exception:
    # En cas d'erreur d'auth, on reste bloqué ici
    authenticated = False

# 4) Si pas authentifié, on coupe tout et on affiche un message
if not authenticated:
    st.error("🔒 Vous devez vous connecter avec votre compte Google pour continuer.")
    st.stop()

# 5) À partir d'ici, l'utilisateur est connecté, on peut charger
#    le manager client et afficher la sidebar.
client_manager = ClientManager()

def page_clients():
    st.header("Gestion des clients")
    client_manager.render_ui()

def page_brief_global():
    st.header("Brief global")
    client_manager.edit_global_brief(client_manager.current_client)

def page_google_sheet():
    st.header("Google Sheet")
    client = client_manager.current_client
    sheet_title = st.text_input(
        "Nom du Google Sheet à créer",
        value=f"{client}_template" if client else ""
    )
    if st.button("Créer la feuille vierge dans Google Sheets"):
        try:
            spreadsheet_id = sheet_manager.create_template(sheet_title)
            st.success(f"Sheet créé avec succès ! ID : {spreadsheet_id}")
            st.markdown(f"[Ouvrir le Google Sheet](https://docs.google.com/spreadsheets/d/{spreadsheet_id})")
            client_manager.save_sheet_id(client, spreadsheet_id)
        except Exception as e:
            st.error(f"Erreur lors de la création du Google Sheet : {e}")

def page_contextualisation_wrapper():
    page_contextualisation()

def page_configuration_ia():
    st.header("Configuration IA")
    st.session_state.provider = st.selectbox("Prestataire IA", ["OpenAI", "Anthropic"])
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
        st.warning("Veuillez sélectionner un client avant de générer.")
        return

    global_brief = client_manager.get_global_brief(client)
    spreadsheet_id = client_manager.get_sheet_id(client)
    if not spreadsheet_id:
        st.warning("Aucun Google Sheet associé. Créez d'abord la feuille.")
        return

    records = sheet_manager.import_sheet(spreadsheet_id)
    if not records:
        st.info("Aucune donnée à traiter dans le Google Sheet.")
        return

    for record in records:
        campaign = record.get("Campagne")
        adgroup = record.get("Ad Group")
        top_keywords = record.get("Top 3 Mots-Clés")
        camp_ctx = client_manager.get_campaign_context(client, campaign)

        if st.button(f"Générer pour {campaign} / {adgroup}"):
            title_prompt = get_title_prompt(global_brief, camp_ctx, adgroup, top_keywords)
            desc_prompt = get_description_prompt(global_brief, camp_ctx, adgroup, top_keywords)
            provider = OpenAIProvider(model=st.session_state.model)
            titles = provider.generate(title_prompt)
            descriptions = provider.generate(desc_prompt)
            sheet_manager.write_results(spreadsheet_id, campaign, adgroup, titles, descriptions)
            st.success(f"Génération terminée pour {campaign} / {adgroup}")

def page_results():
    st.header("Résultats")
    client = client_manager.current_client
    spreadsheet_id = client_manager.get_sheet_id(client)
    if not spreadsheet_id:
        st.warning("Aucun Google Sheet associé. Rien à afficher.")
        return

    df = sheet_manager.fetch_sheet_dataframe(spreadsheet_id)
    if df.empty:
        st.info("Le Google Sheet est vide.")
    else:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Télécharger CSV", data=csv, file_name=f"{client}_ads.csv")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Aller à", [
        "Clients",
        "Brief Global",
        "Google Sheet",
        "Contextualisation",
        "Configuration IA",
        "Génération",
        "Résultats"
    ])

    if page == "Clients":
        page_clients()
    elif page == "Brief Global":
        page_brief_global()
    elif page == "Google Sheet":
        page_google_sheet()
    elif page == "Contextualisation":
        page_contextualisation_wrapper()
    elif page == "Configuration IA":
        page_configuration_ia()
    elif page == "Génération":
        page_generation()
    elif page == "Résultats":
        page_results()

if __name__ == "__main__":
    main()
