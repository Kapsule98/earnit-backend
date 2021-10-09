import os
import pymongo
from main.config import config_by_name
import time
from flask import json, jsonify

config = config_by_name[os.getenv('ENV')]
mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
user_table = db['user']
cart_table = db['cart']
active_offer_table = db['active_offer']

class CartService:
    def get_user_cart(self,username):
        user = user_table.find_one({'username':username})
        if user is None:
            return jsonify({
                "msg":"user not found",
                "status":404
            })
        cart_offers = cart_table.find({'c_id':username})
        res = []
        count = 0
        for cart_offer in cart_offers:
            offer = active_offer_table.find_one({'shop_id':cart_offer['s_id'],'offer_text':cart_offer['offer_text']})
            seller = seller_table.find_one({'username':cart_offer['s_id']})

            if (seller is None):
                ## seller does not exist anymore
                cart_table.delete_many({'s_id':cart_offer['s_id']})
            elif offer is None:
                ## offer does not exist anymore
                cart_table.delete_many({'offer_text':cart_offer['offer_text']})
            else:
                obj = {
                    'seller_display_name':seller['display_name'],
                    'offer_text':offer['offer_text'],
                    'discount_percent':offer['discount_percent'],
                    'min_val':offer['min_val'],
                    'type':offer['type'],
                    'validity':offer['validity'],
                    'time_added_cart':cart_offer['timestamp'],
                    'products':offer['products'],
                    'seller_location':seller['location'],
                    'seller_address':seller['address'],
                    'seller_email':seller['email'],
                }
                print(obj)
                res.append(obj)
                count = count+1
        return jsonify({
            "msg":"user cart fetched",
            "status":200,
            "cart":res,
            "count":count
        })

    def add_offer_in_cart(self,username,offer_text,seller_email):
        user = user_table.find_one({'username':username})
        if user is None:
            return jsonify({
                "msg":"user not fount",
                "status":404
            })
        seller = seller_table.find_one({'email':seller_email})
        offer = active_offer_table.find_one({'offer_text':offer_text,'shop_id':seller['username']})
        if offer is None:
            return jsonify({
                "msg":"offer does not exist",
                "status":404
            })
        cart_offer = {
            'c_id':username,
            's_id':offer['shop_id'],
            'offer_text':offer['offer_text'],
            'timestamp':time.time(),
        }
        existing_in_cart = cart_table.find_one({'c_id':username,'offer_text':offer_text})
        if existing_in_cart is not None:
            return jsonify({
                "msg":"offer aleady in cart",
                "status":200
            })
        else:
            cart_table.insert(cart_offer)
            return jsonify({
                "msg":"offer added to cart",
                "status":200
            })

    def delete_offer(self,username,offer_text,seller_email):
        user = user_table.find_one({'username':username})
        seller = seller_table.find_one({'email':seller_email})
        if user is None or seller is None:
            return jsonify({
                "msg":"user/seller not fount",
                "status":404
            })

        cart_table.find_one_and_delete({'c_id':username,'offer_text':offer_text,'s_id':seller['username']})
        return jsonify({
            "msg":"offer deleted from cart",
            "status":200
        })