from datetime import datetime

from api.utils.database import db


class MedicamentModel(db.Model):
    __tablename__ = 'medicaments'

    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    created = db.Column(db.DateTime, server_default=db.func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    category = db.relationship('CategoryModel')
    stores = db.relationship('StoreModel')

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category_id": self.category_id,
            "created_date": datetime.strftime(self.created, '%Y-%m-%d')
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # Search per created year
    @classmethod
    def find_by_date(cls, year_date):
        return cls.query.filter_by(cls.created_date.year == year_date).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
