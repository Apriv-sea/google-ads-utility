import streamlit as st
from google_oauth import login_user, is_logged_in

from pages import accueil, mon_compte, mes_clients

st.set_page_config(page_title="Google Ads AI Assistant", layout="wide")

# --- Authentification Google OAuth 2.0 ---
login_user()
if not is_logged_in():
    st.warning("🔐 Veuillez vous connecter pour accéder à l'application.")
    st.stop()

# --- Navigation latérale ---
pages = {
    "Accueil": accueil.show,
    "Mon compte": mon_compte.show,
    "Mes clients": mes_clients.show
}

page = st.sidebar.radio("Navigation", list(pages.keys()))
if st.sidebar.button("🚪 Se déconnecter"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# --- Affichage de la page sélectionnée ---
pages[page]()