# Internal
from types_class import Station

# From python
from dataclasses import dataclass
import json

# External
import requests

stations = None
URL_API_STATIONS = "https://mdw02.api-es.ouigo.com/api/Data/GetStations"


def load_stations():
    global stations

    #  check if the stations are already loaded
    if stations is not None:
        return stations
    stations = {}
    try:
        # If not loaded, call the API
        response_stations = requests.get(URL_API_STATIONS, timeout=10)

        # If the response is OK
        if response_stations.status_code == 200:
            stations_json = response_stations.json()

            # Convert the list of dictionaries to a list of Station objects
            stations = [Station(**station) for station in stations_json]

            return stations

        else:
            # If the response is not ok
            print("API call error load_stations ", response_stations.status_code)
            return None

    except Exception as e:
        print("API call exception load_stations ", e)


# Return code Station, only need the name
def find_station_code_by_name(target_name):
    stations_dict = {station._u_i_c_station_code: station for station in load_stations()}
    for code, info in stations_dict.items():
        if info.name == target_name or target_name in info.synonyms:
            return code  # The station code
    return None


class StationsNames:
    find = staticmethod(find_station_code_by_name)

    def __init__(self):
        self._Barcelona = "Barcelona"
        self._Madrid = "Madrid"
        self._Alicante = "Alicante"
        self._Valencia = "Valencia"
        self._Zaragoza = "Zaragoza"
        self._Albacete = "Albacete"

    @property
    def Barcelona(self):
        return self.find(self._Barcelona)

    @property
    def Madrid(self):
        return self.find(self._Madrid)

    @property
    def Alicante(self):
        return self.find(self._Alicante)

    @property
    def Valencia(self):
        return self.find(self._Valencia)

    @property
    def Zaragoza(self):
        return self.find(self._Zaragoza)

    @property
    def Albacete(self):
        return self.find(self._Albacete)



STATIONS_CODES = {"Madrid - Todas": "MT1",
                  "Barcelona": "7171801",
                  "Madrid - Chamartín": "7117000",
                  "Madrid - Atocha": "7160000",
                  "Valencia": "7103216",
                  "Alicante": "7160911",
                  "Zaragoza": "7104040",
                  "Albacete ": "7160600", }
