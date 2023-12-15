# Python
import json

# External
import requests


def update_token():
    url = "https://mdw02.api-es.ouigo.com/api/Token/login"

    payload = json.dumps({
        "username": "ouigo.web",
        "password": "SquirelWeb!2020"
    })

    headers = {

        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
    if response.status_code == 200:
        r = response.json()
        token = r.get("token")
        print("token obtenido")
        return token


class SessionManager:
    BASE_SITE_FOR_SESSION_URL = "https://www.ouigo.com/es/"

    def __init__(self):
        self.session = requests.Session()
        self._update_session_cookie()

    def _update_session_cookie(self):
        # Visit main website to get session cookies
        self.session.get(self.BASE_SITE_FOR_SESSION_URL)

    def get_session(self):
        return self.session
