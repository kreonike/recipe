from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Client(db.Model):
    """Модель клиента"""

    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    parking_logs = db.relationship('ClientParking', backref='client', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'credit_card': self.credit_card,
            'car_number': self.car_number,
        }


class Parking(db.Model):
    """Модель парковки"""

    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client_logs = db.relationship('ClientParking', backref='parking', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'opened': self.opened,
            'count_places': self.count_places,
            'count_available_places': self.count_available_places,
        }


class ClientParking(db.Model):
    """Модель пребывания клиента на парковке"""

    __tablename__ = 'client_parking'
    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'parking_id': self.parking_id,
            'time_in': self.time_in.isoformat() if self.time_in else None,
            'time_out': self.time_out.isoformat() if self.time_out else None,
        }
