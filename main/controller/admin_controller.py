from flask.globals import request
from flask.wrappers import JSONMixin
from flask_restful import Resource
from flask import json, jsonify
from main.service.admin_service import AdminService
from flask_jwt_extended import jwt_required,get_jwt_identity

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class AdminController(Resource):
    def __init__(self,admin_service:AdminService = AdminService()):
        self.admin_service = admin_service

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        try:
            return self.admin_service.get_admins(username)
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    
    def post(self):
        req = request.json
        try:
            res = self.admin_service.register(req)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    def put(self):
        req = request.json
        try:
            res = self.admin_service.verify_email(req)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class AdminLoginController(Resource):
    def __init__(self,admin_service:AdminService = AdminService()):
        self.admin_service = admin_service

    def post(self):
        req = request.json
        try:
            res = self.admin_service.login(req)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)


class AdminPermissionController(Resource):
    def __init__(self,admin_service:AdminService = AdminService()):
        self.admin_service = admin_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            return self.admin_service.get_admin_request_list(username)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def post(self):
        req = request.json
        username = get_jwt_identity()
        try:
            if 'opcode' not in req or 'email' not in req:
                return "request format incorrect",400
            if req['opcode'] == 0:
                return self.admin_service.deny_admin(username,req['email'])
            if req['opcode'] == 1:
                return self.admin_service.approve_admin(username,req['email'])
            else:
                return "opcode not identified",400
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class ShopPermissionController(Resource):
    def __init__(self,admin_service:AdminService = AdminService()):
        self.admin_service = admin_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            return self.admin_service.get_shop_request_list(username)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def post(self):
        req = request.json
        username = get_jwt_identity()
        try:
            if 'opcode' not in req or 'email' not in req:
                return "request format incorrect",400
            if req['opcode'] == 0:
                return self.admin_service.deny_shop(username,req['email'])
            if req['opcode'] == 1:
                return self.admin_service.approve_shop(username,req['email'])
            else:
                return "opcode not identified",400
        except Exception as e:
            print(e)
            return jsonify(error_msg)