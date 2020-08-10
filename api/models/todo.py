from api.utils.database import db


class TodoModel(db.Model):
    __tablename__ = 'todoslist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    med_id = db.Column(db.Integer, db.ForeignKey('medicaments.id'))
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    order = db.Column(db.String(30))
    priority = db.Column(db.String(30))
    created = db.Column(db.DateTime, server_default=db.func.now())

    stocks = db.relationship('StockModel')
    medicaments = db.relationship('MedicamentModel')
    steps = db.relationship('StepModel')

    def __init__(self, stock_id, med_id, name, description, order, priority):
        self.stock_id = stock_id
        self.med_id = med_id
        self.name = name
        self.description = description
        self.order = order
        self.priority = priority

    def json(self):
        return {
            "stock_id": self.stock_id,
            "med_id": self.med_id,
            "name": self.name,
            "description": self.description,
            "order": self.order,
            "priority": self.priority,
            "steps": [step.json() for step in self.steps]
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

