from api.utils.database import db
from datetime import datetime

class StepModel(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    todolist_id = db.Column(db.Integer, db.ForeignKey('todoslist.id'))
    order_in_todolist = db.Column(db.Integer)
    created = db.Column(db.DateTime, server_default=db.func.now())

    todolists = db.relationship('TodoModel')
    tasks = db.relationship('TaskModel', lazy='dynamic')

    def __init__(self, name, description, todolist_id, order_in_todolist):
        self.name = name
        self.description = description
        self.todolist_id = todolist_id
        self.order_in_todolist = order_in_todolist

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "todolist_id": self.todolist_id,
            "order_in_todolist": self.order_in_todolist,
            "tasks": [task.json() for task in self.tasks],
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
    def find_by_order(cls, order):
        return cls.query.filter_by(order_in_todolist=order).all()
