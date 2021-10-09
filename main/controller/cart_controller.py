from flask import json
from flask.globals import request
from flask_restful import Resource
from main.service.cart_service import CartService
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask.json import jsonify

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class CartService(Resource):
    def __init__(self,cart_service:CartService = CartService()):
        self.cart_service = cart_service

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        try:
            res = self.cart_service.get_user_cart(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        req = request.json
        if 'offer_text' not in req or 'seller_email' not in req:
            return jsonify({
                "msg":"request syntax not identified",
                "status":400
            })
        try:
            res = self.cart_service.add_offer_in_cart(username,req['offer_text'],req['seller_email'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def delete(self):
        username = get_jwt_identity()
        req = request.json
        if 'offer_text' not in req or 'seller_email' not in req:
            return jsonify({
                "msg":"request syntax not identified",
                "status":400
            })
        try:
            res = self.cart_service.delete_offer(username,req['offer_text'],req['seller_email'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)