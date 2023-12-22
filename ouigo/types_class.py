from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Train:
    date: str
    price: int
    is_best_price: bool
    is_best_price_month: bool
    Destination: str
    is_promo: bool = field(default=False)


# Spain
@dataclass
class Station_ES:
    _u_i_c_station_code: str
    name: str
    connected_stations: list
    synonyms: list
    hidden: bool


# France
@dataclass
class GeoData:
    latitude: str
    zoom: int
    longitude: str


@dataclass
class Station_FR:
    _u_i_c_station_code: str
    is_agglomeration: bool
    name: str
    synonyms: List[str]
    connected_stations: List[str]
    sequence_number: int
    geo_data: GeoData
    top_origin: bool
    parent: Optional[str] = None
    top_destination: Optional[bool] = None


@dataclass
class Trip_hours:
    departure_timestamp: datetime
    _u_i_c_station_code: str
    name: str
    price: float
    destination: str
