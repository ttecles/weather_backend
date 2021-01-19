from flask import url_for

from app import db, errors
from app.models import Hour, Day, Locality
from app.schema import DaySchema
from tests.base import FlaskWeatherApp, day, hour, ValidateResponseMixin


class TestApiDay(FlaskWeatherApp, ValidateResponseMixin):

    def setUp(self):
        super().setUp()
        self.locality = Locality(id=1, name='Barcelona', country='Spain')
        self.day = Day(**day, locality=self.locality)
        db.session.add_all([self.locality, self.day])

    def test_get(self):
        resp = self.client.get(url_for('api.daily_locality', locality_id=1))

        self.assertListEqual([DaySchema().dump(self.day)], resp.json)

    def test_get_invalid_location(self):
        resp = self.client.get(url_for('api.daily_locality', locality_id=2))

        self.validate_error_response(resp, errors.EntityNotFound('Locality', 2))
