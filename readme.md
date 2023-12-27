# Ouigo Python


This module allows you to retrieve the travels in the API of Ouigo, It also serves to filter the best prices and schedules when searching for trains

This is done directly through Ouigo's API, and does not require an API key. All information is obtained by public methods.

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
```python
from ouigo import Ouigo

# ES for search in Spain or FR for search in France
API = Ouigo(country="es")  
travels = API.find_travels(origin="Madrid", 
                           destination="Barcelona",
                           outbound="2024-01-21",  # you can use this format(yyyy-mm-dd) or datetime object
                           max_price=140,
                           maximum_departure_time=time(23, 00), 
                           minimum_departure_time=time(5, 00))
for train in travels:
    print(train)
    print(f"price {train.price}, is the best price? {train.is_best_price}")
```

Trip(departure_timestamp=datetime.time(7, 5), _u_i_c_station_code='7160000', name='Madrid - Puerta de Atocha - Almudena Grandes', price=22.0, destination='Barcelona - Sants', outbound='2024-01-21')
destination Barcelona - Sants price 22.0 