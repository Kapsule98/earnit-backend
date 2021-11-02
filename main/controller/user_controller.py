from dns import exception
from flask.globals import request
from flask_restful import Resource
from main.service.customer_service import CustomerService
from flask_jwt_extended import jwt_required, get_jwt_identity

class CustomerController(Resource):
    def __init__(self,customer_service:CustomerService = CustomerService()):
        self.customer_service = customer_service

    @jwt_required()
    def get(self):
        try:
            return self.customer_service.get_customers(get_jwt_identity())
        except exception as e:
            print(e)
            return "internal server error",500

    @jwt_required()
    def post(self):
        req = request.json
        if 'email' not in req:
            return "Invalid format",400
        else:
            try:
                return self.customer_service.get_customer(get_jwt_identity(),req['email'])
            except exception as e:
                print(e)
                return "Internal server error",500