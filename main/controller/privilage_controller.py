from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from main.service.privillage_service import PrivillageService
from flask import request
class PrivillageController(Resource):
    def __init__(self,privillage_service:PrivillageService = PrivillageService()):
        self.privillage_service = privillage_service

    @jwt_required()
    def get(self):
        try:
            role = request.args.get('role')
            print(role)
            username = get_jwt_identity()
            res = self.privillage_service.check_privillages(role,username)
            return res
        except Exception as e:
            print(e)
            return "Internal server error",500