import inspect
import typing as t

from app.weather.tu_tiempo_api import TuTiempoAPI

if t.TYPE_CHECKING:
    from app.weather.base import WeatherAPI
__all__ = [TuTiempoAPI]


def creator() -> t.Dict[str, t.Type['WeatherAPI']]:
    from app.weather.base import WeatherAPI
    return {cls.__name__: cls for cls in __all__ if inspect.isclass(cls) and issubclass(cls, WeatherAPI)}


_factories = creator()


def weather_factory(api: str, **kwargs) -> 'WeatherAPI':
    if api not in _factories:
        raise ValueError('Unknown API')
    else:
        api_kls = _factories[api]
        return api_kls(**kwargs)
