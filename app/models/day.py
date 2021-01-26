from app import db


class Day(db.Model):
    __tablename__ = 'Day'
    locality_id = db.Column(db.Integer, db.ForeignKey('Locality.id'), primary_key=True, nullable=False)
    date = db.Column(db.Date(), primary_key=True, nullable=False)  # "2021-1-15"
    temperature_max = db.Column(db.Integer)  # 7,
    temperature_min = db.Column(db.Integer)  # -1,
    icon = db.Column(db.String(10))  # "6",
    text = db.Column(db.String(80))  # "Mostly cloudy",
    humidity = db.Column(db.Integer)  # 89,
    wind = db.Column(db.Integer)  # 4,
    wind_direction = db.Column(db.String(30))  # "Northwest",
    icon_wind = db.Column(db.String(10))  # "NO",
    sunrise = db.Column(db.Time())  # "8:37",
    sunset = db.Column(db.Time())  # "18:10",
    moonrise = db.Column(db.Time())  # "10:28",
    moonset = db.Column(db.Time())  # "20:43",
    moon_phases_icon = db.Column(db.String(10))  # "2"

    locality = db.relationship("Locality", backref="day_forecast")
