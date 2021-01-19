import os

import httpx
import respx

from app.models import Hour, Day, Locality
from app.weather.tu_tiempo_api import URL
from tests.base import FlaskWeatherApp, api_response
from weather import forecast


class TestWeatherCLI(FlaskWeatherApp):

    def setUp(self):
        super().setUp()
        self.runner = self.app.test_cli_runner()

    @respx.mock
    def test_forecast(self):
        respx.get(url=URL).mock(return_value=httpx.Response(200, json=api_response))
        os.environ.update(
            {'WEATHER_API': 'TuTiempoAPI', 'WEATHER_API_KEY': 'zwDX4azaz4X4Xqs', 'WEATHER_LOCATIONS': '3768'})
        result = self.runner.invoke(forecast)

        self.assertEqual("Forecast updated\n", result.output)
        self.assertEqual(0, result.exit_code)

        self.assertEqual(1, Locality.query.count())
        self.assertEqual(1, Day.query.count())
        self.assertEqual(1, Hour.query.count())

        l = Locality.query.get(3768)
        self.assertEqual('Madrid', l.name)
        self.assertEqual('España', l.country)

        d = Day.query.one()
        self.assertEqual(l, d.locality)

    def test_forecast_invalid(self):
        os.environ.update({'WEATHER_API': 'XXX', 'WEATHER_API_KEY': 'zwDX4azaz4X4Xqs'})
        result = self.runner.invoke(forecast)

        self.assertEqual('Invalid Weather API\n', result.output)
        self.assertEqual(1, result.exit_code)