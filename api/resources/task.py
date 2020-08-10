from datetime import datetime
from typing import Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.step import StepModel
from api.models.task import TaskModel


class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Name field cannot be left blank')
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help='description field cannot be left blank')
    parser.add_argument('state',
                        type=str,
                        required=True,
                        help='state field cannot be left blank')
    parser.add_argument('step_id',
                        type=int,
                        required=True,
                        help='is_stocked field cannot be left blank')
    parser.add_argument('order_in_steplist',
                        type=str,
                        required=True,
                        help='order_in_steplist field cannot be left blank')

    @jwt_required()
    def get(self, id: int) -> Tuple[dict, int]:
        task = TaskModel.find_by_id(id)
        if task:
            task_json = task.json()
            step = StepModel.find_by_id(task_json.step_id)
            if step:
                task_json['steps'] = step.json()
                return task_json, 200
            return task_json, 202
        return {"message": 'Task not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        task = TaskModel.find_by_id(id)
        if task:
            task.delete_from_db()
            return {'message': 'Task deleted.'}, 200
        return {'message': 'Task not found.'}, 404

    @jwt_required()
    def put(self, id) -> Tuple[dict, int]:
        data = Task.parser.parse_args()
        task = TaskModel.find_by_id(id)
        # assign new data by checking wheither already exist new item or not
        if task:
            # assign all the new data and keep the "id"
            task = {**task, **dict(zip(data.keys(), data.values()))}
        else:
            task = TaskModel(**data)

        # save data after update
        try:
            task.save_to_db()
        except:
            return {'message': 'An Error inserting the new data'}, 500

        return task.json(), 200


class TaskList(Resource):
    @jwt_required()
    def get(self) -> dict:
        return {'Steps List': list(map(lambda x: x.json(), TaskModel.query.all()))}


class TaskWithoutID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stock_num',
                        type=float,
                        required=True,
                        help='Task numbers field cannot be left blank')
    parser.add_argument('to_stock',
                        type=float,
                        required=True,
                        help='to_stock field cannot be left blank')
    parser.add_argument('accepted_to_stock',
                        type=float,
                        required=True,
                        help='to_stock field cannot be left blank')
    parser.add_argument('is_stocked',
                        type=bool,
                        required=True,
                        help='is_stocked field cannot be left blank')
    parser.add_argument('is_canceled',
                        type=bool,
                        required=True,
                        help='is_canceled field cannot be left blank')
    parser.add_argument('canceled_num',
                        type=float,
                        required=True,
                        help='canceled_num field cannot be left blank')
    parser.add_argument('date_of_stock',
                        type=datetime,
                        required=True,
                        help='date_of_stock field cannot be left blank')
    parser.add_argument('date_availability',
                        type=datetime,
                        required=True,
                        help='data_availability field cannot be left blank')
    parser.add_argument('med_id',
                        type=int,
                        required=True,
                        help='med_id field cannot be left blank')

    @jwt_required()
    def post(self, id: int) -> Tuple[dict, int]:
        if TaskModel.find_by_id(id):
            return {'message': f'An task with id {id} already exists'}, 400

        data = Task.parser.parse_args()

        task = TaskModel(**data)

        try:
            task.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error

        return task.json(), 201
