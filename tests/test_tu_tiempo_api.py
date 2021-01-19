import copy
from unittest import TestCase

import httpx
import respx as respx
from httpx import Response

from app.weather import TuTiempoAPI
from tests.base import api_response, day_s, hour_s


class TestTuTiempoAPI(TestCase):

    def setUp(self) -> None:
        self.api = TuTiempoAPI("api_key", locations=[1])
        self.URL = 'https://api.tutiempo.net/json/?lan=es&apid=api_key&lid=1'

    @respx.mock
    def test_collect_data(self):
        respx.get(self.URL).mock(
            return_value=Response(200, json=api_response))

        data = self.api.collect_data()

        self.assertEqual(1, len(data))
        locality = list(data.keys())[0]
        self.assertEqual(1, locality.id)
        self.assertEqual('Madrid', locality.name)
        self.assertEqual('España', locality.country)

        self.assertEqual(1, len(data[locality]['daily_forecast']))
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
                              'wind_direction': 'Nordeste'}, day_s.dump(data[locality]['daily_forecast'][0]))
        self.assertEqual(1, len(data[locality]['hourly_forecast']))
        self.assertDictEqual({'date': '2021-01-16',
                              'hour_data': '20:00',
                              'humidity': 82,
                              'icon': '1n',
                              'icon_wind': 'SE',
                              'pressure': 1031,
                              'temperature': 4,
                              'text': 'Despejado',
                              'wind': 2,
                              'wind_direction': 'Sureste'}, hour_s.dump(data[locality]['hourly_forecast'][0]))

    @respx.mock
    def test_collect_data_with_special_values(self):
        api_data = copy.deepcopy(api_response)

        api_data["day1"]["moonset"] = '--'

        respx.get(self.URL).mock(
            return_value=Response(200, json=api_data))

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
                              'wind_direction': 'Nordeste'},
                             day_s.dump(data[list(data.keys())[0]]['daily_forecast'][0]))

    @respx.mock
    def test_collect_data_404_error(self):
        respx.get(self.URL).mock(return_value=Response(404))

        data = self.api.collect_data()

        self.assertDictEqual({}, data)

    @respx.mock
    def test_collect_data_connection_error(self):
        respx.get(self.URL).mock(side_effect=httpx.ConnectError)

        data = self.api.collect_data()

        self.assertDictEqual({}, data)

