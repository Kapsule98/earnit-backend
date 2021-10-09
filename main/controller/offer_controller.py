from flask import request
from flask.json import jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from main.service.offer import OfferService
from main.service.redeem_service import redeemService

error_msg = {
    "msg":"Internal server error",
    "status":"400"
}

class OfferController(Resource):
    def __init__(self,offer_service:OfferService = OfferService()):
        self.offer_service = offer_service

    def get(self):
        try:
            res = self.offer_service.get_all_offers()
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerOfferController(Resource):
    def __init__(self,offer_service:OfferService = OfferService()):
        self.offer_service = offer_service

    @jwt_required()
    def get(self):
        seller_username = get_jwt_identity()
        try:
            res = self.offer_service.get_all_seller_offers(seller_username)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

    @jwt_required()
    def post(self): 
        seller_username = get_jwt_identity()
        offer = request.json['offer']
        try:
            res = self.offer_service.add_seller_offer(seller_username,offer)
            return res
            # if 'offer' in req:
            #     offer = req['offer']
            #     res = self.offer_service.add_seller_offer(seller_username,offer)
            #     return res
            # else:
            #     return jsonify(error_msg)
        except Exception as e:
            print (e)
            return jsonify(error_msg)

    @jwt_required()
    def put(self):
        seller_username = get_jwt_identity()
        offer = request.json['offer']
        try:
            res = self.offer_service.modify_seller_offer(seller_username,offer)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)
    @jwt_required()
    def delete(self):
        seller_username = get_jwt_identity()
        req = request.json
        print("delete offer = " ,req)
        try:
            if 'offer_text' in req:
                offer = req['offer_text']
                res = self.offer_service.remove_seller_offer(seller_username,offer)
                return res
            else:
                return jsonify(error_msg)

        except Exception as e:
            print(e)
            return jsonify(error_msg)

class RedeemController(Resource):
    def __init__(self,redeem_service:redeemService = redeemService()):
        self.redeem_service = redeem_service

    @jwt_required()
    def post(self):
        try:
            customer_username = get_jwt_identity()
            req = request.json
            if 'seller_email' not in req:
                return jsonify(error_msg)
            res = self.redeem_service.customer_redeem_offer(customer_username,req,req['seller_email'])
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

class SellerRedeemController(Resource):
    def __init__(self,redeem_service:redeemService = redeemService()):
        self.redeem_service = redeem_service

    @jwt_required()
    def post(self):
        try:
            seller_username = get_jwt_identity()
            req =request.json
            res = self.redeem_service.seller_redeem_offer(seller_username,req)
            return res
        except Exception as e:
            print(e)
            return jsonify(error_msg)

