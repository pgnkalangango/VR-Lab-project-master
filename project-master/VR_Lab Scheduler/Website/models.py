from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Datetime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startdatetime = db.Column(db.DateTime)
    enddatetime = db.Column(db.DateTime)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(150))
    yuh = db.Column(db.String(150))
    name = db.Column(db.String(150))