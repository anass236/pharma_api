
from datetime import datetime

from sqlalchemy import extract

from api.models.medicament import MedicamentModel
from api.utils.database import db


class StockModel(db.Model):

    medicaments: MedicamentModel

    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_num = db.Column(db.DECIMAL(asdecimal=False))
    to_stock = db.Column(db.Float)
    accepted_to_stock = db.Column(db.Float)
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
            "medicament": self.medicaments.json()
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

    @classmethod
    def find_by_med_year(cls, med_id, year):
        return cls.query.filter(extract('year', cls.date_of_stock) == year, med_id == med_id).all()

    @classmethod
    def find_by_month_year(cls, month, year, page, limit=50):
        if not page:
            return cls.query.join(MedicamentModel).filter(cls.med_id == MedicamentModel.id,
                                                          extract('month', cls.date_of_stock) == month,
                                                          extract('year', cls.date_of_stock) == year,
                                                          cls.to_stock > 0).distinct().limit(limit)
        elif not limit:
            return cls.query.join(MedicamentModel).filter(cls.med_id == MedicamentModel.id,
                                                          extract('month', cls.date_of_stock) == month,
                                                          extract('year', cls.date_of_stock) == year,
                                                          cls.to_stock > 0).distinct()

        return cls.query.join(MedicamentModel, cls.med_id == MedicamentModel.id).filter(
                                                      extract('month', cls.date_of_stock) == month,
                                                      extract('year', cls.date_of_stock) == year,
                                                      cls.to_stock > 0).distinct().paginate(
            page=page,
            per_page=limit)

    @classmethod
    def find_by_stock_gt_zero(cls, element, page, limit):
        return cls.query.filter(cls.to_stock >= element).paginate(page=page, per_page=limit)

    @classmethod
    def find_years(cls, year):
        return cls.query.filter(extract('year', cls.date_of_stock)).distinct()
