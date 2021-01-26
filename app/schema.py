from marshmallow import fields, Schema


class LocalitySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    country = fields.String(allow_none=True)


class DaySchema(Schema):
    """default Day Schema"""
    date = fields.Date(format="%Y-%m-%d")  # "2021-1-15"
    temperature_max = fields.Integer()  # 7,
    temperature_min = fields.Integer()  # -1,
    icon = fields.String()  # "6",
    text = fields.String()  # "Mostly cloudy",
    humidity = fields.Integer()  # 89,
    wind = fields.Integer()  # 4,
    wind_direction = fields.String()  # "Northwest",
    icon_wind = fields.String()  # "NO",
    sunrise = fields.Time(format="%H:%M", allow_none=True)  # "8:37",
    sunset = fields.Time(format="%H:%M", allow_none=True)  # "18:10",
    moonrise = fields.Time(format="%H:%M", allow_none=True)  # "10:28",
    moonset = fields.Time(format="%H:%M", allow_none=True)  # "20:43",
    moon_phases_icon = fields.String()  # "2"


class HourSchema(Schema):
    """default Hour Schema"""
    date = fields.Date(format="%Y-%m-%d")  # "2021-1-15"
    hour_data = fields.Time(format="%H:%M")
    temperature = fields.Integer()  # -1,
    icon = fields.String()  # "6",
    text = fields.String()  # "Mostly cloudy",
    humidity = fields.Integer()  # 89,
    wind = fields.Integer()  # 4,
    wind_direction = fields.String()  # "Northwest",
    icon_wind = fields.String()  # "NO",
    pressure = fields.Integer()
