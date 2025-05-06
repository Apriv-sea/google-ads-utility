import streamlit as st
import pandas as pd
from clients.manager import ClientManager
from sheets.gsheets import get_sheet_manager

def download_csv(client):
    cm = ClientManager()
    sm = get_sheet_manager()
    sheet_id = cm.get_sheet_id(client)
    df = sm.fetch_sheet_dataframe(sheet_id)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger CSV", data=csv, file_name=f"{client}_ads.csv")
