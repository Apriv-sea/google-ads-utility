# Entry point for the Streamlit app
import streamlit as st
from app.model_selector import select_model

st.title("Google Ads AI Assistant")

provider, model = select_model()
st.success(f"Fournisseur: {provider}, Modèle: {model}")