import datetime as dt

from flask import jsonify
from flask.views import MethodView

from app.models import Hour, Locality
from app.schema import HourSchema
from app.utils import get_now


class HourList(MethodView):
    schema = HourSchema()

    def get(self, locality_id):
        l = Locality.query.get_or_raise(locality_id)
        return jsonify([self.schema.dump(d) for d in
                        Hour.query.filter_by(locality_id=locality_id).order_by(Hour.date, Hour.hour_data).all() if
                        dt.datetime.combine(date=d.date, time=d.hour_data) >= get_now()])