from typing import Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from api.models.category import CategoryModel


class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='The name field cannot be left blank')

    @jwt_required()
    def get(self, id: int) -> Tuple[dict, int]:
        category = CategoryModel.find_by_id(id)
        if category:
            return category.json()
        return {"message": 'Category not found'}, 404

    @jwt_required()
    def delete(self, id: int) -> Tuple[dict, int]:
        category = CategoryModel.find_by_id(id)
        if category:
            category.delete_from_db()
            return {'message': 'Category deleted.'}, 200
        return {'message': 'Category not found.'}, 404

    @jwt_required()
    def put(self, id: int) -> Tuple[dict, int]:
        category = CategoryModel.find_by_id(id)
        data = Category.parser.parse_args()
        if category:
            category = {**category, **dict(zip(data.keys(), data.values()))}
        else:
            category = CategoryModel(**data)
        try:
            category.save_to_db()
        except:
            return {'message': 'An Error inserting the new data'}, 500

        return category.json(), 200


class CategoryList(Resource):
    @jwt_required()
    def get(self):
        return {'categorys': list(map(lambda x: x.json(), CategoryModel.query.all()))}


class CategoryWithoutID(Resource):
    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        data = Category.parser.parse_args()
        if CategoryModel.find_by_name(data.name):
            return {'message': f'An category with name {data.name} already exists'}, 400

        category = CategoryModel(**data)

        try:
            category.save_to_db()
        except:
            return {"message": "An error occur"}, 500  # Internal Server Error
        return category.json(), 201
