from typing import Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.step import StepModel
from api.models.todo import TodoModel


class Step(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Name field cannot be left blank')
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help='Description field cannot be left blank')
    parser.add_argument('todolist_id',
                        type=int,
                        required=True,
                        help='TodoList_id field cannot be left blank')
    parser.add_argument('order_in_todolist',
                        type=int,
                        required=True,
                        help='Order_in_todolist field cannot be left blank')

    @jwt_required()
    def get(self, id: int) -> Tuple[dict, int]:
        step = StepModel.find_by_id(id)
        if step:
            step_json = step.json()
            todolist = TodoModel.find_by_id(step.todolist_id)
            step_json['todolist'] = todolist.json()
            return step_json, 200
        return {"message": 'Step not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        step = StepModel.find_by_id(id)
        if step:
            step.delete_from_db()
            return {'message': 'Step deleted.'}, 200
        return {'message': 'Step not found.'}, 404

    @jwt_required()
    def put(self, id: int) -> Tuple[dict, int]:
        data = Step.parser.parse_args()
        step = StepModel.find_by_id(id)
        # assign new data by checking wheither already exist new item or not
        if step:
            # assign all the new data and keep the "id"
            step = {**step, **dict(zip(data.keys(), data.values()))}
        else:
            step = StepModel(**data)

        # save data after update
        try:
            step.save_to_db()
        except:
            return {'message': 'An Error inserting the new data'}, 500

        return step.json(), 200


class StepList(Resource):
    @jwt_required()
    def get(self) -> dict:
        return {'Steps List': list(map(lambda x: x.json(), StepModel.query.all()))}


class StepWithoutID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Name field cannot be left blank')
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help='Description field cannot be left blank')
    parser.add_argument('todolist_id',
                        type=int,
                        required=True,
                        help='TodoList_id field cannot be left blank')
    parser.add_argument('order_in_todolist',
                        type=int,
                        required=True,
                        help='Order_in_todolist field cannot be left blank')

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Step.parser.parse_args()
        if StepModel.find_by_name(data.name):
            return {'message': f'An step with name: {data.name} already exists'}, 400

        step = StepModel(**data)

        try:
            step.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error

        return step.json(), 201
