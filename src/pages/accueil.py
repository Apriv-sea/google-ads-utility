import streamlit as st
from google_oauth import get_user_email

def show():
    user_email = get_user_email()
    st.header("Bienvenue sur l'assistant Google Ads")
    st.markdown(f"Vous êtes connecté en tant que : `{user_email}`")