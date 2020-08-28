from datetime import datetime
from typing import Tuple

from flask import request, abort
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import func, distinct, extract, desc

from api.models.category import CategoryModel
from api.models.medicament import MedicamentModel
from api.models.stock import StockModel
from api.utils.database import db


def find_top_agg_column(name_column, agg_func, year=2020, limit=5):
    list_agg_func = ["sum", "avg", "count", "min", "max"]
    print(agg_func)
    if agg_func in list_agg_func:
        expression = eval(f'func.{agg_func}')
        if name_column == 'category':
            return db.session.query(CategoryModel.name.label('Category'),
                                    expression(StockModel.to_stock).label('values')) \
                .filter(extract('year', StockModel.date_of_stock) == year) \
                .join(MedicamentModel, MedicamentModel.id == StockModel.med_id) \
                .join(CategoryModel, MedicamentModel.category_id == CategoryModel.id) \
                .group_by('Category').order_by(desc('values')).limit(limit)
        elif name_column == 'medicament':
            return db.session.query(MedicamentModel.name.label('Medicaments'),
                                    expression(StockModel.to_stock).label('values'), ) \
                .join(MedicamentModel, MedicamentModel.id == StockModel.med_id) \
                .filter(extract('year', StockModel.date_of_stock) == year) \
                .group_by('Medicaments').order_by(desc('values')).limit(limit)
        return "New Column not detected, select only column with name `medicament` or `category`"
    return "Function aggregate not detected, select only function with name `sum`, `avg`, `count`, `min` or `max`"


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

        '''
           @url: stocks?month=&year=&page=&limit=
        '''
        month = request.args.get('month')
        year = request.args.get('year')

        if month and year:
            result = StockModel.find_by_month_year(month, year, page, limit)
            years = db.session.query(distinct(func.date_part('YEAR', StockModel.date_of_stock))).all()
            if result:
                return {'Stocks List': list(map(lambda x: x.json(), result.items)), 'pages': result.pages,
                        'years': sorted([int(x[0]) for x in years if x[0] != -1])}, 200
            return abort(404)

        '''
            @url: stocks?top=5&by=""&year=&func=""
        '''
        name_column = request.args.get('by')
        top = int(request.args.get('top')) if request.args.get('top') else 5
        func_name = request.args.get('func')
        results = find_top_agg_column(name_column=name_column, agg_func=func_name, limit=top)
        if results:
            return {f'Top_{top}_{func_name}': [{f'{name_column}': x[0], 'values': x[1]} for x in results]}
        return {'message': 'result of request not found'}

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Stock.parser.parse_args()

        stock = StockModel(**data)
        try:
            stock.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error

        return stock.json(), 201
