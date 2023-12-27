# Python
import json

# External
import requests


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

        # Get the necessary token for the query's

def update_token(country):
    url_es = "https://mdw02.api-es.ouigo.com/api/Token/login"
    url_fr = "https://mdw.api-fr.ouigo.com/api/Token/login"

    # This information is public, obtained by copying a call to the token from any browser
    payload = json.dumps({
        "username": "ouigo.web",
        "password": "SquirelWeb!2020"
    })

    headers = {

        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }
    if country == "FR":

        response = requests.request("POST", url_fr, headers=headers, data=payload, timeout=10)
    else:
        response = requests.request("POST", url_es, headers=headers, data=payload, timeout=10)

    # Check if the response is OK (status_code = 200)
    if response.status_code == 200:
        r = response.json()
        token = r.get("token")
        return token
    else:
        raise DateProcessingError(f"Fail: update_token,  "
                                  f"status code: {response.status_code},"
                                  f"text: {response.text}")

