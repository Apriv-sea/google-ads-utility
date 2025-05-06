import streamlit as st
from clients.manager import ClientManager
from sheets.gsheets import get_sheet_manager

# Instanciation des managers
client_manager = ClientManager()
sheet_manager = get_sheet_manager()

def page_contextualisation():
    """
    Widgets Streamlit pour saisir et modifier
    les contextes de campagne et d'ad group.
    """
    st.header("Contextualisation")
    client = client_manager.current_client
    if not client:
        st.warning("Veuillez d'abord sélectionner ou créer un client.")
        return

    # Récupération de l'ID du sheet pour ce client
    sheet_id = client_manager.get_sheet_id(client)
    if not sheet_id:
        st.warning("Aucun Google Sheet associé. Veuillez créer ou importer un sheet avant.")
        return

    # Import des données depuis le sheet
    records = sheet_manager.import_sheet(sheet_id)
    if not records:
        st.info("Le Google Sheet est vide ou les en-têtes sont invalides.")
        return

    # 1) Contextes des campagnes
    st.subheader("Contextes des campagnes")
    campaigns = sorted({r["Campagne"] for r in records if r.get("Campagne")})
    for camp in campaigns:
        existing = client_manager.get_campaign_context(client, camp) or ""
        new_ctx = st.text_area(
            label=f"Contexte de la campagne '{camp}'",
            value=existing,
            key=f"camp_ctx_{camp}"
        )
        if new_ctx != existing:
            client_manager.set_campaign_context(client, camp, new_ctx)

    # 2) Contextes des Ad Groups
    st.subheader("Contextes des Ad Groups")
    adgroups = sorted({r["Ad Group"] for r in records if r.get("Ad Group")})
    for ag in adgroups:
        existing = client_manager.get_adgroup_context(client, ag) or ""
        new_ctx = st.text_area(
            label=f"Contexte de l'ad group '{ag}'",
            value=existing,
            key=f"ag_ctx_{ag}"
        )
        if new_ctx != existing:
            client_manager.set_adgroup_context(client, ag, new_ctx)
