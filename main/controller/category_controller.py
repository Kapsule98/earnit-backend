from flask.json import jsonify
from flask_restful import Resource
from main.service.category_service import CategoryService

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class CategoryController(Resource):
    def __init__(self,category_service:CategoryService= CategoryService()):
        self.category_service = category_service
    
    def get(self):
        try:
            res = self.category_service.get_all_categories()
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class ShopByCategoryController(Resource):
    def __init__(self,category_service:CategoryService= CategoryService()):
        self.category_service = category_service

    def get(self,category):
        try:
            res = self.category_service.get_shops_with_category(category)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class OfferByCategoryController(Resource):
    def __init__(self,category_service:CategoryService= CategoryService()):
        self.category_service = category_service

    def get(self,category):
        try:
            res = self.category_service.get_offers_with_category(category)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class OfferByShopController(Resource):
    def __init__(self,category_service:CategoryService= CategoryService()):
        self.category_service = category_service

    def get(self,shop_name):
        try:
            res = self.category_service.get_offers_with_shop_email(shop_name)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    
class ShopByCityController(Resource):
    def __init__(self,category_service:CategoryService= CategoryService()):
        self.category_service = category_service
    
    def get(self,city):
        try:
            return self.category_service.get_shop_in_city(city)
        except Exception as e:
            print(e)
            return jsonify(error_msg)
            
