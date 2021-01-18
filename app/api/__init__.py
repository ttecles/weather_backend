from flask import Blueprint

from .day import DayList
from .hour import HourList

api = Blueprint('api', __name__)

from . import day, hour

day_view = DayList.as_view('daylist')
api.add_url_rule('/days/', view_func=day_view, methods=['GET'])
hour_view = HourList.as_view('hourlist')
api.add_url_rule('/hours/', view_func=hour_view, methods=['GET'])
