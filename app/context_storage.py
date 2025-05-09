
import os
import json

STORAGE_DIR = "client_data"
os.makedirs(STORAGE_DIR, exist_ok=True)

def save_client_context(client_name, context_entreprise, context_campagne, context_adgroup):
    data = {
        "context_entreprise": context_entreprise,
        "context_campagne": context_campagne,
        "context_adgroup": context_adgroup
    }
    file_path = os.path.join(STORAGE_DIR, f"{client_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_client_context(client_name):
    file_path = os.path.join(STORAGE_DIR, f"{client_name}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"context_entreprise": "", "context_campagne": "", "context_adgroup": ""}
