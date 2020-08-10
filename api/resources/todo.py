from typing import Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.medicament import MedicamentModel
from api.models.todo import TodoModel
from api.models.stock import StockModel


class Todo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stock_id',
                        type=int,
                        required=True,
                        help='Stock_id numbers field cannot be left blank')
    parser.add_argument('med_id',
                        type=int,
                        required=True,
                        help='med_id field cannot be left blank')
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help='description field cannot be left blank')
    parser.add_argument('order',
                        type=str,
                        required=True,
                        help='order field cannot be left blank')
    parser.add_argument('name',
                        type=bool,
                        required=True,
                        help='name field cannot be left blank')
    parser.add_argument('priority',
                        type=str,
                        required=True,
                        help='priority field cannot be left blank')

    @jwt_required()
    def get(self, id: int) -> Tuple[dict, int]:
        todo = TodoModel.find_by_id(id)
        if todo:
            todo_json = todo.json()
            medicament = MedicamentModel.find_by_id(todo_json.med_id)
            stock = StockModel.find_by_id(todo_json.stock_id)
            if medicament:
                todo_json['medicaments'] = medicament.json()
                if stock:
                    todo_json['stocks'] = medicament.json()
                    return todo_json, 200
                return todo_json, 202
            return todo_json, 202
        return {"message": 'Todo not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        todo = TodoModel.find_by_id(id)
        if todo:
            todo.delete_from_db()
            return {'message': 'Todo deleted.'}, 200
        return {'message': 'Todo not found.'}, 404

    @jwt_required()
    def put(self, id) -> Tuple[dict, int]:
        data = Todo.parser.parse_args()
        todo = TodoModel.find_by_id(id)
        # assign new data by checking wheither already exist new item or not
        if todo:
            # assign all the new data and keep the "id"
            todo = {**todo, **dict(zip(data.keys(), data.values()))}
        else:
            todo = TodoModel(**data)

        # save data after update
        try:
            todo.save_to_db()
        except:
            return {'message': 'An Error inserting the new data'}, 500

        return todo.json(), 200


class TodoList(Resource):
    @jwt_required()
    def get(self) -> dict:
        return {'Steps List': list(map(lambda x: x.json(), TodoModel.query.all()))}


class TodoWithoutID(Resource):
    parser = reqparse.RequestParser()
    parser = reqparse.RequestParser()
    parser.add_argument('stock_id',
                        type=int,
                        required=True,
                        help='Stock_id numbers field cannot be left blank')
    parser.add_argument('med_id',
                        type=int,
                        required=True,
                        help='med_id field cannot be left blank')
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help='description field cannot be left blank')
    parser.add_argument('order',
                        type=str,
                        required=True,
                        help='order field cannot be left blank')
    parser.add_argument('name',
                        type=bool,
                        required=True,
                        help='name field cannot be left blank')
    parser.add_argument('priority',
                        type=str,
                        required=True,
                        help='priority field cannot be left blank')

    @jwt_required()
    def post(self, id: int) -> Tuple[dict, int]:
        if TodoModel.find_by_id(id):
            return {'message': f'An todo with id {id} already exists'}, 400

        data = Todo.parser.parse_args()

        todo = TodoModel(**data)

        try:
            todo.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error

        return todo.json(), 201
