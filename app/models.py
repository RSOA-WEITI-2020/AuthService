from extensions import db
from sqlalchemy.dialects.mysql import DECIMAL

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    balance = db.Column(DECIMAL(precision=10, scale=2, unsigned=True), nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(80), nullable=False)
