import os
import random
import time
import pymongo
from main.config import config_by_name
from flask import json, jsonify
from main.utils import offer_valid_redeeming, valid_transit , increment_qty

config = config_by_name[os.getenv('ENV')]
mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
customer_table = db['user']
transit_table = db['transit']
redeemed_table = db['redeemed']
active_offer_table = db['active_offer']
user_table = db['user']
archive_table = db['archive']

class HistoryService:
    
    def get_seller_redeemed_offers(self,seller_username):
        seller = seller_table.find_one({'username':seller_username})
        if seller is None:
            return jsonify({
                "msg":"No such seller exists",
                "status":400
            })
        seller_history = redeemed_table.find({'s_id':seller_username})
        res = []
        unique_customers = set()
        for transaction in seller_history:
            user = user_table.find_one({'username':transaction['c_id']})
            if user is not None:
                unique_customers.add(user['display_name'])

                offer = active_offer_table.find_one({'shop_id':seller_username,'offer_text':transaction['offer_text']})
                if offer is None:
                    offer = archive_table.find_one({'shop_id':seller_username,'offer_text':transaction['offer_text']})
                if offer is None:
                    pass
                else:
                    obj = {
                        "customer_display_name":user['display_name'],
                        "offer_text":transaction['offer_text'],
                        "timestamp":transaction['timestamp'],
                        "cp":transaction['cp'],
                        "sp":transaction['sp'],
                        "products":offer['products'],
                        "discount_percent":offer['discount_percent'],
                        "discount_type":offer['type']
                    }
                    res.append(obj)
        return jsonify({
            "msg":"seller history fetched",
            "status":200,
            "history":res,
            "number_customers":len(unique_customers) 
        })
    
    def get_customer_redeemed_offers(self,customer_username):
        print(customer_username)
        customer = customer_table.find_one({'username':customer_username})
        if customer is None:
            return jsonify({
                "msg":"No such customer exists",
                "status":400
            })
        customer_history = redeemed_table.find({'c_id':customer_username})
        print(customer_history)
        res = []
        for transaction in customer_history:
            seller_id = transaction['s_id']
            offer_text = transaction['offer_text']
            seller = seller_table.find_one({'username':seller_id})
            if seller is None:
                seller = {
                    "display_name":"DELETED_SELLER",
                    "shop_name":"DELETED_SELLER",
                    "email":"DELETED_SELLER",
                    "category":"DELETED_SELLER",
                }
            offer = active_offer_table.find_one({'shop_id':seller_id,'offer_text':offer_text})
            if offer is None:
                offer = archive_table.find_one({'shop_id':seller_id,'offer_text':offer_text})

                if offer is None:
                    offer = {
                        "products":['deleted seller'],
                        "validity":['deleted seller'],
                        "type":"Deleted offer",
                        "discount_percent":0,
                        "min_val":0,
                    }

            print("loop vars")
            print(offer)
            print(transaction)
            print(seller)
            obj = {
                "seller_display_name":seller['display_name'],
                "seller_shop_name":seller['shop_name'],
                "seller_email":seller['email'],
                "offer_text":transaction['offer_text'],
                "timestamp":transaction['timestamp'],
                "cp":transaction['cp'],
                "sp":transaction['sp'],
                "credit_earned":transaction['credit_points'],
                "category":seller['category'],
                "products":offer['products'],
                "validity":offer['validity'],
                "type":offer['type'],
                "discount_percent":offer['discount_percent'],
                "min_value":offer["min_val"],
            }
            res.append(obj)
        return jsonify({
            "msg":"customer history fetched",
            "status":200,
            "history":res
        })

    def get_credit_points(self,username):
        user = customer_table.find_one({'username':username})
        if user is None:
            return jsonify({
                "msg":"Customer not found",
                "status":404
            })
        else:
            return jsonify({
                "msg":"Total credit points",
                "credit_points":user['credit_points'],
                "status":200
            })