from flask import url_for

from app import db
from app.models import Hour, Day
from app.schema import DaySchema
from tests.base import FlaskWeatherApp, day, hour


class TestApiDay(FlaskWeatherApp):

    def setUp(self):
        super().setUp()
        self.day = Day(**day)
        self.hour = Hour(**hour)
        db.session.add_all([self.day, self.hour])

    def test_get(self):
        resp = self.client.get(url_for('api.daylist'))

        self.assertListEqual([DaySchema().dump(self.day)], resp.json)