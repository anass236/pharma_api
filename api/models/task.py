from api.utils.database import db


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    state = db.Column(db.String(80))
    step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    order_in_steplist = db.Column(db.String(80))
    created = db.Column(db.DateTime, server_default=db.func.now())

    steps = db.relationship('StepModel')

    def __init__(self, name, description, state, step_id, order_in_steplist):
        self.name = name
        self.description = description
        self.state = state
        self.step_id = step_id
        self.order_in_steplist = order_in_steplist

    def json(self):
        return {
            "name": self.name,
            "description": self.description,
            "state": self.state,
            "step_id": self.step_id,
            "order_in_steplist": self.order_in_steplist
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_ide(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_state(cls, state):
        return cls.query.filter_by(state=state).all()
