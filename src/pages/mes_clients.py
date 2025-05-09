import streamlit as st
from sheets import create_template_sheet

def show():
    st.subheader("Gestion des clients")
    client_name = st.text_input("Nom du client")
    if st.button("Créer une feuille template"):
        credentials_dict = st.secrets["gcp_service_account"]
        create_template_sheet(credentials_dict, client_name)
        st.success("Feuille Google Ads créée.")