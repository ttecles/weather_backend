import abc
import typing as t

from marshmallow import Schema, post_load

from app.models import Day, Hour, Locality


class BaseDaySchema(Schema):
    @post_load
    def make_day(self, data, **kwargs):
        return Day(**data)


class BaseHourSchema(Schema):
    @post_load
    def make_hour(self, data, **kwargs):
        return Hour(**data)


class BaseLocalitySchema(Schema):
    @post_load
    def make_locality(self, data, **kwargs):
        return Locality(**data)


class WeatherAPI(abc.ABC):

    @abc.abstractmethod
    def collect_data(self, timeout=None) -> t.Optional[t.Tuple[t.List[Day], t.List[Hour]]]:
        """

        :return: dictionary with day_day forecast and hour_hour forecast. Objects must match with Day and Hour models

        """
        pass


class DaylyHourlyForecastMixin:
    day_schema: t.ClassVar[BaseDaySchema]
    hour_schema: t.ClassVar[BaseHourSchema]
    locality_schema: t.ClassVar[BaseLocalitySchema]

    def load_data(self, json_forecast) -> t.Optional[t.Dict[Locality, t.Dict[str, t.List[t.Union[Hour, Day]]]]]:
        if self.day_schema is None:
            raise ValueError(f'No day_schema specified on {self.__class__.__name__}')
        if self.hour_schema is None:
            raise ValueError(f'No hour_schema specified on {self.__class__.__name__}')
        if self.locality_schema is None:
            raise ValueError(f'No locality_schema specified on {self.__class__.__name__}')

        forecast = {}
        for l in json_forecast:
            days = l.pop('daily_forecast')
            hours = l.pop('hourly_forecast')
            locality = self.locality_schema.load(l)
            daily_forecast = []
            hourly_forecast = []
            for d in days:
                d.update(locality_id=locality.id)
                daily_forecast.append(self.day_schema.load(d))
            for h in hours:
                h.update(locality_id=locality.id)
                hourly_forecast.append(self.hour_schema.load(h))
            forecast[locality] = dict(daily_forecast=daily_forecast, hourly_forecast=hourly_forecast)
        return forecast
