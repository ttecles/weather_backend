import copy
from unittest import TestCase

import responses

from app.weather import TuTiempoAPI
from app.weather.tu_tiempo_api import URL
from tests.base import api_response, day_s, hour_s


class TestTuTiempoAPI(TestCase):

    def setUp(self) -> None:
        self.api = TuTiempoAPI("api_key", geolocation=(1.0, 1.0))

    @responses.activate
    def test_collect_data(self):
        responses.add(responses.GET, url=URL, json=api_response)

        data = self.api.collect_data()
        self.assertEqual(1, len(responses.calls))
        self.assertEqual(f'{URL}?lan=es&apid=api_key&ll=1.0,1.0',
                         responses.calls[0].request.url)

        self.assertDictEqual({'date': '2021-01-16',
                              'humidity': 85,
                              'icon': '4',
                              'icon_wind': 'NE',
                              'moon_phases_icon': '4',
                              'moonrise': '10:00',
                              'moonset': '22:00',
                              'sunrise': '08:30',
                              'sunset': '21:00',
                              'temperature_max': 8,
                              'temperature_min': -1,
                              'text': 'Parcialmente nuboso',
                              'wind': 4,
                              'wind_direction': 'Nordeste'}, day_s.dump(data[0][0]))
        self.assertDictEqual({'date': '2021-01-16',
                              'hour_data': '20:00',
                              'humidity': 82,
                              'icon': '1n',
                              'icon_wind': 'SE',
                              'pressure': 1031,
                              'temperature': 4,
                              'text': 'Despejado',
                              'wind': 2,
                              'wind_direction': 'Sureste'}, hour_s.dump(data[1][0]))

    @responses.activate
    def test_collect_data_with_special_values(self):
        api_data = copy.deepcopy(api_response)

        api_data["day1"]["moonset"] = '--'

        responses.add(responses.GET, url=URL, json=api_data)

        data = self.api.collect_data()

        self.assertDictEqual({'date': '2021-01-16',
                              'humidity': 85,
                              'icon': '4',
                              'icon_wind': 'NE',
                              'moon_phases_icon': '4',
                              'moonrise': '10:00',
                              'moonset': None,
                              'sunrise': '08:30',
                              'sunset': '21:00',
                              'temperature_max': 8,
                              'temperature_min': -1,
                              'text': 'Parcialmente nuboso',
                              'wind': 4,
                              'wind_direction': 'Nordeste'}, day_s.dump(data[0][0]))

    @responses.activate
    def test_collect_data_404_error(self):
        responses.add(responses.GET, url=URL, status=404)

        data = self.api.collect_data()

        self.assertIsNone(data)

    @responses.activate
    def test_collect_data_connection_error(self):
        responses.add(responses.GET, url=URL, body=ConnectionError())

        data = self.api.collect_data()

        self.assertIsNone(data)

    @responses.activate
    def test_collect_data_404_error(self):
        responses.add(responses.GET, url=URL, status=404)

        data = self.api.collect_data()

        self.assertIsNone(data)
