from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from api.models.user import UserModel
from typing import Tuple

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This filed cannot be left blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This filed cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201

class User(Resource):
    @jwt_required()
    def get(self, username:str) -> Tuple[dict, int]:
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': f'There are no user with the username: {username}'}, 400
        return user.json(), 200
