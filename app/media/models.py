from app import db
from flask import current_app as app
from sqlalchemy.orm import column_property
from sqlalchemy import desc, asc


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer(), primary_key=True)
    instagram = db.Column(db.String(255), unique=True)
    website = db.Column(db.String(255))
    locations = db.Column(db.String(255))
    types = db.Column(db.String(255))

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
        return Media.query.order_by(o).paginate(page, per_page, error_out=False)


    @classmethod
    def all(cls):
        return db.session.query(cls).all()
