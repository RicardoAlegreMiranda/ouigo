# From python
from dataclasses import dataclass
import json

# External
import requests


@dataclass
class Station:
    station_code: str
    name: str
    connected_stations: list
    synonyms: list


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
            print("api llamado")

            for station in stations_json:
                # Get all the data from the json
                station_code = station.get('_u_i_c_station_code')
                name = station.get('name')
                connected_stations = station.get('connected_stations')
                synonyms = station.get('synonyms')
                stations[station_code] = Station(
                    station_code=station_code,
                    name=name,
                    connected_stations=connected_stations,
                    synonyms=synonyms
                )

            return stations

        else:
            # If the response is not ok
            print("API call error load_stations ", response_stations.status_code)
            return None

    except Exception as e:
        print("API call exception load_stations ", e)

# Return code Station, only need the name
def find_station_code_by_name(station_dict, target_name):
    for code, info in station_dict.items():
        if info.name == target_name or target_name in info.synonyms:
            return code  # The station code
    return None

"""
stations_loaded = load_stations()

# Nombre de la estación que quieres buscar
target_station_name = "as"

# Obtener el código de la estación Barcelona
barcelona_station_code = find_station_code_by_name(stations_loaded, target_station_name)

# Verificar si se encontró el código de Barcelona
if barcelona_station_code is not None:
    # Obtener la información de la estación Barcelona
    barcelona_station = stations_loaded[barcelona_station_code]

    # Obtener los códigos de las estaciones conectadas
    connected_station_codes = barcelona_station.connected_stations

    # Obtener la información de las estaciones conectadas
    connected_stations_info = [stations_loaded[code] for code in connected_station_codes]

    # Imprimir la información de las estaciones conectadas
    for station_info in connected_stations_info:
        print("Connected Station:", station_info.name, station_info.station_code)

else:
    print(f"No se encontró la estación con el nombre {target_station_name}")


stations_loaded = load_stations()
mi_estacion = stations_loaded['MT1']  # Aquí asumí que 'MT1' es el código de la estación que te interesa

# Acceder a la lista de estaciones conectadas
connected_stations = mi_estacion.connected_stations
# Ahora, puedes imprimir la lista o hacer cualquier operación que necesites
print("Connected Stations:", connected_stations, mi_estacion.name)



STATIONS_CODES = {"Madrid - Todas": "MT1",
                  "Barcelona": "7171801",
                  "Madrid - Chamartín": "7117000",
                  "Madrid - Atocha": "7160000",
                  "Valencia": "7103216",
                  "Alicante": "7160911",
                  "Zaragoza": "7104040",
                  "Albacete ": "7160600", }"""
