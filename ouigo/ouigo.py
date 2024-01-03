# Internal
from ouigo import seasson, stations, utils
from ouigo.types_class import Train, Trip, Station_ES, Station_FR

# Python
import json
from datetime import datetime, time

# External
import requests


class DateProcessingError(Exception):
    pass


# The main class
class Ouigo:

    def __init__(self, country: str):
        self.country = country.upper()  # "FR" = France , "ES" = Spain
        self.session_manager = seasson.SessionManager()
        self.session = self.session_manager.get_session()
        self.token = seasson.update_token(self.country)
        self.list_stations = stations.load_stations(self.country)
        self.util = utils

        if self.country != "FR" and self.country != "ES":
            raise DateProcessingError(f"Country error {self.country} is not a valid name, "
                                      f"enter the values: FR for search in France or ES for search in Spain")

    def get_list_60_days_travels(self,
                                 outbound: str,  # example: "2024-01-01" # Format YYYY-MM-DD
                                 origin: str,  # example: "Barcelona"
                                 destination: str,  # example: "Madrid"
                                 destination_is_code: bool = False):  # Check if the destination is a code or a name

        """
        returns a 60-day list of the lowest prices between 2 destinations, it is the same as what happens when enter
        the Ouigo website and display the calendar, it shows the cheapest price of each day

        Args:
            outbound (str): example: "2024-01-01" # Format YYYY-MM-DD
            origin (str):  example: "Barcelona"
            destination (str): example: "Madrid"
            destination_is_code (bool): if you use stations code instead of the station name, example: if instead of
             using "Madrid" you use "MT1"
        Returns:
            List[Train]: a list of all available trips in the next 60 days
            example: Train(date='2024-01-01', price=55.0, is_best_price=False, is_best_price_month=False,
            is_promo=False)

        """

        URL_ES = "https://mdw02.api-es.ouigo.com/api/Calendar/prices"  # Search in Spain
        URL_FR = "https://mdw.api-fr.ouigo.com/api/Calendar/prices"  # Search in France

        # Calculate the end of search, you don't recibe prices if you try search in a range of more 30 days of the
        # current date
        if not self.util.process_date(outbound):
            return None

        end = self.util.process_date(outbound)  # Calculate the end of the search (the day)

        # Get the token
        if not self.token:
            self.token = self.update_token()

        # If destinations is not a code(is a name like: Barcelona or Paris) , find the station_code
        if not destination_is_code:
            destination = self.find_station_code_by_name(destination)  # Search the code of the Station
            origin = self.find_station_code_by_name(origin)  # Search the code of the Station

        payload = json.dumps({
            "direction": "outbound",
            "begin": outbound,
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
            response = self.session.post(URL_FR, headers=headers, data=payload, timeout=10)

        else:
            response = self.session.post(URL_ES, headers=headers, data=payload, timeout=10)

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
            raise DateProcessingError(f"Fail: get_travels,  "
                                      f"status code: {response.status_code},"
                                      f"text: {response.text}")

    def journal_search(self,
                       destination: str,
                       origin: str,
                       outbound_date: str,
                       destination_is_code: bool = False):

        """
        Get all possible tickets for a specific date, returns the price and available times, por example: find all
        the posible travels:
        :param origin: example "Paris"
        :param destination: example "Nantes"
        :param destination_is_code:  if destination_is_code is True, the station code must be entered
        (example: MT1 instead of the name, "Madrid")
        :param outbound_date: example "2024-05-25"

        """

        URL_ES = "https://mdw02.api-es.ouigo.com/api/Sale/journeysearch"
        URL_FR = "https://mdw.api-fr.ouigo.com/api/Sale/journeysearch"

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
            response = self.session.post(url=URL_FR, headers=headers, data=payload, timeout=10)

        else:
            response = self.session.post(url=URL_ES, headers=headers, data=payload, timeout=10)

        # Check if the response is OK (status_code = 200)
        if response.status_code == 200:
            response_json = response.json()
            list_trips_hours = []
            # Convert the list of dictionaries to a list of Train objects
            outbound = response_json["outbound"]
            for trip in outbound:
                price = trip.get("price")

                # filters only trips with price
                if price is not None:
                    # adds all the information to the Trip object
                    trip = trip.get("departure_station")
                    hour_str = trip.get("departure_timestamp")
                    trip["price"] = price
                    trip["outbound"] = outbound_date
                    trip["destination"] = self.find_station_name_by_code(destination)
                    hour_datetime = self.util.get_time_from_string(hour_str)
                    trip["departure_timestamp"] = hour_datetime

                    list_trips_hours.append(Trip(**trip))  # creates the object and adds it to the list
            return list_trips_hours
        else:
            raise DateProcessingError(f"Fail in journal_search,  status code: {response.status_code},"
                                      f"text: {response.text}")

    # The main method for search travels
    def find_travels(self,
                     origin: str,  # Example: Madrid, Paris
                     outbound: str,  # Example: "2024-12-31"
                     destination: str = None,
                     max_price: float = None,  # Example 15,5
                     minimum_departure_time: datetime = None,  # Example: time(00,00)
                     maximum_departure_time: datetime = None) -> Trip:
        """
        This is the main method for search and filter trips in ouigo.

        Args:
            origin (str):  mandatory, example: "Barcelona"
            outbound (str): mandatory, example: "2024-01-01" # Format YYYY-MM-DD
            destination (str): optional, example: "Madrid"
            max_price (float):  optional, # Example 15,5
            minimum_departure_time (datetime): optional, filter by  minimum time at which the train leaves the station
            maximum_departure_time (datetime): optional, filter by  maximum time at which the train leaves the station
        Returns:
            return_type (list) : all trains after filtering

        """
        # If the parameter is a datetime object, convert it to str in the format YYYY-MM-DD
        if isinstance(outbound, datetime):
            outbound = outbound.strftime('%Y-%m-%d')

        trains = []
        # if you don't have a destination, get all de connected stations of the origin
        if destination is None:
            connected_stations = []
            for station in self.list_stations:
                if origin in station.name:
                    for connected in station.connected_stations:
                        connected_stations.append(connected)

            origin = self.find_station_code_by_name(origin)  # change the name by a code: example: Madrid -> MT1
            for station_code in connected_stations:
                trips = self.journal_search(outbound_date=outbound,
                                            origin=origin,
                                            destination=station_code,
                                            destination_is_code=True)

                # Save the trips in the list:
                for trip in trips:
                    trains.append(trip)
        else:  # If have destination: example: Madrid to Barcelona
            trips = (self.journal_search(outbound_date=outbound,
                                         origin=origin,
                                         destination=destination))
            # Save the trips in the list:
            for trip in trips:
                trains.append(trip)

        # filters possible trips with the conditions imposed by the user
        filtered_trains = []

        for trip in trains:
            if max_price is not None and trip.price > max_price:
                continue  # If the price is not ok
            if maximum_departure_time is not None and maximum_departure_time < trip.departure_timestamp:
                continue  # If the hour is not ok
            if minimum_departure_time is not None and minimum_departure_time > trip.departure_timestamp:
                continue  # If the price is not ok

            filtered_trains.append(Trip(
                price=trip.price,
                departure_timestamp=trip.departure_timestamp,
                destination=trip.destination,
                name=trip.name,
                _u_i_c_station_code=trip.u_i_c_station_code,
                outbound=outbound
            ))

        return filtered_trains

    def find_station_code_by_name(self, target_name: str):

        """
       Args:
           target_name(str) : find_station_code_by_name("Madrid")
       Returns:
           Return CODE Station, only need the code
           Example of use FR: find_station_code_by_name("Madrid") -> response: "MT1"
        """

        stations_dict = {station._u_i_c_station_code: station for station in self.list_stations}
        for code, info in stations_dict.items():
            if info.name.lower() == target_name.lower() or target_name.capitalize() in info.synonyms:
                return code  # The station code
        raise DateProcessingError(f"{target_name} is not a valid name")

    def find_station_name_by_code(self, code: str):
        """
        Args:
            code(str) : find_station_name_by_code("MT1")
        Returns:
            Return Name Station, only need the code
            Example of use FR: find_station_name_by_code("MT1") -> response: "Madrid"
        """

        for station in self.list_stations:
            if station._u_i_c_station_code == code:
                return station.name
        raise DateProcessingError(f"{code} is not a valid code station")
