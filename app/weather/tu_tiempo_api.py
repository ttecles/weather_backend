import asyncio
import logging
import re
import typing as t

import httpx as httpx
from marshmallow import pre_load, fields

from app.models import Day, Hour, Locality
from app.schema import DaySchema as RestDaySchema, HourSchema as RestHourSchema, LocalitySchema as RestLocalitySchema
from app.weather.base import BaseDaySchema, BaseHourSchema, WeatherAPI, BaseLocalitySchema, DailyHourlyForecastMixin

# defaults
URL = 'https://api.tutiempo.net/json/'
DEFAULT_LOCATION_ID = [3768]  # Madrid
LANGUAGES = ('es', 'en', 'fr', 'pt', 'de', 'it')
DEFAULT_LANGUAGE = 'es'

hour_pattern = re.compile('\d?\d:\d\d')


class LocalitySchema(BaseLocalitySchema, RestLocalitySchema):
    ...


class DaySchema(BaseDaySchema, RestDaySchema):
    locality_id = fields.Integer()

    @pre_load
    def clean_data(self, data, **kwargs):
        for k, v in data.items():
            if k in ('sunrise', 'sunset', 'moonrise', 'moonset'):
                if not hour_pattern.search(data[k]):
                    data[k] = None
        return data


class HourSchema(BaseHourSchema, RestHourSchema):
    locality_id = fields.Integer()


class TuTiempoAPI(WeatherAPI, DailyHourlyForecastMixin):
    TIMEOUT = 30
    day_schema = DaySchema()
    hour_schema = HourSchema()
    locality_schema = LocalitySchema()

    def __init__(self, api_key: str, locations: t.List[int] = None, language: str = None):
        """ Set initial parameters

        :param api_key: ID
        :param geolocation: (latitude,longitude) weather
        :param language: Output language, can be: es, en, fr, pt, de, it
        """
        self.api_key = api_key
        self.l_ids = locations or DEFAULT_LOCATION_ID
        self.language = language or DEFAULT_LANGUAGE
        if self.language not in LANGUAGES:
            raise ValueError('invalid language')

    async def get_locality_data(self, client, locality):
        resp = await client.get(URL + f"?lan={self.language}&apid={self.api_key}&lid={locality}")
        resp.raise_for_status()
        return resp.json()

    async def async_collect_data(self, timeout):
        async with httpx.AsyncClient(timeout=timeout) as client:
            tasks = [self.get_locality_data(client, l) for l in self.l_ids]
            return await asyncio.gather(*tasks, return_exceptions=False)

    def collect_data(self, timeout=None) -> t.Optional[t.Dict[Locality, t.Dict[str, t.List[t.Union[Hour, Day]]]]]:
        fetched = []

        try:
            responses = asyncio.run(self.async_collect_data(timeout))
        except:
            logging.exception("Error while fetching data")
            return {}
        for l_id, data in zip(self.l_ids, responses):
            locality = {'id': l_id, 'name': data.get('locality').get('name'),
                        'country': data.get('locality').get('country')}

            days = [v for k, v in data.items() if k.startswith('day')]
            hours = [v for k, v in data['hour_hour'].items()]
            locality.update(daily_forecast=days)
            locality.update(hourly_forecast=hours)
            fetched.append(locality)
        return self.load_data(fetched)
