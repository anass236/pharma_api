import os

from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from api.config.config import DevelopmentConfig, TestingConfig, ProductionConfig
from api.resources.category import Category, CategoryList, CategoryWithoutID
from api.resources.employee import EmployeeList, Employee, EmployeeWithoutID
from api.resources.medicament import Medicament, MedicamentList, MedicamentWithoutID
from api.resources.step import Step, StepList, StepWithoutID
from api.resources.stock import Stock, StockWithoutID, StockList
from api.resources.store import StoreList, StoreWithoutID, Store
from api.resources.task import TaskWithoutID, TaskList, Task
from api.resources.todo import TodoList, TodoWithoutID, Todo
from api.resources.user import UserRegister, User
from api.utils.database import db
from security import authenticate, identity

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('TEST_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app = Flask(__name__)
app.config.from_object(app_config)

db.init_app(app)

apis = Api(app)
CORS(app)


@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()


jwt = JWT(app, authenticate, identity)  # /Auth

# START CREATE ENDPOINTS

# Employee Endpoint
apis.add_resource(Employee, '/employees/<int:id>')
apis.add_resource(EmployeeList, '/employees')
apis.add_resource(EmployeeWithoutID, '/employees')

# Store Endpoint
apis.add_resource(Store, '/stores/<int:id>')
apis.add_resource(StoreWithoutID, '/stores')
apis.add_resource(StoreList, '/stores')

# Medicament Endpoint
apis.add_resource(Medicament, '/medicaments/<int:id>')
apis.add_resource(MedicamentWithoutID, '/medicaments')
apis.add_resource(MedicamentList, '/medicaments')

# Category Endpoint
apis.add_resource(Category, '/categories/<int:id>')
apis.add_resource(CategoryList, '/categories')
apis.add_resource(CategoryWithoutID, '/categories')

# Stock Endpoint
apis.add_resource(Stock, '/stocks/<int:id>')
apis.add_resource(StockWithoutID, '/stocks')
apis.add_resource(StockList, '/stocks')

# Todos Endpoint
apis.add_resource(Todo, '/todos/<int:id>')
apis.add_resource(TodoWithoutID, '/todos')
apis.add_resource(TodoList, '/todos')

# Steps Endpoint
apis.add_resource(Step, '/steps/<int:id>')
apis.add_resource(StepList, '/steps')
apis.add_resource(StepWithoutID, '/steps')

# Tasks Endpoint
apis.add_resource(Task, '/tasks/<int:id>')
apis.add_resource(TaskList, '/tasks/<int:id>')
apis.add_resource(TaskWithoutID, '/tasks')

# Users Endpoint
apis.add_resource(UserRegister, '/register')
apis.add_resource(User, '/users/<string:username>')
# END ENDPOINTS


if __name__ == '__main__':
    app.run(port=5000, debug=True)
