from datetime import datetime

from api.utils.database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))
    created_date = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "created_date": datetime.strftime(self.created_date, '%Y-%m-%d')
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
