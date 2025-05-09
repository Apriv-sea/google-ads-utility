from google.oauth2.service_account import Credentials
import gspread

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_gspread_client(credentials_dict):
    creds = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
    return gspread.authorize(creds)