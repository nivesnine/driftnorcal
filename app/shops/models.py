from app import db
from flask import current_app as app
from sqlalchemy.orm import column_property
from sqlalchemy import desc, asc


class Shops(db.Model):
    __tablename__ = 'shops'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Integer)
    bio = db.Column(db.String(255))

    def __eq__(self, other):
        return self.name

    def __ne__(self, other):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

