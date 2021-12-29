from flask.json import jsonify
from flask_restful import Resource
from main.service.rating_service import RatingService
from flask import jsonify
from flask_jwt_extended import jwt_manager, jwt_required,get_jwt_identity
from flask import request
error_msg = {
    "msg":"Internal server error",
    "status":"400"
}
class RatingController(Resource):
    def __init__(self,rating_service:RatingService = RatingService()):
        self.rating_service = rating_service

    def get(self,shop_email):
        try:
            return self.rating_service.get_shop_rating(shop_email)
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def post(self,shop_email):
        username = get_jwt_identity()
        req = request.json
        if 'rating' not in req:
            return jsonify({
                "msg":"Rating and shop email not in payload",
                "status":400
            })
        try:
            return self.rating_service.rate_shop(username,shop_email,req['rating'])
        except Exception as e:
            print(e)
            return jsonify(error_msg)