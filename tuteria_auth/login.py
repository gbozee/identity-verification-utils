import typing
from google.oauth2 import id_token
from google.auth.transport import requests
import datetime
from tuteria_auth.gdrive import AdminSheetAPI
import jwt


def google_verification(token: str, client_id: str) -> typing.Optional[dict]:
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Wrong issuer.")

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo["sub"]
        return idinfo
    except ValueError:
        # Invalid token
        return None


def staff_verification(
    email, role="staff", file_url=None, key_location=None, config_obj: dict = None
) -> bool:
    kwargs = {}
    if config_obj:
        kwargs = config_obj
    instance = AdminSheetAPI(key_location=key_location, **kwargs)
    instance.load_file(file_url)
    return instance.match_role(email, role)


def create_app_access_token(
    *,
    data: dict,
    issuer: str,
    secret_key: str,
    timestamp: int,
    expire: datetime.datetime = None,
    algorithm="HS256",
    access_token_jwt_subject="access",
    audience=None,
):
    to_encode = data.copy()
    if expire:
        to_encode.update({"exp": expire})
    to_encode.update({"iss": issuer, "sub": access_token_jwt_subject, "iat": timestamp})
    if audience:
        to_encode.update(aud=audience)
    encoded_jwt = jwt.encode(to_encode, str(secret_key), algorithm=algorithm)
    return encoded_jwt.decode("utf-8")

