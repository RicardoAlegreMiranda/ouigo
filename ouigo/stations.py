# Internal
from ouigo.types_class import Station_FR, Station_ES

# From python
from dataclasses import dataclass
import json

# External
import requests

stations_fr = None
stations_es = None
URL_API_STATIONS_ES = "https://mdw02.api-es.ouigo.com/api/Data/GetStations"
URL_API_STATIONS_FR = "https://mdw.api-fr.ouigo.com/api/Data/GetStations"


class DateProcessingError(Exception):
    pass


def load_stations(country: str):
    """
    This method call the API for get the stations of France or Spain, save the stations for futures call of this method
    Example of use: load_stations("ES")
    Response:[Station_ES(_u_i_c_station_code='MT1', name='Madrid - Todas las estaciones', connected_stations=[
    '7160600','7160911', '7171801', '7104040', '7104104', '7103216'], synonyms=['Madrid'], hidden=False), Station_ES(
    _u_i_c_station_code='7171801',.....
    """

    global stations_fr
    global stations_es

    try:
        # If not loaded, call the API
        if country == "FR":

            if stations_fr is not None:  # check if the stations are already loaded
                return stations_fr

            # Create the list to save the stations
            stations_fr = {}
            response_stations = requests.get(URL_API_STATIONS_FR, timeout=10)  # Call the API to get the stations
        else:  # If the search is not in France, make the search for Spain

            if stations_es is not None:  # check if the stations are already loaded
                return stations_es

            stations_es = {}
            response_stations = requests.get(URL_API_STATIONS_ES, timeout=10)  # Call the API to get the stations

        # If the response is OK
        if response_stations.status_code == 200:
            stations_json = response_stations.json()

            # Convert the list of dictionaries to a list of Station objects
            if country == "FR":
                stations_fr = [Station_FR(**station) for station in stations_json]
                return stations_fr
            else:
                # Convert the list of dictionaries to a list of Station objects
                stations_es = [Station_ES(**station) for station in stations_json]
                return stations_es
        else:
            # If the response is not ok
            raise DateProcessingError(f"API call error load_stations, {response_stations.status_code}")

    except Exception as e:
        raise DateProcessingError(f"API call exception load_stations, {e}")
