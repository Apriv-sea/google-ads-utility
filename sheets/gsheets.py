import os
import json
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from config.settings import GOOGLE_CREDENTIALS_FILE

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetManager:
    """
    Gère l'authentification via token.json et les opérations Google Sheets :
    - création d'un template de sheet
    - lecture des données
    - écriture des résultats
    """

    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        """
        Charge les credentials depuis token.json (généré par Streamlit après Google Sign-In),
        puis met en place self.service pour appeler l'API Sheets.
        """
        token_path = 'token.json'
        if not os.path.exists(token_path):
            st.error("🔒 Vous devez d'abord vous connecter avec Google (bouton Continue with Google).")
            st.stop()

        # Charger les credentials
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # Rafraîchir si nécessaire
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Mettre à jour le token.json
                with open(token_path, 'w', encoding='utf-8') as f:
                    f.write(creds.to_json())
            except Exception as e:
                st.error(f"Erreur lors du rafraîchissement du token : {e}")
                st.stop()

        self.creds = creds
        self.service = build('sheets', 'v4', credentials=creds)

    def create_template(self, sheet_title: str) -> str:
        """
        Crée un nouveau Google Sheet avec les en-têtes définis dans template.json
        et retourne son ID.
        """
        # Charger les en-têtes
        template_path = os.path.join(os.path.dirname(__file__), 'template.json')
        with open(template_path, encoding='utf-8') as f:
            headers = json.load(f)['headers']

        # Construction du spreadsheet
        body = {
            'properties': {'title': sheet_title},
            'sheets': [{'properties': {'title': 'Campagnes'}}]
        }
        sheet = self.service.spreadsheets().create(body=body, fields='spreadsheetId').execute()
        spreadsheet_id = sheet['spreadsheetId']

        # Écriture des en-têtes en A1:...
        end_col = chr(ord('A') + len(headers) - 1)
        header_range = f"Campagnes!A1:{end_col}1"
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=header_range,
            valueInputOption='RAW',
            body={'values': [headers]}
        ).execute()

        return spreadsheet_id

    def import_sheet(self, spreadsheet_id: str) -> list[dict]:
        """
        Lit toutes les lignes du sheet (feuille 'Campagnes') et retourne
        une liste de dicts { en-tête: valeur }.
        """
        try:
            # En-têtes sur la première ligne
            meta = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='Campagnes!A1:Z1'
            ).execute()
            headers = meta.get('values', [])[0]

            # Toutes les autres lignes
            data = self.service.spreadsads().values().get(
                spreadsheetId=spreadsheet_id,
                range='Campagnes!A2:Z'
            ).execute().get('values', [])

            records = []
            for row in data:
                record = {headers[i]: row[i] if i < len(row) else '' for i in range(len(headers))}
                records.append(record)

            return records

        except HttpError as e:
            st.error(f"Erreur lors de l'import du sheet : {e}")
            return []

    def write_results(
        self,
        spreadsheet_id: str,
        campaign_name: str,
        adgroup_name: str,
        titles: list[str],
        descriptions: list[str]
    ):
        """
        Insère (et écrase) les titres et descriptions produits dans les colonnes
        appropriées de la ligne correspondant à campaign_name + adgroup_name.
        """
        records = self.import_sheet(spreadsheet_id)
        if not records:
            st.warning("Aucune donnée trouvée pour écrire les résultats.")
            return

        headers = list(records[0].keys())

        # Chercher la ligne
        for idx, rec in enumerate(records, start=2):
            if rec.get('Campagne') == campaign_name and rec.get('Ad Group') == adgroup_name:
                row = idx
                break
        else:
            st.warning(f"Ligne introuvable pour Campagne='{campaign_name}', Ad Group='{adgroup_name}'")
            return

        # Titres : colonnes 'Titre 1'... 'Titre 10'
        start_t = headers.index('Titre 1')
        end_t   = start_t + len(titles) - 1
        col_start_t = chr(ord('A') + start_t)
        col_end_t   = chr(ord('A') + end_t)
        range_t = f"Campagnes!{col_start_t}{row}:{col_end_t}{row}"
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_t,
            valueInputOption='RAW',
            body={'values': [titles]}
        ).execute()

        # Descriptions : colonnes 'Description 1'... 'Description 5'
        start_d = headers.index('Description 1')
        end_d   = start_d + len(descriptions) - 1
        col_start_d = chr(ord('A') + start_d)
        col_end_d   = chr(ord('A') + end_d)
        range_d = f"Campagnes!{col_start_d}{row}:{col_end_d}{row}"
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_d,
            valueInputOption='RAW',
            body={'values': [descriptions]}
        ).execute()

    def fetch_sheet_dataframe(self, spreadsheet_id: str):
        """
        Retourne un pandas.DataFrame de tout le contenu de la feuille 'Campagnes'.
        """
        import pandas as pd
        records = self.import_sheet(spreadsheet_id)
        return pd.DataFrame(records)

@st.cache(allow_output_mutation=True)
def get_sheet_manager():
    """
    Singleton Streamlit pour SheetManager. Charge les credentials
    et instancie le service Sheets.
    """
    mgr = SheetManager()
    mgr.authenticate()
    return mgr
