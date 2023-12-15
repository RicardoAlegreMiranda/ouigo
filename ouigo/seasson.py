import requests
import json


def update_token():
    url = "https://mdw02.api-es.ouigo.com/api/Token/login"

    payload = json.dumps({
        "username": "ouigo.web",
        "password": "SquirelWeb!2020"
    })
    headers = {
        'authority': 'mdw02.api-es.ouigo.com',
        'accept': 'application/json',
        'accept-language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7,es-AR;q=0.6,ca-ES;q=0.5,ca;q=0.4',
        'content-type': 'application/json',
        'origin': 'https://falbala-cdn-sse-prod.azureedge.net',
        'referer': 'https://falbala-cdn-sse-prod.azureedge.net/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        r = response.json()
        token = r.get("token")
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
