import unittest
import json
from datetime import datetime, timedelta, time

from ouigo.ouigo import DateProcessingError as ProcessingErrorOuigo
from ouigo.ouigo import Ouigo
from ouigo.types_class import Trip, Train
from ouigo import seasson, utils, stations
from ouigo.utils import DateProcessingError as ProcessingErrorUtils

import requests

"""The tests check if the real APIs work. That is why it is not possible to mock exceptions. 
When performing real tests, the API does not return the expected exceptions when mocking errors"""


class TestOuigo(unittest.TestCase):

    def setUp(self):
        self.ouigo_fr = Ouigo(country="FR")
        self.ouigo_es = Ouigo(country="ES")
        self.outbound_date = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    def test_get_list_60_days_travels(self):
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

    def test_get_list_60_days_travels_raises(self):
        with self.assertRaises(ProcessingErrorUtils):
            result = self.ouigo_es.get_list_60_days_travels(outbound="2023-01-01",  # bad outbound date
                                                            origin="MADRID",
                                                            destination="bArCelonA")
            self.assertIsNone(result)

        with self.assertRaises(ProcessingErrorOuigo):
            self.ouigo_es.get_list_60_days_travels(outbound=self.outbound_date,
                                                   origin="MADRID",
                                                   destination="FAIL")  # bad destination date

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

    def test_journal_search_raises(self):
        with self.assertRaises(ProcessingErrorOuigo):
            self.ouigo_es.journal_search(destination="vAlEnCiA",
                                         origin="FAIL",  # bad origin date
                                         outbound_date=self.outbound_date)

    def test_find_travels(self):
        result_es = self.ouigo_es.find_travels(origin="madrid",
                                               outbound=self.outbound_date,
                                               max_price=10,
                                               maximum_departure_time=time(17, 00),
                                               minimum_departure_time=time(10, 00))

        datetime_outbound = (datetime.today() + timedelta(days=7))
        result_fr = self.ouigo_fr.find_travels(origin="paris",
                                               destination="Strasbourg",
                                               outbound=datetime_outbound,
                                               max_price=25,
                                               minimum_departure_time=time(17, 00),
                                               maximum_departure_time=time(10, 15))

        assert isinstance(result_es, list)
        self.assertTrue(all(isinstance(trip, Trip) for trip in result_es))

        assert isinstance(result_fr, list)
        self.assertTrue(all(isinstance(trip, Trip) for trip in result_fr))

    def test_find_station_code_by_name(self):
        # Prueba el método find_station_code_by_name
        target_name = "Paris"
        result = self.ouigo_fr.find_station_code_by_name(target_name)
        assert isinstance(result, str)
        self.assertEqual(result, "PT1")

    def test_find_station_name_by_code(self):
        code = "MT1"
        result = self.ouigo_es.find_station_name_by_code(code)
        assert isinstance(result, str)
        self.assertEqual(result, "Madrid - Todas las estaciones")

    def test_invalid_country(self):
        with self.assertRaises(ProcessingErrorOuigo):
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

    def test_get_time_from_string(self):
        time_string = "2023-12-31T08:30:00+0000"
        expected_time = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S%z").time()
        result_time = utils.get_time_from_string(time_string)
        self.assertEqual(result_time, expected_time)

    def test_process_date_invalid_date_format(self):
        input_date_str = "2023-01-32"

        with self.assertRaises(ProcessingErrorUtils):
            utils.process_date(input_date_str)

    def test_input_date_earlier_than_current_date(self):
        current_date = datetime.now()
        input_date = current_date - timedelta(days=1)
        input_date_str = input_date.strftime("%Y-%m-%d")
        with self.assertRaises(ProcessingErrorUtils):
            utils.process_date(input_date_str)

    def test_input_date_more_than_5_months_ahead(self):
        current_date = datetime.now()
        input_date_str = (current_date + timedelta(days=30 * 6)).strftime("%Y-%m-%d")
        with self.assertRaises(ProcessingErrorUtils):
            utils.process_date(input_date_str)


if __name__ == '__main__':
    unittest.main()
