from datetime import datetime

from api.utils.database import db


class EmployeeModel(db.Model):
    __tablename__ = 'employees'

    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    date_of_birth = db.Column(db.DateTime)
    mobilephone = db.Column(db.String(80))
    role = db.Column(db.String(80))
    empid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, server_default=db.func.now())
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    stores = db.relationship('StoreModel')

    def __init__(self, firstname, lastname, date_of_birth, mobilephone, role, store_id):
        self.firstname = firstname
        self.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
        self.lastname = lastname
        self.mobilephone = mobilephone
        self.role = role
        self.store_id = store_id

    def json(self):
        return {
            "id": self.empid,
            "firstname": self.firstname,
            "date_of_birth": datetime.strftime(self.date_of_birth, '%Y-%m-%d'),
            "lastname": self.lastname,
            "role": self.role,
            "mobilephone": self.mobilephone,
            "store_id": self.store_id,
            "created_date": datetime.strftime(self.created_date, '%Y-%m-%d')
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(empid=_id).first()

    @classmethod
    def find_by_name(cls, lastname):
        return cls.query.filter_by(lastname=lastname).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role).all()

    @classmethod
    def find_by_store(cls, store_id):
        return cls.query.filter_by(store_id=store_id).all()
