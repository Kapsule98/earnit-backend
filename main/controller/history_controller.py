from flask import json
from flask.json import jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from main.service.history_service import HistoryService
error_msg = {
    "msg":"Internal server error",
    "status":400
}


class SellerHistoryController(Resource):
    def __init__(self,history_service  : HistoryService  = HistoryService()):
        self.history_service = history_service

    @jwt_required()
    def get(self):
        try:
            seller_username = get_jwt_identity()
            res = self.history_service.get_seller_redeemed_offers(seller_username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class CustomerHistoryController(Resource):
    def __init__(self,history_service  : HistoryService  = HistoryService()):
        self.history_service = history_service

    @jwt_required()
    def get(self):
        try:
            customer_username = get_jwt_identity()
            res = self.history_service.get_customer_redeemed_offers(customer_username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class CustomerPointsController(Resource):
    def __init__(self,history_service : HistoryService = HistoryService()):
        self.history_service = history_service

    @jwt_required()
    def get(self):
        try:
            customer_username = get_jwt_identity()
            res = self.history_service.get_credit_points(customer_username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)