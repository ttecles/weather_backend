import datetime as dt
from unittest import TestCase

import flask

from app import create_app, db, errors
from app.schema import DaySchema, HourSchema, LocalitySchema

day = dict(date=dt.date(2021, 1, 16), temperature_max=8, temperature_min=-1, icon="4", text="Parcialmente nuboso",
           humidity=85, wind=4, wind_direction="Nordeste", icon_wind="NE", sunrise=dt.time(8, 30),
           sunset=dt.time(21, 00),
           moonrise=dt.time(10, 0), moonset=dt.time(22, 0), moon_phases_icon="4")
hour = dict(date=dt.date(2021, 1, 16), hour_data=dt.time(20, 0), temperature=4, text="Despejado", humidity=82,
            pressure=1031, icon="1n", wind=2, wind_direction="Sureste", icon_wind="SE")

day_s = DaySchema()
hour_s = HourSchema()
locality_s = LocalitySchema()

api_response = {
    "locality":
        {
            "name": "Madrid",
            "country": "España",
        }, "day1": day_s.dump(day),
    "hour_hour": {"hour1": hour_s.dump(hour)},
}


class ValidateResponseMixin:
    def validate_error_response(self, resp: flask.Response, error: errors.BaseError):
        if hasattr(self, 'assertEqual') and hasattr(self, 'assertDictEqual'):
            self.assertEqual(error.status_code, resp.status_code)
            self.assertDictEqual(errors.format_error_content(error), resp.get_json())


class FlaskWeatherApp(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
