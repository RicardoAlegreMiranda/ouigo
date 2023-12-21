# Internal
import seasson, stations
from types_class import Train, Trip_hours, Station_ES, Station_FR

# Python
import json
from datetime import datetime

# External
import requests


# The main class
class Ouigo:

    def __init__(self, country: str):
        self.country = country  # "FR" = France , "ES" = Spain
        self.session_manager = seasson.SessionManager()
        self.session = self.session_manager.get_session()
        self.token = self.update_token()
        self.list_stations = stations.load_stations(country)

    # Get a list of the lowest prices for each day, in a maximum date range of 30 days
    # Example: get_list_30_days_travels(begin="2024-01-01", end="2024-03-31",destination="Barcelona", origin="Madrid")
    # Example: get_list_30_days_travels(begin="2024-01-01", end="2024-03-31", destination="Paris", origin="Nantes")
    # Response: Train(date='2024-01-01', price=55.0, is_best_price=False, is_best_price_month=False, is_promo=False)
    def get_list_30_days_travels(self,
                                 begin: str,  # example: "2024-01-01"
                                 end: str,  # example: "2024-03-31"
                                 destination: str,  # example: "Madrid"
                                 origin: str):  # example: "Barcelona"

        url_es = "https://mdw02.api-es.ouigo.com/api/Calendar/prices"  # Search in Spain
        url_fr = "https://mdw.api-fr.ouigo.com/api/Calendar/prices"  # Search in France

        # Get the token
        if not self.token:
            self.token = self.update_token()

        destination = self.find_station_code_by_name(destination)  # Search the code of the Station
        origin = self.find_station_code_by_name(origin)  # Search the code of the Station

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
        if self.country == "FR":
            response = self.session.post(url_fr, headers=headers, data=payload, timeout=10)
            print("Search in France")

        else:
            response = self.session.post(url_es, headers=headers, data=payload, timeout=10)
            print("Search in Spain")

        # Check if the response is OK (status_code = 200)
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

    # Get all possible tickets for a specific date, returns the price and available times
    def jornay_search(self,
                      destination: str,
                      origin: str,
                      outbound_date: str):

        url_es = "https://mdw02.api-es.ouigo.com/api/Sale/journeysearch"
        url_fr = "https://mdw.api-fr.ouigo.com/api/Sale/journeysearch"
        if not self.token:
            self.token = self.update_token()

        destination = self.find_station_code_by_name(destination)  # Search the code of the Station
        origin = self.find_station_code_by_name(origin)  # Search the code of the Station

        payload = json.dumps({
            "destination": destination,
            "origin": origin,
            "outbound_date": outbound_date,
            "passengers": [
                {
                    "discount_cards": [],
                    "disability_type": "NH",
                    "type": "A"
                }
            ],

        })
        headers = {
            'authorization': "Bearer " + self.token,
            'content-type': 'application/json',
        }

        if self.country == "FR":
            response = self.session.post(url_fr, headers=headers, data=payload, timeout=10)
        else:
            response = self.session.post(url_es, headers=headers, data=payload, timeout=10)

        # Check if the response is OK (status_code = 200)
        if response.status_code == 200:
            response_json = response.json()
            list_trips_hours = []
            # Convert the list of dictionaries to a list of Train objects
            outbound = response_json["outbound"]
            for trip in outbound:

                price = trip.get("price")
                trip = trip.get("departure_station")
                hour_str = trip.get("departure_timestamp")
                trip["price"] = price
                hour_datetime = get_time_from_string(hour_str)
                trip["departure_timestamp"] = hour_datetime

                list_trips_hours.append(Trip_hours(**trip))
            return list_trips_hours
        else:
            print("Fail in jornay_search ", response.status_code, response.text)

    # Get the necessary token for the query's
    def update_token(self):
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
        if self.country == "FR":

            response = requests.request("POST", url_fr, headers=headers, data=payload, timeout=10)
        else:
            response = requests.request("POST", url_es, headers=headers, data=payload, timeout=10)

        # Check if the response is OK (status_code = 200)
        if response.status_code == 200:
            r = response.json()
            token = r.get("token")
            print("token obtenido")
            return token
        else:
            print("Token no obtenido ", response.status_code)
            print(response.text)



    """
    Return code Station, only need the name
    Example of use FR: find_station_code_by_name("Strasbourg", "FR") -> response: "87212027"
    Example of use ES: find_station_code_by_name("Madrid", "ES") -> response: "MT1"
    """

    def find_station_code_by_name(self, target_name):
        stations_dict = {station._u_i_c_station_code: station for station in self.list_stations}
        for code, info in stations_dict.items():
            if info.name == target_name or target_name in info.synonyms:
                return code  # The station code
        return None

    """
            for journey in outbound:
                departure_station = journey.get("departure_station")
                
                print(departure_station)"""


# sends a string, and returns a date in datetime format
def get_time_from_string(time_string):
    # Parse the time string
    format_str = "%Y-%m-%dT%H:%M:%S%z"
    datetime_object = datetime.strptime(time_string, format_str)

    # Get the time from the obtained datetime object
    time = datetime_object.time()

    return time


viajes = Ouigo(country="FR")
list = viajes.jornay_search(outbound_date="2024-03-31", destination="Paris", origin="Nantes")
for l in list:
    print(l)
