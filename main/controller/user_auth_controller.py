## User authentication controller
import json 
from flask import request
from flask.json import jsonify
from flask_restful import Resource
from main.service.user_auth import UserAuthService
from flask_jwt_extended import get_jwt_identity, jwt_required

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class UserRegistrationController(Resource):

    def __init__(self,user_auth_service: UserAuthService = UserAuthService()):
        self.user_auth_service = user_auth_service

    def post(self):
        req = request.json
        try :
            res = self.user_auth_service.register_user(req)
            return res
        except Exception as e:
            print('exception >>> ',e)
            return jsonify(error_msg)
    
    def put(self):
        req = request.json
        try:
            if ('otp' not in req) or ('email' not in req):
                return jsonify({
                    "msg":"email or otp not in req",
                    "status":400
                })
            res = self.user_auth_service.verify_mail(req['otp'],req['email'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)


class UserLoginController(Resource):
    def __init__(self,user_auth_service: UserAuthService = UserAuthService()):
        self.user_auth_service = user_auth_service

    def post(self):
        req = request.json
        try :
            res = self.user_auth_service.login_user(req)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class UserLogoutController(Resource):
    def __init__(self, user_auth_service: UserAuthService = UserAuthService()):
        self.user_auth_service = user_auth_service

    def get(self):
        try :
            res = self.user_auth_service.logout_user()
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class UserGoogleSigninController(Resource):
    def __init__(self, user_auth_service: UserAuthService = UserAuthService()):
        self.user_auth_service = user_auth_service

    def post(self):
        req = request.json
        if 'email' not in req:
            return jsonify({
                "msg":"email not found in req",
                "status":400
            })
        if 'display_name' not in req:
            return jsonify({
                "msg":"display name not found in req",
                "status":400
            })
        if 'uid' not in req:
            return jsonify({
                "msg":"uid not found in req",
                "status":400
            })
        if 'phone' not in req:
            return jsonify({
                "msg":"phone not found in req",
                "status":400
            })
        try :
            return  self.user_auth_service.google_signin(req['email'],req['display_name'],req['uid'],req['phone'])
        except Exception as e:
            print(e)
            return jsonify(error_msg)