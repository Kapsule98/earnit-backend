from os import error
from flask import request
from flask.json import jsonify
from flask_jwt_extended.utils import get_jwt
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import jwt
from pymongo.message import delete
from main.service.shop_details import ShopService

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class SellerContactController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'contact' in req:
                contact = req['contact']
                res = self.shop_service.update_contact_no(username,contact)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerAddressController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'address' in req:
                address = req['address']
                res = self.shop_service.update_address(username,address)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerCategoryController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            res = self.shop_service.get_category(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'category' in req:
                category = req['category']
                res = self.shop_service.add_category(username,category)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def delete(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'category' in req:
                category = req['category']
                res = self.shop_service.remove_category(username,category)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)


class SellerProductController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            res = self.shop_service.get_product(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'products' in req:
                products = req['products']
                res = self.shop_service.add_product(username,products)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def delete(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'products' in req:
                products = req['products']
                res = self.shop_service.remove_product(username,products)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerShopNameController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'shop_name' in req:
                shop_name = req['shop_name']
                res = self.shop_service.update_shop_name(username,shop_name)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerDisplayNameController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'display_name' in req:
                display_name = req['display_name']
                res = self.shop_service.update_display_name(username,display_name)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerOwnerNameController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'owner_name' in req:
                owner_name = req['owner_name']
                res = self.shop_service.update_owner_name(username,owner_name)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerLocationController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'location' in req:
                location = req['location']
                res = self.shop_service.update_location(username,location)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerEmailController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'email' in req:
                email = req['email']
                res = self.shop_service.update_email(username,email)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerActiveTimeController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service
    @jwt_required()
    def post(self):
        req = request.json
        try:
            username = get_jwt_identity()
            if 'active_time' in req:
                active_time = req['active_time']
                res = self.shop_service.update_active_time(username,active_time)
                return res
            else:
                return jsonify(error_msg)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class OpenShopController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            res = self.shop_service.open_shop(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class CloseShopController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            res = self.shop_service.close_shop(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)


class SellerEarningController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            res = self.shop_service.get_earning(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)


class SellerCouponsController(Resource):
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            res = self.shop_service.get_number_of_coupons(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerBioController(Resource): 
    def __init__(self,shop_service:ShopService = ShopService()):
        self.shop_service = shop_service

    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            return self.shop_service.get_bio(username)
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    
    @jwt_required()
    def post(self):
        try:
            req = request.json
            username = get_jwt_identity()
            if 'bio' not in req:
                return jsonify({
                    'msg':"Bio not found in request",
                    'status':400
                })
            bio = req['bio']
            return self.shop_service.update_bio(username,bio)
        except Exception as e:
            print(e)
            return jsonify(error_msg)