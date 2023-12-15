import requests
import json
import seasson


class Ouigo:
    def __init__(self, country: str = None):
        self.country = country

        self._num_queries = 0
        self.session_manager = seasson.SessionManager()
        self.session = self.session_manager.get_session()

    def get_travels(self):
        url = "https://mdw02.api-es.ouigo.com/api/Calendar/prices"

        payload = json.dumps({
            "direction": "outbound",
            "begin": "2023-12-01",
            "end": "2023-12-31",
            "destination": "7103216",
            "origin": "MT1",
            "passengers": [
                {
                    "discount_cards": [],
                    "disability_type": "NH",
                    "type": "A"
                }
            ]
        })
        headers = {
            'authority': 'mdw02.api-es.ouigo.com',
            'accept': 'application/json',
            'accept-language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7,es-AR;q=0.6,ca-ES;q=0.5,ca;q=0.4',
            'authorization': "Bearer " + seasson.update_token(),
            'content-type': 'application/json',
            # 'cookie': 'didomi_token=eyJ1c2VyX2lkIjoiMThhYmQ4MTQtNzhhZi02NTE0LTkxNjItOTg0YjkxYTNjODVjIiwiY3JlYXRlZCI6IjIwMjMtMDktMjJUMTU6Mjg6MDAuOTM3WiIsInVwZGF0ZWQiOiIyMDIzLTA5LTIyVDE1OjI4OjAwLjkzN1oiLCJ2ZXJzaW9uIjpudWxsfQ==; persist%3AsearchHistory={%22searchHistory%22:%22[]%22%2C%22_persist%22:%22{%5C%22version%5C%22:-1%2C%5C%22rehydrated%5C%22:true}%22}; reduxPersistIndex=[%22persist:searchHistory%22]; ouigo_country_lang=%7B%22country%22%3A%22ES%22%2C%22language%22%3A%22es%22%7D',
            'origin': 'https://ventas.ouigo.com',
            'referer': 'https://ventas.ouigo.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = self.session.post(url, headers=headers, data=payload)

        # response = requests.request("POST", url, data=payload)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
        else:
            print("Fail: get_travels ", response.status_code)


oui = Ouigo()
oui.get_travels()
