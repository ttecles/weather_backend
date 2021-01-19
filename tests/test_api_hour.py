import datetime as dt
from unittest import mock

from flask import url_for

from app import db, errors
from app.models import Hour, Locality
from app.schema import HourSchema
from tests.base import FlaskWeatherApp, hour, ValidateResponseMixin


class TestApiDay(FlaskWeatherApp, ValidateResponseMixin):

    def setUp(self):
        super().setUp()
        self.locality = Locality(id=1, name='Barcelona', country='Spain')
        self.hour = Hour(**hour, locality=self.locality)
        db.session.add(self.hour)

    @mock.patch('app.api.hour.get_now')
    def test_get(self, mock_get_now):
        with self.subTest("get"):
            mock_get_now.return_value = dt.datetime(2021, 1, 16, 19, 0)
            resp = self.client.get(url_for('api.hourly_locality', locality_id=1))

            self.assertListEqual([HourSchema().dump(self.hour)], resp.json)

        with self.subTest("older now"):
            mock_get_now.return_value = dt.datetime(2021, 1, 16, 20, 5)
            resp = self.client.get(url_for('api.hourly_locality', locality_id=1))

            self.assertListEqual([], resp.json)

    def test_get_invalid_location(self):
        resp = self.client.get(url_for('api.hourly_locality', locality_id=2))

        self.validate_error_response(resp, errors.EntityNotFound('Locality', 2))
