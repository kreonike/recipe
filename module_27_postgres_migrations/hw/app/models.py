from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Coffee(db.Model):
    __tablename__ = 'coffee'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    origin = db.Column(db.String(200))
    intensifier = db.Column(db.String(100))
    notes = db.Column(db.ARRAY(db.String))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50))
    patronomic = db.Column(db.String(50))
    has_sale = db.Column(db.Boolean, default=False)
    address = db.Column(db.JSON)
    coffee_id = db.Column(db.Integer, db.ForeignKey('coffee.id'))
    coffee = db.relationship('Coffee', backref='users')