from datetime import datetime

from api.utils.database import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    created = db.Column(db.DateTime, server_default=db.func.now())

    employees = db.relationship('EmployeeModel', lazy='dynamic')
    medicaments = db.relationship('MedicamentModel', lazy='dynamic')

    def __init__(self, name, description, address):
        self.name = name
        self.description = description
        self.address = address

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "created_date": datetime.strftime(self.created, '%Y-%m-%d')
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
