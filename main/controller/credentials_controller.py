from flask import request
from flask.json import jsonify
from flask_restful import Resource
from main.service.credentials_service import CredentialService

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class SellerCredentialController(Resource):
    def __init__(self,cred_service:CredentialService = CredentialService()):
        self.cred_service = cred_service
    
    def post(self):
        req = request.json
        try:
            if 'username' not in req:
                return jsonify({
                    "msg":"send valid username",
                    "status":400
                })
            res = self.cred_service.gen_otp_seller(req['username'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    
    def put(self):
        req = request.json
        try:
            if 'username' not in req or 'password' not in req or 'otp' not in req:
                return jsonify({
                    "msg":"pls send vaild request with username, otp and password",
                    "status":400
                })    
            res = self.cred_service.change_seller_password(req['username'],req['password'],req['otp'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class UserCredentialController(Resource):
    def __init__(self,cred_service:CredentialService = CredentialService()):
        self.cred_service = cred_service
    
    def post(self):
        req = request.json
        try:
            if 'username' not in req:
                return jsonify({
                    "msg":"send valid username",
                    "status":400
                })
            res = self.cred_service.gen_otp_user(req['username'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    
    def put(self):
        req = request.json
        try:
            if 'username' not in req or 'password' not in req or 'otp' not in req:
                return jsonify({
                    "msg":"pls send vaild request with username, otp and password",
                    "status":400
                })    
            res = self.cred_service.change_user_password(req['username'],req['password'],req['otp'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)