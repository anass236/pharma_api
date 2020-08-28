from datetime import datetime
from typing import Tuple

from flask import request, abort
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func, distinct

from api.models.medicament import MedicamentModel
from api.models.stock import StockModel
from api.utils.database import db


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
    def get(self) -> Tuple[dict, int]:
        id = int(request.args.get('id'))
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

    def get(self):
        limit = int(request.args.get('limit')) if request.args.get('limit') else None
        page = int(request.args.get('page')) if request.args.get('page') else None
        element = request.args.get('element')
        if element:
            stock = StockModel.find_by_stock_gt_zero(element, page, limit)
            if stock:
                return {"stocks list": list(map(lambda x: x.json(), stock.items)), 'pages': stock.pages}, 200
            return {"message": 'Stock not found'}, 404
        month = request.args.get('month')
        year = request.args.get('year')
        result = StockModel.find_by_month_year(month, year, page, limit)
        years = db.session.query(distinct(func.date_part('YEAR', StockModel.date_of_stock))).all()

        if month and year:
            if result:
                return {'Stocks List': list(map(lambda x: x.json(), result.items)), 'pages': result.pages,
                        'years': sorted([int(x[0]) for x in years if x[0] != -1])}, 200
            return abort(404)

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Stock.parser.parse_args()

        stock = StockModel(**data)
        try:
            stock.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error

        return stock.json(), 201


class StockPerYear(Resource):
    def get(self):
        month = request.args.get('month')
        year = request.args.get('year')
        results = StockModel.find_by_month_year(month, year)
        if results:
            return {'Stocks List': list(map(lambda x: x.json(), results))}, 200
        return abort(404)
