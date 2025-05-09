# Dropdown component for selecting provider and model
import streamlit as st

def select_model():
    provider = st.selectbox("Choisissez un fournisseur IA", ["OpenAI", "Anthropic", "Gemini"])

    model_options = {
        "OpenAI": ["gpt-4", "gpt-4o", "gpt-4o-mini"],
        "Anthropic": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        "Gemini": ["gemini-1.5-pro", "gemini-1.5-flash"]
    }

    model = st.selectbox(f"Modèle {provider}", model_options[provider])
    return provider, model