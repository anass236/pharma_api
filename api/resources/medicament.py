from typing import Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.category import CategoryModel
from api.models.medicament import MedicamentModel


class Medicament(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=float,
                        required=True,
                        help='The name field cannot be left blank')
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='The price field cannot be left blank')
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help='The category identifier cannot be left blank')
    parser.add_argument('name_full',
                        type=str,
                        required=False,
                        help='The name_full can be left blank')
    parser.add_argument('type_med',
                        type=str,
                        required=False,
                        help='The type medication can be left blank')

    @jwt_required()
    def get(self, id: int) -> Tuple[dict, int]:
        medicament = MedicamentModel.find_by_id(id)
        if medicament:
            category = CategoryModel.find_by_id(medicament.category_id)
            med_json = medicament.json()
            med_json['category_name'] = category.name
            return med_json, 200
        return {"message": 'Medicament not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        medicament = MedicamentModel.find_by_id(id)
        if medicament:
            medicament.delete_from_db()
            return {'message': 'Medicament deleted.'}, 200
        return {'message': 'Medicament not found.'}, 404

    @jwt_required()
    def put(self, id: int) -> Tuple[dict, int]:
        medicament = MedicamentModel.find_by_id(id)
        data = Medicament.parser.parse_args()
        # assign new data by checking wheither already exist new item or not
        if medicament:
            # assign all the new data and keep the "id"
            medicament = {**medicament, **dict(zip(data.keys(), data.values()))}
        else:
            medicament = CategoryModel(**data)

        # save data after update
        try:
            medicament.save_to_db()
        except:
            return {'message': 'An Error inserting the new data'}, 500

        return medicament.json(), 200


class MedicamentList(Resource):
    @jwt_required()
    def get(self):
        # select all data
        return {'medicaments': list(map(lambda x: x.json(), MedicamentModel.query.all()))}


class MedicamentWithoutID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=float,
                        required=True,
                        help='The name field cannot be left blank')
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='The price field cannot be left blank')
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help='The category identifier cannot be left blank')
    parser.add_argument('name_full',
                        type=str,
                        required=False,
                        help='The name_full can be left blank')
    parser.add_argument('type_med',
                        type=str,
                        required=False,
                        help='The type medication can be left blank')


    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Medicament.parser.parse_args()
        if MedicamentModel.find_by_name(data['name']):
            return {'message': f"A medicament with a name {data.name} already exists"}, 400

        medicament = MedicamentModel(**data)

        try:
            medicament.save_to_db()
        except:
            return {"message": "An error occur in saving data"}, 500  # Internal Server Error

        return medicament.json(), 201
