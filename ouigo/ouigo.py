# Internal
import seasson, stations, utils
from types_class import Train, Trip_hours, Station_ES, Station_FR

# Python
import json
from datetime import datetime

# External
import requests


class DateProcessingError(Exception):
    pass


# The main class
class Ouigo:

    def __init__(self, country: str):
        self.country = country  # "FR" = France , "ES" = Spain
        self.session_manager = seasson.SessionManager()
        self.session = self.session_manager.get_session()
        self.token = self.update_token()
        self.list_stations = stations.load_stations(country)
        self.util = utils

    # Get a list of the lowest prices for each day, in a maximum date range of 30 days
    # Example: get_list_30_days_travels(begin="2024-01-01", end="2024-03-31",destination="Barcelona", origin="Madrid")
    # Example: get_list_30_days_travels(begin="2024-01-01", end="2024-03-31", destination="Paris", origin="Nantes")
    # Response: Train(date='2024-01-01', price=55.0, is_best_price=False, is_best_price_month=False, is_promo=False)
    def get_list_60_days_travels(self,
                                 begin: str,  # example: "2024-01-01" # Format YYYY-MM-DD
                                 destination: str,  # example: "Madrid"
                                 origin: str,  # example: "Barcelona"
                                 destination_is_code: bool = False):  # Check if the destination is a code or a name

        url_es = "https://mdw02.api-es.ouigo.com/api/Calendar/prices"  # Search in Spain
        url_fr = "https://mdw.api-fr.ouigo.com/api/Calendar/prices"  # Search in France

        # Calculate the end of search, you don't recibe prices if you try search in a range of more 30 days of the
        # current date
        if not self.util.process_date(begin):
            return None

        end = self.util.process_date(begin)

        # Get the token
        if not self.token:
            self.token = self.update_token()

        # If destinations is not a code(is a name like: Barcelona or Paris) , find the station_code
        if not destination_is_code:
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
            trains = []
            for travel in response_json:
                if travel.get('price') is not None:  # Check the price, if not None, add the travel to the list
                    travel['Destination'] = self.find_station_name_by_code(destination)  # Save the name of destination
                    trains.append(Train(**travel))

            return trains
        else:
            print("Fail: get_travels ", response.status_code)

    def get_cheapest_price(self,
                           begin: str,  # example: "2024-01-01"
                           end: str,  # example: 2024-03-31"
                           destination: str,  # example: "7171801"
                           origin: str,  # example: "MT1"
                           destination_is_code: bool = False):
        lists_travels = []
        travels = self.get_list_60_days_travels(begin=begin, end=end, destination=destination, origin=origin)

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
                      outbound_date: str,
                      destination_is_code: bool = False):

        url_es = "https://mdw02.api-es.ouigo.com/api/Sale/journeysearch"
        url_fr = "https://mdw.api-fr.ouigo.com/api/Sale/journeysearch"
        if not self.token:
            self.token = self.update_token()

        # If destinations is not a code(is a name like: Barcelona or Paris) , find the station_code
        if not destination_is_code:
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
                trip["destination"] = self.find_station_name_by_code(destination)
                hour_datetime = self.util.get_time_from_string(hour_str)
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
            print("Token no obtenido ", response.status_code, response.text)

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
        raise DateProcessingError(f"{target_name} is not a valid name")

    def find_station_name_by_code(self, code):
        for station in self.list_stations:
            if station._u_i_c_station_code == code:
                return station.name
        raise DateProcessingError(f"{code} is not a valid code station")

    def find_travels(self,
                     origin: str,  # Example: Madrid, Paris
                     outbound: str,
                     inbound: str = None,
                     destination: str = None,
                     max_price: float = None,
                     minimum_departure_time: datetime = None,
                     maximum_departure_time: datetime = None):
        trains = []
        # if you don't have a destination, get all de connected stations of the origin
        if destination is None:
            connected_stations = []
            for station in self.list_stations:
                if origin in station.name:
                    for connected in station.connected_stations:
                        connected_stations.append(connected)

            origin = self.find_station_code_by_name(origin)
            for station_code in connected_stations:
                trips = self.jornay_search(outbound_date=outbound,
                                           origin=origin,
                                           destination=station_code,
                                           destination_is_code=True)
                if max_price is not None:
                    for trip in trips:
                        if trip.price <= max_price:
                            trains.append(trip)


        else:
            trains.append(self.get_list_60_days_travels(begin=outbound,
                                                        origin=origin,
                                                        destination=destination))
        return trains


viajes = Ouigo(country="es")
# con = viajes.get_list_60_days_travels("2024-01-01","7171801","MT1",destination_is_code=True)

con = viajes.find_travels(outbound="2024-02-01", origin="Madrid", max_price=20)
for c in con:
    print(c)
# print(viajes.obtener_nombre_estacion_por_codigo("7104040"))
