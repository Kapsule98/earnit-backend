from flask_restful import Resource
from main.service.image_service import ImageService
from flask import request
from flask.json import jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class SellerImageController(Resource):
    def __init__(self,image_service:ImageService = ImageService()):
        self.image_service = image_service


    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        try:
            res = self.image_service.get_shop_image(username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        req = request.json
        if 'image' not in req:
            return jsonify({
                "msg":"image not present",
                "status":400
            })
        try:
            image = req['image']
            res = self.image_service.save_shop_image(username,image)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerImageFromEmailController(Resource):

    def __init__(self,image_service:ImageService = ImageService()):
        self.image_service = image_service 


    def get(self,email):
            try:
                res = self.image_service.get_shop_image_from_email(email)
                return res
            except Exception as e:
                print(e)
                return jsonify(error_msg)