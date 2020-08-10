from datetime import datetime
from typing import Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.medicament import MedicamentModel
from api.models.stock import StockModel


class Stock(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stock_num',
                        type=float,
                        required=True,
                        help='Stock numbers field cannot be left blank')
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
    def get(self, id: int) -> Tuple[dict, int]:
        stock = StockModel.find_by_id(id)
        if stock:
            stock_json = stock.json()
            medicament = MedicamentModel.find_by_id(stock_json.med_id)
            if medicament:
                stock_json['medicament'] = medicament.json()
                return stock_json, 200
            else:
                return stock_json, 202
        return {"message": 'Stock not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        stock = StockModel.find_by_id(id)
        if stock:
            stock.delete_from_db()
            return {'message': 'Stock deleted.'}, 200
        return {'message': 'Stock not found.'}, 404

    @jwt_required()
    def put(self, id) -> Tuple[dict, int]:
        data = Stock.parser.parse_args()
        stock = StockModel.find_by_id(id)
        # assign new data by checking wheither already exist new item or not
        if stock:
            # assign all the new data and keep the "id"
            stock = {**stock, **dict(zip(data.keys(), data.values()))}
        else:
            stock = StockModel(**data)

        # save data after update
        try:
            stock.save_to_db()
        except:
            return {'message': 'An Error inserting the new data'}, 500

        return stock.json(), 200


class StockList(Resource):
    @jwt_required()
    def get(self) -> dict:
        return {'Steps List': list(map(lambda x: x.json(), StockModel.query.all()))}


class StockWithoutID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stock_num',
                        type=float,
                        required=True,
                        help='Stock numbers field cannot be left blank')
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
                        type=str,
                        required=True,
                        help='date_of_stock field cannot be left blank')
    parser.add_argument('date_availability',
                        type=str,
                        required=True,
                        help='data_availability field cannot be left blank')
    parser.add_argument('med_id',
                        type=int,
                        required=True,
                        help='med_id field cannot be left blank')

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Stock.parser.parse_args()

        stock = StockModel(**data)
        try:
            stock.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error

        return stock.json(), 201
