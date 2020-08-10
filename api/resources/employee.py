from typing import Tuple
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.employee import EmployeeModel
from api.models.store import StoreModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help='First name cannot be left blank')
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help='Last name cannot be left blank')
    parser.add_argument('date_of_birth',
                        type=str,
                        required=False,
                        help='data of birth cannot be left blank')
    parser.add_argument('mobilephone',
                        type=str,
                        required=False,
                        help='mobilephone cannot be left blank')
    parser.add_argument('role',
                        type=str,
                        required=False,
                        help='Role cannot be left blank')
    parser.add_argument('store_id',
                        type=int,
                        required=False,
                        help='Store identifier cannot be left blank')

    @jwt_required()
    def get(self, id: int) -> Tuple[dict, int]:
        employee = EmployeeModel.find_by_id(id)
        if employee:
            stores = StoreModel.find_by_id(employee.store_id)
            employee_json = employee.json()
            if stores:
                employee_json['stores'] = stores.json()
                return employee_json
            return employee.json(), 201
        return {"message": 'Employee not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        employee = EmployeeModel.find_by_id(id)
        if employee:
            employee.delete_from_db()
            return {'message': 'Employee deleted.'}, 200
        return {'message': 'Employee not found.'}, 404

    @jwt_required()
    def put(self, id: int) -> Tuple[dict, int]:
        data = Employee.parser.parse_args()
        employee = EmployeeModel.find_by_id(id)

        if employee:
            employee = {**employee, **dict(zip(data.keys(), data.values()))}
        else:
            employee = EmployeeModel(**data)
        try:
            employee.save_to_db()
        except:
            return {'message': 'Error on saving the updated/new employee in database'}, 500

        return employee.json(), 200


class EmployeeList(Resource):
    def get(self) -> Tuple[dict, int]:
        return {'employees': list(map(lambda x: x.json(), EmployeeModel.query.all()))}, 200


class EmployeeStore(Resource):
    @jwt_required()
    def get(self, store_id: int) -> Tuple[dict, int]:
        employee = EmployeeModel.find_by_store(store_id)
        if employee:
            return employee.json(), 200
        return {"message": 'Employee not found'}, 404


class EmployeeRole(Resource):
    @jwt_required()
    def get(self, role: str) -> Tuple[dict, int]:
        employee = EmployeeModel.find_by_role(role)
        if employee:
            return employee.json(), 200
        return {"message": 'Employee not found'}, 404

    @jwt_required()
    def delete(self, role: str) -> Tuple[dict, int]:
        employee = EmployeeModel.find_by_role(role)
        if employee:
            employee.delete_from_db()
            return {'message': f'Employee with {role} is deleted.'}, 200
        return {'message': 'Employee not found.'}, 404


class EmployeeWithoutID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help='First name cannot be left blank')
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help='Last name cannot be left blank')
    parser.add_argument('date_of_birth',
                        type=str,
                        required=False,
                        help='data of birth cannot be left blank')
    parser.add_argument('mobilephone',
                        type=str,
                        required=False,
                        help='mobilephone cannot be left blank')
    parser.add_argument('role',
                        type=str,
                        required=False,
                        help='Role cannot be left blank')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Store identifier cannot be left blank')

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Employee.parser.parse_args()

        employee = EmployeeModel(**data)
        print(employee.json())
        try:
            employee.save_to_db()
        except:
            print(employee)
            return {"message": "An error in saving the new data"}, 500  # Internal Server Error

        return employee.json(), 201
