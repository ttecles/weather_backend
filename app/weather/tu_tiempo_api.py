import logging
import re
import typing as t

import requests
from marshmallow import pre_load

from app.models import Day, Hour
from app.schema import DaySchema as RestDaySchema, HourSchema as RestHourSchema
from app.weather.base import BaseDaySchema, BaseHourSchema, WeatherAPI, DayHourForecast

# defaults
URL = 'https://api.tutiempo.net/json/'
DEFAULT_GEOLOCATION = (40.4178, -3.7022)  # Madrid
LANGUAGES = ('es', 'en', 'fr', 'pt', 'de', 'it')
DEFAULT_LANGUAGE = 'es'

hour_pattern = re.compile('\d?\d:\d\d')


class DaySchema(BaseDaySchema, RestDaySchema):

    @pre_load
    def clean_data(self, data, **kwargs):
        for k, v in data.items():
            if k in ('sunrise', 'sunset', 'moonrise', 'moonset'):
                if not hour_pattern.search(data[k]):
                    data[k] = None
        return data


class HourSchema(BaseHourSchema, RestHourSchema):
    ...


class TuTiempoAPI(WeatherAPI, DayHourForecast):
    TIMEOUT = 30
    day_schema = DaySchema()
    hour_schema = HourSchema()

    def __init__(self, api_key: str, geolocation: t.Tuple[float, float] = None, language: str = None):
        """ Set initial parameters

        :param api_key: ID
        :param geolocation: (latitude,longitude) weather
        :param language: Output language, can be: es, en, fr, pt, de, it
        """
        self.api_key = api_key
        self.latitude, self.longitude = geolocation or DEFAULT_GEOLOCATION
        self.language = language or DEFAULT_LANGUAGE
        if self.language not in LANGUAGES:
            raise ValueError('invalid language')

    def collect_data(self, timeout=None) -> t.Optional[t.Tuple[t.List[Day], t.List[Hour]]]:
        try:
            resp = requests.get(
                URL + f"?lan={self.language}&apid={self.api_key}&ll={self.latitude},{self.longitude}",
                timeout=timeout)
            resp.raise_for_status()
        except Exception as e:
            logging.exception("Error collecting weather data")
            return None
        data = resp.json()
        days = [v for k, v in data.items() if k.startswith('day')]
        hours = [v for k, v in data['hour_hour'].items()]
        return self.load_data(days, hours)
