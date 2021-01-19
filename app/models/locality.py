from app import db


class Locality(db.Model):
    __tablename__ = 'Locality'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40))
    country = db.Column(db.String(40))

    def __str__(self):
        return f"{self.name}({self.country})"
