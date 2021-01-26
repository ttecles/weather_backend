from flask import jsonify
from flask.views import MethodView

from app.models import Day, Locality
from app.schema import DaySchema


class DayList(MethodView):
    schema = DaySchema()

    def get(self, locality_id):
        l = Locality.query.get_or_raise(locality_id)
        return jsonify(
            [self.schema.dump(d) for d in Day.query.filter_by(locality_id=locality_id).order_by(Day.date).all()])
