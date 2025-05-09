import streamlit as st
from google_oauth import get_user_email

def show():
    st.subheader("Informations de votre compte")
    user_email = get_user_email()
    st.write("📧 Email :", user_email)