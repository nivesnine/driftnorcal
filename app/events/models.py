from app import db
from flask import current_app as app
from sqlalchemy.orm import column_property
from sqlalchemy import desc, asc
from datetime import date

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    date = db.Column(db.Date())
    host = db.Column(db.Integer())
    location = db.Column(db.Integer())
    price = db.Column(db.Integer())
    details = db.Column(db.String())

    def __eq__(self, other):
        return self.name

    def __ne__(self, other):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    @classmethod
    def get_sortable_list(cls, order, direction, page):
        per_page = app.config["ADMIN_PER_PAGE"]
        if direction == 'desc':
            o = desc(order)
        else:
            o = asc(order)
        return Event.query.order_by(o).paginate(page, per_page, error_out=False)


    @classmethod
    def get_upcoming(cls):
        return db.session.query(cls).filter(Event.date >= date.today()).all()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()
