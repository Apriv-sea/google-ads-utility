import json
from pathlib import Path
import streamlit as st

class ClientManager:
    def __init__(self):
        self.base_dir = Path('clients/data')
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.current_client = st.session_state.get('current_client', None)

    def render_ui(self):
        clients = [d.name for d in self.base_dir.iterdir() if d.is_dir()]
        new_client = st.text_input("Nouveau client", "")
        existing = st.selectbox("Sélectionner un client existant", [""] + clients)
        chosen = new_client if new_client else (existing if existing else None)
        if chosen and chosen != self.current_client:
            st.session_state.current_client = chosen
            self.current_client = chosen
            (self.base_dir / chosen).mkdir(exist_ok=True)
        if st.button("Supprimer client"):
            if self.current_client:
                import shutil
                shutil.rmtree(self.base_dir / self.current_client)
                st.session_state.current_client = None
                self.current_client = None

    def save_sheet_id(self, client, sheet_id):
        meta = self._load_json(client, 'meta.json')
        meta['sheet_id'] = sheet_id
        self._save_json(client, 'meta.json', meta)

    def get_sheet_id(self, client):
        data = self._load_json(client, 'meta.json')
        return data.get('sheet_id')

    def edit_global_brief(self, client):
        if not client: return
        path = self.base_dir / client / 'global_brief.json'
        current = path.read_text() if path.exists() else ""
        new = st.text_area("Brief global", value=current)
        if new != current:
            path.write_text(new)

    def get_global_brief(self, client):
        path = self.base_dir / client / 'global_brief.json'
        return path.read_text() if path.exists() else ""

    def set_campaign_context(self, client, campaign, context):
        data = self._load_json(client, 'campaign_contexts.json')
        data[campaign] = context
        self._save_json(client, 'campaign_contexts.json', data)

    def get_campaign_context(self, client, campaign):
        return self._load_json(client, 'campaign_contexts.json').get(campaign)

    def set_adgroup_context(self, client, adgroup, context):
        data = self._load_json(client, 'adgroup_contexts.json')
        data[adgroup] = context
        self._save_json(client, 'adgroup_contexts.json', data)

    def get_adgroup_context(self, client, adgroup):
        return self._load_json(client, 'adgroup_contexts.json').get(adgroup)

    def _load_json(self, client, fname):
        path = self.base_dir / client / fname
        if path.exists():
            return json.loads(path.read_text())
        return {}

    def _save_json(self, client, fname, data):
        path = self.base_dir / client / fname
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
