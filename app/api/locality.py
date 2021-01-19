from flask import jsonify
from flask.views import MethodView

from app.models import Locality
from app.schema import LocalitySchema


class LocalityList(MethodView):
    schema = LocalitySchema()

    def get(self):
        return jsonify([self.schema.dump(l) for l in Locality.query.all()])