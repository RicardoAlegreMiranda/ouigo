from dataclasses import dataclass


@dataclass
class Train:
    date: str
    price: int
    is_best_price: bool
    is_best_price_month: bool

@dataclass
class Station:
    _u_i_c_station_code: str
    name: str
    connected_stations: list
    synonyms: list
    hidden: bool

