
from google.cloud import secretmanager
import json

def load_google_credentials():
    client = secretmanager.SecretManagerServiceClient()
    project_id = "135447600769"  # ID réel de ton projet Google Cloud
    name = f"projects/{project_id}/secrets/credentials/versions/latest"

    response = client.access_secret_version(request={"name": name})
    secret_content = response.payload.data.decode("UTF-8")
    return json.loads(secret_content)
