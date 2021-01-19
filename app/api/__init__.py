from flask import Blueprint

from .day import DayList
from .hour import HourList

api = Blueprint('api', __name__)

from . import day, hour

day_view = DayList.as_view('daily_locality')
api.add_url_rule('/days/locality/<int:locality_id>', view_func=day_view, methods=['GET'])
hour_view = HourList.as_view('hourly_locality')
api.add_url_rule('/hours/locality/<int:locality_id>', view_func=hour_view, methods=['GET'])
