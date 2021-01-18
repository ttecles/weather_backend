import abc
import typing as t

from marshmallow import Schema, post_load

from app.models import Day, Hour


class BaseDaySchema(Schema):
    @post_load
    def make_day(self, data, **kwargs):
        return Day(**data)


class BaseHourSchema(Schema):
    @post_load
    def make_hour(self, data, **kwargs):
        return Hour(**data)


class WeatherAPI(abc.ABC):

    @abc.abstractmethod
    def collect_data(self, timeout=None) -> t.Optional[t.Tuple[t.List[Day], t.List[Hour]]]:
        """

        :return: dictionary with day_day forecast and hour_hour forecast. Objects must match with Day and Hour models

        """
        pass


class DayHourForecast:
    day_schema: t.ClassVar[BaseDaySchema]
    hour_schema: t.ClassVar[BaseHourSchema]

    def load_data(self, days, hours):
        if self.day_schema is None:
            raise ValueError(f'No day_schema specified on {self.__class__.__name__}')
        if self.hour_schema is None:
            raise ValueError(f'No hour_schema specified on {self.__class__.__name__}')
        return [self.day_schema.load(d) for d in days], [self.hour_schema.load(h) for h in hours]
