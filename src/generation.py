import openai
import json
from model_selector import get_title_prompt, get_desc_prompt

def parse_llm_output(text, expected_length):
    try:
        items = json.loads(text)
        if isinstance(items, list) and len(items) == expected_length:
            return items
    except json.JSONDecodeError:
        pass
    return None

def generate_ads_for_sheet(credentials_dict, sheet_id, context, provider, model, api_key):
    import gspread
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_info(credentials_dict, scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(sheet_id).sheet1
    rows = sheet.get_all_values()[1:]  # skip header

    for idx, row in enumerate(rows, start=2):
        campaign = row[0]
        adgroup = row[1]
        keywords = row[2]

        prompt_titles = get_title_prompt(context['context_entreprise'], context['context_campagne'], adgroup, keywords)
        prompt_descs = get_desc_prompt(context['context_entreprise'], context['context_campagne'], adgroup, keywords)

        if provider == "OpenAI":
            openai.api_key = api_key
            titles_resp = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt_titles}],
                temperature=0.7
            )
            titles_raw = titles_resp.choices[0].message.content.strip()
            titles = parse_llm_output(titles_raw, 10)

            descs_resp = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt_descs}],
                temperature=0.7
            )
            descs_raw = descs_resp.choices[0].message.content.strip()
            descs = parse_llm_output(descs_raw, 5)

            if titles and descs:
                sheet.update(f"D{idx}:M{idx}", [titles])
                sheet.update(f"N{idx}:R{idx}", [descs])
