from app import db


class Day(db.Model):
    __tablename__ = 'Day'
    date = db.Column(db.Date(), primary_key=True)  # "2021-1-15"
    temperature_max = db.Column(db.Integer)  # 7,
    temperature_min = db.Column(db.Integer)  # -1,
    icon = db.Column(db.String(10))  # "6",
    text = db.Column(db.String(30))  # "Mostly cloudy",
    humidity = db.Column(db.Integer)  # 89,
    wind = db.Column(db.Integer)  # 4,
    wind_direction = db.Column(db.String(30))  # "Northwest",
    icon_wind = db.Column(db.String(10))  # "NO",
    sunrise = db.Column(db.Time())  # "8:37",
    sunset = db.Column(db.Time())  # "18:10",
    moonrise = db.Column(db.Time())  # "10:28",
    moonset = db.Column(db.Time())  # "20:43",
    moon_phases_icon = db.Column(db.String(10))  # "2"


class Hour(db.Model):
    __tablename__ = 'Hour'
    date = db.Column(db.Date(), primary_key=True)  # "2021-1-15"
    hour_data = db.Column(db.Time(), primary_key=True)  # "13:00",
    temperature = db.Column(db.Integer)  # -1,
    icon = db.Column(db.String(10))  # "6",
    text = db.Column(db.String(30))  # "Mostly cloudy",
    humidity = db.Column(db.Integer)  # 89,
    wind = db.Column(db.Integer)  # 4,
    wind_direction = db.Column(db.String(30))  # "Northwest",
    icon_wind = db.Column(db.String(10))  # "NO",
    pressure = db.Column(db.Integer)  # 1016,
