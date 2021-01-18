from flask import jsonify
from flask.views import MethodView

from app.models import Day
from app.schema import DaySchema


class DayList(MethodView):
    schema = DaySchema()

    def get(self):
        return jsonify([self.schema.dump(d) for d in Day.query.order_by(Day.date).all()])
