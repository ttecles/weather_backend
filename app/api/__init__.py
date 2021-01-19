from flask import Blueprint

from .day import DayList
from .hour import HourList
from .locality import LocalityList

api = Blueprint('api', __name__)

from . import day, hour

locality_list_view = LocalityList.as_view('locality_list')
api.add_url_rule('/localities', view_func=locality_list_view, methods=['GET'])
day_list_view = DayList.as_view('daily_locality')
api.add_url_rule('/daily/locality/<int:locality_id>', view_func=day_list_view, methods=['GET'])
hour_list_view = HourList.as_view('hourly_locality')
api.add_url_rule('/hourly/locality/<int:locality_id>', view_func=hour_list_view, methods=['GET'])
