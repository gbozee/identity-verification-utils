from urllib.parse import quote_plus

import gspread
from oauth2client.service_account import ServiceAccountCredentials

DEFAULT_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def build_credential_json(
    project_id: str = None,
    private_key_id: str = None,
    private_key=None,
    client_email=None,
    client_id: str = None,
):

    return {
        "type": "service_account",
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{quote_plus(client_email.encode('utf-8'))}",
    }


def create_credentials_from_file(client_secret, additional_scopes=None):
    scope = (additional_scopes or []) + DEFAULT_SCOPES
    credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)

    gc = gspread.authorize(credentials)
    return gc


def create_credentials(additional_scopes=None, **kwargs):
    scope = (additional_scopes or []) + DEFAULT_SCOPES
    credential_dict = build_credential_json(**kwargs)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credential_dict, scope
    )

    gc = gspread.authorize(credentials)
    return gc



class AdminSheetAPI:
    def __init__(
        self,
        key_location: str = None,
        project_id: str = None,
        private_key_id: str = None,
        private_key=None,
        client_email=None,
        client_id: str = None,
    ):
        if key_location:
            self.gc = create_credentials(key_location)
        else:
            self.gc = create_credentials(
                project_id=project_id,
                private_key=private_key,
                private_key_id=private_key_id,
                client_email=client_email,
                client_id=client_id,
            )
        self.file = None
        self.data = []

    def load_file(self, url):
        self.file = self.gc.open_by_url(url).sheet1

    def match_role(self, email: str, role: str) -> bool:
        list_of_lists = self.file.get_all_values()
        list_of_lists.pop(0)
        instance = [
            x for x in list_of_lists if x[0].lower().strip() == email.lower().strip()
        ]
        if instance:
            return instance[0][1].lower().strip() == role.lower().strip()
        return False
