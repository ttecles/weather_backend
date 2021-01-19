from flask import url_for

from app import db, errors
from app.models import Hour, Day, Locality
from app.schema import DaySchema, LocalitySchema
from tests.base import FlaskWeatherApp, day, hour, ValidateResponseMixin


class TestApiLocality(FlaskWeatherApp, ValidateResponseMixin):

    def setUp(self):
        super().setUp()
        self.locality = Locality(id=1, name='Barcelona', country='Spain')
        db.session.add(self.locality)


    def test_get(self):
        resp = self.client.get(url_for('api.locality_list'))

        self.assertListEqual([LocalitySchema().dump(self.locality)], resp.json)
