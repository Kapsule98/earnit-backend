from flask import request
from flask import json
from flask.json import jsonify
from flask_restful import Resource
from main.service.seller_auth import SellerAuthService
from flask_jwt_extended import jwt_required,get_jwt_identity

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class SellerRegisterController(Resource):
    def __init__(self,seller_auth:SellerAuthService = SellerAuthService()):
        self.seller_auth = seller_auth

    def post(self):
        req = request.json
        try:
            res = self.seller_auth.register(req)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    
    @jwt_required()
    def put(self):
        req = request.json
        try:
            if ('email' not in req) or ('otp' not in req):
                return jsonify({
                    "msg":"email or otp not in req",
                    "status":400
                })
            else:
                username = get_jwt_identity()
                res = self.seller_auth.verify_mail(req['otp'],req['email'],username)
                return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def delete(self):
        username = get_jwt_identity()
        try:
            res = self.seller_auth.delete_account(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerLoginController(Resource):
    def __init__(self,seller_auth:SellerAuthService = SellerAuthService()):
        self.seller_auth = seller_auth

    def post(self):
        req = request.json
        try:
            res = self.seller_auth.login(req)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerLogoutController(Resource):
    def __init__(self,seller_auth:SellerAuthService = SellerAuthService()):
        self.seller_auth = seller_auth

    def get(self):
        try:
            return self.seller_auth.logout()
        except Exception as e:
            print(e)
            return jsonify(error_msg)
