from datetime import datetime

from api.utils.database import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    name = db.Column(db.String(80))
    creation_date = db.Column(db.DateTime, server_default=db.func.now())
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    medicaments = db.relationship('MedicamentModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_date": datetime.strftime(self.creation_date, '%Y-%m-%d')
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
