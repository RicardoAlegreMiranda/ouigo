# Internal
from stations import StationsNames
import seasson
from types_class import Train

# Python
import json


class Ouigo:
    def __init__(self, country: str = None):
        self.country = country
        self._num_queries = 0
        self.session_manager = seasson.SessionManager()
        self.session = self.session_manager.get_session()
        self.token = None
        self.stations_names = StationsNames()

    def get_list_30_days_travels(self,
                                 begin: str,  # example: "2024-01-01"
                                 end: str,  # example: 2024-03-31"
                                 destination: str,  # example: "7171801"
                                 origin: str):  # example: "MT1"
        url = "https://mdw02.api-es.ouigo.com/api/Calendar/prices"

        if not self.token:
            self.token = seasson.update_token()

        payload = json.dumps({
            "direction": "outbound",
            "begin": begin,
            "end": end,
            "destination": destination,
            "origin": origin,
            "passengers": [
                {
                    "discount_cards": [],
                    "disability_type": "NH",
                    "type": "A"
                }
            ]
        })
        headers = {
            'authorization': "Bearer " + self.token,
            'content-type': 'application/json',
        }

        response = self.session.post(url, headers=headers, data=payload, timeout=10)

        if response.status_code == 200:
            response_json = response.json()

            # Convert the list of dictionaries to a list of Train objects
            trains = [Train(**travel) for travel in response_json]

            return trains
        elif response.status_code == 204:
            print("The date is out of range, please enter a date up to 6 months from the current date.")
        else:
            print("Fail: get_travels ", response.status_code)

    def get_cheapest_price(self,
                           begin: str,  # example: "2024-01-01"
                           end: str,  # example: 2024-03-31"
                           destination: str,  # example: "7171801"
                           origin: str):  # example: "MT1"
        lists_travels = []
        travels = self.get_list_30_days_travels(begin=begin, end=end, destination=destination, origin=origin)

        for travel in travels:
            mounth = travel.is_best_price_month
            best = travel.is_best_price

            if mounth == True or best == True:
                lists_travels.append(travel)

        return lists_travels


viajes = Ouigo()

l = viajes.get_cheapest_price(begin="2024-01-01", end="2024-03-31", destination="7171801", origin=viajes.stations_names.Madrid)

for a in l:
    print(a.date)
