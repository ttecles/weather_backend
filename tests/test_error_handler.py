from flask import url_for
from werkzeug.exceptions import InternalServerError

from app import errors
from tests.base import FlaskWeatherApp


class TestApi(FlaskWeatherApp):

    def test_entity_not_found_error(self):
        def raise_error():
            raise errors.EntityNotFound('Locality', '123')

        self.app.add_url_rule('/error', 'error', raise_error)

        resp = self.client.get(url_for('error'), json={})

        self.assertEqual(404, resp.status_code)
        self.assertDictEqual({'error': {'type': 'EntityNotFound',
                                        'message': "entity with given id doesn't exist",
                                        'entity': 'Locality',
                                        'id': '123'}},
                             resp.get_json())

    def test_internal_server_error(self):
        self.app.config['PROPAGATE_EXCEPTIONS'] = False

        def raise_error():
            raise RuntimeError('error content')

        self.app.add_url_rule('/error', 'error', raise_error)
        resp = self.client.get(url_for('error'), json={})

        self.assertEqual(500, resp.status_code)
        self.assertDictEqual({'error': {'type': "InternalServerError", "message": InternalServerError.description}},
                             resp.get_json())
