import os
import json
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetManager:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        token_path = 'token.json'
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            flow = Flow.from_client_secrets_file(
                'credentials.json', SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            st.write("Veuillez vous rendre sur ce lien pour autoriser l'accès :")
            st.write(auth_url)
            code = st.text_input('Entrez le code de validation')
            if code:
                flow.fetch_token(code=code)
                creds = flow.credentials
                with open(token_path, 'w') as token_file:
                    token_file.write(creds.to_json())
        self.creds = creds
        self.service = build('sheets', 'v4', credentials=creds)

    def create_template(self, sheet_title: str) -> str:
        with open(os.path.join(os.path.dirname(__file__), 'template.json')) as f:
            headers = json.load(f)['headers']
        body = {
            'properties': {'title': sheet_title},
            'sheets': [{'properties': {'title': 'Campagnes'}}]
        }
        sheet = self.service.spreadsheets().create(body=body, fields='spreadsheetId').execute()
        spreadsheet_id = sheet['spreadsheetId']
        header_range = 'Campagnes!A1:{}1'.format(chr(ord('A') + len(headers) - 1))
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=header_range,
            valueInputOption='RAW',
            body={'values': [headers]}
        ).execute()
        return spreadsheet_id

    def import_sheet(self, spreadsheet_id: str) -> list:
        try:
            meta = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='Campagnes!A1:Z1'
            ).execute()
            headers = meta.get('values', [])[0]
            data = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='Campagnes!A2:Z'
            ).execute().get('values', [])
            records = []
            for row in data:
                record = {headers[i]: row[i] if i < len(row) else '' for i in range(len(headers))}
                records.append(record)
            return records
        except HttpError as e:
            st.error(f"Erreur d'import Sheet: {e}")
            return []

    def write_results(self, spreadsheet_id: str, campaign_name: str, adgroup_name: str, titles: list, descriptions: list):
        records = self.import_sheet(spreadsheet_id)
        headers = list(records[0].keys()) if records else []
        for idx, record in enumerate(records, start=2):
            if record.get('Campagne') == campaign_name and record.get('Ad Group') == adgroup_name:
                row_idx = idx
                break
        else:
            st.warning(f"Ligne non trouvée pour Campagne={campaign_name}, Ad Group={adgroup_name}")
            return
        title_idx = headers.index('Titre 1')
        title_range = f"Campagnes!{chr(ord('A')+title_idx)}{row_idx}:{chr(ord('A')+title_idx+len(titles)-1)}{row_idx}"
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=title_range,
            valueInputOption='RAW',
            body={'values': [titles]}
        ).execute()
        desc_idx = headers.index('Description 1')
        desc_range = f"Campagnes!{chr(ord('A')+desc_idx)}{row_idx}:{chr(ord('A')+desc_idx+len(descriptions)-1)}{row_idx}"
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=desc_range,
            valueInputOption='RAW',
            body={'values': [descriptions]}
        ).execute()

    def fetch_sheet_dataframe(self, spreadsheet_id: str):
        import pandas as pd
        records = self.import_sheet(spreadsheet_id)
        return pd.DataFrame(records)

@st.experimental_singleton
def get_sheet_manager():
    mgr = SheetManager()
    mgr.authenticate()
    return mgr
