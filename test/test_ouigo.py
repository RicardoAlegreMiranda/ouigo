import unittest
import json
from datetime import datetime, timedelta, time

from ouigo.ouigo import Ouigo, DateProcessingError
from ouigo.types_class import Trip, Train
from ouigo import seasson, utils, stations


class TestOuigo(unittest.TestCase):

    def setUp(self):
        self.ouigo_fr = Ouigo(country="FR")
        self.ouigo_es = Ouigo(country="ES")
        self.outbound_date = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    def test_get_list_60_days_travels_ES(self):
        result_es = self.ouigo_es.get_list_60_days_travels(outbound=self.outbound_date,
                                                           origin="MADRID",
                                                           destination="bArCelonA")

        result_fr = self.ouigo_fr.get_list_60_days_travels(outbound=self.outbound_date,
                                                           origin="paris",
                                                           destination="nANTES")

        assert isinstance(result_es, list)
        assert isinstance(result_fr, list)

        self.assertTrue(all(isinstance(trip, Train) for trip in result_es))  # Test Spain
        self.assertTrue(all(isinstance(trip, Train) for trip in result_fr))  # Test France

    def test_journal_search(self):
        result_es = self.ouigo_es.journal_search(destination="vAlEnCiA",
                                                 origin="mAdRiD",
                                                 outbound_date=self.outbound_date)

        result_fr = self.ouigo_fr.journal_search(destination="PT1",
                                                 origin="LY1",
                                                 outbound_date=self.outbound_date,
                                                 destination_is_code=True)
        # Test Spain
        assert isinstance(result_es, list)
        self.assertTrue(all(isinstance(trip, Trip) for trip in result_es))
        # Test France
        assert isinstance(result_fr, list)
        self.assertTrue(all(isinstance(trip, Trip) for trip in result_fr))

    def test_find_travels(self):
        result_es = self.ouigo_es.find_travels(origin="madrid",
                                               outbound=self.outbound_date,
                                               max_price=100,
                                               maximum_departure_time=time(23, 00),
                                               minimum_departure_time=time(6, 00))

        result_fr = self.ouigo_fr.find_travels(origin="paris",
                                               destination="Strasbourg",
                                               outbound=self.outbound_date)

        assert isinstance(result_es, list)
        self.assertTrue(all(isinstance(trip, Trip) for trip in result_es))

        assert isinstance(result_fr, list)
        self.assertTrue(all(isinstance(trip, Trip) for trip in result_fr))

    def test_find_station_code_by_name(self):
        # Prueba el método find_station_code_by_name
        target_name = "Paris"
        result = self.ouigo_fr.find_station_code_by_name(target_name)
        assert isinstance(result, str)
        self.assertEquals(result, "PT1")

    def test_find_station_name_by_code(self):
        code = "MT1"
        result = self.ouigo_es.find_station_name_by_code(code)
        assert isinstance(result, str)
        self.assertEquals(result, "Madrid - Todas las estaciones")

    def test_invalid_country(self):
        with self.assertRaises(DateProcessingError):
            Ouigo(country="INVALID_COUNTRY")

    def test_update_token(self):
        token_json = seasson.update_token(self.ouigo_es)
        assert isinstance(token_json, str)

    def test_season(self):
        sm = seasson.SessionManager()
        assert sm is not None

    def test_process_date(self):
        result = utils.process_date(self.outbound_date)
        assert isinstance(result, str)

    def test_stations(self):
        list_fr = self.ouigo_fr.list_stations
        list_es = self.ouigo_es.list_stations

        assert len(list_es) > 5
        assert len(list_fr) > 5
        assert isinstance(list_fr, list)
        assert isinstance(list_es, list)


if __name__ == '__main__':
    unittest.main()
