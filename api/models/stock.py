from datetime import datetime

from api.utils.database import db


class StockModel(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_num = db.Column(db.Integer)
    to_stock = db.Column(db.Integer)
    accepted_to_stock = db.Column(db.Integer)
    is_stocked = db.Column(db.Boolean, default=False)
    is_canceled = db.Column(db.Boolean, default=False)
    canceled_num = db.Column(db.Integer)
    date_of_stock = db.Column(db.DateTime)
    date_availability = db.Column(db.DateTime)
    med_id = db.Column(db.Integer, db.ForeignKey('medicaments.id'))

    medicaments = db.relationship('MedicamentModel')

    def __init__(self, stock_num, to_stock, accepted_to_stock,
                 is_stocked, is_canceled, canceled_num, date_of_stock,
                 date_availability, med_id):
        self.stock_num = stock_num
        self.to_stock = to_stock
        self.accepted_to_stock = accepted_to_stock
        self.is_stocked = is_stocked
        self.is_canceled = is_canceled
        self.canceled_num = canceled_num
        self.date_of_stock = datetime.strptime(date_of_stock, '%Y-%m-%d')
        self.date_availability = datetime.strptime(date_availability, '%Y-%m-%d')
        self.med_id = med_id

    def json(self):
        return {
            "id": self.id,
            "stock_num": self.stock_num,
            "to_stock": self.to_stock,
            "accepted_to_stock": self.accepted_to_stock,
            "is_stocked": self.is_stocked,
            "is_canceled": self.is_canceled,
            "date_of_stock": datetime.strftime(self.date_of_stock, '%Y-%m-%d'),
            "date_availability": datetime.strftime(self.date_availability, '%Y-%m-%d'),
            "med_id": self.med_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_accepted(cls, is_stocked):
        return cls.query.filter_by(is_stocked=is_stocked).first()

    @classmethod
    def find_by_canceled_stocks(cls, is_canceled):
        return cls.query.filter_by(is_canceled=is_canceled).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
