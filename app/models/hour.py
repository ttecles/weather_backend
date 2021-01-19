from app import db


class Hour(db.Model):
    __tablename__ = 'Hour'
    locality_id = db.Column(db.Integer, db.ForeignKey('Locality.id'), primary_key=True, nullable=False)
    date = db.Column(db.Date(), primary_key=True)  # "2021-1-15"
    hour_data = db.Column(db.Time(), primary_key=True)  # "13:00",
    temperature = db.Column(db.Integer)  # -1,
    icon = db.Column(db.String(10))  # "6",
    text = db.Column(db.String(80))  # "Mostly cloudy",
    humidity = db.Column(db.Integer)  # 89,
    wind = db.Column(db.Integer)  # 4,
    wind_direction = db.Column(db.String(30))  # "Northwest",
    icon_wind = db.Column(db.String(10))  # "NO",
    pressure = db.Column(db.Integer)  # 1016,

    locality = db.relationship("Locality", backref="hour_forecast")