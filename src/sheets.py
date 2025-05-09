import gspread
from google.oauth2.service_account import Credentials

def create_template_sheet(credentials_dict, client_name):
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
    gc = gspread.authorize(creds)

    sheet = gc.create(f"Template Google Ads - {client_name}")
    worksheet = sheet.sheet1
    worksheet.update("A1:R1", [[
        "Nom Campagne", "Nom Ad Group", "Top 3 keywords",
        "Titre 1", "Titre 2", "Titre 3", "Titre 4", "Titre 5",
        "Titre 6", "Titre 7", "Titre 8", "Titre 9", "Titre 10",
        "Description 1", "Description 2", "Description 3", "Description 4", "Description 5"
    ]])

    return sheet.url, sheet.id
