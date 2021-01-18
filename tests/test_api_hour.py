import datetime as dt
from unittest import mock

from flask import url_for

from app import db
from app.models import Hour
from app.schema import HourSchema
from tests.base import FlaskWeatherApp, hour


class TestApiDay(FlaskWeatherApp):

    def setUp(self):
        super().setUp()
        self.hour = Hour(**hour)
        db.session.add(self.hour)

    @mock.patch('app.api.hour.get_now')
    def test_get(self, mock_get_now):
        with self.subTest("get"):
            mock_get_now.return_value = dt.datetime(2021, 1, 16, 19, 0)
            resp = self.client.get(url_for('api.hourlist'))

            self.assertListEqual([HourSchema().dump(self.hour)], resp.json)

        with self.subTest("older now"):
            mock_get_now.return_value = dt.datetime(2021, 1, 16, 20, 5)
            resp = self.client.get(url_for('api.hourlist'))

            self.assertListEqual([], resp.json)
