import requests
from constants import OAUTH_PROVIDERS

RC3 = OAUTH_PROVIDERS["RC3"]

RC3_REDIRECT_URI = RC3["redirect_uri"]
RC3_TOKEN_URI = RC3["token_uri"]
RC3_CLIENT_ID = RC3["client_id"]
RC3_CLIENT_SECRET = RC3["client_secret"]


def get_username(refresh_token):
    access_token = get_access_token(refresh_token)

    resp = requests.get(
        "https://rc3.world/api/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    resp_data = resp.json()
    if not resp_data["authenticated"]:
        raise Exception(f"user not authenticated: {resp_data}")

    return resp_data["username"]


def get_refresh_token(authoziation_code):
    payload = {
        "grant_type": "authorization_code",
        "code": authoziation_code,
        "redirect_uri": RC3_REDIRECT_URI,
        "client_id": RC3_CLIENT_ID,
        "client_secret": RC3_CLIENT_SECRET,
    }

    resp = requests.post("https://rc3.world/sso/token/", data=payload)
    resp_data = resp.json()
    if resp_data.get("error"):
        raise Exception(f"failed to exchange auth code for refresh token: {resp_data}")

    return resp_data["refresh_token"]


def get_access_token(refresh_token):
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": RC3_TOKEN_URI,
        "client_id": RC3_CLIENT_ID,
        "client_secret": RC3_CLIENT_SECRET,
    }

    resp = requests.post("https://rc3.world/sso/token/", data=payload)
    resp_data = resp.json()
    if resp_data.get("error"):
        raise Exception(f"failed to exchange refresh token for access token: {resp_data}")

    return resp_data["access_token"]


def gen_login_redirect(state):
    return f"https://rc3.world/sso/authorize?response_type=code&client_id={RC3_CLIENT_ID}&redirect_uri={RC3_REDIRECT_URI}&scopes=username&state={state}"
