from typing import Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.medicament import MedicamentModel
from api.models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Name field cannot be left blank')
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help='descrption field cannot be left blank')
    parser.add_argument('address',
                        type=str,
                        required=False,
                        help='address field cannot be left blank')
  
    @jwt_required()
    def get(self, id: int) -> Tuple[dict, int]:
        store = StoreModel.find_by_id(id)
        if store:
            store_json = store.json()
            medicament = MedicamentModel.find_by_id(store_json.med_id)
            if medicament:
                store_json['medicament'] = medicament.json()
                return store_json, 200
            return store_json, 202
        return {"message": 'Store not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        store = StoreModel.find_by_id(id)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted.'}, 200
        return {'message': 'Store not found.'}, 404

    @jwt_required()
    def put(self, id) -> Tuple[dict, int]:
        data = Store.parser.parse_args()
        store = StoreModel.find_by_id(id)
        # assign new data by checking wheither already exist new item or not
        if store:
            # assign all the new data and keep the "id"
            store = {**store, **dict(zip(data.keys(), data.values()))}
        else:
            store = StoreModel(**data)

        # save data after update
        try:
            store.save_to_db()
        except:
            return {'message': 'An Error inserting the new data'}, 500

        return store.json(), 200


class StoreList(Resource):
    @jwt_required()
    def get(self) -> dict:
        return {'Steps List': list(map(lambda x: x.json(), StoreModel.query.all()))}


class StoreWithoutID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Name field cannot be left blank')
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help='descrption field cannot be left blank')
    parser.add_argument('address',
                        type=str,
                        required=False,
                        help='address field cannot be left blank')
   
    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Store.parser.parse_args()
        store = StoreModel(**data)
        if store.find_by_name(data.name):
            return {'message': f'An store with a name: {data.name} already exists'}, 400
        try:
            store.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error

        return store.json(), 201
