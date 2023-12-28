from ouigo import Ouigo

# ES for search in Spain or FR for search in France
API = Ouigo(country="ES")
prices_to_valencia = API.journal_search(outbound_date="2024-01-15",
                                        origin="Madrid",
                                        destination="Valencia")
for prices in prices_to_valencia:
    print(prices)

"""
# Le envío una fecha de inicio, un número de veces y el día de sálida (viernes, sábado, domingo, etc..) y me
# devuelve una lista con fechas ordenadas, (Semana 1, semana 2, ...)
def obtener_listado_fechas(fecha_inicio, numero_busquedas: int, dia_semana_salida: int):
    # Convierte la fecha de inicio en un objeto datetime
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    # Crea el listado de fecha
    lista_fechas = []

    # Si el día de salida es 7 o superior, significa que NO devuelve salidas en día de semana (viernes, sabado, ...)
    # devuelve días consecutivos normales, sin que sean solo 1 día a la semana
    if dia_semana_salida <= 6:

        # Aquí busca fecha 1 día por semana (3,10,17,...)
        while True:
            if fecha_inicio.weekday() == dia_semana_salida:
                lista_fechas.append(fecha_inicio)

            fecha_inicio += timedelta(days=1)

            if len(lista_fechas) >= numero_busquedas:
                break
    # Aquí devuelve todos los días de la semana (día 1,2,3,4...)
    else:
        for i in range(numero_busquedas):
            # Añadimos la fecha actual a la lista.
            lista_fechas.append(fecha_inicio)

            # Sumamos un día a la fecha actual.
            fecha_inicio += timedelta(days=1)

    return lista_fechas

def main():
    API = Ouigo(country="es")
    today = datetime.today()
    viernes = obtener_listado_fechas(today, 16, 5)
    lista_vuelta = []
    futuros = []
    for dia in viernes:
        with ThreadPoolExecutor() as executor:
            # Utiliza la multitarea para buscar viajes de ida en paralelo
            futuro = executor.submit(API.find_travels(origin="Madrid",
                                                      outbound=dia,
                                                      max_price=25,
                                                      maximum_departure_time=time(12, 00),
                                                      minimum_departure_time=time(7, 00)))
            futuros.append(futuro)

        # Obtén el resultado del único futuro (en este caso)
        for futuro in futuros:
            r = futuro.result()
            for res in r:
                print(res)
        # Puedes hacer más cosas con el resultado aquí


if __name__ == "__main__":
    main()



# Guarda el tiempo de inicio
inicio = datetime.now()
API = Ouigo(country="es")
hoy = datetime.today()
viernes = obtener_listado_fechas(hoy, 2, 4)
lista = []
lista_vuelta = []
futuros = []
with ThreadPoolExecutor() as executor:
    for dia in viernes:

        viajes = executor.submit(API.find_travels(origin="Madrid",
                                                  destination="Barcelona",
                                                  outbound=dia,
                                                  max_price=20,
                                                  maximum_departure_time=time(12, 00),
                                                  minimum_departure_time=time(7, 00)))

        futuros.append(viajes)
        for futu in futuros:
            for f in futu:
                viajes = f.result()

        for viaje_ida in viajes:
            lista.append(viaje_ida)
    for viaje_ida in lista:
        fecha_datetime = datetime.strptime(viaje_ida.outbound, "%Y-%m-%d")
        fecha_vuelta = fecha_datetime + timedelta(days=1)

        viajes_vuelta = API.find_travels(origin=viaje_ida.destination,
                                         outbound=fecha_vuelta,
                                         max_price=20,
                                         minimum_departure_time=time(11, 00),
                                         maximum_departure_time=time(19, 00))


        for vuelta in viajes_vuelta:
            if (viaje_ida.price + vuelta.price) < 41:
                mensaje = (f"destino {viaje_ida.destination}, "
                           f"fecha {viaje_ida.outbound}, "
                           f"salida {viaje_ida.departure_timestamp}, "
                           f"vuelta {vuelta.departure_timestamp}, "
                           f"precio total = {(viaje_ida.price + vuelta.price)}")
                lista_vuelta.append(mensaje)

mi_lista_sin_duplicados = list(set(lista_vuelta))
for viaje in mi_lista_sin_duplicados:
    print(viaje)
# Guarda la fecha y hora de finalización
fin = datetime.now()

# Calcula la diferencia para obtener el tiempo total
tiempo_total = fin - inicio

print(f"El script tardó {tiempo_total} segundos en ejecutarse.")

"""
