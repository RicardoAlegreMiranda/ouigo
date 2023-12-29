# Ouigo Python


This module allows you to retrieve the travels in the API of Ouigo, It also serves to filter the best prices and schedules when searching for trains

This is done directly through Ouigo's API, and does not require an API key. All information is obtained by public methods.
# Screenshot
![ouigo_find_travels3.JPG](..%2F..%2FDownloads%2Fouigo_find_travels3.JPG)
## Disclaimer
> __DISCLAIMER:__ This library is not affiliated, endorsed, or sponsored by Ouigo or any of its affiliates.  
> All trademarks related to Ouigo and its affiliates are owned by the relevant companies.  
> The author(s) of this library assume no responsibility for any consequences resulting from the use of this library.  
> The author(s) of this library also assume no liability for any damages, losses, or expenses that may arise from the use of this library.  
> Any use of this library is entirely at the user's own risk.  
> It is solely the user's responsibility to ensure compliance with Ouigo's terms of use and any applicable laws 
> and regulations.  
> The library is an independent project aimed at providing a convenient way to interact with the Ouigo API, allowing
> individuals to find travels for personal use, and then ultimately purchase them via Ouigo's website.
> While the author(s) will make efforts to ensure the library's functionality, they do not guarantee the accuracy,
> completeness, or timeliness of the information provided.  
> The author(s) do not guarantee the availability or continuity of the library, and updates may not be guaranteed.  
> Support for this library may be provided at the author(s)'s discretion, but it is not guaranteed.  
> Users are encouraged to report any issues or feedback to the author(s) via appropriate channels.  
> By using this library, users acknowledge that they have read, understood, and agreed to the terms of this disclaimer.

## Installation
Run the following command in the terminal:

```
pip install ouigo
```

## Usage
To create an instance:
```python
from ouigo import Ouigo
"""
It is necessary to indicate in which country you are 
going to carry out the searches (ES = Spain, FR = France)
"""
api = Ouigo(country="ES") 

```
## find_travels
This method searches for all the stations connected to the source station, and returns a list of Train objects with the information of all the trips available for that day at the source station.

From each trip you obtain the data:
- departure_timestamp = The departure time of the train in datetime format
- _u_i_c_station_code: the arrival station code
- name = the name of the departure station
- destination = the name of the arrival station
- outbound the departure date of the trip (string format)
```python
from ouigo import Ouigo

# ES for search in Spain or FR for search in France
API = Ouigo(country="es")  
travels = API.find_travels(origin="Madrid", 
                           outbound="2024-01-21")

for train in travels:
    print(train)
          

"""
console output example: 

Trip(departure_timestamp=datetime.time(18, 15), _u_i_c_station_code='7117000', name='Madrid - Chamartín - Clara Campoamor', price=39.0, destination='Alicante - Terminal', outbound='2024-01-21')
Trip(departure_timestamp=datetime.time(7, 5), _u_i_c_station_code='7160000', name='Madrid - Puerta de Atocha - Almudena Grandes', price=22.0, destination='Barcelona - Sants', outbound='2024-01-21')
...................... etc etc etc
"""
```

You can also filter by indicating:
- destination = Name of the destination or station code (you can consult the json of the stations)
- max_price = filters the maximum price
- maximum_departure_time = data in time format,
- minimum_departure_time = data in time format,
```python


from ouigo import Ouigo
from datetime import time
from ouigo.types_class import Trip

# ES for search in Spain or FR for search in France
API = Ouigo(country="FR")
travels: Trip = API.find_travels(origin="Paris",
                                 outbound="2024-01-21",  
                                 destination="Nantes",
                                 max_price=25,
                                 maximum_departure_time=time(13, 00),
                                 minimum_departure_time=time(7, 00))

for train in travels:
    print(f"price {train.price}, departure time {train.departure_timestamp} ")

"""
Console output example:

price 10.0, departure time 07:11:00 
price 10.0, departure time 07:26:00 
price 16.0, departure time 07:44:00 
"""
```

## get_list_60_days_travels
It is a quick method to find the best prices of the month to a specific destination

Returns a 60-day list of the lowest prices between 2 destinations, it is the same as what happens when enter
        the Ouigo website and display the calendar, it shows the cheapest price of each day

```python
from ouigo import Ouigo

# ES for search in Spain or FR for search in France
API = Ouigo(country="ES")
prices_to_valencia = API.get_list_60_days_travels(outbound="2024-01-15",
                                                  origin="Madrid",
                                                  destination="Valencia")
for prices in prices_to_valencia:
    print(prices)
"""
Console output
Train(date='2024-01-15', price=9.0, is_best_price=True, is_best_price_month=True, Destination='Valencia - Joaquín Sorolla', is_promo=False)
Train(date='2024-01-16', price=9.0, is_best_price=True, is_best_price_month=True, Destination='Valencia - Joaquín Sorolla', is_promo=False)
Train(date='2024-01-17', price=9.0, is_best_price=True, is_best_price_month=True, Destination='Valencia - Joaquín Sorolla', is_promo=False)
Train(date='2024-01-18', price=9.0, is_best_price=True, is_best_price_month=True, Destination='Valencia - Joaquín Sorolla', is_promo=False)
Train(date='2024-01-19', price=15.0, is_best_price=False, is_best_price_month=False, Destination='Valencia - Joaquín Sorolla', is_promo=False)
Train(date='2024-01-20', price=15.0, is_best_price=False, is_best_price_month=False, Destination='Valencia - Joaquín Sorolla', is_promo=False)
Train(date='2024-01-21', price=9.0, is_best_price=True, is_best_price_month=True, Destination='Valencia - Joaquín Sorolla', is_promo=False)
Train(date='2024-01-22', price=13.0, is_best_price=False, is_best_price_month=True, Destination='Valencia - Joaquín Sorolla', is_promo=False)
.....etc etc etc
"""
```

# journal_search
It is a quick method to find all the prices for a specific day and place, it is useful for finding return trips or a quick way to find outward trips.
```python
# ES for search in Spain or FR for search in France
API = Ouigo(country="ES")
prices_to_valencia = API.journal_search(outbound_date="2024-01-15",
                                        origin="Madrid",
                                        destination="Valencia")
for prices in prices_to_valencia:
    print(prices)


"""
Console output:
Trip(departure_timestamp=datetime.time(7, 15), _u_i_c_station_code='7117000', name='Madrid - Chamartín - Clara Campoamor', price=13.0, destination='Valencia - Joaquín Sorolla', outbound='2024-01-15')
Trip(departure_timestamp=datetime.time(11, 15), _u_i_c_station_code='7117000', name='Madrid - Chamartín - Clara Campoamor', price=9.0, destination='Valencia - Joaquín Sorolla', outbound='2024-01-15')
Trip(departure_timestamp=datetime.time(13, 15), _u_i_c_station_code='7117000', name='Madrid - Chamartín - Clara Campoamor', price=9.0, destination='Valencia - Joaquín Sorolla', outbound='2024-01-15')
Trip(departure_timestamp=datetime.time(17, 15), _u_i_c_station_code='7117000', name='Madrid - Chamartín - Clara Campoamor', price=15.0, destination='Valencia - Joaquín Sorolla', outbound='2024-01-15')
Trip(departure_timestamp=datetime.time(20, 15), _u_i_c_station_code='7117000', name='Madrid - Chamartín - Clara Campoamor', price=9.0, destination='Valencia - Joaquín Sorolla', outbound='2024-01-15')
"""
```